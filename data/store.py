"""Sole owner of persistent SQLite evidence index; immutable versions + run observations."""
import sys, pathlib, sqlite3, json, os
from common import *
def stats(folder):
 # Read-only diagnostics stay inside the storage owner. Other components must
 # not inspect SQLite directly, including isolated replay databases.
 uri=(folder/'index.sqlite').resolve().as_uri()+'?mode=ro'
 with sqlite3.connect(uri,uri=True) as db:
  versions=db.execute('SELECT item_id,version_id,record FROM versions ORDER BY item_id,version_id').fetchall()
  latest=db.execute('SELECT item_id,version_id FROM latest ORDER BY item_id').fetchall()
  return dict(item_count=len(latest),version_count=len(versions),observation_count=db.execute('SELECT COUNT(*) FROM observations').fetchone()[0],duplicate_item_versions=len(versions)-len({(x[0],x[1]) for x in versions}),duplicate_latest_items=len(latest)-len({x[0] for x in latest}),versions_fingerprint=digest(versions),latest_fingerprint=digest(latest))

def main():
 if len(sys.argv)<2: raise ValueError('Expected init|upsert RUN_DIR|list|get ITEM_ID [VERSION_ID]|stats')
 cmd=sys.argv[1]
 if cmd not in ('init','upsert','list','get','stats'): raise ValueError('Unknown store command')
 if (cmd=='upsert' and len(sys.argv)!=3) or (cmd=='get' and len(sys.argv) not in (3,4)) or (cmd in ('init','list','stats') and len(sys.argv)!=2): raise ValueError('Invalid store arguments')
 folder=pathlib.Path(os.getenv('PIPELINE_STORE_DIR','data/evidence'))
 if cmd=='stats': emit(stats(folder)); return
 folder.mkdir(parents=True,exist_ok=True)
 with sqlite3.connect(folder/'index.sqlite') as db:
  db.executescript('CREATE TABLE IF NOT EXISTS versions(item_id TEXT,version_id TEXT,record TEXT,first_seen TEXT,PRIMARY KEY(item_id,version_id)); CREATE TABLE IF NOT EXISTS latest(item_id TEXT PRIMARY KEY,version_id TEXT); CREATE TABLE IF NOT EXISTS observations(run_id TEXT,item_id TEXT,version_id TEXT,observed_at TEXT,change TEXT);')
  if cmd=='init': return
  if cmd=='upsert':
   run=pathlib.Path(sys.argv[2])
   with stage('store_upsert',run) as rec:
    records=incoming(); rec['input_count']=len(records)
    for item in records:
     require_keys(item,['item_id','version_id','text_path','segments_path'])
     ident,version=item['item_id'],item['version_id']
     old=db.execute('SELECT version_id FROM latest WHERE item_id=?',(ident,)).fetchone()
     exists=db.execute('SELECT 1 FROM versions WHERE item_id=? AND version_id=?',(ident,version)).fetchone()
     change='unchanged' if exists else ('changed' if old else 'new')
     db.execute('INSERT OR IGNORE INTO versions VALUES(?,?,?,?)',(ident,version,json.dumps(item),now()))
     db.execute('INSERT OR REPLACE INTO latest VALUES(?,?)',(ident,version))
     db.execute('INSERT INTO observations VALUES(?,?,?,?,?)',(str(run),ident,version,now(),change))
     emit(dict(item_id=ident,version_id=version,change=change)); rec['output_count']+=1
  elif cmd=='list':
   for row in db.execute('SELECT v.record FROM versions v JOIN latest l USING(item_id,version_id) ORDER BY item_id'): emit(json.loads(row[0]))
  else:
   query='SELECT record FROM versions WHERE item_id=? AND version_id=?' if len(sys.argv)==4 else 'SELECT v.record FROM versions v JOIN latest l USING(item_id,version_id) WHERE item_id=?'
   row=db.execute(query,tuple(sys.argv[2:])).fetchone()
   if row is None: raise RuntimeError('Evidence item/version not found')
   emit(json.loads(row[0]))
if __name__=='__main__': cli(main)
