"""Audit HTTP, kesetaraan HTML, hash sumber/asset, dan referensi lokal. Python stdlib."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin, unquote
from urllib.request import urlopen
import hashlib,json,re,sys
PROJECT=Path(__file__).resolve().parents[1]; ROOT=PROJECT.parent
BASE=sys.argv[1].rstrip('/') if len(sys.argv)>1 else 'http://127.0.0.1:8000'
PAGES={'admin':{'index':'/admin','advance-sweet-alert':'/admin/advance-sweet-alert','auth-login':'/admin/auth-login','calendar':'/admin/calendar','form-elements':'/admin/form-elements','tables-datatable':'/admin/tables-datatable'},'landing':{'index':'/','about':'/about','service':'/service','menu':'/menu','booking':'/booking','team':'/team'}}
SOURCES={'admin':ROOT/'upcube/upcube','landing':ROOT/'restoran/restoran-1.0.0'}
class Document(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tokens=[];self.assets=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  self.tokens.append(('start',tag,tuple(sorted(attrs))))
  a=dict(attrs)
  if tag in ['img','script','source'] and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('href'):self.assets.append(a['href'])
  if tag in ['a','form']:self.links.append(a.get('href',a.get('action','')))
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag):self.tokens.append(('end',tag))
 def handle_data(self,data):
  data=re.sub(r'\s+',' ',data).strip()
  if data:self.tokens.append(('text',data))
def converted(s,group):
 def attr(m):
  k,q,v=m.groups()
  if v.endswith('.html') and v[:-5] in PAGES[group]:v=BASE+PAGES[group][v[:-5]].rstrip('/')
  elif (group=='admin' and v.startswith('assets/')) or (group=='landing' and v.startswith(('css/','js/','img/','lib/'))):v=BASE+'/assets/'+group+'/'+(v[7:] if group=='admin' else v)
  return k+'='+q+v+q
 return re.sub(r'\b(href|src|action)=([\"\x27])(.*?)\2',attr,s)
def parse(s):d=Document();d.feed(s);return d
report={'pages':[],'missing_html_assets':{},'missing_css_assets':{},'unprovided_links':{},'asset_http':{},'source_changed':[],'asset_changed':[]}
css=set();all_assets=set()
for group,pages in PAGES.items():
 missing={};links=set()
 for name,path in pages.items():
  original=(SOURCES[group]/(name+'.html')).read_text(encoding='utf-8')
  response=urlopen(BASE+path);rendered=response.read().decode('utf-8')
  source=parse(converted(original,group));result=parse(rendered)
  equal=source.tokens==result.tokens
  entry={'group':group,'page':name,'url':path,'status':response.status,'html_equal':equal}
  if not equal:
   import difflib
   entry['differences']=list(difflib.unified_diff([str(t) for t in source.tokens],[str(t) for t in result.tokens]))[:75]
  report['pages'].append(entry);print(path,response.status,'HTML MATCH' if equal else 'HTML DIFF')
  for url in result.assets:
   if not url.startswith(BASE+'/'):continue
   rel=unquote(urlsplit(url).path).lstrip('/');file=PROJECT/'public'/rel
   all_assets.add(urlsplit(url).path)
   if not file.is_file():missing.setdefault(rel,[]).append(name)
   elif file.suffix=='.css':css.add(file)
  for link in parse(original).links:
   if link.endswith('.html') and link[:-5] not in pages:links.add(link)
 report['missing_html_assets'][group]=missing;report['unprovided_links'][group]=sorted(links)
visited=set()
while css:
 file=css.pop()
 if file in visited:continue
 visited.add(file)
 text=file.read_text(encoding='utf-8',errors='replace')
 for value in re.findall(r'url\(\s*[\"\x27]?([^\)\"\x27]+)[\"\x27]?\s*\)',text):
  value=value.strip()
  if value.startswith(('data:','http:','https:','//','#')):continue
  local=(file.parent/unquote(urlsplit(value).path)).resolve()
  if not local.is_file():report['missing_css_assets'].setdefault(file.relative_to(PROJECT).as_posix(),[]).append(value)
  elif local.suffix=='.css':css.add(local)
  if local.is_file() and local.is_relative_to(PROJECT/'public'):all_assets.add('/'+local.relative_to(PROJECT/'public').as_posix())
for relative,expected in json.loads((PROJECT/'docs/source-sha256.json').read_text()).items():
 source=ROOT/relative
 if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:report['source_changed'].append(relative)
 for group,folder in SOURCES.items():
  if not source.is_relative_to(folder):continue
  rel=source.relative_to(folder)
  if group=='admin':
   if rel.parts[0]!='assets':continue
   rel=Path(*rel.parts[1:])
  elif rel.parts[0] not in ['css','js','img','lib','scss']:continue
  dest=PROJECT/'public/assets'/group/rel
  if not dest.is_file() or dest.read_bytes()!=source.read_bytes():report['asset_changed'].append(dest.relative_to(PROJECT).as_posix())
for asset in sorted(all_assets):
 try:
  with urlopen(BASE+asset) as r:report['asset_http'][asset]=r.status
 except Exception as e:report['asset_http'][asset]=str(e)
(PROJECT/'docs/audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Source changes:',len(report['source_changed']),'Asset differences:',len(report['asset_changed']))
print('Missing HTML assets:',report['missing_html_assets'])
print('Missing CSS dependencies:',report['missing_css_assets'])
print('Asset HTTP:',len(report['asset_http']),'checked')
sys.exit(1 if report['source_changed'] or report['asset_changed'] or any(not p['html_equal'] for p in report['pages']) else 0)
