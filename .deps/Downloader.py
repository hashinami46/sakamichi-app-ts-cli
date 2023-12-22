# -*- coding: utf-8 -*-
import os, re, json, httpx, UnityPy, argparse, shutil, subprocess
from PIL import Image
from PyCriCodecs import CPK, USM, ACB, AWB, HCA

s46_member_data = json.load(open("./.config/member.data.json", "r", encoding="utf-8"))["sakurazaka46"]
h46_member_data = json.load(open("./.config/member.data.json", "r", encoding="utf-8"))["hinatazaka46"]

def downloader_mode_2(
  infile: str,
  outdir: str,
  key: int
) -> None:
  USM(infile, key=key).extract(dirname=outdir)
  
def downloader_mode_3(
  infile: str,
  outdir: str,
  key: int
) -> None:
  CPK(infile).extract()
  USM("movie", key=key).extract(dirname=outdir)
  ACB("music").extract(dirname=outdir, decode=True, key=key)
  
def downloader_mode_4(
  asset_type: str,
  infile: str,
  outfile: str
) -> None:
  with httpx.stream("GET", infile, timeout=None) as res:
    assets = UnityPy.load(res.read())
    for asset in assets.objects:
      if asset.type.name == "Texture2D":
        asset.read().image.save(outfile)
      if asset_type not in ["nogifes_card", "itsunogi_sprites"]:
        with Image.open(outfile) as img:
          img.resize((900, 1200), resample=Image.LANCZOS).save(outfile)
          exit(0)

def downloader_mode_5(
  asset_type: str,
  catalog: str,
  path_server: str,
  path_local: str,
  from_index: int = 0,
  to_index: int = 0,
  mode: str = "catalog"
) -> None:
  urlserver     = None
  member_datas  = s46_member_data if "sakukoi" in asset_type else h46_member_data if "hinakoi" in asset_type else []
  data_table    = [{"assetBundleName": os.path.join(folderpath, filename), "fileSize": str(os.path.getsize(os.path.join(folderpath, filename)))} for folderpath, _, filepath in os.walk(os.path.join(".temp", asset_type.split("_")[0].title()), topdown=True) for filename in filepath] if mode == "local" else json.load(open(catalog, "r", encoding="utf-8"))["data"] if mode == "catalog" else []
  filtered_data = [data for data in data_table if (100000 <= int(data["fileSize"]) <= 1000000 and "card" in asset_type) or (int(data["fileSize"]) >= 1000000 and "movie" in asset_type)] or []
  datas = []
  if mode == "catalog":
    urlserver = path_server.split("/")
    urlserver[-2] = catalog.split("_")[2]
    if 0 <= from_index < len(filtered_data) and 0 < to_index <= len(filtered_data):
      datas = filtered_data[from_index:to_index]
    elif from_index >= 0 and to_index >= len(filtered_data):
      datas = filtered_data[from_index:]
    elif from_index == 0 and to_index == 0:
      datas = filtered_data
  elif mode == "local":
    datas = filtered_data
  print(f"Data length      : {str(len(data_table))}")
  print(f"Requested assets : {asset_type}")
  print(f"Length           : {str(len(filtered_data))}")
  print(f"Requested length : {str(len(datas))} ({str(from_index)} to {str(to_index)})")
  print(f"Mode             : {mode}")
  
  def executor(
    filename: str
  ) -> None:
    if "movie" in asset_type and os.path.exists(os.path.join(path_local, f"{filename.split('/')[-1]}.mp4")):
      print(f"\x1b[38;5;11m{filename.split('/')[1]}.mp4 already exists\x1b[0m")
    else:
      data = None
      if mode == "catalog":
        with httpx.stream("GET", "/".join(urlserver) + "/" + filename, timeout=None) as res:
          if res.status_code != 200:
            print("\x1b[38;5;1mWhoops, server error\x1b[0m")
            exit(1)
          data = bytearray(res.read())
      else:
        data = bytearray(open(filename, "rb").read())
      key  = data[7]
      for i in range(150):
        data[i] ^= key
      assets = UnityPy.load(bytes(data))
      if assets.objects and "card" in asset_type:
        for asset in assets.objects:
          matcher = r"(^\d{7}_|^\d{3}$|^\d{3}_)" if asset_type == "sakukoi_card" else r"(^\d{8}_\d|^\d{3}_\d$)"
          if asset.type.name == "Texture2D" and re.match(matcher, asset.read().name):
            member_data = [data for data in (s46_member_data if "sakukoi" in asset_type else h46_member_data) if not data[asset_type.split("_")[0]] == "" and re.search(f"{data['gen']+data[asset_type.split('_')[0]]}", asset.read().name[0:3] if len(asset.read().name) <= 5 else asset.read().name[3:6] if 6 <= len(asset.read().name) <= 10 else "000")]
            folder_path = os.path.join(path_local, f"{member_data[0]['gen']}. {member_data[0]['name']}") if member_data else os.path.join(path_local, "00. 不特定")
            if not os.path.exists(folder_path):
              os.makedirs(folder_path)
            if not os.path.exists(os.path.join(folder_path, f"{asset.read().name}.png")):
              asset.read().image.save(os.path.join(folder_path, f"{asset.read().name}.png"))
              print(f"{asset.read().name} saved!")
            else:
              print(f"\x1b[38;5;11m{asset.read().name} already exist\x1b[0m")
      elif not assets.objects and "movie" in asset_type:
        if not os.path.exists(path_local):
          os.makedirs(path_local)
        key = data[15]
        for i in range(150):
          data[i] ^= key
        open(os.path.join(path_local, f"{filename.split('/')[-1]}.mp4"), "wb").write(bytes(data))
        print(f"{filename.split('/')[1]}.mp4 saved!")
    if mode == "local":
      os.remove(filename)
  for assetBundle in datas:
    executor(assetBundle["assetBundleName"])

