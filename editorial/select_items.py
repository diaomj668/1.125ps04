from common import *
from model import generate
def main():
 run=runarg()
 with stage('select_items',run) as rec:
  items=incoming(); rec['input_count']=len(items)
  if not items: raise RuntimeError('No eligible evidence; cannot select material')
  distinct={x.get('underlying_id',x['item_id']):x for x in items}
  publishers={x['publisher_id'] for x in distinct.values()}
  if len(distinct)<12 or len(publishers)<6 or any(sum(x['kind']==kind for x in distinct.values())<2 for kind in ('feed','youtube','podcast')):
   raise RuntimeError('Insufficient eligible coverage: require 12 distinct items, 6 independent publishers, and 2 items per required kind before paid selection')
  prompt=(run/'prompts/select_items.md').read_text()+'\n'+(run/'config/editorial_policy.md').read_text()
  result=generate(run,'select_items',prompt,{'project':load(run/'config/project.json'),'as_of_date':load(run/'run.json')['as_of_date'],'items':evidence_packet(items)},rec)
  decisions=result['decisions']; expected={(x['item_id'],x['version_id']) for x in items}; seen=set()
  for d in decisions:
   require_keys(d,['item_id','version_id','decision','reason','piece_ids'])
   key=(d['item_id'],d['version_id'])
   if key not in expected or key in seen: raise ValueError('Unknown or repeated editorial decision')
   seen.add(key)
   if d['decision'] not in ('accept','reject','defer') or not d['reason'].strip(): raise ValueError('Invalid decision or empty reason')
   if d['decision']!='accept' and d['piece_ids']: raise ValueError('Rejected/deferred item cannot have piece assignments')
   if d['decision']=='accept' and (not d['piece_ids'] or not set(d['piece_ids'])<=set(['01','02','03'])): raise ValueError('Accepted item needs valid piece IDs')
  if seen!=expected: raise ValueError('AI omitted eligible items')
  for d in decisions: emit(d); rec['output_count']+=1
if __name__=='__main__': cli(main)
