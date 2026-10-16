from common import *
def review_history(run):
 """Follow recorded predecessors for project-level review, never publication."""
 history=[]; seen=set()
 while run.resolve() not in seen:
  seen.add(run.resolve()); history.append(run)
  if not (run/'run.json').exists(): break
  previous=load(run/'run.json').get('previous_run_id')
  if not previous or pathlib.Path(previous).name!=previous: break
  run=ROOT/'runs'/previous
  if not (run/'run.json').exists(): break
 return history

def source_sample_recorded(run):
 path=run/'human_review.md'; text=path.read_text() if path.exists() else ''
 return text.count('- My judgment:')>=6 and not any('TO COMPLETE' in line for line in text.splitlines() if line.startswith(('- My judgment:','- Supporting passage / timestamp:','- Correction and reason')))

def policy_comparison_recorded(run):
 names=('before/editorial_policy.md','before/decisions.jsonl','after/config/editorial_policy.md','after/decisions.jsonl','comparison.json','comparison.md')
 if not all((run/'policy_revision'/name).exists() for name in names): return False
 comparison=(run/'policy_revision/comparison.md').read_text()
 interpretation=comparison.partition('## Student Interpretation')[2].split('\n## ',1)[0].strip()
 return bool(interpretation) and 'TO COMPLETE' not in interpretation

def current_student_approval(run):
 if not (run/'approval.json').exists() or not (run/'review.json').exists(): return False
 import sys
 sys.path.insert(0,str(ROOT/'review'))
 from check_content import assess
 approval=load(run/'approval.json'); saved=load(run/'review.json')
 if approval.get('decision')!='approve' or approval.get('review_id')!=saved.get('review_id'): return False
 current=assess(run)
 return current['passed'] and current['review_id']==approval['review_id']

def handoff_status(run):
 """Read recorded handoff facts; publication never implies editorial approval."""
 links=load(run/'package/publication_links.json') if (run/'package/publication_links.json').exists() else []
 by_piece={x['piece_id']:dict(x) for x in links}
 publication=run/'video_production/youtube/publication.json'
 published=[]
 if publication.exists():
  for video in load(publication).get('videos',[]):
   if video.get('metadata_saved_and_visibility_confirmed') is True and video.get('visibility') in ('public','unlisted') and video.get('youtube_url'):
    published.append(video)
    entry=by_piece.setdefault(video['piece_id'],dict(piece_id=video['piece_id'],substack_url=None))
    entry['youtube_url']=video['youtube_url']
 expected={'01','02','03'}
 published_ids={x['piece_id'] for x in published}
 history=review_history(run)
 sample_recorded=any(source_sample_recorded(r) for r in history)
 policy_recorded=any(policy_comparison_recorded(r) for r in history)
 live_dates={load(r/'run.json')['as_of_date'] for r in history if (r/'run.json').exists() and load(r/'run.json').get('mode')=='live'}
 comparison_path=ROOT/'docs/run-comparison.json'
 if (run/'run.json').exists() and comparison_path.exists():
  comparison=load(comparison_path); run_ids=[comparison.get('first_run'),comparison.get('second_run')]
  if load(run/'run.json').get('run_id') in run_ids:
   for ident in run_ids:
    if ident and pathlib.Path(ident).name==ident:
     metadata=ROOT/'runs'/ident/'run.json'
     if metadata.exists() and load(metadata).get('mode')=='live': live_dates.add(load(metadata)['as_of_date'])
 actions=[]
 if not sample_recorded: actions.append('Complete the student evidence-review sample')
 if not policy_recorded: actions.append('Revise editorial policy, rerun affected stages, and record the comparison and student interpretation')
 if not current_student_approval(run):
  actions.extend(['Complete final student editorial, caption, and audiovisual review',
                  'Record matching student approval after final review; prepare the reviewed package'])
 elif not (run/'package/manifest.json').exists(): actions.append('Prepare the reviewed package')
 if len(live_dates)<2: actions.append('Complete the second live run on another UTC date and compare update/duplicate/failure behavior')
 else: actions.append('Review and explain the two-run comparison, including substantive changes, duplicates, and failures')
 if expected-published_ids: actions.append('Complete Google Vids/HeyGen production and YouTube publication for pieces: '+', '.join(sorted(expected-published_ids)))
 missing_articles=expected-{pid for pid,x in by_piece.items() if x.get('substack_url')}
 if missing_articles: actions.append('Publish free-access Substack articles for pieces: '+', '.join(sorted(missing_articles)))
 if missing_articles or any(x.get('article_cross_link_pending',True) for x in published): actions.append('Add and verify matching article/video cross-links')
 if missing_articles or len(published_ids)<3 or any(not x.get('logged_out_access_verified') for x in published): actions.append('Verify final article and video access while logged out')
 actions.extend(['Record and link the separate 4–6 minute technical demonstration',
                 'Complete submission identity, reflection, repository, and final links'])
 return actions,[by_piece[k] for k in sorted(by_piece)] or None

