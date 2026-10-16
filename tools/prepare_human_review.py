"""Create an unfilled student worksheet; never creates approval or personal judgments."""
from common import *
def main():
 run=runarg(); ds=rows(run/'decisions.jsonl'); accepted=[x for x in ds if x['decision']=='accept'][:3]; others=[x for x in ds if x['decision'] in ('reject','defer')][:3]
 items={x['item_id']:x for x in rows(run/'eligible.jsonl')}
 lines=['# Student editorial review — NOT COMPLETED\n','The student must inspect original passages/transcripts and fill this worksheet.\n']
 for d in accepted+others:
  item=items.get(d['item_id'],{})
  lines+=[f'## {d["item_id"]}\n',f'- AI decision: {d["decision"]}\n- AI reason: {d["reason"]}\n- Version: {d["version_id"]}\n- My judgment: **TO COMPLETE**\n- Supporting passage / timestamp: **TO COMPLETE**\n- Correction and reason (if needed): **TO COMPLETE**\n']
  lines+=[f'- Source: [{item.get("title",d["item_id"])}]({item.get("url","")})\n- Retained text: `{item.get("text_path","")}`\n- Timestamped segments: `{item.get("segments_path") or "Not applicable (written source)"}`\n']
 if len(accepted)<3 or len(others)<3: lines+=['\nCoverage incomplete: need 3 accepted and 3 rejected/deferred items. Do not force model rejection merely to fill the sample.\n']
 lines+=['\n## Policy revision\n- Problem observed: TO COMPLETE\n- Before/after policy paths: TO COMPLETE\n- Affected rerun artifacts: TO COMPLETE\n- What changed and why: TO COMPLETE\n','\n## Approval\nAfter final checks, create approval.json yourself with the CURRENT review_id, decision, reviewer, reviewed_at and notes. No approval has been granted by this worksheet.\n']
 path=run/'human_review.md'
 if path.exists(): raise RuntimeError('Worksheet exists; refusing to overwrite student work')
 path.write_text('\n'.join(lines)); print(path)
if __name__=='__main__': cli(main)
