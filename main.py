import os,json,urllib.request as U
E=os.environ
KN=(-33,-31,-18,-14,14,18,31,33)
KD=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17)
MV=(0,100,300,320,500,900,0)
RK=(1,-1,16,-16)
CM={116:12,119:14,112:13,4:3,7:11,0:7}
B=[0]*128;KP={}
BUD=60000
TT={};KL={};PTH=[];REP=set();HS={}
def att(s,by):
 for ds,v in ((15*by,17*by),1),(KN,2),(BD,3),(RK,4),(KD,5),(KD,6):
  for o in ds:
   t=s
   while not (t:=t+o)&136:
    if B[t]==v*by:return 1
    if B[t] or v<3 or v==6:break
def gen(cap):
 ms=[];ap=ms.append
 for s,p in enumerate(B):
  if p*W<=0:continue
  a=abs(p)
  if a==1:
   d=-16*W
   for o in (d-1,d,d+1):
    t=s+o
    if t&136:continue
    v=B[t]
    if o==d:
     if v:continue
    elif v*W>=0 and t!=EP:continue
    if t>>4 in (0,7):
     for q in (5,4,3,2):ap(s|t<<7|q<<14)
    elif o!=d or not cap:
     ap(s|t<<7)
     if o==d and s>>4 in (1,6) and not B[s+2*d]:ap(s|(s+2*d)<<7)
  else:
   for o in (KN,BD,(1,16,-1,-16),KD,KD)[a-2]:
    t=s+o
    while not t&136:
     v=B[t]
     if v*W<0 or not (v or cap):ap(s|t<<7)
     if v or a in (2,6):break
     t+=o
   if a==6 and not cap:
    for dd,bt in ((2,1),(-2,2)):
     if CA&(bt*4**(W<0)) and not (B[s+dd//2] or B[s+dd] or dd<0 and B[s-3]) and not att(s,-W) and not att(s+dd//2,-W):ap(s|(s+dd)<<7)
 return ms
def mk(m):
 global W,CA,EP
 s=m&127;t=(m>>7)&127;p=B[s];a=abs(p)
 u=(B[:],CA,EP,KP[1],KP[-1])
 if a==1 and t==EP:B[t+16*W]=0
 B[s]=0;B[t]=((m>>14)or p//W)*W
 if a==6:
  KP[W]=t
  if abs(t-s)==2:
   r=(s+3,s-4)[t<s];B[(s+t)//2]=B[r];B[r]=0
 CA&=CM.get(s,15)&CM.get(t,15)
 EP=(s+t)//2 if a==1 and abs(t-s)==32 else -1
 W=-W
 return u
def ev():
 e=0
 for s,p in enumerate(B):
  if p:
   a=abs(p);r=(s>>4)^7*(p>0);cf=min(s&7,7-s&7);c=cf+min(r,7-r)
   e+=(MV[a]+(3*r*r//2+2*r,9*c,7*c,3*cf+15*(r==6),3*c,-6*min(r,3)-4*c)[a-1])*(p//a)
 return e*W
def sk(m,tm,ply):
 if m==tm:return 1<<28
 t=(m>>7)&127;v=B[t]
 if v or m>>14 or t==EP:return (1<<24)+((MV[abs(v)] or MV[m>>14] or 100)*16-MV[abs(B[m&127])]//16)
 return (1<<20) if m in KL.get(ply,()) else min(HS.get(m,0),1<<19)
def neg(d,a,b,ply):
 global ND,TB,W,CA,EP
 ND+=1
 if ND>=BUD:1/0
 k=(tuple(B),W,CA,EP)
 if ply and (k in PTH or k in REP):return 0
 ent=TT.get(k);tm=ent and ent[3]
 if ent and ply and ent[0]>=d:
  v,f=ent[1],ent[2]
  if f==0:return v
  if f==1:a=max(a,v)
  else:b=min(b,v)
  if a>=b:return v
 a0=a;bst=-10**6
 ic=d<=0 and att(KP[W],-W)
 if d<=0 and not ic:
  bst=ev()
  if bst>=b:return bst
  a=max(a,bst)
 PTH.append(k)
 for m in sorted(gen(d<=0 and not ic),key=lambda m:-sk(m,tm,ply)):
  u=mk(m)
  if att(KP[-W],W):
   B[:],CA,EP,KP[1],KP[-1]=u;W=-W;continue
  v=-neg(d-1,-b,-a,ply+1)
  B[:],CA,EP,KP[1],KP[-1]=u;W=-W
  if v>bst:bst=v;bm=m
  a=max(a,v)
  if a>=b:
   if d>0:
    t=(m>>7)&127
    if not B[t] and m<16384 and t!=EP:KL[ply]=[m]+KL.get(ply,[])[:1];HS[m]=HS.get(m,0)+d*d
   break
 PTH.pop()
 if bst==-10**6:return -100000+ply if att(KP[W],-W) else 0
 if not ply:TB=bm
 if d>0:TT[k]=(d,bst,(bst<=a0)*2+(bst>=b),bm)
 return bst
def parse(f):
 global W,CA,EP
 B[:]=[0]*128;CA=0;EP=-1
 f=f.split();s=0
 for ch in f[0]:
  if ch=="/":s+=8
  elif ch.isdigit():s+=int(ch)
  else:
   p="PNBRQK".find(ch.upper())+1
   if ch.islower():p=-p
   B[s]=p
   if p*p==36:KP[p//6]=s
   s+=1
 W=1-2*(f[1]=="b")
 for i in range(4):
  if "KQkq"[i] in f[2]:CA|=1<<i
 if f[3]!="-":EP=(8-int(f[3][1]))*16+ord(f[3][0])-97
OP=U.build_opener(U.ProxyHandler({}))
S="status"
def post(p,o):
 return json.loads(OP.open(U.Request(E["MAKEFUN_ENV_URL"]+p,data=json.dumps(o).encode())).read())
def main():
 global ND,TB
 G=None;g={}
 while g.get(S)!="done":
  if g.get(S)!="your_move":
   g=post("/game",{});continue
  gm=g["game"];lm=g["legal_moves"]
  if gm!=G:G=gm;REP.clear()
  parse(g["fen"]);REP.add((tuple(B),W,CA,EP))
  ND=TB=0;TT.clear();PTH.clear();HS.clear()
  for d in range(1,80):
   try:neg(d,-10**6,10**6,0)
   except:break
  m=TB;s=m&127;t=(m>>7)&127
  u=f"{chr(97+(s&7))}{8-s//16}{chr(97+(t&7))}{8-t//16}"+("  nbrq"[m>>14]if m>>14 else"")
  if u not in lm:u=lm[0]
  g=post("/move",{"game":gm,"move":u})
if __name__=="__main__":main()