def summary(run):
 meta=load(run/'run.json'); receipts=[load(p) for p in sorted((run/'logs').glob('*.json'))]
 artifact_errors=[]
 def records(name):
  path=run/name
  if not path.exists(): return None
  result=[]
  for index,line in enumerate(path.read_text().splitlines(),1):
   if not line.strip(): continue
   try:
    x=json.loads(line)
    if not isinstance(x,dict): raise ValueError('Record is not an object')
    result.append(x)
   except (ValueError,TypeError): artifact_errors.append({'artifact':name,'line':index,'error':'Malformed JSONL record'})
  return result
 counts={}
 for key,name in [('discovered','candidates.jsonl'),('extracted','items.jsonl'),('eligible','eligible.jsonl'),('excluded','exclusions.jsonl'),('articles','articles.jsonl'),('video_scripts','video_scripts.jsonl')]:
  rs=records(name); counts[key]=len(rs) if rs is not None else None
 changes=records('changes.jsonl'); decisions=records('decisions.jsonl')
 for k in ('new','changed','unchanged'): counts[k]=sum(x['change']==k for x in changes) if changes is not None else None
 for k,v in [('accepted','accept'),('rejected','reject'),('deferred','defer')]: counts[k]=sum(x['decision']==v for x in decisions) if decisions is not None else None
 eligible=records('eligible.jsonl'); unique={x.get('underlying_id',x['item_id']):x for x in eligible or []}
 coverage=dict(distinct_items=len(unique),independent_publishers=len({x['publisher_id'] for x in unique.values()}),by_kind={k:sum(x['kind']==k for x in unique.values()) for k in ('feed','youtube','podcast')}) if eligible is not None else None
 latest={}
 for r in sorted(receipts,key=lambda r:r['started_at']): latest[r['stage']]=r
 failed=[r for r in latest.values() if r['status'] not in ('completed',)]
 review={}
 if (run/'review.json').exists():
  try: review=load(run/'review.json')
  except (ValueError,OSError): artifact_errors.append({'artifact':'review.json','error':'Unreadable/incomplete assessment'})
 status='awaiting_review' if not artifact_errors and review.get('passed') and counts['articles']==3 and counts['video_scripts']==3 else 'failed'
 if (run/'package/manifest.json').exists() and status=='awaiting_review':
  import sys
  sys.path.insert(0,str(ROOT/'review'))
  from check_content import assess
  current=assess(run); approval=load(run/'approval.json') if (run/'approval.json').exists() else {}
  if current['passed'] and current['review_id']==approval.get('review_id')==load(run/'package/manifest.json').get('review_id') and approval.get('decision')=='approve': status='ready_for_production'
 candidates=records('candidates.jsonl') or []
 cost=sum(r['cost_usd'] for r in receipts if isinstance(r.get('cost_usd'),(int,float)))
 actions,publication_links=handoff_status(run)
 return dict(run_id=meta['run_id'],as_of_date=meta['as_of_date'],mode=meta['mode'],status=status,counts=counts,artifact_errors=artifact_errors,coverage=coverage,duplicate_observations=len(candidates)-len({x['item_id'] for x in candidates}),failed_or_incomplete_stages=[{'stage':r['stage'],'status':r['status'],'errors':r['errors']} for r in failed],historical_failures=[r for r in receipts if r['status']!='completed'],elapsed_seconds=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(meta['started_at'].replace('Z','+00:00'))).total_seconds(),active_stage_seconds=sum((dt.datetime.fromisoformat(r['finished_at'].replace('Z','+00:00'))-dt.datetime.fromisoformat(r['started_at'].replace('Z','+00:00'))).total_seconds() for r in receipts if r['stage'] not in ('run','collect_sources','create_series','summarize_run')),known_or_estimated_cost_usd=cost,unknown_cost_calls=sum(r.get('cost_usd') is None for r in receipts),models=sorted({m for r in receipts for m in r.get('models',[])}),tools=sorted({m for r in receipts for m in r.get('tools',[])}),remaining_manual_actions=actions,publication_links=publication_links)
def main():
 run=runarg()
 with stage('summarize_run',run) as rec:
  result=summary(run); rec['output_count']=1; emit(result)
if __name__=='__main__': cli(main)
