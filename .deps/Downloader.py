X='sakukoi_card'
H='itsunogi_sprites'
G='nogifes_card'
W='Texture2D'
V='GET'
U=bytes
T=range
O='movie'
N=exit
L=len
E=int
C=print
import os as D,re,json as R,httpx as M,UnityPy as S,argparse as I
from PIL import Image as F
from PyCriCodecs import CPK,USM,ACB
def J(infile,outdir,key):USM(infile,key=key).extract(dirname=outdir)
def K(infile,outdir,key):A=outdir;CPK(infile).extract();USM(O,key=key).extract(dirname=A);ACB('music').extract(dirname=A,decode=True,key=key)
def P(asset_type,infile,outfile):
	A=outfile
	with M.stream(V,infile,timeout=None)as C:
		D=S.load(C.read())
		for B in D.objects:
			if B.type.name==W:B.read().image.save(A)
			if asset_type not in[G,H]:
				with F.open(A)as E:E.resize((900,1200),resample=F.LANCZOS).save(A)
def Q(asset_type,member_data,catalog,path_server,path_local,from_index=0,to_index=0):
	d='assetBundleName';c='fileSize';b='location';a='card';Y=path_local;P=catalog;J=to_index;I='data';H='/';B=from_index;F=asset_type;Z=path_server.split(H);Z[-2]=P.split('_')[2]
	def Q(filename):
		c='gen';b='content-length';G=filename
		with M.stream(V,H.join(Z)+H+G,timeout=None)as J:
			if J.status_code!=200:C('\x1b[38;5;1mWhoops, server error\x1b[0m');N(1)
			I=bytearray(J.read());L=I[7]
			for P in T(150):I[P]^=L
			Q=S.load(U(I))
			if Q.objects and a in F:
				for B in Q.objects:
					d='\\d{7}_'if F==X else'\\d{8}_\\d'
					if B.type.name==W and 100000<=E(J.headers[b])<=1000000 and re.match(d,B.read().name):
						for K in R.loads(member_data):
							if B.read().name[3:6]==K[c]+K[F.split('_')[0]]:
								A=f"{Y}/{K[c]}. {K['name']}"
								if not D.path.exists(A):D.makedirs(A)
								if D.path.exists(f"{A}/{B.read().name}.png"):C(f"[38;5;11m{B.read().name} already exist[0m")
								if not D.path.exists(f"{A}/{B.read().name}.png"):B.read().image.save(f"{A}/{B.read().name}.png");C(f"{B.read().name} saved!")
			elif not Q.objects and O in F:
				if E(J.headers[b])>=1000000:
					A=f"{Y}"
					if not D.path.exists(A):D.makedirs(A)
					if D.path.exists(f"{A}/{G.split(H)[1]}.mp4"):C(f"[38;5;11m{G} already exists![0m")
					if not D.path.exists(f"{A}/{G.split(H)[1]}.mp4"):
						L=I[15]
						for P in T(150):I[P]^=L
						with open(f"{A}/{G.split(H)[1]}.mp4",'wb')as e:e.write(U(I))
						C(f"{G}.mp4 Downloaded!")
		J.close()
	e=M.Client()
	with open(P,'rb')as f:G=R.load(f)
	if B>L(G[I])or J>L(G[I]):C('\x1b[38;5;1mWhoops, an error occured!\x1b[0m');N(1)
	C(f"Data length : {str(L(G[I]))}")
	if B==0 or J==0:K=G[I]
	if B!=0 and J!=0:K=G[I][B:J]
	if B!=0 and J==0:K=G[I][B:]
	C(f"Total requested range: {str(L(K))}")
	if a in F:
		for A in K:
			if A[b]==2 and 100000<=E(A[c])<=1000000:Q(A[d])
	elif O in F:
		for A in K:
			if A[b]==2 and E(A[c])>=1000000:Q(A[d])
	e.close()
B=I.ArgumentParser(description='Downloader Helper')
B.add_argument('--type')
B.add_argument('--infile')
B.add_argument('--outdir')
B.add_argument('--key')
B.add_argument('--outfile')
B.add_argument('--memberdata')
B.add_argument('--catalog')
B.add_argument('--pathserver')
B.add_argument('--pathlocal')
B.add_argument('--fromindex')
B.add_argument('--toindex')
A=B.parse_args()
if __name__=='__main__':
	if A.type in['nogifes_movie_card','nogifes_reward_movie']:J(A.infile,A.outdir,E(A.key))
	elif A.type in['nogifes_focus_data_lo','nogifes_focus_data_hi']:K(A.infile,A.outdir,E(A.key))
	elif A.type in[G,H,'itsunogi_card','itsunogi_photo']:P(A.type,A.infile,A.outfile)
	elif A.type in[X,'hinakoi_card','sakukoi_movie','hinakoi_movie']:
		try:Q(A.type,A.memberdata,A.catalog,A.pathserver,A.pathlocal,E(A.fromindex),E(A.toindex))
		except KeyboardInterrupt:C('Process Cancelled by User');N(1)