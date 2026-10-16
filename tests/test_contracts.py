import datetime as dt, importlib.util, json, os, pathlib, subprocess, sys
import pytest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'processing'),str(ROOT/'review')]
from common import save,jsonl,load,digest
from filter_items import reason

def test_inclusive_utc_window():
 d=dt.date(2026,10,14)
 assert reason('2026-09-14T23:59:59Z',d)=='outside_window'
 assert reason('2026-09-15T00:00:00Z',d) is None
 assert reason('2026-10-14T23:59:59Z',d) is None
 assert reason('2026-10-15T00:00:00Z',d)=='future_date'
 assert reason(None,d)=='unknown_date'
 assert reason('2026-02-30',d)=='invalid_date'

def test_store_versions_and_duplicate_observations(tmp_path):
 env=os.environ|{'PIPELINE_STORE_DIR':str(tmp_path/'index')}
 def call(*args,records=None):
  return subprocess.run(['bash','data/store.sh',*args],cwd=ROOT,env=env,input=''.join(json.dumps(x)+'\n' for x in records or []),text=True,capture_output=True)
 item=dict(item_id='fixture:item',version_id='v1',text_path='fixture.txt',segments_path=None,retrieved_at='2026-10-14T00:00:00Z')
 assert call('init').returncode==0
 assert json.loads(call('stats').stdout)['version_count']==0
 r=call('upsert',str(tmp_path/'run'),records=[item,item])
 assert r.returncode==0,r.stderr
 assert [json.loads(x)['change'] for x in r.stdout.splitlines()]==['new','unchanged']
 initial_stats=json.loads(call('stats').stdout)
 assert (initial_stats['item_count'],initial_stats['version_count'],initial_stats['observation_count'])==(1,1,2)
 item['retrieved_at']='2026-10-15T00:00:00Z'
 assert json.loads(call('upsert',str(tmp_path/'run'),records=[item]).stdout)['change']=='unchanged'
 repeated_stats=json.loads(call('stats').stdout)
 assert repeated_stats['versions_fingerprint']==initial_stats['versions_fingerprint']
 assert repeated_stats['latest_fingerprint']==initial_stats['latest_fingerprint']
 assert repeated_stats['observation_count']==3
 item['version_id']='v2'
 assert json.loads(call('upsert',str(tmp_path/'run'),records=[item]).stdout)['change']=='changed'
 assert json.loads(call('get','fixture:item','v1').stdout)['version_id']=='v1'
 assert len(call('list').stdout.splitlines())==1
 assert call('get','missing').returncode==1
 final_stats=json.loads(call('stats').stdout)
 assert (final_stats['item_count'],final_stats['version_count'],final_stats['observation_count'])==(1,2,4)
 assert final_stats['duplicate_item_versions']==final_stats['duplicate_latest_items']==0
 assert call('stats','extra').returncode==2

def test_store_stats_does_not_create_missing_database(tmp_path):
 folder=tmp_path/'absent-store'
 result=subprocess.run(['bash','data/store.sh','stats'],cwd=ROOT,env=os.environ|{'PIPELINE_STORE_DIR':str(folder)},text=True,capture_output=True)
 assert result.returncode==1
 assert not folder.exists()

def test_media_timestamp_parser():
 from importlib.util import spec_from_file_location,module_from_spec
 spec=spec_from_file_location('extraction',ROOT/'processing/extract_content.py'); module=module_from_spec(spec); spec.loader.exec_module(module)
 rs=module.parse_vtt('WEBVTT\n\n00:01.000 --> 00:04.500\nHello <b>world</b>\n\n00:05.000 --> 00:06.000\nSecond segment\n')
 assert rs[0]==dict(segment_id='s00001',start_seconds=1.0,end_seconds=4.5,text='Hello world')
 assert len(rs)==2

def test_missing_artifacts_are_blocking_and_fingerprint_changes():
 # Repo-relative records are contract requirements; use a temporary directory in the repository.
 import tempfile,shutil
 from check_content import assess
 run=pathlib.Path(tempfile.mkdtemp(prefix='test-',dir=ROOT/'tests'))
 try:
  save(run/'run.json',{'as_of_date':'2026-10-14'})
  save(run/'config/project.json',{'publication_name':'Fixture'})
  a=assess(run)
  assert not a['passed']
  assert any(i['severity']=='error' for i in a['issues'])
  jsonl(run/'briefs.jsonl',[])
  b=assess(run)
  assert a['review_id']!=b['review_id']
  save(run/'review.json',b)
  save(run/'approval.json',{'review_id':b['review_id'],'decision':'approve','reviewer':'fixture','reviewed_at':'2026-10-14T00:00:00Z','notes':'Not human evidence'})
  p=subprocess.run(['bash','publishing/prepare_package.sh',str(run)],cwd=ROOT,capture_output=True,text=True)
  assert p.returncode==1
  assert not (run/'package').exists()
 finally: shutil.rmtree(run)

