from common import *
def main():
 if len(sys.argv)!=6: raise ValueError('receipt.py RUN_DIR STAGE STATUS INPUT_COUNT OUTPUT_COUNT')
 run,name,status,inputs,outputs=sys.argv[1:]
 with stage(name,run) as rec:
  rec.update(status=status,input_count=int(inputs),output_count=int(outputs))
  if status!='completed': rec['errors'].append('One or more child stages failed; see child receipts and stage_status.json')
if __name__=='__main__': cli(main)
