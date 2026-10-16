"""Read-only source feasibility probe; results are discovery, not evidence."""
import concurrent.futures,json,re
import requests,feedparser
from bs4 import BeautifulSoup
urls=['https://getdx.com/podcast/','https://www.htmlallthethings.com/podcast/ai-basics-for-developers','https://www.latent.space/feed','https://feeds.transistor.fm/software-engineering-daily','https://changelog.com/practicalai/feed','https://www.youtube.com/@Fireship/videos','https://www.youtube.com/@WebDevSimplified/videos','https://www.youtube.com/@ThePrimeTimeagen/videos','https://simonwillison.net/atom/everything/','https://www.cursor.com/changelog/rss.xml','https://www.anthropic.com/news']
def probe(url):
 try:
  r=requests.get(url,timeout=25); result={'url':url,'status':r.status_code}
  feed=feedparser.parse(r.content)
  if feed.entries:
   result['entries']=[{'title':e.get('title'),'published':e.get('published'),'url':e.get('link'),'enclosures':e.get('enclosures',[])} for e in feed.entries[:15]]
  else:
   soup=BeautifulSoup(r.text,'html.parser')
   result['feeds']=[x.get('href') for x in soup.select('link[type="application/rss+xml"],link[type="application/atom+xml"]')]
   result['media_links']=[a.get('href') for a in soup.select('a[href]') if any(k in a.get('href','') for k in ['rss','transistor','youtube','simplecast','mp3','buzzsprout','feed'])][:20]
   result['youtube_channels']=list(set(re.findall(r'"channelId":"([^"]+)"',r.text)))[:3]
  return result
 except Exception as e: return {'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(probe,urls))
print(json.dumps(results,indent=2))
