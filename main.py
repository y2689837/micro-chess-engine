import json as J,urllib.request as U
KN=(-33,-31,-18,-14,14,18,31,33);KD=(-17,-16,-15,-1,1,15,16,17);BD=(-17,-15,15,17);RK=(1,-1,16,-16)
DR=(0,0,KN,BD,RK,KD,KD)
CM={116:12,119:14,112:13,4:3,7:11,0:7}
MV=(0,100,300,320,500,900,0)
B=[0]*160;KP={};TT={};HS={};REP=set();ND=0;TB=0
def att(s,by):
 if by in (B[s+17*by],B[s+15*by]):return 1
 for d in KN:
  if B[s+d]==2*by:return 1
 for d in KD:
  t=s+d;pc=3 if d in BD else 4
  while not t&136:
   p=B[t]
   if p:
    if p in (pc*by,5*by) or (p==6*by and t==s+d):return 1
    break
   t+=d
 return 0
def gen(cp):
 M=[];ap=M.append
 def ad(s,t):
  for pr in (5,4,3,2) if t<16 or t>111 else (0,):ap(s|t<<7|pr<<14)
 for s,p in enumerate(B):
  if p*W<=0:continue
  a=abs(p)
  if a==1:
   d=-16*W;t=s+d
   if not B[t] and not cp:
    ad(s,t)
    if (s>>4)==6-5*(W<0) and not B[s+2*d]:ap(s|(s+2*d)<<7)
   for t in (s+d-1,s+d+1):
    if not t&136 and (B[t]*W<0 or t==EP):ad(s,t)
  elif a>1:
   for d in DR[a]:
    t=s+d
    if a in (2,6):
     if not t&136 and B[t]*W<=0 and not (cp and not B[t]):ap(s|t<<7)
    else:
     while not t&136:
      if B[t]:
       if B[t]*W<0:ap(s|t<<7)
       break
      if not cp:ap(s|t<<7)
      t+=d
 if not cp:
  K0=KP[W]
  if not att(K0,-W):
   for bit,to,em in ((1,K0+2,(K0+1,K0+2)),(2,K0-2,(K0-1,K0-2,K0-3))):
    if CA&(bit<<(W<0)*2) and not att(em[0],-W) and all(not B[x] for x in em):ap(K0|to<<7)
 return M
def mk(m):
 global W,CA,EP
 s=m&127;t=(m>>7)&127;p=B[s];u=(B[:],CA,EP,KP[1],KP[-1])
 if t==EP and abs(p)==1 and not B[t]:B[t+16*W]=0
 B[t]=p;B[s]=0
 if m>>14:B[t]=(m>>14)*W
 if abs(p)==6:
  KP[W]=t
  if t-s==2:B[t-1]=B[t+1];B[t+1]=0
  if s-t==2:B[t+1]=B[t-2];B[t-2]=0
 CA&=CM.get(s,15)&CM.get(t,15)
 EP=(s+t)//2 if abs(p)==1 and abs(t-s)==32 else -1
 W=-W
 return u
def sk(m,tm):
 t=(m>>7)&127;v=B[t]
 if m==tm:return 1<<28
 if v or m>>14 or t==EP:return (1<<24)+((MV[abs(v)] or MV[m>>14] or 100)*16-MV[abs(B[m&127])]//16)
 return HS.get(m,0)
def neg(d,a,b,ply):
 global ND,TB,W,CA,EP
 ND+=1
 if ND>=9e4:1/0
 k=(tuple(B),W,CA,EP)
 if ply and k in REP:return 0
 ent=TT.get(k);tm=ent and ent[3]
 if ent and ply and ent[0]>=d:
  v,f=ent[1],ent[2]
  if f==0:return v
  if f==1:a=max(a,v)
  elif f==2:b=min(b,v)
  if a>=b:return v
 a0=a;bst=-1e9;bm=0
 ic=d<=0 and att(KP[W],-W)
 if d<=0 and not ic:
  e=0
  for s,p in enumerate(B):
   if p:
    a2=abs(p);r=(s>>4)^(7 if p>0 else 0);f2=min(s&7,7-(s&7));c=f2+min(r,7-r)
    e+=(MV[a2]+(3*r*r//2+2*r,9*c,7*c,3*f2+15*(r==6),3*c,-6*min(r,3)-4*c)[a2-1])*(p//a2)
  bst=e*W
  if bst>=b:return bst
  a=max(a,bst)
 for m in sorted(gen(d<=0 and not ic),key=lambda m:-sk(m,tm)):
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
    if not B[t] and not m>>14 and t!=EP:HS[m]=HS.get(m,0)+d*d
   break
 if bst==-1e9:return -100000+ply if att(KP[W],-W) else 0
 if not ply:TB=bm
 if d>0:TT[k]=(d,bst,(bst<=a0)*2+(bst>=b),bm)
 return bst
OP=U.build_opener(U.ProxyHandler({}))
def post(p,o):
 try:return J.load(OP.open(U.Request(U.os.environ["MAKEFUN_ENV_URL"]+p,data=J.dumps(o).encode()),timeout=9))
 except Exception:return {}
def main():
 global ND,TB,W,CA,EP
 G=None;g={}
 while g.get("status")!="done":
  if g.get("status")!="your_move":g=post("/game",{});continue
  gm=g["game"];lm=g["legal_moves"]
  if gm!=G:G=gm;REP.clear()
  B[:]=[0]*160;CA=0;EP=-1
  f=g["fen"].split();s=0
  for ch in f[0]:
   if ch=="/":s+=8
   elif ch.isdigit():s+=int(ch)
   else:
    p="PNBRQK".find(ch.upper())+1
    if ch.islower():p=-p
    B[s]=p
    if abs(p)==6:KP[p//6]=s
    s+=1
  W=1-2*(f[1]=="b")
  for c in "qkQK":CA=CA*2+(c in f[2])
  if f[3]!="-":EP=(8-int(f[3][1]))*16+ord(f[3][0])-97
  REP.add((tuple(B),W,CA,EP))
  ND=TB=0;TT.clear();HS.clear()
  for d in range(1,80):
   try:neg(d,-1e9,1e9,0)
   except Exception:break
  m=TB;s=m&127;t=(m>>7)&127
  u="abcdefgh"[s&7]+str(8-(s>>4))+"abcdefgh"[t&7]+str(8-(t>>4))+("nbrq"[(m>>14)-2] if m>>14 else "")
  if u not in lm:u=lm[0]
  g=post("/move",{"game":gm,"move":u})
main()
