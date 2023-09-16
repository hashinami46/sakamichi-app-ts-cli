s='Process Cancelled by User'
r='nogifra_sounds'
q='nogifra_movies'
p='nogifra_images'
o='sakukoi_card'
n='itsunogi_sprites'
m='nogifes_card'
l='GET'
k=KeyboardInterrupt
j=bytes
i=range
g='Texture2D'
f='movie'
b='3'
a='09'
Z='08'
Y='07'
X='06'
W=open
V='05'
U='02'
T='01'
S=exit
R='04'
Q='03'
P=len
O=''
N=int
L=print
K='4'
J='1'
I='sakumsg'
H='sakukoi'
G='2'
D='hinamsg'
C='hinakoi'
B='name'
A='gen'
import os as E,re,json,httpx as c,UnityPy as d,argparse as t
from PIL import Image as h
from PyCriCodecs import CPK,USM as e,ACB,AWB,HCA
u=[{B:'櫻坂46',A:O,H:O,I:'33'},{B:'上村莉菜',A:J,H:T,I:K},{B:'小池美波',A:J,H:U,I:'7'},{B:'小林由依',A:J,H:Q,I:'8'},{B:'齋藤冬優花',A:J,H:R,I:'9'},{B:'土生瑞穂',A:J,H:V,I:'15'},{B:'遠藤光',A:G,H:U,I:O},{B:'大園玲',A:G,H:Q,I:'56'},{B:'大沼晶保',A:G,H:R,I:'57'},{B:'幸坂茉莉乃',A:G,H:V,I:'58'},{B:'武元唯衣',A:G,H:X,I:'46'},{B:'田村保乃',A:G,H:Y,I:'47'},{B:'藤吉夏鈴',A:G,H:Z,I:'48'},{B:'増本綺良',A:G,H:a,I:'59'},{B:'松田里奈',A:G,H:'10',I:'49'},{B:'森田ひかる',A:G,H:'11',I:'51'},{B:'守屋麗奈',A:G,H:'12',I:'60'},{B:'山﨑天',A:G,H:'13',I:'52'}]
v=[{B:'日向坂46',A:O,C:O,D:'43'},{B:'潮紗理菜',A:J,C:T,D:'22'},{B:'加藤史帆',A:J,C:Q,D:'25'},{B:'齊藤京子',A:J,C:R,D:'26'},{B:'佐々木久美',A:J,C:V,D:'27'},{B:'佐々木美玲',A:J,C:X,D:'28'},{B:'高瀬愛奈',A:J,C:Y,D:'29'},{B:'高本彩花',A:J,C:Z,D:'30'},{B:'東村芽依',A:J,C:a,D:'32'},{B:'金村美玖',A:G,C:T,D:'34'},{B:'河田陽菜',A:G,C:U,D:'35'},{B:'小坂菜緒',A:G,C:Q,D:'36'},{B:'富田鈴花',A:G,C:R,D:'37'},{B:'丹生明里',A:G,C:V,D:'38'},{B:'濱岸ひより',A:G,C:X,D:'39'},{B:'松田好花',A:G,C:Y,D:'40'},{B:'宮田愛萌',A:G,C:Z,D:O},{B:'渡邉美穂',A:G,C:a,D:O},{B:'上村ひなの',A:b,C:T,D:'53'},{B:'髙橋未来虹',A:b,C:U,D:'61'},{B:'森本茉莉',A:b,C:Q,D:'62'},{B:'山口陽世',A:b,C:R,D:'63'},{B:'石塚瑶季',A:K,C:T,D:'66'},{B:'岸帆夏',A:K,C:U,D:'67'},{B:'小西夏菜実',A:K,C:Q,D:'68'},{B:'清水理央',A:K,C:R,D:'69'},{B:'正源司陽子',A:K,C:V,D:'70'},{B:'竹内希来里',A:K,C:X,D:'71'},{B:'平尾帆夏',A:K,C:Y,D:'72'},{B:'平岡海月',A:K,C:Z,D:'73'},{B:'藤嶌果歩',A:K,C:a,D:'74'},{B:'宮地すみれ',A:K,C:'10',D:'75'},{B:'山下葉留花',A:K,C:'11',D:'76'},{B:'渡辺莉奈',A:K,C:'12',D:'77'}]
A1=[{B:'齋藤飛鳥',A:J,'asukamsg':J}]
def w(infile,outdir,key):e(infile,key=key).extract(dirname=outdir)
def x(infile,outdir,key):A=outdir;CPK(infile).extract();e(f,key=key).extract(dirname=A);ACB('music').extract(dirname=A,decode=True,key=key)
def y(asset_type,infile,outfile):
	A=outfile
	with c.stream(l,infile,timeout=None)as C:
		D=d.load(C.read())
		for B in D.objects:
			if B.type.name==g:B.read().image.save(A)
			if asset_type not in[m,n]:
				with h.open(A)as E:E.resize((900,1200),resample=h.LANCZOS).save(A);S(0)
