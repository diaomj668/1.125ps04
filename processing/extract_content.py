import json, pathlib, re, subprocess, sys, tempfile, shutil, html
import trafilatura, yt_dlp
from common import *
def store_get(item_id):
 p=subprocess.run(['bash','data/store.sh','get',item_id],capture_output=True,text=True)
 return json.loads(p.stdout) if p.returncode==0 else None
def download(url,path,limit):
 with fetch(url,stream=True) as response:
  total=0
  with open(path,'wb') as f:
   for chunk in response.iter_content(65536):
    total+=len(chunk)
    if total>limit: raise RuntimeError('Media download exceeds configured size limit')
    f.write(chunk)
def parse_vtt(text):
 result=[]
 pattern=r'(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})'
 def seconds(x):
  m=re.search(pattern,x)
  return int(m[1] or 0)*3600+int(m[2])*60+int(m[3])+int(m[4])/1000 if m else None
 for block in re.split(r'\n\s*\n',text.replace('\r','')):
  lines=block.splitlines(); timing=next((i for i,x in enumerate(lines) if '-->' in x),None)
  if timing is None: continue
  left,right=lines[timing].split('-->',1); start,end=seconds(left),seconds(right)
  words=html.unescape(re.sub('<[^>]+>','', ' '.join(lines[timing+1:]))).strip()
  if words and start is not None and end is not None and end>start:
   result.append(dict(segment_id=f's{len(result)+1:05}',start_seconds=start,end_seconds=end,text=words))
 return result
def transcribe(path,run,rec):
 if not os.getenv('OPENAI_API_KEY'): raise RuntimeError('No timestamped transcript available and OPENAI_API_KEY is not configured for transcription')
 from openai import OpenAI
 import imageio_ffmpeg
 client=OpenAI(timeout=240,max_retries=1); rec['models'].append('whisper-1'); rec['cost_usd']=None
 segments=[]
 with tempfile.TemporaryDirectory() as temp:
  command=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','segment','-segment_time','600','-c:a','libmp3lame','-b:a','48k',temp+'/%04d.mp3']
  subprocess.run(command,check=True,capture_output=True,timeout=600)
  for i,chunk in enumerate(sorted(pathlib.Path(temp).glob('*.mp3'))):
   with chunk.open('rb') as f: response=client.audio.transcriptions.create(model='whisper-1',file=f,response_format='verbose_json',timestamp_granularities=['segment'])
   raw=response.model_dump(); save(run/'transcription_calls'/f'{digest(str(path))[:16]}-{i}.json',raw)
   for x in raw.get('segments',[]):
    segments.append(dict(segment_id=f's{len(segments)+1:05}',start_seconds=x['start']+600*i,end_seconds=x['end']+600*i,text=x['text'].strip()))
 return segments

def youtube(item,temp,run,rec,limit):
 with yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'noprogress':True,'skip_download':True,'socket_timeout':20,'retries':1,'extractor_retries':1}) as ydl:
  info=ydl.extract_info(item['url'],download=False)
  # Prefer native English captions. Rate-limited/missing captions fall back to
  # transcription of the downloaded audio rather than blocking a usable video.
  segments=[]
  caption_errors=[]
  for tracks in (info.get('subtitles',{}),info.get('automatic_captions',{})):
   languages=sorted((k for k in tracks if k=='en' or k.startswith('en-')),key=lambda k: (k!='en-orig',k!='en',k))
   for language in languages[:2]:
    try:
     track=next((x for x in tracks[language] if x.get('ext')=='json3'),None)
     if track:
      raw=fetch(track['url']).json(); save(temp/'captions.json',raw)
      for event in raw.get('events',[]):
       text=''.join(s.get('utf8','') for s in event.get('segs',[])).strip()
       start=event.get('tStartMs',0)/1000; end=start+event.get('dDurationMs',0)/1000
       if text and end>start: segments.append(dict(segment_id=f's{len(segments)+1:05}',start_seconds=start,end_seconds=end,text=text))
     else:
      track=next((x for x in tracks[language] if x.get('ext')=='vtt'),None)
      if track: segments=parse_vtt(fetch(track['url']).text)
     if segments: break
    except Exception as error: caption_errors.append(type(error).__name__)
   if segments: break
  if caption_errors:
   rec.setdefault('warnings',[]).append({'item_id':item['item_id'],'detail':'Caption retrieval failed; audio transcription fallback available','error_types':caption_errors})
 # Actual media is retained in addition to captions; metadata alone is insufficient.
 media=temp/'source.m4a'
 with yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'noprogress':True,'format':'bestaudio[ext=m4a]/bestaudio','outtmpl':str(media),'max_filesize':limit,'socket_timeout':20,'retries':1,'extractor_retries':1,'noplaylist':True}) as ydl: ydl.download([item['url']])
 if not media.exists() or media.stat().st_size==0: raise RuntimeError('YouTube media was not downloaded')
 if not segments: segments=transcribe(media,run,rec)
 return segments,media

