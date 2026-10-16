from common import *
run,name,code=sys.argv[1:]; path=pathlib.Path(run)/'stage_status.json'
x=load(path) if path.exists() else {}; x[name]=int(code); save(path,x)