def z(asset_type,catalog,path_server,path_local,from_index=0,to_index=0):
	a='fileSize';Z='location';Y='card';T=catalog;R='assetBundleName';O=to_index;M='data';J=from_index;I=path_local;G='/';F=asset_type
	if H in F:U=u
	elif C in F:U=v
	V=path_server.split(G);V[-2]=T.split('_')[2]
	def X(filename):
		R='content-length';M=filename
		with c.stream(l,G.join(V)+G+M,timeout=None)as H:
			if H.status_code!=200:L('\x1b[38;5;1mWhoops, server error\x1b[0m');S(1)
			D=bytearray(H.read());O=D[7]
			for P in i(150):D[P]^=O
			Q=d.load(j(D))
			if Q.objects and Y in F:
				for C in Q.objects:
					T='\\d{7}_'if F==o else'\\d{8}_\\d'
					if C.type.name==g and 100000<=N(H.headers[R])<=1000000 and re.match(T,C.read().name):
						for K in U:
							if C.read().name[3:6]==K[A]+K[F.split('_')[0]]:
								J=E.path.join(I,f"{K[A]}. {K[B]}")
								if not E.path.exists(J):E.makedirs(J)
								if E.path.exists(E.path.join(J,f"{C.read().name}.png")):L(f"[38;5;11m{C.read().name} already exist[0m")
								if not E.path.exists(E.path.join(J,f"{C.read().name}.png")):C.read().image.save(E.path.join(J,f"{C.read().name}.png"));L(f"{C.read().name} saved!")
			elif not Q.objects and f in F:
				if N(H.headers[R])>=1000000:
					if not E.path.exists(I):E.makedirs(I)
					O=D[15]
					for P in i(150):D[P]^=O
					with W(E.path.join(I,f"{M.split(G)[1]}.mp4"),'wb')as X:X.write(j(D))
					L(f"{M.split(G)[1]}.mp4 Downloaded!")
		H.close()
	b=c.Client()
	with W(T,'rb')as e:K=json.load(e)
	if J>P(K[M])or O>P(K[M]):L('\x1b[38;5;1mWhoops, an error occured!\x1b[0m');S(1)
	L(f"Data length : {str(P(K[M]))}")
	if J==0 or O==0:Q=K[M]
	if J!=0 and O!=0:Q=K[M][J:O]
	if J!=0 and O==0:Q=K[M][J:]
	L(f"Total requested range: {str(P(Q))}")
	if Y in F:
		for D in Q:
			if D[Z]==2 and 100000<=N(D[a])<=1000000:X(D[R])
	elif f in F:
		for D in Q:
			if D[Z]==2 and N(D[a])>=1000000:
				if E.path.exists(E.path.join(I,f"{D[R].split(G)[1]}.mp4")):L(f"[38;5;11m{D[R].split(G)[1]} already exists![0m")
				if not E.path.exists(E.path.join(I,f"{D[R].split(G)[1]}.mp4")):X(D[R])
	b.close()
def A0(asset_type,infile,outdir):
	G='audio';D=asset_type;B=outdir;A=infile
	if D==p:
		F=d.load(A)
		if P(F.objects)==2:
			for C in F.objects:
				if not E.path.exists(B):E.makedirs(B)
				if E.path.exists(E.path.join(B,f"{C.read().name}.png")):E.remove(A);L(f"[38;5;11m{C.read().name} already exist[0m")
				if C.type.name==g and not E.path.exists(E.path.join(B,f"{C.read().name}.png")):C.read().image.save(E.path.join(B,f"{C.read().name}.png"));E.remove(A);L(f"{C.read().name} saved!")
	elif D==q:e(A).extract(dirname=B)
	elif D==r:
		if A.endswith('.awb',0,P(A)):
			for H in AWB(A).getfiles():W(G,'ab').write(H)
			with W(f"{B}.wav",'wb')as I:I.write(HCA(G,key=0xdaa20c336eeae72).decode())
M=t.ArgumentParser(description='Downloader Helper')
M.add_argument('--type')
M.add_argument('--infile')
M.add_argument('--outdir')
M.add_argument('--key')
M.add_argument('--outfile')
M.add_argument('--catalog')
M.add_argument('--pathserver')
M.add_argument('--pathlocal')
M.add_argument('--fromindex')
M.add_argument('--toindex')
F=M.parse_args()
if __name__=='__main__':
	if F.type in['nogifes_movie_card','nogifes_reward_movie']:w(F.infile,F.outdir,N(F.key))
	elif F.type in['nogifes_focus_data_lo','nogifes_focus_data_hi']:x(F.infile,F.outdir,N(F.key))
	elif F.type in[m,n,'itsunogi_card','itsunogi_photo']:y(F.type,F.infile,F.outfile)
	elif F.type in[o,'hinakoi_card','sakukoi_movie','hinakoi_movie']:
		try:z(F.type,F.catalog,F.pathserver,F.pathlocal,N(F.fromindex),N(F.toindex))
		except k:L(s);S(0)
	elif F.type in[p,r,q]:
		try:A0(F.type,F.infile,F.outdir)
		except k:L(s);S(0)