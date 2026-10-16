"""Pure text metrics; exclude production directions and references from narration."""
import re
def word_count(text): return len(re.findall(r"\b[\w'-]+\b",text))
def narration_text(markdown):
 body=markdown.split('\n## References')[0]
 blocks=re.findall(r'^\*\*Narration:\*\*[ \t]*(.*?)(?=^\*\*[^*\n]+:\*\*|^#{1,6}\s|\Z)',body,flags=re.S|re.M)
 text='\n'.join(blocks) if blocks else body
 # Standalone evidence lines and claim markers are production annotations.
 text=re.sub(r'^\s*\[\d{2}-c\d+\].*$', '', text, flags=re.M)
 return re.sub(r'\[\d{2}-c\d+\]', '', text)
