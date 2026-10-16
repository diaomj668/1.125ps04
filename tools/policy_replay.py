"""Replay selection on saved real evidence with a student-edited policy.
This is not a new live collection and cannot replace the second-day run.
"""
import shutil, subprocess
from common import *
def main():
 if len(sys.argv)!=3: raise ValueError('Usage: policy_replay.py SOURCE_RUN STUDENT_POLICY_FILE')
 source=pathlib.Path(sys.argv[1]); policy=pathlib.Path(sys.argv[2]); original=load(source/'run.json')
 if not policy.read_text().strip(): raise ValueError('Policy must not be empty')
 if not (source/'corpus.jsonl').exists(): raise ValueError('Saved evidence corpus is required')
 ident='policy-replay-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
 run=pathlib.Path('runs')/ident; run.mkdir(parents=True)
 for name in ('config','prompts'): shutil.copytree(source/name,run/name)
 (run/'config/editorial_policy.md').write_text(policy.read_text())
 shutil.copyfile(source/'corpus.jsonl',run/'corpus.jsonl')
 save(run/'run.json',dict(run_id=ident,started_at=now(),as_of_date=now()[:10],mode='replay',previous_run_id=original['run_id'],source_run_id=original['run_id'],source_as_of_date=original['as_of_date'],replay_type='policy_comparison_on_real_saved_evidence',fictional=False,notice='No collection performed. Does not replace a second live run. Student must explain and author their own policy revision.'))
 for script,source_name,target in [('processing/filter_items.sh','corpus.jsonl','eligible.jsonl'),('editorial/select_items.sh','eligible.jsonl','decisions.jsonl')]:
  with (run/source_name).open() as inp, (run/target).open('w') as out:
   result=subprocess.run(['bash',script,str(run)],stdin=inp,stdout=out)
  if result.returncode: raise RuntimeError('Policy replay stage failed: '+script+'; artifacts preserved at '+str(run))
 before={(x['item_id'],x['version_id']) for x in rows(source/'eligible.jsonl')}
 after={(x['item_id'],x['version_id']) for x in rows(run/'eligible.jsonl')}
 save(run/'comparison_context.json',dict(same_eligible_evidence=before==after,source_run=original['run_id'],source_as_of_date=original['as_of_date'],replay_as_of_date=load(run/'run.json')['as_of_date'],note='If eligibility differs, do not attribute every decision difference to policy alone. Prompts and source evidence were held fixed; only the supplied policy was replaced.'))
 print(run)
if __name__=='__main__': cli(main)
