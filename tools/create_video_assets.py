"""Create exact-script narration and source clips for final editing in Google Vids."""
import sys,json,re,subprocess,wave,datetime,time,textwrap
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'lib'))
from common import ROOT,save,load,now,safe_error
from openai import OpenAI
import imageio_ffmpeg
RUN=ROOT/'runs/20261014T225746Z-d041cf';OUT=RUN/'video_production/google_vids/media';FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CONTENT={
'01':[
('Supervising coding agents','Access. Checks. Diagnosis.','Each capability addresses a different part of delivery.'),
('Remote supervision','Phone → agent on your computer','The computer must remain on and online.'),
('Checking secrets','Copilot /security-review','An announced check does not guarantee application security.'),
('Cursor Security Review','Severity → attack path → proposed fix','Teams / Enterprise; access and cost to verify; drafts skipped.'),
('Performance diagnosis','Flame graph + heatmap','An analysis artifact is not a measured optimization gain.'),
('ReviewBench','219 pull requests · 187 repositories','19 languages; relevance to a small project still needs assessment.'),
('Inspect the resulting work','Supervision → checks → diagnosis','Independent effectiveness evidence remains limited.')],
'02':[
('Assessing delivery','A success signal needs supporting evidence','Check the actual output and its intended behavior.'),
('Copilot review incident','Successful status — missing review','GitHub reported a specific September 28 delivery failure.'),
('Review metrics','A prompted change is not a correctness verdict','ReviewBench reduces the representation of tiny single-file changes.'),
('Security findings','A report format does not establish accuracy','Cursor describes the feature; access and cost remain to be checked.'),
('FilmCraft account','Familiar interface, reported usability problems','Fireship account; hardware and version details are missing.'),
('Hackathon prototype','“Frontend in 30 minutes”','Lance’s team account; not an independently verified solo-project result.'),
('Evaluate the outcome','Output + representative behavior + total effort','Independent comparisons and maintenance follow-up remain missing.')],
'03':[
('Evaluating an agent task','One bounded task, explicit checks','A proposed workflow, not a proven productivity result.'),
('Repository guidance','Instructions → test commands → outputs','Guidance does not establish that checks ran or passed.'),
('Inspect review delivery','Check that the review actually arrived','GitHub advised affected customers to request reviews again.'),
('Trying Security Review','Verify access → inspect → reproduce','Check cost and eligibility; draft pull requests are skipped.'),
('Profiling coverage','95.1% of recorded stacks','Willison’s workload: AnyIO worker thread, not a universal bottleneck.'),
('Bound the first trial','Short tasks and periodic check-ins','Practitioner accounts do not establish universal quotas.'),
('Record one complete cycle','Define → check → inspect → account for effort','Include testing and correction; expand after examining the result.')]
}
def command(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1800:])
 return p

def duration(path):
 p=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True)
 m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',p.stderr)
 if not m:raise RuntimeError('No media duration found: '+str(path))
 return int(m[1])*3600+int(m[2])*60+float(m[3])

def wav_seconds(path):
 # Streaming WAV headers may declare an unknown frame count. Count real PCM bytes.
 with wave.open(str(path)) as audio:
  actual_bytes=0
  while True:
   chunk=audio.readframes(65536)
   if not chunk:break
   actual_bytes+=len(chunk)
  return actual_bytes/(audio.getsampwidth()*audio.getnchannels()*audio.getframerate())

def filter_path(path):return str(path).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")

