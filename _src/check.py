import json,re,html,concurrent.futures as cf,subprocess
exec(open('data3.py').read())
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
def chk(u):
  try:
    r=subprocess.run(["curl","-sL","-m","25","-A",UA,"-H","Accept-Language: en-US","-o","/tmp/pg","-w","%{http_code} %{url_effective}",u],capture_output=True,text=True,timeout=40)
    code,eff=r.stdout.split(" ",1)
    body=open('/tmp/pg','rb').read().decode('utf8','ignore') if False else ""
  except Exception as e: return u,"ERR",u,"",""
  return u,code,eff,"",""
def chk2(u):
  import tempfile,os
  f=tempfile.mktemp()
  r=subprocess.run(["curl","-sL","-m","25","-A",UA,"-H","Accept-Language: en-US","-o",f,"-w","%{http_code} %{url_effective}",u],capture_output=True,text=True)
  try: code,eff=r.stdout.split(" ",1)
  except: code,eff="ERR",u
  b=open(f,'rb').read().decode('utf8','ignore') if os.path.exists(f) else ""
  t=re.search(r'<title[^>]*>(.*?)</title>',b,re.S|re.I)
  d=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)',b,re.I) or re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description',b,re.I) or re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']*)',b,re.I)
  clean=lambda s: html.unescape(re.sub(r'\s+',' ',s)).strip() if s else ""
  return u,code,eff,clean(t.group(1)) if t else "",clean(d.group(1)) if d else ""
urls=[u for L in (C,M,A) for c,ts in L for n,u,d in ts]
res={}
with cf.ThreadPoolExecutor(16) as ex:
  for u,code,eff,t,d in ex.map(chk2,urls): res[u]={"code":code,"final":eff,"title":t,"desc":d}
json.dump(res,open('urlcheck.json','w'),indent=1)
for u,v in res.items():
  if v["code"]!="200": print(v["code"],u,"->",v["final"])
print(len(res),"checked")
