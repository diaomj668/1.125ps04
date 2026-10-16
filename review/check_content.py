import re, datetime as dt
from common import *
from content_metrics import word_count,narration_text
def assess(run):
 issues=[]; fingerprint={}; used={}; project=load(run/'config/project.json'); asof=load(run/'run.json')['as_of_date']
 def issue(where,text,severity='error'): issues.append(dict(artifact=where,severity=severity,explanation=text))
 def capture(path):
  p=pathlib.Path(path)
  if not p.exists(): issue(str(p),'Required artifact missing'); return None
  fingerprint[rel(p)]=digest(p.read_text()); return p
 required=['briefs.jsonl','decisions.jsonl','eligible.jsonl','articles.jsonl','video_scripts.jsonl']
 for name in required: capture(run/name)
 briefs=rows(run/'briefs.jsonl'); decisions=rows(run/'decisions.jsonl'); eligible=rows(run/'eligible.jsonl')
 items={(x['item_id'],x['version_id']):x for x in eligible}; accepted={(d['item_id'],d['version_id']):d for d in decisions if d['decision']=='accept'}
 if len(briefs)!=3 or {x['piece_id'] for x in briefs}!={'01','02','03'}: issue('briefs','Need exactly three distinct pieces')
 if len({b.get('argument','') for b in briefs})!=3: issue('briefs','Central arguments must differ')
 if len(decisions)!=len(eligible) or {(d['item_id'],d['version_id']) for d in decisions}!=set(items): issue('decisions','Need exactly one decision per eligible item')
 for b in briefs:
  pid=b['piece_id']; pubs=set(); ids=set()
  for field in ('argument','synthesis','limitations'):
   if not b.get(field): issue(pid,'Missing '+field)
  if not b.get('claims'): issue(pid,'No supported claims')
  for c in b.get('claims',[]):
   if c.get('type') not in ('reported_fact','source_claim','inference'): issue(pid,'Invalid claim type')
   if not c.get('claim_id','').startswith(pid+'-c') or c.get('claim_id') in ids: issue(pid,'Invalid or repeated claim ID')
   ids.add(c.get('claim_id'))
   if not c.get('evidence'): issue(pid,'Claim has no evidence')
   for e in c.get('evidence',[]):
    key=(e['item_id'],e['version_id']); x=items.get(key)
    if not x: issue(pid,'Unresolved evidence version '+str(key)); continue
    if key not in accepted or pid not in accepted[key]['piece_ids']: issue(pid,'Evidence was not accepted/assigned to this piece')
    used[key]=x; pubs.add(x['publisher_id'])
    d=date(x.get('published_at')); end=dt.date.fromisoformat(asof)
    if d is None or not end-dt.timedelta(days=29)<=d<=end: issue(pid,'Evidence outside valid date window')
    text=capture(x['text_path'])
    if not text: continue
    loc=e.get('locator',{})
    if x['kind']=='feed':
     if loc.get('type')!='text' or not loc.get('quote') or loc['quote'] not in text.read_text(): issue(pid,'Exact supporting quote not found')
    else:
     segments=capture(x.get('segments_path') or 'missing_segments')
     if segments:
      ss=load(segments)
      if loc.get('type')!='segment' or not any(s['segment_id']==loc.get('segment_id') for s in ss): issue(pid,'Timestamp segment not found')
      if any(not isinstance(s.get('start_seconds'),(int,float)) or not isinstance(s.get('end_seconds'),(int,float)) or s['end_seconds']<=s['start_seconds'] for s in ss): issue(pid,'Invalid transcript timestamps')
  if len(pubs)<3: issue(pid,'Fewer than three independent publishers')
  for kind in ('articles','video_scripts'):
   manifest=rows(run/(kind+'.jsonl')); match=[x for x in manifest if x.get('piece_id')==pid]
   if len(match)!=1: issue(pid,'Missing/duplicate '+kind+' manifest'); continue
   p=capture(match[0]['path'])
   if not p: continue
   body=p.read_text().split('\n## References')[0]
   if set(match[0].get('claim_ids',[]))!=ids or any(x not in body for x in ids): issue(pid,kind+' claim markers do not match brief')
   if asof not in body: issue(pid,kind+' missing actual as-of date')
   words=word_count(narration_text(body) if kind=='video_scripts' else body)
   low,high=(600,900) if kind=='articles' else (390,650)
   if not low<=words<=high: issue(pid,f'{kind}: approximately {words} words; target {low}–{high}', 'warning')
 distinct={x.get('underlying_id',x['item_id']):x for x in used.values()}
 all_distinct={x.get('underlying_id',x['item_id']):x for x in eligible}
 if len(all_distinct)<12: issue('coverage','Fewer than 12 distinct eligible substantive items')
 if len({x['publisher_id'] for x in all_distinct.values()})<6: issue('coverage','Fewer than 6 independent eligible publishers')
 for k in ('feed','youtube','podcast'):
  if sum(x['kind']==k for x in all_distinct.values())<2: issue('coverage','Fewer than 2 eligible items of kind '+k)
  if not any(x['kind']==k for x in distinct.values()): issue('coverage',k+' does not contribute evidence to the series')
 issue('human_review','Machine checks cannot establish semantic support, original reasoning, publisher independence, cross-post identity, article/video factual consistency or appropriate uncertainty. Student must review.', 'warning')
 fingerprint['as_of_date']=asof
 return dict(review_id=digest(fingerprint),passed=not any(i['severity']=='error' for i in issues),issues=issues,assessed_at=now())
def main():
 run=runarg()
 with stage('check_content',run) as rec:
  result=assess(run); rec['output_count']=1; emit(result)
if __name__=='__main__': cli(main)
