Y='sakukoi_card'
H='itsunogi_sprites'
G='nogifes_card'
X='Texture2D'
W='GET'
V=bytes
U=range
Q='movie'
P=exit
N=len
E=int
D=print
import os as B,re,json as S,httpx as O,UnityPy as T,argparse as I
from PIL import Image as F
from PyCriCodecs import CPK,USM,ACB
def J(infile,outdir,key):USM(infile,key=key).extract(dirname=outdir)
def K(infile,outdir,key):A=outdir;CPK(infile).extract();USM(Q,key=key).extract(dirname=A);ACB('music').extract(dirname=A,decode=True,key=key)
def L(asset_type,infile,outfile):
	A=outfile
	with O.stream(W,infile,timeout=None)as C:
		D=T.load(C.read())
		for B in D.objects:
			if B.type.name==X:B.read().image.save(A)
			if asset_type not in[G,H]:
				with F.open(A)as E:E.resize((900,1200),resample=F.LANCZOS).save(A)
def M(asset_type,member_data,catalog,path_server,path_local,from_index=0,to_index=0):
	d='fileSize';c='location';b='card';R=catalog;M='assetBundleName';K=to_index;J='data';H=from_index;G=path_local;F=asset_type;C='/';Z=path_server.split(C);Z[-2]=R.split('_')[2]
	def a(filename):
		c='gen';a='content-length';L=filename
		with O.stream(W,C.join(Z)+C+L,timeout=None)as I:
			if I.status_code!=200:D('\x1b[38;5;1mWhoops, server error\x1b[0m');P(1)
			H=bytearray(I.read());M=H[7]
			for N in U(150):H[N]^=M
			R=T.load(V(H))
			if R.objects and b in F:
				for A in R.objects:
					d='\\d{7}_'if F==Y else'\\d{8}_\\d'
					if A.type.name==X and 100000<=E(I.headers[a])<=1000000 and re.match(d,A.read().name):
						for K in S.loads(member_data):
							if A.read().name[3:6]==K[c]+K[F.split('_')[0]]:
								J=B.path.join(G,f"{K[c]}. {K['name']}")
								if not B.path.exists(J):B.makedirs(J)
								if B.path.exists(B.path.join(J,f"{A.read().name}.png")):D(f"[38;5;11m{A.read().name} already exist[0m")
								if not B.path.exists(B.path.join(J,f"{A.read().name}.png")):A.read().image.save(B.path.join(J,f"{A.read().name}.png"));D(f"{A.read().name} saved!")
			elif not R.objects and Q in F:
				if E(I.headers[a])>=1000000:
					if not B.path.exists(G):B.makedirs(G)
					M=H[15]
					for N in U(150):H[N]^=M
					with open(B.path.join(G,f"{L.split(C)[1]}.mp4"),'wb')as e:e.write(V(H))
					D(f"{L.split(C)[1]}.mp4 Downloaded!")
		I.close()
	e=O.Client()
	with open(R,'rb')as f:I=S.load(f)
	if H>N(I[J])or K>N(I[J]):D('\x1b[38;5;1mWhoops, an error occured!\x1b[0m');P(1)
	D(f"Data length : {str(N(I[J]))}")
	if H==0 or K==0:L=I[J]
	if H!=0 and K!=0:L=I[J][H:K]
	if H!=0 and K==0:L=I[J][H:]
	D(f"Total requested range: {str(N(L))}")
	if b in F:
		for A in L:
			if A[c]==2 and 100000<=E(A[d])<=1000000:a(A[M])
	elif Q in F:
		for A in L:
			if A[c]==2 and E(A[d])>=1000000:
				if B.path.exists(B.path.join(G,f"{A[M].split(C)[1]}.mp4")):D(f"[38;5;11m{A[M].split(C)[1]} already exists![0m")
				if not B.path.exists(B.path.join(G,f"{A[M].split(C)[1]}.mp4")):a(A[M])
	e.close()
C=I.ArgumentParser(description='Downloader Helper')
C.add_argument('--type')
C.add_argument('--infile')
C.add_argument('--outdir')
C.add_argument('--key')
C.add_argument('--outfile')
C.add_argument('--memberdata')
C.add_argument('--catalog')
C.add_argument('--pathserver')
C.add_argument('--pathlocal')
C.add_argument('--fromindex')
C.add_argument('--toindex')
A=C.parse_args()
if __name__=='__main__':
	if A.type in['nogifes_movie_card','nogifes_reward_movie']:J(A.infile,A.outdir,E(A.key))
	elif A.type in['nogifes_focus_data_lo','nogifes_focus_data_hi']:K(A.infile,A.outdir,E(A.key))
	elif A.type in[G,H,'itsunogi_card','itsunogi_photo']:L(A.type,A.infile,A.outfile)
	elif A.type in[Y,'hinakoi_card','sakukoi_movie','hinakoi_movie']:
		try:M(A.type,A.memberdata,A.catalog,A.pathserver,A.pathlocal,E(A.fromindex),E(A.toindex))
		except KeyboardInterrupt:D('Process Cancelled by User');P(1)