def validate_candidate(candidate):
 if not isinstance(candidate,dict): raise ValueError('Candidate must be a JSON object')
 required=('item_id','source_id','publisher_id','kind','title','url','published_at','retrieved_at','media_url')
 missing=[key for key in required if key not in candidate]
 if missing: raise ValueError('Candidate missing required fields: '+', '.join(missing))
 for key in required:
  value=candidate[key]
  if value is None and key in ('published_at','media_url'): continue
  if not isinstance(value,str) or not value.strip(): raise ValueError('Invalid candidate field: '+key)
 if candidate['kind'] not in ('feed','youtube','podcast'): raise ValueError('Invalid candidate kind')

def main():
 run=runarg()
 with stage('extract_content',run) as rec:
  rec['tools']+=['requests','trafilatura','yt-dlp']; records=incoming(); rec['input_count']=len(records)
  # Validate the whole batch before retrieval. Invalid input is exit 2;
  # inaccessible valid sources remain partial operational failures (exit 1).
  for candidate in records: validate_candidate(candidate)
  project=load(run/'config/project.json'); limit=project.get('media_max_megabytes',200)*1024**2
  preexcluded=[]
  for candidate in records:
   try:
    item=dict(candidate)
    from filter_items import reason
    why=reason(item.get('published_at'),dt.date.fromisoformat(load(run/'run.json')['as_of_date']))
    if item['kind']!='feed' and why:
     preexcluded.append(dict(item_id=item['item_id'],reason=why,detail='Excluded before costly media retrieval; not a substantive evidence record',published_at=item.get('published_at')))
     continue
    cached=store_get(item['item_id'])
    with tempfile.TemporaryDirectory() as tmp:
     temp=pathlib.Path(tmp); segments=None; media=None; content=None
     if item['kind']=='feed':
      content=trafilatura.extract(fetch(item['url']).text,include_comments=False,include_tables=True)
      if not content or len(content.split())<100: raise RuntimeError('Substantive written content unavailable (minimum 100 words)')
     elif cached and all(cached.get(k)==item.get(k) for k in ('url','published_at','title')) and pathlib.Path(cached['text_path']).exists() and pathlib.Path(cached['segments_path']).exists():
      # Immutable media IDs assumed unchanged; refreshed title/date triggers retrieval. Document this tradeoff.
      out=dict(cached); out['retrieved_at']=item['retrieved_at']; emit(out); rec['output_count']+=1
      rec['cached_items']=rec.get('cached_items',0)+1; continue
     elif item['kind']=='youtube': segments,media=youtube(item,temp,run,rec,limit)
     else:
      if not item.get('media_url'): raise RuntimeError('Podcast audio enclosure missing')
      media=temp/'source.mp3'; download(item['media_url'],media,limit)
      segments=transcribe(media,run,rec)
     if segments is not None:
      if not segments: raise RuntimeError('No timestamped transcript segments')
      content='\n'.join(s['text'] for s in segments)
     if not content or len(content.split())<100: raise RuntimeError('Insufficient substantive evidence')
     # Same recording across endpoints: deterministic normalized transcript hash.
     recording=digest(re.sub(r'\W+',' ',content).lower().strip())
     if segments is not None: item['underlying_id']='recording:'+recording
     else: item['underlying_id']=item['item_id']
     item['version_id']=digest({k:item.get(k) for k in ('item_id','title','url','published_at','media_url')}|{'content':content,'segments':segments})
     base=pathlib.Path('data/assets')/digest(item['item_id'])[:20]/item['version_id']; base.mkdir(parents=True,exist_ok=True)
     text_path=base/'text.txt'
     if not text_path.exists(): text_path.write_text(content)
     item['text_path']=str(text_path); item['segments_path']=None
     if segments is not None:
      segment_path=base/'segments.json'
      if not segment_path.exists(): save(segment_path,segments)
      item['segments_path']=str(segment_path)
     if media:
      target=pathlib.Path('data/media')/digest(item['item_id'])[:20]/item['version_id']/media.name
      target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(media,target); item['retained_media_path']=str(target)
     item['extraction_method']='trafilatura' if item['kind']=='feed' else 'timestamped transcript with downloaded audio'
     emit(item); rec['output_count']+=1
   except Exception as e: rec['errors'].append({'item_id':candidate.get('item_id'),'error':str(e)})
  jsonl(run/'candidate_exclusions.jsonl',preexcluded)
  rec['pre_excluded_media']=len(preexcluded)
  if rec['errors']: rec['status']='incomplete'
 if rec['errors']: raise RuntimeError('Extraction incomplete; see receipt for inaccessible items')
if __name__=='__main__': cli(main)
