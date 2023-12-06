u='Process Cancelled by User'
t='nogifra_sounds'
s='nogifra_movies'
r='nogifra_images'
q='sakukoi_card'
p='catalog'
o='itsunogi_sprites'
n='nogifes_card'
m='GET'
l=KeyboardInterrupt
k=bytearray
i='Texture2D'
h=bytes
g=range
d='movie'
c='3'
b='09'
a='08'
Z='07'
Y='06'
W='05'
V='02'
U='01'
T=open
S='04'
R='03'
Q=int
P=exit
O=len
N=''
L='4'
K='1'
J=print
I='sakumsg'
H='sakukoi'
G='2'
E='hinamsg'
C='hinakoi'
B='name'
A='gen'
import os as D,re,json,httpx as e,UnityPy as X,argparse as v,shutil
from PIL import Image as j
from PyCriCodecs import CPK,USM as f,ACB,AWB,HCA
w=[{B:'櫻坂46',A:N,H:N,I:'33'},{B:'新参者櫻坂46三期生',A:N,H:N,I:'73'},{B:'上村莉菜',A:K,H:U,I:L},{B:'小池美波',A:K,H:V,I:'7'},{B:'小林由依',A:K,H:R,I:'8'},{B:'齋藤冬優花',A:K,H:S,I:'9'},{B:'土生瑞穂',A:K,H:W,I:'15'},{B:'遠藤光',A:G,H:V,I:N},{B:'大園玲',A:G,H:R,I:'56'},{B:'大沼晶保',A:G,H:S,I:'57'},{B:'幸坂茉莉乃',A:G,H:W,I:'58'},{B:'武元唯衣',A:G,H:Y,I:'46'},{B:'田村保乃',A:G,H:Z,I:'47'},{B:'藤吉夏鈴',A:G,H:a,I:'48'},{B:'増本綺良',A:G,H:b,I:'59'},{B:'松田里奈',A:G,H:'10',I:'49'},{B:'森田ひかる',A:G,H:'11',I:'51'},{B:'守屋麗奈',A:G,H:'12',I:'60'},{B:'山﨑天',A:G,H:'13',I:'52'}]
x=[{B:'日向坂46',A:N,C:N,E:'43'},{B:'新参者日向坂46四期生',A:N,C:N,E:'78'},{B:'潮紗理菜',A:K,C:U,E:'22'},{B:'加藤史帆',A:K,C:R,E:'25'},{B:'齊藤京子',A:K,C:S,E:'26'},{B:'佐々木久美',A:K,C:W,E:'27'},{B:'佐々木美玲',A:K,C:Y,E:'28'},{B:'高瀬愛奈',A:K,C:Z,E:'29'},{B:'高本彩花',A:K,C:a,E:'30'},{B:'東村芽依',A:K,C:b,E:'32'},{B:'金村美玖',A:G,C:U,E:'34'},{B:'河田陽菜',A:G,C:V,E:'35'},{B:'小坂菜緒',A:G,C:R,E:'36'},{B:'富田鈴花',A:G,C:S,E:'37'},{B:'丹生明里',A:G,C:W,E:'38'},{B:'濱岸ひより',A:G,C:Y,E:'39'},{B:'松田好花',A:G,C:Z,E:'40'},{B:'宮田愛萌',A:G,C:a,E:N},{B:'渡邉美穂',A:G,C:b,E:N},{B:'上村ひなの',A:c,C:U,E:'53'},{B:'髙橋未来虹',A:c,C:V,E:'61'},{B:'森本茉莉',A:c,C:R,E:'62'},{B:'山口陽世',A:c,C:S,E:'63'},{B:'石塚瑶季',A:L,C:U,E:'66'},{B:'岸帆夏',A:L,C:V,E:'67'},{B:'小西夏菜実',A:L,C:R,E:'68'},{B:'清水理央',A:L,C:S,E:'69'},{B:'正源司陽子',A:L,C:W,E:'70'},{B:'竹内希来里',A:L,C:Y,E:'71'},{B:'平尾帆夏',A:L,C:Z,E:'72'},{B:'平岡海月',A:L,C:a,E:'73'},{B:'藤嶌果歩',A:L,C:b,E:'74'},{B:'宮地すみれ',A:L,C:'10',E:'75'},{B:'山下葉留花',A:L,C:'11',E:'76'},{B:'渡辺莉奈',A:L,C:'12',E:'77'}]
A6=[{B:'齋藤飛鳥',A:K,'asukamsg':K}]
def y(infile,outdir,key):f(infile,key=key).extract(dirname=outdir)
def z(infile,outdir,key):A=outdir;CPK(infile).extract();f(d,key=key).extract(dirname=A);ACB('music').extract(dirname=A,decode=True,key=key)
def A0(asset_type,infile,outfile):
	A=outfile
	with e.stream(m,infile,timeout=None)as C:
		D=X.load(C.read())
		for B in D.objects:
			if B.type.name==i:B.read().image.save(A)
			if asset_type not in[n,o]:
				with j.open(A)as E:E.resize((900,1200),resample=j.LANCZOS).save(A);P(0)
