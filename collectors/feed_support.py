"""RSS/Atom parsing shared by written and podcast collectors only."""
import calendar, datetime as dt, feedparser, re
from common import *
def collect(run,kind):
 with stage('fetch_'+('feeds' if kind=='feed' else 'podcasts'),run) as rec:
  rec['tools']+=['requests','feedparser']; sources=load(run/'config/sources.json'); project=load(run/'config/project.json')
  for source in sources:
   if source['kind']!=kind: continue
   rec['input_count']+=1
   try:
    parsed=feedparser.parse(fetch(source['url'],timeout=project.get('source_timeout_seconds',30)).content)
    if parsed.bozo and not parsed.entries: raise RuntimeError('Invalid or unreadable RSS/Atom')
    entries=parsed.entries
    if source.get('include_title_pattern'): entries=[e for e in entries if re.search(source['include_title_pattern'],e.get('title',''),re.I)]
    for entry in entries[:source.get('max_items',project.get('max_items_per_source',10))]:
     url=entry.get('link')
     if not url: continue
     media=next((x.get('href') for x in entry.get('enclosures',[]) if x.get('type','').startswith('audio/')),None)
     if kind=='podcast' and not media: continue
     published=entry.get('published_parsed') # Do NOT substitute updated date for publication.
     stamp=dt.datetime.fromtimestamp(calendar.timegm(published),dt.timezone.utc).isoformat().replace('+00:00','Z') if published else None
     underlying=entry.get('id') if kind=='podcast' else url.split('#')[0]
     emit(dict(item_id=kind+':'+digest([source['publisher_id'],underlying])[:24],source_id=source['source_id'],publisher_id=source['publisher_id'],kind=kind,title=entry.get('title','Untitled'),url=url,published_at=stamp,retrieved_at=now(),media_url=media,discovery_url=source['url']))
     rec['output_count']+=1
   except Exception as e: rec['errors'].append({'source_id':source['source_id'],'error':str(e)})
  if rec['errors']: rec['status']='incomplete'
 if rec['errors']: raise RuntimeError('One or more sources failed; valid partial records retained')
