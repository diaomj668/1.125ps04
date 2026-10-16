"""Readable views of retained technical-demo evidence; never runs the pipeline."""
import argparse, subprocess
from common import *

FIRST=ROOT/'runs/20261014T225746Z-d041cf'
SECOND=ROOT/'runs/20261015T194925Z-8e319e'

def heading(title):
 print(title+'\n')

def architecture():
 heading('ARCHITECTURE AND ENTRY POINT')
 print('Topic: AI coding assistants for individual developers building small projects.')
 print('Entry point: bash run.sh\n')
 print('run.sh -> collect_sources.sh -> create_series.sh -> summarize_run.sh')
 print('  Collection: RSS + YouTube + podcasts')
 print('  Processing: text/media extraction -> store -> 30-day filtering')
 print('  Editorial: AI selection -> three briefs -> articles + scripts -> checks')
 print('  Human handoff: student approval -> run.sh --package -> publication\n')
 print('Sixteen Bash entry points coordinate focused owning components.')
 print('Only data/store.sh and data/store.py access the SQLite evidence index.')
 print('Project/source/policy settings: config/; model instructions: prompts/.')
 print('Text/media references and intermediate JSONL records remain inspectable.')
 print('\nInspect: run.sh, workflows/, SUBMISSION.md architecture diagram.')

def trace():
 heading('PUBLISHED CLAIM -> BRIEF -> DECISION -> TIMESTAMPED PODCAST')
 result=subprocess.run([sys.executable,'tools/trace_claim.py',rel(FIRST),'03-c4'],cwd=ROOT,capture_output=True,text=True)
 if result.returncode: raise RuntimeError(result.stderr)
 data=json.loads(result.stdout); evidence=data['evidence']; item=evidence[0]
 print('Claim 03-c4: '+data['claim']['statement'])
 print('\nAI decision: '+item['editorial_decision']['decision'])
 print('Assigned pieces: '+', '.join(item['editorial_decision']['piece_ids']))
 print('Source: '+item['title'])
 print('Published: '+item['published_at'])
 print('Collected: '+item['retrieved_at'])
 print('Item ID: '+item['item_id'])
 print('Version: '+item['version_id'])
 for entry in evidence:
  segment=entry['passage']['segment']; start=segment['start_seconds']; end=segment['end_seconds']
  print(f'  {int(start)//60}:{int(start)%60:02} ({start:.2f}-{end:.2f}s), {segment["segment_id"]}: {segment["text"]}')
 print('\nOriginal episode: '+item['url'])
 print('Transcript file: '+item['passage']['segments_path'])
 print('Decision file: '+rel(FIRST/'decisions.jsonl'))
 print('Brief file: '+rel(FIRST/'briefs.jsonl'))
 print('Published article: '+data['publication_links'][0]['substack_url'])
 print('Matching video: '+data['publication_links'][0]['youtube_url'])
 print('\nClaim is an attributed experience, not a controlled productivity result.')

def runs():
 heading('TWO ACTUAL LIVE EXECUTIONS')
 for path in (FIRST,SECOND):
  meta=load(path/'run.json'); report=load(path/'summary.json')
  print(f'{meta["as_of_date"]} UTC | mode={meta["mode"]} | {meta["run_id"]}')
  print(f'  Extracted {report["counts"]["extracted"]}/{report["counts"]["discovered"]}; eligible {report["coverage"]["distinct_items"]}; publishers {report["coverage"]["independent_publishers"]}')
 comparison=load(ROOT/'docs/run-comparison.json')
 print('\nSuccessful extraction comparison:')
 for key,label in [('new_items','Newly retained'),('changed_items','Changed version IDs'),('unchanged_items','Identical version IDs')]: print(f'  {label}: {len(comparison[key])}')
 print('\nNew October 15 video: sponsored side-project function rename/test scaffolding.')
 print('It informed the repaired demonstration drafts; sponsor and limits disclosed.')
 print('Six changed hashes do not establish six substantive new developments.')
 print('Final publication choice: October 14 articles/videos, as-of October 14.')
 print('October 15 outputs are retained for comparison and repair demonstration.')
 print('\nInspect: docs/run-comparison.md and each run\'s run.json/logs/.')

