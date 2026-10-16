"""Trace an actual draft claim through brief, selection, store version and passage."""
import subprocess
from common import *
def main():
 if len(sys.argv)!=3: raise ValueError('Usage: trace_claim.py RUN_DIR CLAIM_ID')
 run=pathlib.Path(sys.argv[1]); wanted=sys.argv[2]
 for brief in rows(run/'briefs.jsonl'):
  for claim in brief['claims']:
   if claim['claim_id']!=wanted: continue
   evidence=[]
   for ref in claim['evidence']:
    p=subprocess.run(['bash','data/store.sh','get',ref['item_id'],ref['version_id']],capture_output=True,text=True)
    if p.returncode: raise RuntimeError('Cannot retrieve referenced evidence version')
    item=json.loads(p.stdout); locator=ref['locator']; passage={}
    if locator['type']=='text':
     text=pathlib.Path(item['text_path']).read_text()
     if locator['quote'] not in text: raise RuntimeError('Source quote does not resolve')
     passage={'quote':locator['quote'],'text_path':item['text_path']}
    else:
     segment=next((s for s in load(item['segments_path']) if s['segment_id']==locator['segment_id']),None)
     if not segment: raise RuntimeError('Source segment does not resolve')
     passage={'segment':segment,'segments_path':item['segments_path']}
    decisions=[d for d in rows(run/'decisions.jsonl') if (d['item_id'],d['version_id'])==(ref['item_id'],ref['version_id'])]
    evidence.append(dict(item_id=item['item_id'],version_id=item['version_id'],title=item['title'],publisher_id=item['publisher_id'],kind=item['kind'],url=item['url'],published_at=item['published_at'],retrieved_at=item['retrieved_at'],editorial_decision=decisions[0] if decisions else None,passage=passage))
   articles=[x for x in rows(run/'articles.jsonl') if wanted in x['claim_ids']]
   videos=[x for x in rows(run/'video_scripts.jsonl') if wanted in x['claim_ids']]
   links=load(run/'package/publication_links.json') if (run/'package/publication_links.json').exists() else []
   emit(dict(run_id=load(run/'run.json')['run_id'],as_of_date=load(run/'run.json')['as_of_date'],piece_id=brief['piece_id'],brief_title=brief['title'],argument=brief['argument'],claim=claim,article_manifests=articles,video_script_manifests=videos,evidence=evidence,publication_links=[x for x in links if x['piece_id']==brief['piece_id']],publication_status='Verify real links; drafts and scripts are not published articles or rendered videos.'))
   return
 raise RuntimeError('Claim ID not found')
if __name__=='__main__': cli(main)
