from common import *
from model import generate
from render_support import source_notes, material, material_packet
def main():
 run=runarg()
 with stage('write_articles',run) as rec:
  briefs=incoming(); rec['input_count']=len(briefs)
  if len(briefs)!=3 or any(not b.get('claims') for b in briefs): raise ValueError('Expected three supported, nonempty briefs; resolve editorial assignments before generation')
  items=material(run,briefs)
  payload={'project':load(run/'config/project.json'),'as_of_date':load(run/'run.json')['as_of_date'],'briefs':briefs,'items':material_packet(briefs,items)}
  result=generate(run,'write_articles',(run/'prompts/write_articles.md').read_text(),payload,rec)
  pieces=result['pieces']; byid={b['piece_id']:b for b in briefs}
  if len(pieces)!=3 or {p['piece_id'] for p in pieces}!=set(byid): raise ValueError('Expected three unique generated pieces')
  for p in pieces:
   b=byid[p['piece_id']]; expected={c['claim_id'] for c in b['claims']}
   if set(p['claim_ids'])!=expected or any(c not in p['markdown'] for c in expected): raise ValueError('Generated content omitted or introduced claim IDs')
   path=run/'articles'/(p['piece_id']+'.md'); path.parent.mkdir(parents=True,exist_ok=True)
   body=p['markdown'].split('\n## References')[0]
   path.write_text(body+'\n'+source_notes(b,items))
   emit(dict(piece_id=p['piece_id'],path=rel(path),claim_ids=p['claim_ids'])); rec['output_count']+=1
if __name__=='__main__': cli(main)
