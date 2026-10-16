"""Discover videos through channel Atom feeds, with yt-dlp fallback on real errors."""
import datetime as dt, re
import feedparser, yt_dlp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from common import *

def candidate(source,ident,title,published_at,discovery):
 return dict(item_id='youtube:'+ident,source_id=source['source_id'],publisher_id=source['publisher_id'],kind='youtube',title=title,url='https://www.youtube.com/watch?v='+ident,published_at=published_at,retrieved_at=now(),media_url=None,discovery_url=discovery)

def discover_direct(source,limit):
 options={'quiet':True,'no_warnings':True,'noprogress':True,'skip_download':True,'playlistend':limit,'socket_timeout':20,'retries':1,'extractor_retries':1,'extract_flat':'in_playlist'}
 with yt_dlp.YoutubeDL(options) as ydl:
  info=ydl.extract_info(source['url'],download=False)
  if not info: raise RuntimeError('No readable YouTube metadata returned')
  for e in info.get('entries',[info]):
   if not e: continue
   ident=e['id'];published=None
   timestamp=e.get('timestamp')
   if timestamp:published=dt.datetime.fromtimestamp(timestamp,dt.timezone.utc).isoformat().replace('+00:00','Z')
   if not published:
    if not e.get('upload_date'):e=ydl.extract_info('https://www.youtube.com/watch?v='+ident,download=False)
    if e.get('upload_date'):published=dt.datetime.strptime(e['upload_date'],'%Y%m%d').replace(tzinfo=dt.timezone.utc).isoformat().replace('+00:00','Z')
   yield candidate(source,ident,e.get('title','Untitled'),published,source['url'])

def discover_feed(source,limit):
 url=source['url'];feed_url=None
 if '/feeds/videos.xml' in url:feed_url=url
 elif '/@' in url or '/channel/' in url:
  page=fetch(url).text;soup=BeautifulSoup(page,'html.parser');link=soup.select_one('link[type="application/rss+xml"]')
  if link:feed_url=urljoin(url,link['href'])
  else:
   match=re.search(r'"(?:channelId|externalId)":"(UC[^" ]+)"',page)
   if match:feed_url='https://www.youtube.com/feeds/videos.xml?channel_id='+match[1]
  if not feed_url:raise RuntimeError('Channel feed identity could not be resolved')
 else:return None
 parsed=feedparser.parse(fetch(feed_url).content)
 if not parsed.entries and parsed.bozo:raise RuntimeError('Invalid channel Atom response')
 return [candidate(source,e.get('yt_videoid') or e.get('id','').split(':')[-1],e.get('title','Untitled'),e.get('published'),feed_url) for e in parsed.entries[:limit]]

def main():
 run=runarg()
 with stage('fetch_youtube',run) as rec:
  rec['tools']+=['requests','YouTube Atom','yt-dlp'];project=load(run/'config/project.json')
  for source in load(run/'config/sources.json'):
   if source['kind']!='youtube':continue
   rec['input_count']+=1;limit=source.get('max_items',project.get('max_items_per_source',10))
   try:
    try:records=discover_feed(source,limit)
    except Exception as error:
     rec.setdefault('warnings',[]).append({'source_id':source['source_id'],'failed_route':'channel_feed','error':safe_error(error),'recovery':'yt-dlp direct channel discovery'})
     records=None
    if records is None:records=discover_direct(source,limit)
    for record in records:emit(record);rec['output_count']+=1
   except Exception as error:rec['errors'].append({'source_id':source['source_id'],'error':safe_error(error)})
  if rec['errors']:rec['status']='incomplete'
 if rec['errors']:raise RuntimeError('YouTube collection incomplete; valid partial records retained')
if __name__=='__main__':cli(main)
