"""Demonstrate duplicate-free ingestion of retained real evidence, offline."""
import collections, hashlib, subprocess
from common import *

SELECTED_IDS=('feed:26e4a943393a1b788d1e2dae','youtube:wajoP_5Cpw8','podcast:acc83661b4084b701efe6573')

def file_hash(path):
 return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()

def main():
 if len(sys.argv)!=2: raise ValueError('Usage: replay_saved_evidence.py SOURCE_LIVE_RUN')
 source=pathlib.Path(sys.argv[1]).resolve()
 metadata=load(source/'run.json')
 if metadata.get('mode')!='live': raise ValueError('Source must be an actual retained live run')
 evidence={x['item_id']:x for x in rows(source/'eligible.jsonl')}
 if not set(SELECTED_IDS)<=set(evidence): raise ValueError('Required retained source items are missing')
 selected=[evidence[ident] for ident in SELECTED_IDS]
 if {x['kind'] for x in selected}!={'feed','youtube','podcast'}: raise ValueError('Expected one real item of each input kind')
 paths=sorted({x[key] for x in selected for key in ('text_path','segments_path') if x.get(key)})
 asset_hashes={path:file_hash(path) for path in paths}
 started=now(); ident='replay-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
 run=ROOT/'runs'/ident; run.mkdir()
 isolated=run/'isolated_store'
 formal=ROOT/'data/evidence'
 if isolated.resolve()==formal.resolve(): raise ValueError('Replay store must be isolated')
 save(run/'run.json',dict(run_id=ident,started_at=started,as_of_date=started[:10],mode='replay',previous_run_id=metadata['run_id'],source_live_run=rel(source),source_evidence_as_of_date=metadata['as_of_date'],scope='Offline storage ingestion only; no new collection, freshness claim, editorial generation, or publication'))
 jsonl(run/'input.jsonl',selected)
 save(run/'source_provenance.json',dict(source_run_id=metadata['run_id'],source_evidence_as_of_date=metadata['as_of_date'],source_file=rel(source/'eligible.jsonl'),source_file_sha256=file_hash(source/'eligible.jsonl'),input_sha256=file_hash(run/'input.jsonl'),items=[{k:x.get(k) for k in ('item_id','version_id','kind','title','url','published_at','retrieved_at','text_path','segments_path','retained_media_path')} for x in selected],retained_asset_sha256=asset_hashes))
 commands=[]
 def command(args,store,output,records=None):
  argv=['bash','data/store.sh',*args]; start=now()
  result=subprocess.run(argv,cwd=ROOT,env=os.environ|{'PIPELINE_STORE_DIR':str(store)},input=records,text=True,capture_output=True)
  output.parent.mkdir(parents=True,exist_ok=True); output.write_text(result.stdout)
  output.with_suffix(output.suffix+'.stderr.txt').write_text(result.stderr)
  commands.append(dict(command=argv,store_directory=rel(store),started_at=start,finished_at=now(),exit_code=result.returncode,stdout=rel(output),stderr=rel(output.with_suffix(output.suffix+'.stderr.txt'))))
  jsonl(run/'commands.jsonl',commands)
  if result.returncode: raise RuntimeError('Storage command failed; see retained stdout and stderr')
  return result.stdout
 with stage('replay_saved_evidence',run) as receipt:
  receipt['tools']+=['bash data/store.sh']; receipt['input_count']=len(selected)
  formal_before=json.loads(command(['stats'],formal,run/'formal_store_before.json'))
  command(['init'],isolated,run/'init.stdout.txt')
  empty=json.loads(command(['stats'],isolated,run/'empty.stats.json'))
  if empty['item_count'] or empty['version_count']: raise RuntimeError('Replay store was not empty')
  payload=(run/'input.jsonl').read_text(); phases={}; changes={}
  for phase in ('seed','replay_1','replay_2'):
   phase_dir=run/phase; phase_dir.mkdir()
   save(phase_dir/'run.json',dict(run_id=ident+'/'+phase,mode='replay',as_of_date=started[:10],source_live_run=rel(source),input_path=rel(run/'input.jsonl')))
   output=command(['upsert',rel(phase_dir)],isolated,phase_dir/'changes.jsonl',payload)
   records=[json.loads(line) for line in output.splitlines() if line.strip()]
   expected='new' if phase=='seed' else 'unchanged'
   if len(records)!=len(selected) or any(x['change']!=expected for x in records): raise RuntimeError('Unexpected change labels during '+phase)
   phases[phase]=json.loads(command(['stats'],isolated,phase_dir/'stats.json'))
   command(['list'],isolated,phase_dir/'stored_items.jsonl')
   changes[phase]=dict(collections.Counter(x['change'] for x in records))
   if phases[phase]['item_count']!=3 or phases[phase]['version_count']!=3: raise RuntimeError('Repeated ingestion changed distinct evidence counts')
   if phases[phase]['duplicate_item_versions'] or phases[phase]['duplicate_latest_items']: raise RuntimeError('Duplicate evidence detected')
   if phase!='seed' and any(phases[phase][key]!=phases['seed'][key] for key in ('versions_fingerprint','latest_fingerprint')): raise RuntimeError('Replay changed retained evidence or latest mappings')
  formal_after=json.loads(command(['stats'],formal,run/'formal_store_after.json'))
  if formal_before!=formal_after: raise RuntimeError('Formal store changed during isolated demonstration; investigate concurrent activity')
  if asset_hashes!={path:file_hash(path) for path in paths}: raise RuntimeError('Referenced source files changed during demonstration')
  result=dict(passed=True,mode='replay',source_live_run=metadata['run_id'],source_evidence_as_of_date=metadata['as_of_date'],executed_at=started,completed_at=now(),input_records=3,input_kinds=['feed','youtube','podcast'],empty_store=empty,phases=phases,change_counts=changes,item_count_unchanged=True,version_count_unchanged=True,stored_records_unchanged=True,formal_store_unchanged=True,retained_assets_unchanged=True,observation_counts=[phases[p]['observation_count'] for p in ('seed','replay_1','replay_2')],observation_note='Repeated observations are intentional audit logs, not duplicate evidence items or versions.',paid_model_calls=0,cost_usd=0.0,new_collection=False,fixture_material=False,not_a_third_live_run=True,not_a_withheld_item_update_demo=True)
  save(run/'verification.json',result)
  table='\n'.join(f'| {p} | {phases[p]["item_count"]} | {phases[p]["version_count"]} | {phases[p]["observation_count"]} | {next(iter(changes[p]))} |' for p in phases)
  (run/'README.md').write_text(f'''# Real-Evidence Duplicate-Free Replay

Executed at {started}. This is a labeled offline replay, not a third live run. The three records are unchanged real evidence retained by live run `{metadata['run_id']}`. The historical evidence as-of date is {metadata['as_of_date']}; the replay's actual execution date is recorded separately. No new source-freshness or publication claim is made.

## Actual Results

| Phase | Distinct items | Evidence versions | Audit observations | All input labels |
| --- | ---: | ---: | ---: | --- |
{table}

The empty isolated store initially contained zero items and zero versions. Seeding created three of each. Two further ingestions of the identical JSONL input kept both counts at three and marked every record unchanged. The evidence-record and latest-mapping fingerprints stayed identical. Observations increased from three to six to nine because each ingestion is logged; these are not duplicate evidence records.

The formal store's read-only before/after diagnostics are identical, and retained text/transcript hashes are unchanged. Only `data/store.sh` and its owning Python component accessed either index. No model calls, media extraction, network collection, fictional fixtures, fabricated source dates, or publication changes were used.

## Evidence and Reproduction

- `input.jsonl`: the exact three original records, one written source, one YouTube item, and one podcast episode.
- `source_provenance.json`: original URLs, publication/retrieval dates, exact source version IDs, asset paths, and hashes.
- `seed/`, `replay_1/`, `replay_2/`: actual change records, stage receipts, count diagnostics, and stored-item snapshots.
- `commands.jsonl`: actual storage command invocations, isolated/formal store paths, timestamps, exit codes, and output paths.
- `verification.json`: assertions and measured results.
- `formal_store_before.json` and `formal_store_after.json`: read-only evidence that the formal store was untouched.

Reproduce from the project root with `PYTHONPATH=lib .venv/bin/python tools/replay_saved_evidence.py {rel(source)}`. Each execution creates a new uniquely named replay directory and its own isolated store; it never overwrites this record or the live runs. `bash data/store.sh stats` is a read-only diagnostic extension; set `PIPELINE_STORE_DIR` to the isolated store to inspect its counts.

This demonstrates the architecture's duplicate-free replay checkpoint. It is separate from the conditional withheld-item update demonstration, which was not needed because the second live run found meaningful new material. The separate student technical demonstration video is still to be recorded.
''')
  receipt['output_count']=9
 emit(dict(run_dir=rel(run),passed=True,verification_path=rel(run/'verification.json')))

if __name__=='__main__': cli(main)
