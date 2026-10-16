"""Shared citation rendering only; article/script generation remains in each owner."""
from common import *
def source_notes(brief,items):
 lines=['\n## References\n']
 for claim in brief['claims']:
  lines.append(f'\n**{claim["claim_id"]}** ({claim["type"]}): {claim["statement"]}\n')
  for e in claim['evidence']:
   item=items[(e['item_id'],e['version_id'])]; loc=e['locator']; url=item['url']
   if loc['type']=='segment':
    seg=next(s for s in load(item['segments_path']) if s['segment_id']==loc['segment_id'])
    start=int(seg['start_seconds']); stamp=f'{start//60}:{start%60:02}'
    if item['kind']=='youtube': url+=('&' if '?' in url else '?')+'t='+str(start)+'s'
    lines.append(f'- [{item["title"]}]({url}), {stamp}, segment {loc["segment_id"]}. Source version `{item["version_id"]}`.\n')
   else: lines.append(f'- [{item["title"]}]({url}). Passage: “{loc["quote"]}” Source version `{item["version_id"]}`.\n')
 return ''.join(lines)
def material(run,briefs):
 refs={(e['item_id'],e['version_id']) for b in briefs for c in b['claims'] for e in c['evidence']}
 items={(x['item_id'],x['version_id']):x for x in rows(run/'eligible.jsonl') if (x['item_id'],x['version_id']) in refs}
 if set(items)!=refs: raise ValueError('Unresolvable brief references')
 return items


def material_packet(briefs, items):
 refs={key:[] for key in items}
 for b in briefs:
  for c in b['claims']:
   for e in c['evidence']: refs[(e['item_id'],e['version_id'])].append(e['locator'])
 packet=[]
 for key,item in items.items():
  x=dict(item); text=pathlib.Path(item['text_path']).read_text()
  if item.get('segments_path'):
   segments=load(item['segments_path']); wanted={loc['segment_id'] for loc in refs[key] if loc['type']=='segment'}
   positions={i for i,s in enumerate(segments) if s['segment_id'] in wanted}
   keep={j for i in positions for j in (i-1,i,i+1) if 0<=j<len(segments)}
   x['segments']=[segments[i] for i in sorted(keep)]
   x['text']='Referenced timestamped passages with neighboring segments are supplied below; full transcript retained at text_path.'
  else:
   excerpts=[]
   for loc in refs[key]:
    quote=loc.get('quote',''); index=text.find(quote) if quote else -1
    if index<0: raise ValueError('Exact brief quote not found in retained evidence')
    excerpt=text[max(0,index-600):index+len(quote)+600]
    if excerpt not in excerpts: excerpts.append(excerpt)
   x['text']='\n[passage boundary]\n'.join(excerpts); x['segments']=[]
  x['packet_scope']='Exact referenced evidence plus context; not the entire source.'
  packet.append(x)
 return packet