def replay():
 heading('REAL-EVIDENCE DUPLICATE-FREE REPLAY')
 pointer=load(ROOT/'docs/duplicate_replay.json'); folder=ROOT/pointer['run_dir']
 verification=load(folder/'verification.json'); provenance=load(folder/'source_provenance.json')
 print('Actual replay execution: '+verification['executed_at'])
 print('Original source evidence date: '+verification['source_evidence_as_of_date'])
 for item in provenance['items']: print(f'  {item["kind"]}: {item["title"]}')
 print('\nPhase          Items  Versions  Observations  Labels')
 for phase,data in verification['phases'].items():
  label=next(iter(verification['change_counts'][phase]))
  print(f'{phase:14} {data["item_count"]:5} {data["version_count"]:9} {data["observation_count"]:13}  {label}')
 print('\nFormal store unchanged: '+str(verification['formal_store_unchanged']))
 print('Evidence and current-version fingerprints unchanged: '+str(verification['stored_records_unchanged']))
 print('Model calls: 0. New collection: false. Cost: $0.')
 print('Observations are intentional audit logs, not duplicate evidence versions.')
 print('This isolated offline replay is NOT a third live run or a fictional fixture.')
 print('\nInspect: '+rel(folder/'verification.json'))
 print('Changes: '+rel(folder/'seed/changes.jsonl')+' and replay_1/ / replay_2/.')

def failures():
 heading('FRESHNESS, REAL FAILURE, AND REPAIR')
 for path in (FIRST,SECOND):
  date_value=load(path/'run.json')['as_of_date']; exclusions=rows(path/'exclusions.jsonl')
  print(f'{date_value}: {len(exclusions)} exclusions. Example:')
  print('  '+exclusions[0]['reason']+'; '+exclusions[0]['detail'])
 for p in sorted((SECOND/'logs').glob('extract_content-*.json')):
  receipt=load(p)
  print(f'\nReal extraction receipt: {receipt["status"]}; {receipt["output_count"]}/{receipt["input_count"]}')
  print('Cached media extractions reused: '+str(receipt.get('cached_items',0)))
  for error in receipt['errors']: print('  '+str(error))
 before=load(SECOND/'editorial_revision/before/review.json'); after=load(SECOND/'review.json')
 print('\nOriginal October 15 content assessment passed: '+str(before['passed']))
 print('Blocking issue: YouTube material was selected but never used in a claim.')
 print('Current content assessment passed after repair: '+str(after['passed']))
 print('Original outputs and failure receipts remain; they were not relabeled success.')
 print('\nInspect: exclusions.jsonl, logs/, and editorial_revision/before/review.json.')

def policy():
 heading('HUMAN EDITORIAL REVIEW AND POLICY REVISION')
 comparison=load(FIRST/'policy_revision/comparison.json')
 print('Student source-review sample: three accepted and three rejected/deferred.')
 print('Issue: plan labels alone do not establish practical task relevance.')
 print('Revision: separate access, setup requirements, and small-project relevance.')
 print('Cursor Security Review changed from reject to a narrow, qualified accept.')
 print('Access/cost limitations stayed explicit; deployment-focused Rollouts excluded.')
 print('Controlled inputs: identical saved source versions; actual AI selection rerun.')
 print('Decision labels changed: '+str(len(comparison['decision_changes'])))
 print('Model variation can also contribute; not every difference proves policy effect.')
 print('Profiling correction: diagnosis and artifacts, not proven repair or speedup.')
 approval=load(FIRST/'approval.json')
 print('\nFinal student decision: '+approval['decision']+' (selected October 14 series).')
 print('Approval fingerprint matches the reviewed package.')
 print('\nInspect: human_review.md, policy_revision/comparison.md, approval.json.')

def outputs():
 heading('PUBLISHED SERIES AND ARCHITECTURAL TRADEOFF')
 final=load(ROOT/'docs/final_series.json')
 for piece in final['pieces']:
  print(f'Piece {piece["piece_id"]}:\n  {piece["substack_url"]}\n  {piece["youtube_url"]}')
 print('\nTradeoff: unchanged media identity/title/date permits transcript reuse.')
 print('Benefit: fewer downloads/transcriptions. Risk: missing edits in place.')
 print('Same recording across endpoints still needs human reconciliation.')
 print('Limits: vendors and experienced practitioners dominate; no general gain proved.')
 print('Student confirmed no-login access; YouTube clickable external links deferred.')
 print('\nInspect: package/publication_links.json, config/, and docs/SOURCE_NOTES.md.')

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('view',choices=['architecture','trace','runs','replay','failures','policy','outputs'])
 args=parser.parse_args()
 print('Saved-evidence view only: no collection, generation, or new pipeline run.\n')
 globals()[args.view]()

if __name__=='__main__': cli(main)
