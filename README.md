# Sakamichi App TS

<div align="center">
  <img src="https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E" alt="JavaScript">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Shell Script">
</div>

## 🌸 Support Me
<div align="center">
  <a href="https://www.buymeacoffee.com/hashinami"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="BuyMeACoffe"></a>
</div>

## 🚀 Description
Typescript based cli tools to download Sakamichi Series App assets such as photo, video, audio, and text.
Each assets need different requirements. You will facing error if you haven't install or provide the requirements needed. 

## ⚠️ Warning!
Please read till the end for common usage and knowledge. \
~~This app is only supported linux for now! I don't have any idea why it won't work on windows.~~ \
I found the bug that caused errors on windows. So, I created a separated python script to extract the assets. \
If you encounter any errors, maybe you haven't installed the requirements. \
**But I warn you, if you use WSL (Windows Subsystem for Linux), you'll facing some errors that I still don't know how to fix that.** \
Please make sure that you already successfully installed the requirements before using this app! \
This is the app bundle version. I don't wanna put the source code here. It still lacks of bugs and if you wanna help me to fix the bugs, just contact me [here](hashinami46@gmail.com). 

## 📝 Requirements
### **Runtime**
- Nodejs >= 18 (Suggested: 20.5.1)
- Python3 >= 3.10 (Suggested: 3.10.12)
### **External Dependencies**
- wget
- ffmpeg
- git
### **Libs**
- All python3 libs in requirements.txt
- PyCriCodecs

