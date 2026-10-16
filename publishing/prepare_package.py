import shutil, sys
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parents[1]/'review'))
from common import *
from check_content import assess
def main():
 run=runarg()
 with stage('prepare_package',run) as rec:
  current=assess(run); previous=load(run/'review.json')
  approval=load(run/'approval.json') if (run/'approval.json').exists() else {}
  if not current['passed'] or previous['review_id']!=current['review_id'] or approval.get('review_id')!=current['review_id'] or approval.get('decision')!='approve': raise RuntimeError('Passing current checks and matching student approval required; missing or stale approval')
  require_keys(approval,['reviewer','reviewed_at','notes'])
  if not approval['reviewer'].strip() or not date(approval['reviewed_at']): raise ValueError('Reviewer and valid review date required')
  package=run/'package'; package.mkdir(exist_ok=True); assets=[]
  briefs={b['piece_id']:b for b in rows(run/'briefs.jsonl')}
  for kind in ('articles','video_scripts'):
   for m in rows(run/(kind+'.jsonl')):
    target=package/kind/(m['piece_id']+'.md'); target.parent.mkdir(exist_ok=True)
    shutil.copyfile(m['path'],target); assets.append(dict(piece_id=m['piece_id'],kind=kind,path=rel(target)))
    if kind=='articles':
     note=package/('sources-'+m['piece_id']+'.md'); text=pathlib.Path(m['path']).read_text(); note.write_text('# Source notes\n'+text.split('\n## References',1)[1]); assets.append(dict(piece_id=m['piece_id'],kind='source_notes',path=rel(note)))
  sys.path.insert(0,str(ROOT/'reporting'))
  from summarize_run import handoff_status
  actions,published_links=handoff_status(run)
  links=package/'publication_links.json'
  if not links.exists(): save(links,published_links or [dict(piece_id=x,substack_url=None,youtube_url=None) for x in ('01','02','03')])
  manifest=dict(review_id=current['review_id'],assets=assets,manual_steps=[a for a in actions if a!='Prepare the reviewed package'])
  save(package/'manifest.json',manifest); rec['output_count']=len(assets); emit(manifest)
if __name__=='__main__': cli(main)
