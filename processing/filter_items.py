import datetime as dt
from common import *
def reason(value,asof):
 if value is None or value=='': return 'unknown_date'
 d=date(value)
 if d is None: return 'invalid_date'
 if d>asof: return 'future_date'
 if d<asof-dt.timedelta(days=29): return 'outside_window'
 return None
def main():
 run=runarg()
 with stage('filter_items',run) as rec:
  records=incoming(); rec['input_count']=len(records); excluded=[]
  asof=dt.date.fromisoformat(load(run/'run.json')['as_of_date'])
  for item in records:
   why=reason(item.get('published_at'),asof)
   if why: excluded.append(dict(item_id=item['item_id'],version_id=item['version_id'],reason=why,detail=f'published_at={item.get("published_at")}; inclusive window {asof-dt.timedelta(days=29)} through {asof} UTC'))
   else: emit(item); rec['output_count']+=1
  jsonl(run/'exclusions.jsonl',excluded)
if __name__=='__main__': cli(main)
