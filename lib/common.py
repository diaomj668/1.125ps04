"""Shared IO, validation and receipts only; stage business logic stays in its owner."""
import contextlib, datetime as dt, hashlib, json, os, pathlib, sys, time, uuid
ROOT = pathlib.Path(__file__).resolve().parents[1]
os.chdir(ROOT)
def now(): return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')
def load(p): return json.loads(pathlib.Path(p).read_text())
def save(p,x):
 p=pathlib.Path(p); p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rows(p):
 p=pathlib.Path(p)
 return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
def incoming():
 try: return [json.loads(l) for l in sys.stdin if l.strip()]
 except json.JSONDecodeError as e: raise ValueError('Malformed JSONL input: '+str(e))
def emit(x): print(json.dumps(x,ensure_ascii=False),flush=True)
def jsonl(p,rs):
 p=pathlib.Path(p); p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def rel(p): return str(pathlib.Path(p).resolve().relative_to(ROOT))
def date(value):
 if not value: return None
 try:
  parsed=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
  if parsed.tzinfo is None: parsed=parsed.replace(tzinfo=dt.timezone.utc)
  return parsed.astimezone(dt.timezone.utc).date()
 except (ValueError,TypeError):
  try: return dt.date.fromisoformat(value)
  except (ValueError,TypeError): return None
def runarg():
 if len(sys.argv)!=2: raise ValueError('Expected RUN_DIR as first positional argument')
 r=pathlib.Path(sys.argv[1]); load(r/'run.json'); return r
def fetch(url,**kw):
 import requests
 r=requests.get(url,timeout=kw.pop('timeout',30),headers={'User-Agent':'PS04EvidencePipeline/1.0 (educational research)'},**kw)
 r.raise_for_status(); return r
@contextlib.contextmanager
def stage(name,run):
 start=now(); meta=dict(stage=name,status='completed',input_count=0,output_count=0,started_at=start,tools=['python'],models=[],cost_usd=0.0,cost_estimated=False,errors=[])
 try: yield meta
 except Exception as e:
  meta['status']='invalid' if isinstance(e,(ValueError,KeyError)) else 'failed'
  meta['errors'].append(safe_error(e)); print(f'{name}: {safe_error(e)}',file=sys.stderr)
  raise
 finally:
  meta['finished_at']=now()
  save(pathlib.Path(run)/'logs'/f'{name.replace("/","_")}-{uuid.uuid4().hex}.json',meta)
def safe_error(error):
 message=str(error)
 for key in ('OPENAI_API_KEY','ANTHROPIC_API_KEY'):
  secret=os.getenv(key)
  if secret: message=message.replace(secret,'[REDACTED]')
 return message

def cli(fn):
 try: fn()
 except (ValueError,KeyError) as e: print(safe_error(e),file=sys.stderr); sys.exit(2)
 except Exception as e: print(safe_error(e),file=sys.stderr); sys.exit(1)
def require_keys(obj,keys):
 for k in keys:
  if k not in obj: raise ValueError('Missing required field: '+k)
def evidence_packet(items):
 out=[]
 for item in items:
  x=dict(item)
  x['segments']=load(x['segments_path']) if x.get('segments_path') else []
  x['text']=('Full transcript is supplied as timestamped segments below; text_path is retained.' if x['segments'] else pathlib.Path(x['text_path']).read_text())
  out.append(x)
 return out

try:
 from dotenv import load_dotenv
 load_dotenv(ROOT/'.env',override=False)
except ImportError:
 pass