def A1(asset_type,catalog,path_server,path_local,from_index=0,to_index=0,mode=p):
	o='fileSize';n='location';a=catalog;Z='card';W=path_server;V='_';R='assetBundleName';N=to_index;M='data';K=from_index;I=path_local;G='/';F=asset_type
	if H in F:b=w
	elif C in F:b=x
	def c(assets,filename,filesize):
		M=filesize;L=filename;K=assets
		if K.objects and Z in F:
			for C in K.objects:
				N='(^\\d{7}_|^\\d{3}$|^\\d{3}_)'if F==q else'(^\\d{8}_\\d|^\\d{3}_\\d$)'
				if C.type.name==i and 100000<=M<=1000000 and re.match(N,C.read().name):
					for E in b:
						if O(C.read().name)>6 and C.read().name[3:6]==E[A]+E[F.split(V)[0]]or 3>O(C.read().name)<6 and C.read().name[0:3]==E[A]+E[F.split(V)[0]]or O(C.read().name)==3 and C.read().name==E[A]+E[F.split(V)[0]]:
							H=D.path.join(I,f"{E[A]}. {E[B]}")
							if not D.path.exists(H):D.makedirs(H)
							if D.path.exists(D.path.join(H,f"{C.read().name}.png")):J(f"[38;5;11m{C.read().name} already exist[0m")
							if not D.path.exists(D.path.join(H,f"{C.read().name}.png")):C.read().image.save(D.path.join(H,f"{C.read().name}.png"));J(f"{C.read().name} saved!")
		elif not K.objects and d in F:
			if M>=1000000:
				if not D.path.exists(I):D.makedirs(I)
				P=data[15]
				for Q in g(150):data[Q]^=P
				with T(D.path.join(I,f"{L.split(G)[1]}.mp4"),'wb')as R:R.write(h(data))
				J(f"{L.split(G)[1]}.mp4 Downloaded!")
	def f(filename):
		C=filename;D=W.split(G);D[-2]=a.split(V)[2]
		with e.stream(m,G.join(D)+G+C,timeout=None)as A:
			if A.status_code!=200:J('\x1b[38;5;1mWhoops, server error\x1b[0m');P(1)
			B=k(A.read());E=B[7]
			for F in g(150):B[F]^=E
			H=X.load(h(B));c(H,C,Q(A.headers['content-length']))
		A.close()
	def j(filename,filesize):
		A=filename;B=k(T(A,'rb').read());C=B[7]
		for E in g(150):B[E]^=C
		F=X.load(h(B));H=f"rand/{A.split(G)[-1]}";c(F,H,filesize);D.remove(A)
	if mode==p:
		r=e.Client()
		with T(a,'rb')as s:L=json.load(s)
		if K>O(L[M])or N>O(L[M]):J('\x1b[38;5;1mWhoops, an error occured!\x1b[0m');P(1)
		J(f"Data length : {str(O(L[M]))}")
		if K==0 or N==0:S=L[M]
		if K!=0 and N!=0:S=L[M][K:N]
		if K!=0 and N==0:S=L[M][K:]
		J(f"Total requested range: {str(O(S))}")
		for E in S:
			if Z in F:
				if E[n]==2 and 100000<=Q(E[o])<=1000000:f(E[R])
			elif d in F:
				if E[n]==2 and Q(E[o])>=1000000:
					if D.path.exists(D.path.join(I,f"{E[R].split(G)[1]}.mp4")):J(f"[38;5;11m{E[R].split(G)[1]} already exists![0m")
					if not D.path.exists(D.path.join(I,f"{E[R].split(G)[1]}.mp4")):f(E[R])
		r.close()
	elif mode=='local':
		if not D.path.exists(W):J(f"[38;5;1mWhoops, please provide {F} assets![0m");P(1)
		Y=[]
		def l(folderpath):
			A=folderpath
			for B in D.listdir(A):
				if D.path.isfile(D.path.join(A,B)):Y.append(D.path.join(A,B))
				else:l(D.path.join(A,B))
		l(W)
		if not Y:J(f"[38;5;1mWhoops, please provide {F} assets![0m");P(1)
		for E in Y:
			U=D.path.getsize(E)
			if Z in F and 100000<=U<=1000000:j(E,U)
			elif d in F and U>=1000000:
				if D.path.exists(D.path.join(I,f"{E.split(G)[-1]}.mp4")):J(f"[38;5;11m{E.split(G)[-1]} already exists![0m");D.remove(E)
				else:j(E,U)
