import os,json,urllib.request as U
KN=(-33,-31,-18,-14,14,18,31,33)
KD=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
MT=(0,100,300,320,500,950,0)
PS=("OOOOhhhhTTY^QQT[OOOYQMJOQTTEOOOO",
"6;@@;EOO@OTW@QWY@OWY@QTW;EOT6;@@",
"",
"OOOOQTTTMOOOMOOOMOOOMOOOMOOOOOOQ","","@;;6@;;6@;;6E@@;JEEETYYOY^^TY^TO")
CM={116:12,119:14,112:13,4:3,7:11,0:7}
E=os.environ
B=[0]*128;KP={}
N=STOP=0
BUD=int(E.get("BOT_BUDGET",45000))
def att(s,by):
 for ds,v in ((15*by,17*by),1),(KN,2),(KD,6):
  for o in ds:
   if not (s+o)&136 and B[s+o]==v*by:return 1
 for o in KD:
  t=s+o
  while not t&136:
   p=B[t]
   if p:
    if p//by in (5,3 if o in BD else 4):return 1
    break
   t+=o
 return 0
def gen(cap):
 ms=[];ap=ms.append
 for s in range(128):
  p=B[s]
  if p*W<=0:continue
  a=abs(p)
  if a==1:
   d=-16*W;pr,sr=(0,6) if W>0 else (7,1)
   def pm(t):
    for q in (5,4,3,2):ap(s|t<<7|q<<14)
   t=s+d
   if not B[t]:
    if t>>4==pr:pm(t)
    elif not cap:
     ap(s|t<<7)
     if (s>>4)==sr and not B[s+2*d]:ap(s|(s+2*d)<<7)
   for dd in (d-1,d+1):
    t=s+dd
    if t&136:continue
    if B[t]*W<0:pm(t) if t>>4==pr else ap(s|t<<7)
    elif t==EP:ap(s|t<<7|1<<17)
  else:
   sl=2<a<6
   for o in ((),(),KN,BD,RD,KD,KD)[a]:
    t=s+o
    while not t&136:
     if B[t]:
      if B[t]*W<0:ap(s|t<<7)
      break
     if not cap:ap(s|t<<7)
     if not sl:break
     t+=o
   if a==6 and not cap:
    kh=60+56*W
    for dd,bt in (1,1),(-1,2):
     if CA&(bt*4**(W<0)) and not B[kh+dd] and not B[kh+2*dd] and (dd>0 or not B[kh+3*dd]) and B[kh+(3+(dd<0))*dd]==4*W and all(not att(kh+i*dd,-W) for i in (0,1,2)):ap(s|(kh+2*dd)<<7)
 return ms
def push(m):
 global W,CA,EP
 s=m&127;t=m>>7&127;pr=m>>14&7;ef=m>>17
 old=(B[:],CA,EP,W,KP[1],KP[-1])
 p=B[s]
 cp=B[t] if not ef else -W
 if cp:B[t if not ef else t+16*W]=0
 B[s]=0
 B[t]=pr*W if pr else p
 if p==6*W:
  KP[W]=t
  if abs(t-s)==2:
   rs,rt=(s+3,s+1) if t>s else (s-4,s-1)
   B[rt]=B[rs];B[rs]=0
 CA &= CM.get(s,15)&CM.get(t,15)
 EP=(s+t)//2 if p==W and abs(t-s)==32 else -1
 W=-W
 return old
def pop(tk):
 global B,W,CA,EP
 B,CA,EP,W,KP[1],KP[-1]=tk
def parse(f):
 global B,W,CA,EP
 B=[0]*128;CA=0;EP=-1
 f=f.split()
 s=0
 for ch in f[0]:
  if ch=="/":s+=8
  elif ch.isdigit():s+=int(ch)
  else:
   p="PNBRQK".find(ch.upper())+1
   if ch.islower():p=-p
   B[s]=p
   if abs(p)==6:KP[(p>0)-(p<0)]=s
   s+=1
 W=1 if f[1]=="w" else -1
 for i in range(4):
  if "KQkq"[i] in f[2]:CA|=1<<i
 if f[3]!="-":EP=(8-int(f[3][1]))*16+ord(f[3][0])-97
def uci(m):
 s=m&127;t=m>>7&127
 r=chr(97+(s&7))+str(8-(s>>4))+chr(97+(t&7))+str(8-(t>>4))
 if m>>14&7:r+="  nbrq"[m>>14&7]
 return r
def ev():
 sc=0
 for s in range(128):
  p=B[s]
  if p:
   r=s>>4;f=s&7;a=abs(p)
   v=MT[a]+((ord(PS[a-1][(r if p>0 else 7-r)*4+min(f,7-f)])-79)*2 if a in (1,2,4) else 0)
   sc+=v if p>0 else -v
 return sc*W
def neg(d,ply,a,b):
 global N,STOP,TB
 if STOP:return 0
 N+=1;STOP=N>=BUD
 if d<=0:
  st=ev()
  if st>=b:return b
  a=max(a,st)
 ms=gen(d<=0)
 ms.sort(key=lambda m:-MT[abs(B[(m>>7)&127])])
 bst=-999999;bm=0
 for m in ms:
  tk=push(m)
  if att(KP[-W],W):pop(tk);continue
  s=-neg(d-1,ply+1,-b,-a)
  pop(tk)
  if STOP:return bst if bm else a if d<=0 else 0
  if s>bst:
   bst=s;bm=m
   if ply==0:TB=m
  if s>a:a=s
  if a>=b:return b if d<=0 else bst
 if not bm and d>0:return -100000+ply if att(KP[W],-W) else 0
 return a if d<=0 else bst
def find():
 global N,STOP,TB
 N=STOP=TB=0;bm=0
 for d in range(1,64):
  neg(d,0,-999999,999999)
  if STOP or not TB:break
  bm=TB
 return bm
OP=U.build_opener(U.ProxyHandler({}))
def post(p,o):
 with OP.open(U.Request(E["MAKEFUN_ENV_URL"]+p,data=json.dumps(o).encode())) as r:return json.loads(r.read())
def main():
 g=post("/game",{})
 while g.get("status")!="done":
  while g.get("status")=="your_move":
   parse(g["fen"])
   m=find()
   u=uci(m)
   if u not in g["legal_moves"]:u=g["legal_moves"][0]
   g=post("/move",{"game":g["game"],"move":u})
  g=post("/game",{})
if __name__=="__main__":main()