## 🛠️ Installation and Setup
### 🐇 Quick Installation 
**For linux user**, you can easily run `bash install.sh` for quick setup. Try install the libs manually if you facing an error.\
For downloading mobame assets, you need to setup your credentials in `.config/secrets.credentials.json`. Just fill the `refresh_token` and this app will autogenerate the `access_token`.
### 🐢 Manual Installation
1. Install Node with npm, Python3 with pip, and external dependencies such as wget, ffmpeg, and git
- [git](https://git-scm.com/downloads)
- [wget](https://www.gnu.org/software/wget/)
- [ffmpeg](https://ffmpeg.org/download.html)
- [Nodejs](https://nodejs.org/en/download)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
2. Install Libs
- **Try excuting this command to check the runtime is already installed or not.**
```
node --version
npm --version
# python3 for linux, python for windows
python3 --version
pip --version
```
- **If you don't get any errors, continue to the next step. Download the PyCriCodecs.**
```
pip install -r requirements.txt
git clone https://github.com/Youjose/PyCriCodecs.git
```
- **For linux user, you should edit the setup.py in PyCriCodecs because linux doesn't support \\ to declare path. You can skip this if you using windows.**
```
# in the part
"CriCodecs\\CriCodecs.cpp"
# change to
"CriCodecs/CriCodecs.cpp"
```
- **The last step is go to PyCriCodecs dir and excute this command in the terminal.**
```
pip install . -v
```
- **Finally you can remove PyCriCodecs dir since it's already installed in your system.**
3. Setup Credentials
- **Fill the `refresh_token` for each group and the guide is finished.**
```
...
"nogitalk": {
    "name": "nogizaka46-talk",
    "email": "",
    "refresh_token": "",
    "access_token": "",
    "type": "mobame",
    "appname": "nogizaka46-mobame"
  },
...
```

## 🆕 Updating Guide
**Always use the latest package update because there might be some bugs fix.**
- **Using git clone** \
If you use git clone to download these assets just simply excute this command in the project root directory. It will automatically download the latest update.
Just copy the code "git config --global --add blablabla" to your terminal and retry the pull command if you get error message "dubious ownership in repository".
```
git pull origin main
```
- **Download from zip** \
If you already mastering git and download the app from zip, you should download the update and extract the contents inside the zip to your old project root dir. If you got replace confirmation message, just say yes. It won't delete your catalog or downloads dir.

## 🔫 Supported Apps and Usage
### 🎮 Nogifes
- **Photo Common & Movie Card Thumbnail**
```
Arguments
-A Appname
-S Server (1 or 2) try server 2 if server 1 maintenance
-T Asset Type
-f & -t 5 digit assets range index

node cli.js -A nogifes -S 1 -T photo_common -f 00001 -t 00002
node cli.js -A nogifes -S 1 -T movie_card_th -f 00001 -t 00002
```

- **Movie Card, Reward Movie, Focus Data High & Low**
```
Arguments
-A Appname
-S Server (1 or 2) try server 2 if server 1 maintenance
-T Asset Type
-f & -t 5 digit assets range index

node cli.js -A nogifes -S 1 -T movie_card -f 00001 -t 00002
node cli.js -A nogifes -S 1 -T reward_movie -f 00001 -t 00002
node cli.js -A nogifes -S 1 -T focus_data_hi -f 00001 -t 00002
node cli.js -A nogifes -S 1 -T focus_data_lo -f 00001 -t 00002
```

- **Card**
```
Arguments
-A Appname
-S Server (1 or 2) try server 2 if server 1 maintenance
-T Asset Type
-f & -t 6 digit assets range index ( latest event asset index is 008000 )

node cli.js -A nogifes -S 1 -T card -f 008000 -t 008001
```

### 🎮 Itsunogi
- **Sprites**
```
Arguments
-A Appname
-T Asset Type
-mid Member id. Check this using command node cli.js --cheatsheet n46
-sid Series id. I use this argument to define the event id
-f & -t 3 digit assets range index 

node cli.js -A itsunogi -T sprites -mid 37 -sid 10 -f 001 -t 017
```

- **Photo & Card**
```
Arguments
-A Appname
-T Asset Type
-mid Member id. Check this using command node cli.js --cheatsheet n46
-f & -t 3 digit assets range index 

node cli.js -A itsunogi -T photo -mid 56 -f 001 -t 002
node cli.js -A itsunogi -T card -mid 56 -f 001 -t 002
```

### 🎮 Nogikoi
- **Sprites**
```
Arguments
-A appname
-S Server (1 or 2) 1 is nogikoi mobile server and 2 is nogikoi gree server
-T Asset Type
-mid Member id. Check this using command node cli.js --cheatsheet n46
-f & -t 2 digit assets range index 

node cli.js -A nogikoi -S 1 -T sprites -mid 46 -f 07 -t 08
```

- **Card PNG, Card JPG (with frames) & Card Background**
```
Arguments
-A appname
-S Server (1 or 2) 1 is nogikoi mobile server and 2 is nogikoi gree server
-T Asset Type. P for pink, B for blue, G for green.
-s Card Star. Should between 1-8
-f & -t 4-5 digit assets range index 

node cli.js -A nogikoi -S 1 -T card_p_png -s 7 -f 9999 -t 10000
node cli.js -A nogikoi -S 1 -T card_p_png_bg -s 7 -f 9999 -t 10000
node cli.js -A nogikoi -S 1 -T card_p_jpg -s 8 -f 9999 -t 10000
```

### 🎮 Sakukoi & Hinakoi
- **Card & Movie**
```
Arguments
-A Appname
-T Asset Type
-f & -t I'm not sure how many digits since it depends on the catalog you provided. 

node cli.js -A sakukoi -T card -f 03000 -t 04000
node cli.js -A sakukoi -T movie -f 09470 -t 10000
```

### 💌 Sakamichi Mobile Messages
- **All Daily Text, Images, Videos, and Call**
```
Arguments
-A Appname (nogitalk or sakutalk or hinatalk)
-T Asset Type. Should be timeline or past_messages
-M Membername. You can provide single membername or more 
-D yyyy-mm-dd formatted date. You can provide single date or two (from date and to date)
--text Include text assets downloading. If you just want to extract photo, audio, and video, ignore this arguments

node cli.js -A nogitalk -T timeline -M 柴田柚菜 -D 2022-06-28 
node cli.js -A nogitalk -T timeline -M 柴田柚菜 -D 2022-06-28 2022-06-30
node cli.js -A sakutalk -T timeline -M 大園玲 -D 2022-06-28 2022-06-30 --text
node cli.js -A hinatalk -T timeline -M 加藤史帆 潮紗理菜 -D 2022-06-28 2022-06-30 --text
```

### 💌 Saito Asuka Mobile Messages
- **All Daily Text, Images, Videos, and Call**
```
Arguments
-A Appname. Should be asukatalk
-T Asset Type. Should be timeline or past_messages
-M Membername. Should be 齋藤飛鳥
-D yyyy-mm-dd formatted date. You can provide single date or two (from date and to date)
--text Include text assets downloading. If you just want to extract photo, audio, and video, ignore this arguments

node cli.js -A asukatalk -T timeline -M 齋藤飛鳥 -D 2022-06-28 
node cli.js -A asukatalk -T timeline -M 齋藤飛鳥 -D 2022-06-28 2022-06-30 --text
```

### ⚙️ Other Arguments
```
Arguments 
--cheatsheet Display member id table. Should be n46, s46, h46, or asuka
-v, --version Show app build version

node cli.js --cheatsheet n46
node cli.js -v
```

## 🌲 Directory Structure
```
.
├── .catalog
│   ├── hinakoi_catalog_223072101
│   └── sakukoi_catalog_223090101
├── .config
│   └── .secrets.credentials.json
├── .deps
│   └── Downloader.py
├── .env
└── cli.js
```

## 📋 To do List
- [ ] Create blogs downloader.
- [ ] Create audio types assets downloader.
- [ ] Create Nogifra assets decrypter.

## 🪵 Changelog
- 2023-09-10_1.0.2
```
• Fix Sakukoi and Hinakoi movie download logic.
  The app will skip already downloaded movies and make it faster.
• You can set custom download dir.
  Declare SAKAMICHI_SAVE_DIR="" in .env and fill with the custom path you want.
```
- 2023-09-07_1.0.1
```
• Minor bug fix
```
- 2023-09-06_1.0.0
```
• Now working on Windows
• Separate python extraction script
• Remove ffpb
• Generate new requirements.txt
```

## 🐞 Known Bugs
- Failed install Pillow
> Unfortunately Pillow 9.0.1 doesn't supported in python 3.11 for now. You should downgrade your python to 3.10.
- Node syntax missmatch
> Make sure that you already installed Node v18 or above.
- Python syntax missmatch
> It's weird. If you already updated this app, you won't facing this errors.
- Suddenly error when downloading nogifes card
> It's normal. Try to rerun the command again. This error usually occurs because of your network.
- Error occurred when extracting Hinakoi and Sakukoi assets.
> 2 reason. You placed the wrong catalog or you have the newest catalog and you give the catalog name with the old one. For example, latest sakukoi catalog is sakukoi_catalog_223090101, but you naming it like this sakukoi_catalog_223080201 this will make you get an error because latest assets doesn't found in the old server path.

## 📑 Note
* How to get `refresh_token`? 
> Nah. I won't tell you. Please search by yourself 🙏
* How to get hinakoi and sakukoi catalog? 
> Go to `android/data/<sakukoi or hinakoi game folder>/` and search here.
* I already add `refresh_token` in the secrets.credentials.json file, but I still can't download the mobame assets.
> Well, just create `.env` file and put this variable on it 
```
CREDS_PATH=".config/.secrets.credentials.json"
```
* How to download movie in nogikoi?
> Nah. Idk since the movies is securely encrypted.
* Can't downloads hinakoi and sakukoi assets even if catalog already provided.
> It's a bit tricky. Try to extract the catalog using zip extractor like winrar or ZArchiver, then rename the extracted catalog to something like the directory tree above. If you lucky, you won't get any errors.

## ⭐ Credits
- [Colmsg](https://github.com/proshunsuke/colmsg)
- [UnityPy](https://pypi.org/project/UnityPy/)
- [PyCriCodecs](https://github.com/Youjose/PyCriCodecs) 
- And all my friends that helps me to maintain and find the issues.

## ©️ License
This application is provided as open source and is offered as-is. The author is not responsible for any damages caused by this application. By using this application, users agree to assume any risks associated with its use.\
This application is provided under the MIT License.

Please be aware of the following items in Article 8 (Prohibited Activities) of the App's Terms of Use:
- (16) Acts of accessing or attempting to access this service by means other than those specified by the company
- (17) Acts of accessing or attempting to access this service using automated methods (including crawlers and similar technologies)