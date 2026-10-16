import shutil
from common import *
def main():
 if len(sys.argv)!=1: raise ValueError('No positional arguments expected')
 project=load('config/project.json'); sources=load('config/sources.json')
 for k in ('publication_name','topic','audience','central_question'):
  if not isinstance(project.get(k),str) or not project[k].strip(): raise ValueError('Nonempty project field required: '+k)
 if not isinstance(sources,list) or not sources: raise ValueError('Configure source array before running')
 source_ids=set()
 for x in sources:
  require_keys(x,['source_id','publisher_id','kind','url'])
  if x['kind'] not in ('feed','youtube','podcast') or not x['url'].startswith(('https://','http://')): raise ValueError('Invalid source kind/URL')
  if x['source_id'] in source_ids: raise ValueError('Repeated source ID')
  source_ids.add(x['source_id'])
 for path in ['config/editorial_policy.md']+[f'prompts/{p}.md' for p in ('select_items','create_briefs','write_articles','write_video_scripts')]:
  if not pathlib.Path(path).read_text().strip(): raise ValueError('Empty policy/prompt '+path)
 started=now(); ident=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
 run=pathlib.Path('runs')/ident; run.mkdir(parents=True)
 for folder in ('config','prompts'): shutil.copytree(folder,run/folder)
 previous=sorted(p.parent.name for p in pathlib.Path('runs').glob('*/run.json') if load(p).get('mode')=='live')
 save(run/'run.json',dict(run_id=ident,started_at=started,as_of_date=started[:10],mode='live',previous_run_id=previous[-1] if previous else None))
 print(run)
if __name__=='__main__': cli(main)