def main():
 selected=sys.argv[1:] or ['01','02','03'];client=OpenAI(timeout=240,max_retries=0)
 OUT.mkdir(parents=True,exist_ok=True);overall=[]
 for pid in selected:
  scenes=load(RUN/'video_production'/pid/'scenes.json');assert len(scenes)==len(CONTENT[pid])
  dest=OUT/pid;dest.mkdir(exist_ok=True);records=[]
  for idx,(scene,display) in enumerate(zip(scenes,CONTENT[pid]),1):
   stem=f'scene-{idx:02}';wav=dest/(stem+'.wav');request={'model':'tts-1','voice':'alloy','speed':0.86,'input':scene['narration'],'response_format':'wav'}
   receipt=dest/(stem+'.speech_receipt.json')
   if not wav.exists():
    if receipt.exists() and load(receipt).get('status')=='failed':raise RuntimeError('Prior speech failure retained; inspect before retry: '+str(receipt))
    save(dest/(stem+'.speech_request.json'),request);began=now();start=time.monotonic()
    try:
     response=client.audio.speech.create(**request);response.write_to_file(wav)
     seconds=wav_seconds(wav)
     save(receipt,{'status':'completed','started_at':began,'finished_at':now(),'elapsed_seconds':time.monotonic()-start,'model':'tts-1','voice':'alloy','input_characters':len(request['input']),'audio_seconds':seconds,'cost_usd':None,'cost_note':'Provider invoice not available; no zero-cost claim.','response_request_id':getattr(response,'request_id',None)})
    except Exception as error:
     save(receipt,{'status':'failed','started_at':began,'finished_at':now(),'error':safe_error(error),'cost_usd':None});raise
   seconds=wav_seconds(wav)
   video=dest/(stem+'.mp4')
   if not video.exists():
    title,hero,limitation=display
    texts={'kicker':f'SMALL PROJECT, REAL SOFTWARE  /  {pid}  /  {idx:02} OF {len(scenes):02}', 'title':title,'hero':'\n'.join(textwrap.wrap(hero,43)),'limit':'\n'.join(textwrap.wrap(limitation,75)),'footer':'Evidence as of 2026-10-14  |  AI-generated narration  |  Source references accompany the article'}
    if idx==1:texts['footer']='Evidence as of 2026-10-14  |  AI-generated narration'
    filters=[]
    for key,(y,size,color,font) in {'kicker':(80,28,'0x6EE7CF',FONT),'title':(190,65,'white',BOLD),'hero':(365,61,'white',FONT),'limit':(665,34,'0xCDD8E7',FONT),'footer':(955,24,'0xAAB8CB',FONT)}.items():
     path=dest/(stem+'-'+key+'.txt');path.write_text(texts[key]);filters.append(f"drawtext=fontfile='{filter_path(font)}':textfile='{filter_path(path)}':x=100:y={y}:fontsize={size}:fontcolor={color}:line_spacing=18")
    command([FF,'-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x0B1324:s=1920x1080:r=24','-i',str(wav),'-vf',','.join(filters),'-c:v','libx264','-preset','ultrafast','-tune','stillimage','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t',str(seconds+.15),'-af','apad=pad_dur=0.15','-movflags','+faststart',str(video)])
   records.append({'scene':idx,'narration':scene['narration'],'claim_ids':scene['claim_ids'],'audio_path':str(wav.relative_to(ROOT)),'source_clip_path':str(video.relative_to(ROOT)),'measured_source_clip_seconds':duration(video)})
   print(f'Piece {pid}: scene {idx}/{len(scenes)} ready',flush=True)
  listing=dest/'concat.txt';listing.write_text(''.join("file '"+str((dest/f'scene-{i:02}.mp4').resolve())+"'\n" for i in range(1,len(scenes)+1)))
  joined=dest/'source-video.mp4'
  if not joined.exists():command([FF,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(joined)])
  seconds=duration(joined)
  if not 185<=seconds<=290:
   target=min(280,max(195,seconds));factor=seconds/target;adjusted=dest/'source-video-paced.mp4'
   command([FF,'-hide_banner','-loglevel','error','-y','-i',str(joined),'-vf',f'setpts=PTS/{factor}','-af',f'atempo={factor}','-c:v','libx264','-preset','ultrafast','-crf','23','-c:a','aac','-b:a','128k','-movflags','+faststart',str(adjusted)]);joined=adjusted;seconds=duration(joined)
  assert 180<=seconds<=300,(pid,seconds)
  record={'piece_id':pid,'status':'source_media_ready_not_google_vids_export','built_at':now(),'source_video_path':str(joined.relative_to(ROOT)),'measured_source_video_seconds':seconds,'scenes':records,'provider_voice_model':'tts-1','voice':'alloy','no_visible_presenter':True,'google_vids_editing_and_export_completed':False,'cost_usd':None}
  save(dest/'media_manifest.json',record);overall.append(record);print(f'Piece {pid}: source video ready, {seconds:.2f} seconds',flush=True)
 save(OUT/'media_manifest.json',overall)
if __name__=='__main__':
 try:main()
 except Exception as e:print(safe_error(e),file=sys.stderr);sys.exit(1)