def test_passing_review_package_links_and_stale_approval():
 import shutil,tempfile
 from check_content import assess
 run=pathlib.Path(tempfile.mkdtemp(prefix='fixture-',dir=ROOT/'tests'))
 try:
  save(run/'run.json',{'as_of_date':'2026-10-14'})
  save(run/'config/project.json',{'publication_name':'EXPLICIT TEST FIXTURE'})
  items=[]
  for i in range(12):
   kind=('feed','youtube','podcast')[i//4]
   path=run/f'evidence-{i}.txt'; path.write_text('Exact supporting fixture passage. ' * 10)
   seg=run/f'segments-{i}.json'
   if kind!='feed': save(seg,[{'segment_id':'s00001','start_seconds':1.0,'end_seconds':4.0,'text':'Exact supporting fixture passage.'}])
   items.append(dict(item_id=f'fixture:{i}',version_id='fixture-v1',publisher_id=f'fixture-publisher-{i%6}',kind=kind,url='https://example.invalid',published_at='2026-10-14T00:00:00Z',text_path=str(path.relative_to(ROOT)),segments_path=str(seg.relative_to(ROOT)) if kind!='feed' else None))
  jsonl(run/'eligible.jsonl',items)
  jsonl(run/'decisions.jsonl',[dict(item_id=x['item_id'],version_id=x['version_id'],decision='accept',piece_ids=['01','02','03']) for x in items])
  briefs=[]
  for pid in ('01','02','03'):
   claims=[]
   for j,i in enumerate((0,4,8)):
    x=items[i]; loc={'type':'text','quote':'Exact supporting fixture passage.'} if x['kind']=='feed' else {'type':'segment','segment_id':'s00001'}
    claims.append(dict(claim_id=f'{pid}-c{j+1}',statement='Fictional test assertion',type='source_claim',evidence=[dict(item_id=x['item_id'],version_id=x['version_id'],locator=loc)]))
   briefs.append(dict(piece_id=pid,argument='Distinct fixture argument '+pid,synthesis='Compare fixture sources',limitations='Fictional fixtures, not evidence',claims=claims))
  jsonl(run/'briefs.jsonl',briefs)
  for kind,words in [('articles',650),('video_scripts',450)]:
   manifest=[]
   for b in briefs:
    path=run/kind/(b['piece_id']+'.md'); path.parent.mkdir(exist_ok=True)
    text='2026-10-14 '+' '.join(c['claim_id'] for c in b['claims'])+' '+'fixture '*words+'\n## References\nFictional test references\n'
    path.write_text(text)
    manifest.append(dict(piece_id=b['piece_id'],path=str(path.relative_to(ROOT)),claim_ids=[c['claim_id'] for c in b['claims']]))
   jsonl(run/(kind+'.jsonl'),manifest)
  current=assess(run)
  assert current['passed'],current['issues']
  save(run/'review.json',current)
  save(run/'approval.json',dict(review_id=current['review_id'],decision='approve',reviewer='EXPLICIT AUTOMATED TEST FIXTURE ONLY',reviewed_at='2026-10-14T00:00:00Z',notes='Not a real publication approval'))
  cmd=['bash','publishing/prepare_package.sh',str(run)]
  result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
  assert result.returncode==0,result.stderr
  sys.path.insert(0,str(ROOT/'reporting'))
  from summarize_run import handoff_status
  assert not any('student approval' in x or 'final student editorial' in x for x in handoff_status(run)[0])
  links=load(run/'package/publication_links.json'); links[0]['substack_url']='https://example.invalid/fixture'; save(run/'package/publication_links.json',links)
  assert subprocess.run(cmd,cwd=ROOT,capture_output=True).returncode==0
  assert load(run/'package/publication_links.json')[0]['substack_url']=='https://example.invalid/fixture'
  article=run/'articles/01.md'; article.write_text(article.read_text()+' Changed fixture body.')
  assert assess(run)['review_id']!=current['review_id']
  assert any('student approval' in x for x in handoff_status(run)[0])
  assert subprocess.run(cmd,cwd=ROOT,capture_output=True).returncode==1
 finally: shutil.rmtree(run)

def test_incomplete_report_survives_malformed_stage_output():
 import tempfile,shutil
 sys.path.insert(0,str(ROOT/'reporting'))
 from summarize_run import summary
 run=pathlib.Path(tempfile.mkdtemp(prefix='broken-fixture-',dir=ROOT/'tests'))
 try:
  save(run/'run.json',dict(run_id='fictional-broken',started_at='2026-10-14T00:00:00Z',as_of_date='2026-10-14',mode='replay'))
  (run/'items.jsonl').write_text('[download] fictional progress\n{"item_id":"fixture"}\n')
  (run/'review.json').write_text('')
  result=summary(run)
  assert result['status']=='failed'
  assert result['counts']['extracted']==1
  assert result['counts']['eligible'] is None
  assert len(result['artifact_errors'])==2
 finally: shutil.rmtree(run)

def test_caption_rate_limit_falls_back_to_downloaded_audio(tmp_path,monkeypatch):
 from importlib.util import spec_from_file_location,module_from_spec
 spec=spec_from_file_location('caption_fallback',ROOT/'processing/extract_content.py'); module=module_from_spec(spec); spec.loader.exec_module(module)
 class FakeDownloader:
  def __init__(self,options): self.options=options
  def __enter__(self): return self
  def __exit__(self,*args): pass
  def extract_info(self,*args,**kwargs): return {'subtitles':{'en':[{'ext':'json3','url':'https://example.invalid/rate-limited'}]}}
  def download(self,urls): pathlib.Path(self.options['outtmpl']).write_bytes(b'fictional audio fixture')
 monkeypatch.setattr(module.yt_dlp,'YoutubeDL',FakeDownloader)
 def fail_caption(*args,**kwargs): raise RuntimeError('Simulated 429')
 monkeypatch.setattr(module,'fetch',fail_caption)
 segments=[dict(segment_id='s00001',start_seconds=0.0,end_seconds=1.0,text='Fictional transcription')]
 calls=[]
 def fake_transcribe(path,run,receipt):
  calls.append(path); assert path.read_bytes()==b'fictional audio fixture'; return segments
 monkeypatch.setattr(module,'transcribe',fake_transcribe)
 receipt={}
 got,path=module.youtube({'url':'https://example.invalid/video','item_id':'fictional:video'},tmp_path,tmp_path,receipt,10000)
 assert got==segments and len(calls)==1
 assert receipt['warnings'][0]['item_id']=='fictional:video'

def test_video_length_counts_spoken_text_not_production_notes():
 from content_metrics import narration_text,word_count
 script='# Title\n**Visual directions:** '+('visual '*800)+'\n\n**Narration:**\n'+('spoken '*420)+'\n\n**Inline evidence — not spoken:** '+('evidence '*900)+'\n\n## Scene 2\n**Visual directions:** Diagram\n**Narration:**\n'+('closing '*30)+'\n\n**Visual direction:** '+('diagram '*800)+'\n\n## References\n'+('reference '*900)
 assert word_count(narration_text(script))==450

def test_video_length_accepts_inline_and_multiline_narration():
 from content_metrics import narration_text,word_count
 script='# Title\n**Visual direction:** '+('diagram '*800)+'\n**Narration:** '+('spoken '*220)+'[01-c1]\n\n[01-c1] [Evidence](https://example.invalid) '+('citation '*500)+'\n\n**Visual direction:** More diagrams\n**Narration:**\n'+('spoken '*230)+'\n\n## References\n'+('reference '*800)
 spoken=narration_text(script)
 assert word_count(spoken)==450
 assert 'diagram' not in spoken and 'citation' not in spoken and 'reference' not in spoken

def test_brief_stage_requires_substantive_evidence_from_all_inputs():
 spec=importlib.util.spec_from_file_location('brief_coverage',ROOT/'editorial/create_briefs.py'); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
 items=[dict(item_id=kind,version_id='fixture',kind=kind) for kind in ('feed','youtube','podcast')]
 def brief(*kinds): return dict(claims=[dict(evidence=[dict(item_id=k,version_id='fixture') for k in kinds])])
 with pytest.raises(ValueError,match='youtube'): module.validate_input_coverage([brief('feed','podcast')],items)
 module.validate_input_coverage([brief('feed'),brief('youtube'),brief('podcast')],items)

@pytest.mark.parametrize('report,checker_exit,expected',[
 ('{"passed":true}',0,0), ('{"passed":false}',0,1),
 ('{}',0,1), ('{"passed":"true"}',0,1),
 ('invalid JSON',0,1), ('{"passed":true}',1,1),
])
def test_series_workflow_propagates_assessment(tmp_path,report,checker_exit,expected):
 (tmp_path/'eligible.jsonl').write_text('')
 script='''
 function bash() {
  case "$1" in
   review/check_content.sh) printf '%s\\n' "$FIXTURE_REPORT"; return "$FIXTURE_EXIT";;
   editorial/select_items.sh|editorial/create_briefs.sh|content/write_articles.sh|content/write_video_scripts.sh) return 0;;
   *) command bash "$@";;
  esac
 }
 source workflows/create_series.sh "$1"
 '''
 result=subprocess.run(['bash','-c',script,'fixture',str(tmp_path)],cwd=ROOT,env=os.environ|{'FIXTURE_REPORT':report,'FIXTURE_EXIT':str(checker_exit)},text=True,capture_output=True)
 assert result.returncode==expected,result.stderr
 receipts=[load(p) for p in (tmp_path/'logs').glob('*.json')]
 assert len(receipts)==1
 assert receipts[0]['status']==('completed' if expected==0 else 'incomplete')

@pytest.mark.parametrize('candidate',[
 {'item_id':'fixture:invalid','published_at':'2026-10-14'},
 [],
 dict(item_id=7,source_id='fixture',publisher_id='fixture',kind='feed',title='Fixture',url='https://example.invalid',published_at=None,retrieved_at='2026-10-14T00:00:00Z',media_url=None),
 dict(item_id='fixture:invalid',source_id='fixture',publisher_id='fixture',kind='unknown',title='Fixture',url='https://example.invalid',published_at=None,retrieved_at='2026-10-14T00:00:00Z',media_url=None),
])
def test_extraction_invalid_input_exit_two(tmp_path,candidate):
 save(tmp_path/'run.json',{'as_of_date':'2026-10-14'})
 result=subprocess.run(['bash','processing/extract_content.sh',str(tmp_path)],cwd=ROOT,input=json.dumps(candidate)+'\n',text=True,capture_output=True)
 assert result.returncode==2,result.stderr
 assert result.stdout==''
 receipt=load(next((tmp_path/'logs').glob('*.json')))
 assert receipt['status']=='invalid'

def test_extraction_validates_batch_before_retrieval(tmp_path,monkeypatch):
 spec=importlib.util.spec_from_file_location('batch_extraction',ROOT/'processing/extract_content.py'); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
 valid=dict(item_id='fixture:valid',source_id='fixture',publisher_id='fixture',kind='feed',title='Fixture',url='https://example.invalid',published_at='2026-10-14',retrieved_at='2026-10-14T00:00:00Z',media_url=None)
 monkeypatch.setattr(module,'runarg',lambda:tmp_path)
 monkeypatch.setattr(module,'incoming',lambda:[valid,{}])
 def forbidden(*args): pytest.fail('Retrieval or store access occurred before batch validation')
 monkeypatch.setattr(module,'fetch',forbidden)
 monkeypatch.setattr(module,'store_get',forbidden)
 with pytest.raises(ValueError,match='missing required fields'): module.main()

def test_extraction_preserves_partial_operational_results(tmp_path,monkeypatch):
 import contextlib,io
 spec=importlib.util.spec_from_file_location('partial_extraction',ROOT/'processing/extract_content.py'); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
 save(tmp_path/'run.json',{'as_of_date':'2026-10-14'})
 save(tmp_path/'config/project.json',{})
 base=dict(source_id='fixture',publisher_id='fixture',title='Fixture',url='https://example.invalid',published_at='2026-10-14',retrieved_at='2026-10-14T00:00:00Z',media_url=None)
 candidates=[base|dict(item_id='fixture:fail',kind='feed'),base|dict(item_id='fixture:cached',kind='youtube')]
 text=tmp_path/'text.txt'; text.write_text('Retained fixture text')
 segments=tmp_path/'segments.json'; save(segments,[])
 cached=candidates[1]|dict(text_path=str(text),segments_path=str(segments),version_id='fixture-v1')
 monkeypatch.setattr(module,'runarg',lambda:tmp_path)
 monkeypatch.setattr(module,'incoming',lambda:candidates)
 monkeypatch.setattr(module,'store_get',lambda item_id:cached if item_id=='fixture:cached' else None)
 def fail_fetch(*args): raise RuntimeError('Simulated unavailable source')
 monkeypatch.setattr(module,'fetch',fail_fetch)
 output=io.StringIO()
 with contextlib.redirect_stdout(output),pytest.raises(RuntimeError,match='Extraction incomplete'): module.main()
 assert json.loads(output.getvalue())['item_id']=='fixture:cached'
 receipt=load(next((tmp_path/'logs').glob('*.json')))
 assert receipt['status']=='incomplete' and receipt['output_count']==1

def test_handoff_reports_actual_uploads_and_pending_work(tmp_path):
 sys.path.insert(0,str(ROOT/'reporting'))
 from summarize_run import handoff_status
 missing,links=handoff_status(tmp_path)
 assert any('YouTube publication' in x for x in missing) and links is None
 save(tmp_path/'video_production/youtube/publication.json',{'videos':[dict(piece_id=pid,youtube_url='https://example.invalid/'+pid,visibility='unlisted',metadata_saved_and_visibility_confirmed=True,article_cross_link_pending=True,logged_out_access_verified=False) for pid in ('01','02','03')]})
 actions,links=handoff_status(tmp_path)
 assert len(links)==3
 assert not any('YouTube publication' in x for x in actions)
 assert any('Substack' in x for x in actions)
 assert any('logged out' in x for x in actions)
 assert any('approval' in x for x in actions)
 (tmp_path/'human_review.md').write_text(('- My judgment: Accept fixture.\n- Supporting passage / timestamp: Fixture passage.\n- Correction and reason (if needed): None.\n')*6)
 for name in ('before/editorial_policy.md','before/decisions.jsonl','after/config/editorial_policy.md','after/decisions.jsonl','comparison.json'):
  path=tmp_path/'policy_revision'/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text('Explicit test fixture')
 comparison=tmp_path/'policy_revision/comparison.md'
 comparison.write_text('## Student Interpretation\nTO COMPLETE\n')
 assert any('Revise editorial policy' in x for x in handoff_status(tmp_path)[0])
 comparison.write_text('## Student Interpretation\nRecorded fixture interpretation.\n')
 completed_actions=handoff_status(tmp_path)[0]
 assert not any('Revise editorial policy' in x or 'evidence-review sample' in x for x in completed_actions)
 # An upload record without confirmation must not count as publication.
 data=load(tmp_path/'video_production/youtube/publication.json'); data['videos'][0]['metadata_saved_and_visibility_confirmed']=False
 save(tmp_path/'video_production/youtube/publication.json',data)
 assert any('YouTube publication for pieces: 01' in x for x in handoff_status(tmp_path)[0])

def test_second_run_retains_project_review_but_not_prior_publication(tmp_path,monkeypatch):
 sys.path.insert(0,str(ROOT/'reporting'))
 import summarize_run
 monkeypatch.setattr(summarize_run,'ROOT',tmp_path)
 first=tmp_path/'runs/first'; second=tmp_path/'runs/second'
 save(first/'run.json',dict(run_id='first',mode='live',as_of_date='2026-10-14',previous_run_id=None))
 save(second/'run.json',dict(run_id='second',mode='live',as_of_date='2026-10-15',previous_run_id='first'))
 (first/'human_review.md').write_text('- My judgment: Explicit fixture judgment.\n'*6)
 for name in ('before/editorial_policy.md','before/decisions.jsonl','after/config/editorial_policy.md','after/decisions.jsonl','comparison.json'):
  p=first/'policy_revision'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('Explicit fixture')
 (first/'policy_revision/comparison.md').write_text('## Student Interpretation\nRecorded fixture interpretation.\n')
 save(first/'video_production/youtube/publication.json',{'videos':[dict(piece_id='01',youtube_url='https://example.invalid/old',visibility='unlisted',metadata_saved_and_visibility_confirmed=True)]})
 actions,links=summarize_run.handoff_status(second)
 assert not any('Complete the second live run' in x or 'Revise editorial policy' in x or 'evidence-review sample' in x for x in actions)
 assert any('two-run comparison' in x for x in actions)
 assert any('YouTube publication' in x for x in actions) and links is None
 assert not (second/'approval.json').exists()
