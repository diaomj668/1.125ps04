"""Compare saved runs without changing evidence or calling models."""
from common import *
def main():
 if len(sys.argv)!=3: raise ValueError('Usage: compare_runs.py FIRST_RUN SECOND_RUN')
 a,b=map(pathlib.Path,sys.argv[1:]); first=load(a/'run.json'); second=load(b/'run.json')
 ai={x['item_id']:x for x in rows(a/'items.jsonl')}; bi={x['item_id']:x for x in rows(b/'items.jsonl')}
 ad={x['item_id']:x for x in rows(a/'decisions.jsonl')}; bd={x['item_id']:x for x in rows(b/'decisions.jsonl')}
 result=dict(first_run=first['run_id'],second_run=second['run_id'],two_live_runs_on_different_utc_dates=first['mode']==second['mode']=='live' and first['as_of_date']!=second['as_of_date'],new_items=[bi[k] for k in bi.keys()-ai.keys()],changed_items=[{'item_id':k,'before':ai[k]['version_id'],'after':bi[k]['version_id']} for k in ai.keys()&bi.keys() if ai[k]['version_id']!=bi[k]['version_id']],unchanged_items=sorted(k for k in ai.keys()&bi.keys() if ai[k]['version_id']==bi[k]['version_id']),editorial_changes=[{'item_id':k,'before':ad.get(k),'after':bd.get(k)} for k in ad.keys()|bd.keys() if ad.get(k)!=bd.get(k)],note='Explain the significance of changes in SUBMISSION.md. No-new-material is a valid observation; use a labeled withheld-item replay to demonstrate updates if needed.')
 emit(result)
if __name__=='__main__': cli(main)
