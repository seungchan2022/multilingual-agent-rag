import json,sys,unicodedata,re
ns=json.load(open(sys.argv[1],encoding='utf-8'))['query']
names={}
for k,v in ns['namespaces'].items():
    for key in ['*','canonical']:
        if v.get(key): names[v[key].lower()]=int(k)
for al in ns['namespacealiases']: names[al['*'].lower()]=al['id']
m=json.load(open(sys.argv[2],encoding='utf-8')); c=json.load(open(sys.argv[3],encoding='utf-8'))
def norm(t):
    t=t.replace('_',' ').replace('\xa0',' ')
    t=re.sub('[‎‏‪-‮]','',t)
    t=re.sub(r'\s+',' ',t).strip()
    t=unicodedata.normalize('NFC',t)
    if t: t=t[0].upper()+t[1:]
    return t
def nonmain(t):
    return ':' in t and names.get(t.split(':')[0].strip().lower(),0)!=0
cx=set(); dropped_ns=0
for t in m:
    n=norm(t)
    if not n: continue
    if nonmain(n): dropped_ns+=1; continue
    cx.add(n)
talk=set(norm(t.split(':',1)[1]) for t in c if t.startswith('토론:'))
u=cx|talk
print('cx',len(cx),'dropped non-main',dropped_ns,'talk',len(talk),'inter',len(cx&talk),'union',len(u),'pct',round(100*len(u)/769013,3))