def downloader_mode_6(
  asset_type: str, 
  infile: str,
  outdir: str
) -> None:
  if asset_type == "nogifra_images":
    assets = UnityPy.load(infile)
    if len(assets.objects) == 2:
      for asset in assets.objects:
        if not os.path.exists(outdir):
          os.makedirs(outdir)
        if os.path.exists(os.path.join(outdir, f"{asset.read().name}.png")):
          os.remove(infile)
          print(f"\x1b[38;5;11m{asset.read().name} already exist\x1b[0m")
        if asset.type.name == "Texture2D" and not os.path.exists(os.path.join(outdir, f"{asset.read().name}.png")):
          asset.read().image.save(os.path.join(outdir, f"{asset.read().name}.png"))
          os.remove(infile)
          print(f"{asset.read().name} saved!")
  elif asset_type == "nogifra_movies":
    USM(infile).extract(dirname=outdir)
  elif asset_type == "nogifra_sounds":
    if infile.endswith(".awb", 0, len(infile)):
      for file in AWB(infile).getfiles():
        open("audio", "ab").write(file)
      with open(f"{outdir}.wav", "wb") as hcafile:
        hcafile.write(HCA("audio", key=0x0DAA20C336EEAE72).decode())

def downloader_mode_7(
  asset_type: str,
  catalog: str,
  path_server: str,
  path_local: str,
  from_index: int = 0,
  to_index: int = 0
) -> None:
  urlserver = path_server.split("/")
  urlserver[-2] = catalog.split("_")[2]
  
  def executor(
    filename: str,
    signature: str
  ) -> None:
    member_data = [data for data in s46_member_data + h46_member_data if re.search(r"_(\d{3})$" if re.search(r"(live_movie|voice)", filename) else r"_(\d{3})_", filename.replace(".cpk", "")) and data["unison"] == re.search(r"_(\d{3})$" if re.search(r"(live_movie|voice)", filename) else r"_(\d{3})_", filename.replace(".cpk", "")).group(1)]
    save_folder = os.path.join(path_local, "/".join(filename.split("/")[:-1]), f'{member_data[0]["unison"][0]}{int(member_data[0]["gen"]):02}. {member_data[0]["name"]}') if member_data else os.path.join(path_local, "/".join(filename.split("/")[:-1]), "000. 不特定") if not re.search(r"(appeal_movie)", asset_type) else os.path.join(path_local, "/".join(filename.split("/")[:-1]))
    if re.match(r"^sound.*\.cpk$", filename):
      if not os.path.exists(os.path.join(save_folder, filename.split("/")[-1].replace(".cpk", ".wav"))):
        with httpx.stream("GET", "/".join(urlserver) + f"/{filename}?{signature}", timeout=None) as res:
          if res.status_code != 200:
            print("\x1b[38;5;1mWhoops, server error\x1b[0m")
            exit(1)
          open(filename.split("/")[-1], "wb").write(bytearray(res.read()))
        res.close()
        CPK(filename.split("/")[-1]).extract()
        ACB(os.path.join(filename.split("/")[-1].replace(".cpk", ""), [acb for acb in os.listdir(filename.split("/")[-1].replace(".cpk", "")) if acb.endswith(".acb")][0])).extract(dirname=filename.split("/")[-1].replace(".cpk", ""), decode=True, key=0x0000047561F95FCF)
        if not os.path.exists(save_folder):
          os.makedirs(save_folder)
        os.rename(os.path.join(filename.split("/")[-1].replace(".cpk", ""), [wav for wav in os.listdir(filename.split("/")[-1].replace(".cpk", "")) if wav.endswith(".wav")][0]), os.path.join(save_folder, filename.split("/")[-1].replace(".cpk", ".wav")))
        shutil.rmtree(filename.split("/")[-1].replace(".cpk", ""))
        os.remove(filename.split("/")[-1])
        print(f'{filename.split("/")[-1].replace(".cpk", "")} saved!')
      else :
        print(f'\x1b[38;5;11m{filename.split("/")[-1].replace(".cpk", "")} already exist\x1b[0m')
    if re.match(r"^video.*\.cpk$", filename):
      if not os.path.exists(os.path.join(save_folder, filename.split("/")[-1].replace(".cpk", ".mp4"))):
        print(f'／ Downloading {filename.split("/")[-1].replace(".cpk", "")} ＼')
        with httpx.stream("GET", "/".join(urlserver) + f"/{filename}?{signature}", timeout=None) as res:
          if res.status_code != 200:
            print("\x1b[38;5;1mWhoops, server error\x1b[0m")
            exit(1)
          open(filename.split("/")[-1], "wb").write(bytearray(res.read()))
        res.close()
        CPK(filename.split("/")[-1]).extract()
        USM(os.path.join(filename.split("/")[-1].replace(".cpk", ""), [usme for usme in os.listdir(filename.split("/")[-1].replace(".cpk", "")) if usme.endswith(".usme")][0]), key=0x0000047561F95FCF).extract(dirname=filename.split("/")[-1].replace(".cpk", ""))
        print(f'{filename.split("/")[-1].replace(".cpk", "")} demuxed!')
        if asset_type == "live_movie":
          live_song = [song for song in json.load(open(catalog, "r", encoding="utf-8"))["assets_masters"] if re.sub(r"_\d{3}.cpk$", "", filename).replace("video/live_movie/live_movie_", "sound/song/live_music_") in song["code"]][0]
          with httpx.stream("GET", "/".join(urlserver) + f'/{live_song["code"]}?{live_song["signature"]}') as res:
            if res.status_code != 200:
              print("\x1b[38;5;1mWhoops, server error\x1b[0m")
              exit(1)
            open(live_song["code"].split("/")[-1], "wb").write(bytearray(res.read()))
          res.close()
          CPK(live_song["code"].split("/")[-1]).extract()
          ACB(os.path.join(live_song["code"].split("/")[-1].replace(".cpk", ""), [acb for acb in os.listdir(live_song["code"].split("/")[-1].replace(".cpk", "")) if acb.endswith(".acb")][0])).extract(dirname=filename.split("/")[-1].replace(".cpk", ""), decode=True, key=0x0000047561F95FCF)
          shutil.rmtree(live_song["code"].split("/")[-1].replace(".cpk", ""))
          os.remove(live_song["code"].split("/")[-1])
        if not os.path.exists(save_folder):
          os.makedirs(save_folder)
        if re.search(r"(appeal_movie|fav_rank|exf_member_movie|live_movie|gacha_effect|smart_movie|making_movie)", filename.split("/")[-1]):
          subprocess.run(["ffmpeg", "-i", os.path.join(filename.split("/")[-1].replace(".cpk", ""), [ivf for ivf in os.listdir(filename.split("/")[-1].replace(".cpk", "")) if ivf.endswith(".ivf")][0]), "-i", os.path.join(filename.split("/")[-1].replace(".cpk", ""), [audio for audio in os.listdir(filename.split("/")[-1].replace(".cpk", "")) if re.search("(.sfa|.wav)$", audio) ][0] ), "-c:v", "libx264", "-ab", "320k", "-c:a:0", "libmp3lame", os.path.join(save_folder, filename.split("/")[-1].replace(".cpk", ".mp4"))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
          print(f'{filename.split("/")[-1].replace(".cpk", "")} converted!')
        if re.search(r"(movie_photo|gacha_movie|profile|sign_movie)", filename.split("/")[-1]):
          subprocess.run(["ffmpeg", "-i", os.path.join(filename.split("/")[-1].replace(".cpk", ""), [ivf for ivf in os.listdir(filename.split("/")[-1].replace(".cpk", "")) if ivf.endswith(".ivf")][0]), "-c:v", "libx264", os.path.join(save_folder, filename.split("/")[-1].replace(".cpk", ".mp4"))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
          print(f'{filename.split("/")[-1].replace(".cpk", "")} converted!')
        shutil.rmtree(filename.split("/")[-1].replace(".cpk", ""))
        os.remove(filename.split("/")[-1])
        print(f'＼ {filename.split("/")[-1].replace(".cpk", "")} Downloaded! ／')
      else :
        print(f'\x1b[38;5;11m{filename.split("/")[-1].replace(".cpk", "")} already exist\x1b[0m')

    if re.search(r"^.*\.unity3d$", filename):
      with httpx.stream("GET", "/".join(urlserver) + f"/{filename}?{signature}", timeout=None) as res:
        if res.status_code != 200:
          print("\x1b[38;5;1mWhoops, server error\x1b[0m")
          exit(1)
        assets = UnityPy.load(bytes(res.read()))
        if assets.objects:
          if not os.path.exists(save_folder):
            os.makedirs(save_folder)
          for asset in assets.objects:
            if asset.type.name == "Texture2D" and not re.search(r"(_s|_m|_icon)" if asset_type == "scene_card" else r"(_m|_icon)", asset.read().name):
              if not os.path.exists(os.path.join(path_local, save_folder, f"{asset.read().name}.png")):
                asset.read().image.save(os.path.join(path_local, save_folder, f"{asset.read().name}.png"))
                print(f"{asset.read().name} saved!")
              else:
                print(f'\x1b[38;5;11m{asset.read().name} already exist\x1b[0m')
      res.close()
    if re.search(r"^.*\.mp4$", filename):
      if not os.path.exists(os.path.join(save_folder, filename.split("/")[-1])):
        with httpx.stream("GET", "/".join(urlserver) + f"/{filename}?{signature}", timeout=None) as res:
          if res.status_code != 200:
            print("\x1b[38;5;1mWhoops, server error\x1b[0m")
            exit(1)
          if not os.path.exists(save_folder):
            os.makedirs(save_folder)
          open(os.path.join(save_folder, filename.split("/")[-1]), "wb").write(bytearray(res.read()))
          print(f'{filename.split("/")[-1].replace(".mp4", "")} saved!')
        res.close()
      else :
        print(f'\x1b[38;5;11m{filename.split("/")[-1].replace(".mp4", "")} already exist\x1b[0m')
  if asset_type in [
    # unity
    "scene_card", 
    "stamp", 
    # cpk
    "appeal_movie", 
    "chara_profile",
    "exf_member_movie",
    "fav_rank_cheer", 
    "fav_rank_movie", 
    "gacha_effect_chara", 
    "gacha_effect_pickup", 
    "gacha_movie", 
    "live_movie", 
    "making_movie",
    "movie_photo", 
    "profile_movie", 
    "smart_movie", 
    # mp4
    "card_movie",
    "chara_movie", 
    "event_reward_movie",
    # wav
    "bgm", 
    "voice"
    ]:
    assets_masters = json.load(open(catalog, "r", encoding="utf-8"))["assets_masters"]
    filtered_data = []
    if asset_type in ["scene_card", "stamp"]:
      filtered_data = [item for item in assets_masters if asset_type in item["code"] and item["code"].endswith(".unity3d")]
    elif asset_type == "chara_profile":
      filtered_data = [item for item in assets_masters if "profile/chara_" in item["code"] and item["code"].endswith(".cpk")]
    elif asset_type == "live_movie":
      filtered_data = [item for item in assets_masters if asset_type in item["code"] and not re.search(r"(_low.cpk|.unity3d)$", item["code"]) ]
    elif asset_type in ["card_movie", "chara_movie", "event_reward_movie"]:
      filtered_data = [item for item in assets_masters if asset_type in item["code"] and item["code"].endswith(".mp4")]
    else:
      filtered_data = [item for item in assets_masters if asset_type in item["code"] and not item["code"].endswith(".unity3d")]
    datas = []
    if 0 <= from_index < len(filtered_data) and 0 < to_index <= len(filtered_data):
      datas = filtered_data[from_index:to_index]
    elif from_index >= 0 and to_index >= len(filtered_data):
      datas = filtered_data[from_index:]
    elif from_index == 0 and to_index == 0:
      datas = filtered_data
    print(f"Data length      : {str(len(assets_masters))}")
    print(f"Data length      : {str(len(assets_masters))}")
    print(f"Requested assets : {asset_type}")
    print(f"Length           : {str(len(filtered_data))}")
    print(f"Requested length : {str(len(datas))} ({str(from_index)} to {str(to_index)})")
    for url in datas:
      executor(url["code"], url["signature"])
  else:
    print("\x1b[38;5;1mWhoops, seems that you placed the wrong asset type\x1b[0m")
  
parser = argparse.ArgumentParser(description="Downloader Helper")
parser.add_argument("--type")
parser.add_argument("--infile")
parser.add_argument("--outdir")
parser.add_argument("--key")
parser.add_argument("--outfile")
parser.add_argument("--catalog")
parser.add_argument("--pathserver")
parser.add_argument("--pathlocal")
parser.add_argument("--fromindex")
parser.add_argument("--toindex")
parser.add_argument("--mode")
args = parser.parse_args()

if __name__ == "__main__":
  if args.type in ["nogifes_movie_card", "nogifes_reward_movie"]:
    downloader_mode_2(args.infile, args.outdir, int(args.key))
  elif args.type in ["nogifes_focus_data_lo", "nogifes_focus_data_hi"]:
    downloader_mode_3(args.infile, args.outdir, int(args.key))
  elif args.type in ["nogifes_card", "itsunogi_sprites", "itsunogi_card", "itsunogi_photo"]:
    downloader_mode_4(args.type, args.infile, args.outfile)
  elif args.type in ["sakukoi_card", "hinakoi_card", "sakukoi_movie", "hinakoi_movie"]:
    args_catalog = args.catalog if args.catalog else "none"
    args_fromindex = args.fromindex if args.fromindex else "0"
    args_toindex = args.toindex if args.toindex else "0"
    try:
      downloader_mode_5(args.type, args_catalog, args.pathserver, args.pathlocal, int(args_fromindex), int(args_toindex), args.mode)
    except KeyboardInterrupt:
      print("Process Cancelled by User")
      exit(0)
  elif args.type in ["nogifra_images", "nogifra_sounds", "nogifra_movies"]:
    try:
      downloader_mode_6(args.type, args.infile, args.outdir)
    except KeyboardInterrupt:
      print("Process Cancelled by User")
      exit(0)
  elif args.type.startswith("unison_"):
    try:
      args_fromindex = args.fromindex if args.fromindex else "0"
      args_toindex = args.toindex if args.toindex else "0"
      downloader_mode_7(args.type.replace("unison_", ""), args.catalog, args.pathserver, args.pathlocal, int(args_fromindex), int(args_toindex))
    except KeyboardInterrupt:
      print("Process Cancelled by User")
      exit(0)
  