from common import *
from model import generate
def validate_input_coverage(briefs,items):
 by_key={(x['item_id'],x['version_id']):x for x in items}
 kinds={by_key[(e['item_id'],e['version_id'])]['kind'] for b in briefs for c in b['claims'] for e in c['evidence']}
 missing={'feed','youtube','podcast'}-kinds
 if missing: raise ValueError('Briefs omit required input evidence: '+', '.join(sorted(missing)))

def main():
 run=runarg()
 with stage('create_briefs',run) as rec:
  decisions=incoming(); rec['input_count']=len(decisions)
  accepted={(d['item_id'],d['version_id']):d for d in decisions if d['decision']=='accept'}
  items=[x for x in rows(run/'eligible.jsonl') if (x['item_id'],x['version_id']) in accepted]
  if len({x["publisher_id"] for x in items})<3:
   raise RuntimeError("Need at least three independent accepted publishers before briefing")
  for pid in ('01','02','03'):
   publishers={x['publisher_id'] for x in items if pid in accepted[(x['item_id'],x['version_id'])]['piece_ids']}
   if len(publishers)<3: raise RuntimeError('Piece '+pid+' needs three assigned independent publishers before briefing')
  prompt=(run/'prompts/create_briefs.md').read_text()+'\n'+(run/'config/editorial_policy.md').read_text()
  result=generate(run,'create_briefs',prompt,{'project':load(run/'config/project.json'),'as_of_date':load(run/'run.json')['as_of_date'],'decisions':decisions,'items':evidence_packet(items)},rec)
  briefs=result['briefs']
  if len(briefs)!=3 or {b['piece_id'] for b in briefs}!={'01','02','03'}: raise ValueError('Expected exactly 3 distinct pieces')
  for b in briefs:
   require_keys(b,['piece_id','title','question','argument','synthesis','limitations','claims'])
   if not b['claims']: raise ValueError('Unsupported empty brief for piece '+b['piece_id'])
   for claim in b['claims']:
    for e in claim['evidence']:
     key=(e['item_id'],e['version_id'])
     if key not in accepted or b['piece_id'] not in accepted[key]['piece_ids']: raise ValueError('Brief uses unaccepted/unassigned evidence')
  validate_input_coverage(briefs,items)
  for b in briefs: emit(b); rec['output_count']+=1
if __name__=='__main__': cli(main)