def A2(asset_type,infile,outdir):
	G='audio';E=asset_type;B=outdir;A=infile
	if E==r:
		F=X.load(A)
		if O(F.objects)==2:
			for C in F.objects:
				if not D.path.exists(B):D.makedirs(B)
				if D.path.exists(D.path.join(B,f"{C.read().name}.png")):D.remove(A);J(f"[38;5;11m{C.read().name} already exist[0m")
				if C.type.name==i and not D.path.exists(D.path.join(B,f"{C.read().name}.png")):C.read().image.save(D.path.join(B,f"{C.read().name}.png"));D.remove(A);J(f"{C.read().name} saved!")
	elif E==s:f(A).extract(dirname=B)
	elif E==t:
		if A.endswith('.awb',0,O(A)):
			for H in AWB(A).getfiles():T(G,'ab').write(H)
			with T(f"{B}.wav",'wb')as I:I.write(HCA(G,key=0xdaa20c336eeae72).decode())
'\ndef downloader_mode_7(\n  asset_type: str,\n  catalog: str,\n  path_server: str,\n  path_local: str,\n  from_index: int = 0,\n  to_index: int = 0\n) -> None:\n  urlserver = path_server.split("/")\n  urlserver[-2] = catalog.split("_")[2]\n  def executor(\n    filename: str,\n    signature: str\n  ) -> None:\n    if re.match(r"^sound.*\\.cpk$", filename):\n      if not os.path.exists(os.path.join(path_local, filename.replace(".cpk", ".wav"))):\n        with httpx.stream("GET", "/".join(urlserver) + f"/{filename}?{signature}") as res:\n          if res.status_code != 200:\n            print("\x1b[38;5;1mWhoops, server error\x1b[0m")\n            exit(1)\n          open(filename.split("/")[-1], "wb").write(bytearray(res.read()))\n        res.close()\n        CPK(filename.split("/")[-1]).extract()\n        ACB(os.path.join(filename.split("/")[-1].replace(".cpk", ""), filename.split("/")[-1].replace(".cpk", ".acb"))).extract(dirname=filename.split("/")[-1].replace(".cpk", ""), decode=True, key=0x0000047561F95FCF)\n        if not os.path.exists(os.path.join(path_local, "/".join(filename.split("/")[:-1]))):\n          os.makedirs(os.path.join(path_local, "/".join(filename.split("/")[:-1])))\n        for x in os.listdir(filename.split("/")[-1].replace(".cpk", "")):\n          if x.endswith(".wav"):\n            os.rename(os.path.join(filename.split("/")[-1].replace(".cpk", ""), x), os.path.join(path_local, filename.replace(".cpk", ".wav")))\n            print(f\'{filename.split("/")[-1].replace(".cpk", "")} saved!\')\n        shutil.rmtree(filename.split("/")[-1].replace(".cpk", ""))\n        os.remove(filename.split("/")[-1])\n      else :\n        print(f\'\x1b[38;5;11m{filename.split("/")[-1].replace(".cpk", "")} already exist\x1b[0m\')\n    if re.match(r"^video.*\\.cpk$", filename):\n      #\n      with httpx.stream("GET", "/".join(urlserver) + f"/{filename}?{signature}") as res:\n        if res.status_code != 200:\n          print("\x1b[38;5;1mWhoops, server error\x1b[0m")\n          exit(1)\n        open(filename.split("/")[-1], "wb").write(bytearray(res.read()))\n      res.close()\n      CPK(filename.split("/")[-1]).extract()\n      #\n      USM(os.path.join(filename.split("/")[-1].replace(".cpk", ""), filename.split("/")[-1].replace(".cpk", ".usme")), key=0x0000047561F95FCF).extract(dirname=filename.split("/")[-1].replace(".cpk", ""))\n  executor("video/appeal_movies/appeal_movie_0001.cpk", "Expires=1708066625&Signature=flSpO0Tc44ZbaKw7f5aHFLnGNt3zyOe9bxKTp8JjyEE9kAmcXcPvRU1cFr87htd2ERv~uXArbZIIN05JZ78zCX66k1d9dk1fuR~JzK4LrXWEhirU0ymLr6b9JeCJterf6kkIHEwjuaQ-A1bGjZCAv4dT7GigGaXS50OE4K21g2zdnLpgm-NYDNwji-nUa0VW17jh9cJWWmqKSMkoRxnWkrc897OlUrV9qJsrASb9a9V~pj59V2JppVFKaSnHPhGc-HH4LZBB6wGH2FF5--LmfsLLavnO7-eH--B6RmvEBLuiSSm~gVYrsepZhJ7zrHqXW5-OvZPns-7SpxbQAaMJ5w__&Key-Pair-Id=APKAJ665I7LWWV7VQIFQ")\n  #executor("sound/drama_bgm/bgm_006.cpk", "Expires=1708066624&Signature=eiD3y-rM43yn6Dn3tMyzDr71GeXprDP4OnJpwFOsADMtB2-IX7bG4z2KRTG1d9JwjlwsmC-n5m8P9JHYRvyVZN5tMZGtVj--3KkXZPR7L8eKJhCOGUS~p5-m3HKgb~SpWy9f-6-LJUqJDziYABjYh5GyIQS3rLU0B4MmDr4OSbXLojmD9KdUj7Qzf8VjJvZcEOlHSCQVhn-ByPHbEOvf~4jHTXr~8YfryInwwuNI8dQhatxjwvIAGBL8wm2ZOAKiTGMYywbbo0ShqDW8LfX66yAHlMDrm~2Xc-i7JVP6wBvp4icdyiEyBWHvZ9aAfxG5DYiqLeQ9ym00z2oM~VZZyg__&Key-Pair-Id=APKAJ665I7LWWV7VQIFQ")\n'
M=v.ArgumentParser(description='Downloader Helper')
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
M.add_argument('--mode')
F=M.parse_args()
if __name__=='__main__':
	if F.type in['nogifes_movie_card','nogifes_reward_movie']:y(F.infile,F.outdir,Q(F.key))
	elif F.type in['nogifes_focus_data_lo','nogifes_focus_data_hi']:z(F.infile,F.outdir,Q(F.key))
	elif F.type in[n,o,'itsunogi_card','itsunogi_photo']:A0(F.type,F.infile,F.outfile)
	elif F.type in[q,'hinakoi_card','sakukoi_movie','hinakoi_movie']:
		A3=F.catalog if F.catalog else'none';A4=F.fromindex if F.fromindex else'0';A5=F.toindex if F.toindex else'0'
		try:A1(F.type,A3,F.pathserver,F.pathlocal,Q(A4),Q(A5),F.mode)
		except l:J(u);P(0)
	elif F.type in[r,t,s]:
		try:A2(F.type,F.infile,F.outdir)
		except l:J(u);P(0)
	'\n  elif args.type == "unison":\n    args_fromindex = args.fromindex if args.fromindex else "0"\n    args_toindex = args.toindex if args.toindex else "0"\n    downloader_mode_7(args.type, args.catalog, args.pathserver, args.pathlocal)\n  '