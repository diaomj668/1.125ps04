import shutil
from common import *
def main():
 run=runarg()
 if load(run/'run.json')['as_of_date']!=now()[:10]: raise RuntimeError('Start a new live run on a different UTC date; cannot reuse an old as-of date')
 if (run/'approval.json').exists() or (run/'package').exists(): raise RuntimeError('Cannot regenerate reviewed/packaged content. Start a new run.')
 backup=run/'attempts'/uuid.uuid4().hex; backup.mkdir(parents=True)
 for p in list(run.iterdir()):
  if p.name in ('attempts','config','prompts','logs','model_calls','transcription_calls','run.json'): continue
  if p.is_dir(): shutil.copytree(p,backup/p.name)
  else: shutil.copyfile(p,backup/p.name)
 print('Previous attempt preserved: '+str(backup),file=sys.stderr)
if __name__=='__main__': cli(main)
