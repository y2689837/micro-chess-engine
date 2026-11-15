import os,json,urllib.request as R
M=[0,100,320,330,500,975,0]
NO=[-33,-31,-18,-14,14,18,31,33]
D4=[-17,-15,15,17];D2=[-16,-1,1,16];D8=D4+D2
CM={0:13,7:14,4:12,112:7,119:11,116:3}
B=[0]*128;KP=[4,116];W=1;CA=0;EP=-1;ND=0;I=10**6
U0=os.getenv('MAKEFUN_ENV_URL','')
TT={};HS={};KL={};PTH=[];REP=set();key=lambda:(tuple(B),W,CA,EP)
def at(s,y):
 for ds,ps,sl in(((-15*y,-17*y),2,0),(NO,4,0),(D8,64,0),(D4,40,1),(D2,48,1)):
  for o in ds:
   t=s+o
   while not t&0x88 and not B[t]and sl:t+=o
   if not t&0x88 and B[t]*y>0 and 1<<abs(B[t])&ps:return 1
 return 0
def gen(cap=0):
 ms=[];ap=ms.append
 for s,p in enumerate(B):
  if p*W<1:continue
  a=abs(p);r=s>>4
  if a==1:
   dr=16*W;lr=(7+5*W)//2;px=(5,4,3,2)if r==lr else(0,)
   for o in(dr-1,dr+1):
    t=s+o
    if not t&0x88 and(B[t]*W<0 or t==EP):
     for x in px:ap(s|t<<7|x<<14)
   t=s+dr
   if not cap and not B[t]:
    for x in px:ap(s|t<<7|x<<14)
    if r==7-lr and not B[t+dr]:ap(s|(t+dr)<<7)
  else:
   ds=(NO,D4,D2,D8,D8)[a-2]
   for o in ds:
    t=s
    while not(t+o)&0x88:
     t+=o;v=B[t]
     if v:
      if v*W<0:ap(s|t<<7)
      break
     if not cap:ap(s|t<<7)
     if a in(2,6):break
 if not cap:
  h=112*(W<0);c=at(h+4,-W)
  for bb,ee,tr in((1,(5,6),5),(2,(1,2,3),3)):
   if not c and CA&(bb*(4-3*(W>0)))and not any(B[h+x]for x in ee)and not at(h+tr,-W):ap((h+4)|(h+2*tr-4)<<7)
 return ms
def mk(m):
 global W,CA,EP
 z=(B[:],CA,EP,KP[:]);f=m&127;t=(m>>7)&127;a=abs(B[f]);B[f]=0
 if a==1 and t==EP:B[t-16*W]=0
 B[t]=(m>>14 or a)*W
 if a==6:
  KP[W<0]=t
  if t-f==2:B[f+1]=B[f+3];B[f+3]=0
  elif f-t==2:B[f-1]=B[f-4];B[f-4]=0
 CA&=CM.get(f,15)&CM.get(t,15)
 EP=(f+t)//2 if a==1 and abs(t-f)==32 else -1
 W=-W;return z
def un(z):
 global W,CA,EP
 B[:]=z[0];CA=z[1];EP=z[2];KP[:]=z[3];W=-W
def ev():
 s=0
 for i,p in enumerate(B):
  if not p:continue
  x=abs(p);r=i>>4;f=i&7
  if p<0:r=7-r
  cf=min(f,7-f);cr=min(r,7-r)
  v=M[x]+(0,5,4,0,2,-5)[x-1]*(cf+cr)
  if x==1:v+=3*r**2//2+2*r
  elif x==4:v+=3*cf+25*(r==6)
  s+=v*(2*(p>0)-1)
 return s*W
def scr(m,ply,tm):
 if m==tm:return 1<<28
 t=(m>>7)&127;vv=M[abs(B[t])]
 if vv or m>>14:return(1<<24)+((vv or M[m>>14]or 100)*16-M[abs(B[m&127])]//16)
 if m in KL.get(ply,()):return 1<<20
 return min(HS.get(m,0),1<<19)
def S(d,a,b,ply):
 global ND;ND+=1
 if ND>6e4:1/0
 k=key()
 if ply and(k in PTH or k in REP):return 0
 ic=at(KP[W<0],-W);be=-I
 if d<=0 and not ic:
  be=ev()
  if be>=b:return be
 tm=0;a0=a
 if d>0:
  e=TT.get(k)
  if e:
   tm=e[3]
   if e[0]>=d:
    v=e[1]
    if e[2]==0:return v
    if e[2]==1:a=max(a,v)
    else:b=min(b,v)
    if a>=b:return v
 ms=gen(d<=0 and not ic)
 ms.sort(key=lambda m:-scr(m,ply,tm))
 PTH.append(k);best=be
 for m in ms:
  st=mk(m)
  if at(KP[W>0],W):un(st);continue
  v=-S(d-1,-b,-a,ply+1)
  un(st)
  if v>best:best=v;bm=m;a=max(a,v)
  if a>=b:
   t=(m>>7)&127
   if B[t]==0 and not m>>14 and t!=EP:
    KL[ply]=[m]+KL.get(ply,[0])[:1]
    HS[m]=HS.get(m,0)+d*d
   break
 PTH.pop()
 if best==-I:return-I//10+ply if ic else 0
 if d<=0:return best
 TT[k]=(d,best,(best<=a0)*2+(best>=b),bm)
 return best
def setfen(f):
 global W,CA,EP
 B[:]=[0]*128;ps=f.split();sq=112
 for ch in ps[0]:
  if ch=='/':sq-=24
  elif'0'<ch<':':sq+=int(ch)
  else:
   v='PNBRQKpnbrqk'.index(ch);v+=1-2*(v>5)*(v-2)
   B[sq]=v;sq+=1
   if abs(v)==6:KP[v<0]=sq-1
 W=2*(ps[1]=='w')-1
 CA=sum(1<<'KQkq'.index(ch)for ch in ps[2]if ch in'KQkq')
 EP=-1 if ps[3]=='-'else(int(ps[3][1])-1)*16+ord(ps[3][0])-97
 return key()
def main():
 global ND;cur=0
 while 1:
  g=json.loads(R.urlopen(U0+'/game',b'{}').read());st=g['status']
  if st=='done':break
  if st!='your_move':continue
  gn=g['game']
  if gn!=cur:cur=gn;REP.clear()
  REP.add(setfen(g['fen']))
  for x in(TT,HS,KL,PTH):x.clear()
  ND=0;m=0
  try:
   for d in range(1,80):
    S(d,-I,I,0)
    e=TT.get(key())
    if e:m=e[3]
  except:pass
  mv=''
  if m:
   for x in(m&127,(m>>7)&127):mv+=chr(97+(x&7))+str((x>>4)+1)
   if m>>14:mv+='nbrq'[(m>>14)-2]
  elif g['legal_moves']:mv=g['legal_moves'][0]
  if mv:R.urlopen(U0+'/move',json.dumps({'game':gn,'move':mv}).encode())
if __name__=='__main__':main()
