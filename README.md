# Sakamichi App TS

## 🚀 Description
Typescript based cli tools to download Sakamichi Series App assets such as audio, video, and text.
Each assets need different requirements. You will facing error if you haven't install or provide the requirements. 

## 📝 Requirements
### **Runtime**
- Nodejs >= 18 
- Python3 >= 3.9
### **External Dependencies**
- wget
- ffmpeg
### **Libs**
- All python3 libs in requirements.txt
- PyCriCodecs

## ⚠️ Warning!
This app is only supported linux for now! I don't have any idea why it won't work on windows. 
If you encounter any errors, maybe you haven't installed the requirements. 

## 🛠️ Installation and Setup
You can easily run `bash install.sh` for quick setup. Try install the libs manually if you facing an error.\
For downloading mobame assets, you need to setup your credentials in `.config/secrets.credentials.json`. Just fill the `refresh_token` and this app will autogenerate the `access_token.\
Please read till the end for common usage and knowledge.

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
-S Server ( 1 or 2 ) try server 2 if server 1 maintenance
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
-f & -t I'm not sure how many digits since. It depends on the catalogue you provide. 

node cli.js -A sakukoi -T card -f 03000 -t 03500
node cli.js -A  hinakoi -T card -f 03000 -t 03500
```

### 💌 Sakamichi Mobile Messages
- **All Daily Text, Images, Videos, and Call**
```
Arguments
-A Appname (nogitalk or sakutalk or hinatalk)
-T Asset Type. Should be timeline or past_messages
-M Membername. You can provide single membername or more 
-D yyyy-mm-dd formatted date. You can provide single date or two (from date and to date)

node cli.js -A nogitalk -T timeline -M 柴田柚菜 -D 2022-06-28 
node cli.js -A nogitalk -T timeline -M 柴田柚菜 -D 2022-06-28 2022-06-30
node cli.js -A sakutalk -T timeline -M 大園玲 -D 2022-06-28 2022-06-30 --text
node cli.js -A hinatalk -T timeline -M 加藤史帆 潮紗理菜 -D 2022-06-28 2022-06-30 --text
```

### 💌 Saito Asuka Mobile Messages

```
Arguments
-A Appname. Should be asukatalk
-T Asset Type. Should be timeline or past_messages
-M Membername. Should be 齋藤飛鳥
-D yyyy-mm-dd formatted date. You can provide single date or two (from date and to date)

node cli.js -A asukatalk -T timeline -M 齋藤飛鳥 -D 2022-06-28 
node cli.js -A asukatalk -T timeline -M 齋藤飛鳥 -D 2022-06-28 2022-06-30
```

## 🌲 Directory Structure
```
.
├── .catalog
├── .config/
│   └── .secrets.credentials.json
├── .env
└── cli.js
```

## 📑 Note
* How to get `refresh_token`? 
> Nah. I won't tell you. Please search by yourself 🙏
* How to get hinakoi and sakukoi catalog? 
> Go to `android/data/<sakukoi or hinakoi game folder>/` and search here.

## ⭐ Credits
- [UnityPy](https://pypi.org/project/UnityPy/)
- [PyCriCodecs](https://github.com/Youjose/PyCriCodecs)

## ©️ License
This application is provided as open source and is offered as-is. The author is not responsible for any damages caused by this application. By using this application, users agree to assume any risks associated with its use.\
This application is provided under the MIT License.

Please be aware of the following items in Article 8 (Prohibited Activities) of the App's Terms of Use:
- (16) Acts of accessing or attempting to access this service by means other than those specified by the company
- (17) Acts of accessing or attempting to access this service using automated methods (including crawlers and similar technologies)