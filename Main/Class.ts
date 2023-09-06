import fs from "fs";
import path from "path";
import { z } from "zod";
import axios from "axios";
import dotenv from "dotenv";
import dedent from "ts-dedent";
import fetch from "node-fetch";
import cliProgress from "cli-progress";
import { execSync } from "child_process";
import winston, { Logger } from "winston";
import DailyRotateFile from "winston-daily-rotate-file";

import {
  wrongAppname,
  wrongType,
  refreshTokenInvalid,
  refreshTokenUnavailable,
  accessTokenUpdated,
  reqHeadersUnnecessary,
  getGroupsMembersSuccess,
  methodError,
  messagesNotFound,
  fileNotFound,
  fileAlreadyExist,
  catalogNotFound,
  depsNotInstalled
} from "./Alert";
import {
  n46_member_data,
  s46_member_data,
  h46_member_data,
  asuka_member_data
} from "./Dictionary";
import {
  ServerLocal,
  AssetTypes,
  zType1, 
  zType2,
  zType3, 
  zType4,
  zType5, 
  zType6,
  zType7,
  zAssetTypes,
  zRefreshToken,
  RefreshToken,
  BearerToken,
  ReqHeaders,
  StatusData,
  DateType,
  MessageType,
  SakamichiMember,
  GroupsMembers
} from "./Types";

export const root_dir : string = __dirname; //.substring(0, __dirname.lastIndexOf("/"));                                   /* Define your root project */
export const temp_dir : string = path.join(root_dir, ".temp");                                                         /* Define your temp project */
export const ctlg_dir : string = path.join(root_dir, ".catalog");                                                      /* Don't Change This! Sakukoi and Hinakoi catalog dictionary folder */
export const deps_dir : string = path.join(root_dir, ".deps");                                                         /* Don't Change This! External dependency software such as quickbms */
export const logs_dir : string = path.join(root_dir, ".log");                                                          /* Project's logs dir */
export const wtmp_dir : string = path.join("Z:", root_dir, ".temp").replaceAll("/", "\\");                             /* Your temp project, but windows formatted */
export const wdep_dir : string = path.join("Z:", root_dir, ".deps").replaceAll("/", "\\");                             /* Your temp project, but windows formatted */
export const save_dir : string = path.join(root_dir, "Downloads");
export const cnfg_dir = path.join(root_dir, ".config");
dotenv.config({ path: `${root_dir}/.env` });
export const transport = new DailyRotateFile({filename: `${root_dir}/.log/logging-%DATE%.log`, datePattern: "YYYY-MM-DD", maxSize : "20m", maxFiles: "10d"}); 
export const logging = winston.createLogger({transports: [transport]});

export class Getter {
  constructor (private appname: string) { this.appname = appname };
  base_server_local = async ():Promise<
    ServerLocal
  > => {
    return this.appname === "nogifes_1"
    ? { base_server: "https://v1static.nogifes.jp", base_local: path.join(save_dir, "/Nogifes") }
    : this.appname === "nogifes_2"
    ? { base_server: "https://v2static.nogifes.jp", base_local: path.join(save_dir, "/Nogifes") }
    : this.appname === "nogikoi_1"
    ? { base_server: "https://prd-content.static.game.nogikoi.jp", base_local: path.join(save_dir, "/Nogikoi") }
    : this.appname === "nogikoi_2"
    ? { base_server: "https://prd-content-gree.static.game.nogikoi.jp", base_local: path.join(save_dir, "/Nogikoi") }
    : this.appname === "hinakoi"
    ? { base_server: "https://prd-content.static.game.hinakoi.jp", base_local: path.join(save_dir, "/Hinakoi") }
    : this.appname === "sakukoi"
    ? { base_server: "https://prod-content.static.game.sakukoi.jp", base_local: path.join(save_dir, "/Sakukoi") }
    : this.appname === "itsunogi"
    ? { base_server: "https://res.nogizaka46-always.emtg.jp", base_local: path.join(save_dir, "/Itsunogi") }
    : this.appname === "nogitalk"
    ? { base_server: "https://api.n46.glastonr.net/v2", base_local: path.join(save_dir, "/Mobame/nogizaka46") }
    : this.appname === "sakutalk"
    ? { base_server: "https://api.s46.glastonr.net/v2", base_local: path.join(save_dir, "/Mobame/sakurazaka46") }
    : this.appname === "hinatalk"
    ? { base_server: "https://api.kh.glastonr.net/v2", base_local: path.join(save_dir, "/Mobame/hinatazaka46") }
    : this.appname === "asukatalk"
    ? { base_server: "https://api.asukasaito.glastonr.net/v2", base_local: path.join(save_dir, "/Mobame/Saito Asuka") }
    : this.appname === "nogiblog"
    ? { base_server: "https://api.n46.glastonr.net/v2", base_local: path.join(save_dir, "/Blog/nogizaka46") }
    : this.appname === "sakublog"
    ? { base_server: "https://api.s46.glastonr.net/v2", base_local: path.join(save_dir, "/Blog/sakurazaka46") }
    : this.appname === "hinablog"
    ? { base_server: "https://api.kh.glastonr.net/v2", base_local: path.join(save_dir, "/Blog/hinatazaka46") }
    : { base_server: undefined, base_local: undefined };
  };
  path_server_local = async (
    type?: AssetTypes
  ):Promise<
    ServerLocal
  > => {
    const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
    if (!type || !zAssetTypes.safeParse(type).success) { logging.error(wrongType); console.log(wrongType); process.exit(1)};
    return type === "nogifes_photo_common"
    ? { path_server: "/resource/Background/Photo", path_local: `/photo_common` }
    : type === "nogifes_reward_movie" 
    ? { path_server: "/resource/Movie/Reward", path_local: `/reward_movie` }
    : type === "nogifes_focus_data_lo"
    ? { path_server: "/resource/Movie/Focus", path_local: `/focus_data` }
    : type === "nogifes_focus_data_hi"
    ? { path_server: "/resource/Movie/HighFocusMovie", path_local: `/focus_data_high` }
    : type === "nogifes_movie_card"   
    ? { path_server: "/resource/Movie/MovieCard", path_local: `/movie_card` }
    : type === "nogifes_movie_card_th"
    ? { path_server: "/resource/Movie/MovieCard/Thumbnail", path_local: `/movie_card_thumbnail` }
    : type === "nogifes_card"         
    ? { path_server: "/resource/Android_2017_4_1f1/card", path_local: `/card` }
    : type === "nogikoi_card_b_png"   
    ? { path_server: "/assets/img/card/mypage/1", path_local: `/card_b_png` }
    : type === "nogikoi_card_p_png"   
    ? { path_server: "/assets/img/card/mypage/2", path_local: `/card_p_png` }
    : type === "nogikoi_card_g_png"   
    ? { path_server: "/assets/img/card/mypage/3", path_local: `/card_g_png` }
    : type === "nogikoi_card_b_jpg"   
    ? { path_server: "/assets/img/card/l/1", path_local: `/card_b_jpg` }
    : type === "nogikoi_card_p_jpg"   
    ? { path_server: "/assets/img/card/l/2", path_local: `/card_p_jpg` }
    : type === "nogikoi_card_g_jpg"   
    ? { path_server: "/assets/img/card/l/3", path_local: `/card_g_jpg` }
    : type === "nogikoi_card_b_png_bg"
    ? { path_server: "/assets/img/card/bg/1", path_local: `/card_b_png_bg` }
    : type === "nogikoi_card_p_png_bg"
    ? { path_server: "/assets/img/card/bg/2", path_local: `/card_p_png_bg` }
    : type === "nogikoi_card_g_png_bg"
    ? { path_server: "/assets/img/card/bg/3", path_local: `/card_g_png_bg` }
    : type === "nogikoi_sprites"      
    ? { path_server: "/assets/img/member/story", path_local:`/member`}
    : type === "itsunogi_sprites"     
    ? { path_server: "/asset/1.1.453/Android/conciergeimage", path_local: `/conciergeimage` }
    : type === "itsunogi_card"        
    ? { path_server: "/asset/1.1.453/Android/card/card", path_local: `/card` }
    : type === "itsunogi_photo"       
    ? { path_server: "/asset/1.1.453/Android/card/photo", path_local: `/photo` }
    //: type === "itsunogi_sound"       
    //? { path_server: "/asset/1.1.453/Android/sound/alarm_voice", path_local: `/alarm_voice` }
    : zType6.safeParse(type).success
    ? { path_server : `${base_server}/assets/production/000000000/Android`, path_local : `${base_local}/card` }
    : zType7.safeParse(type).success
    ? { path_server : `${base_server}/assets/production/000000000/Android`, path_local : `${base_local}/movie` }
    : { path_server: undefined, path_local: undefined };
  };
  filepath_server_local = async (
    type: AssetTypes,
    index: number,
    star: number = 0,
    memberid: number = 0,
    seriesid: number = 0,
  ):Promise<
    ServerLocal|ServerLocal[]
  > => {
    const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
    const { path_server, path_local }: ServerLocal = await new Getter(this.appname).path_server_local(type);
    if (!base_server || !base_local) { logging.error(wrongAppname); console.log(wrongAppname); process.exit(1) }
    if (!path_server || !path_local) { logging.error(wrongType); console.log(wrongType); process.exit(1) }
    return type === "nogifes_photo_common"
    ? { filepath_server : `${base_server}${path_server}/photo_common_${String(index).padStart(5, "0")}.png`, filepath_local : `${base_local}${path_local}/photo_common_${String(index).padStart(5, "0")}.png`}
    : type === "nogifes_reward_movie" 
    ? { filepath_server : `${base_server}${path_server}/reward_movie_${String(index).padStart(5, "0")}.usme`, filepath_local : `${base_local}${path_local}/reward_movie_${String(index).padStart(5, "0")}.mp4`}
    : type === "nogifes_focus_data_lo"
    ? { filepath_server : `${base_server}${path_server}/focus_data_${String(index).padStart(5, "0")}.cpk`, filepath_local : `${base_local}${path_local}/focus_data_${String(index).padStart(5, "0")}.mp4`}
    : type === "nogifes_focus_data_hi"
    ? { filepath_server : `${base_server}${path_server}/focus_data_high_${String(index).padStart(5, "0")}.cpk`, filepath_local : `${path.join(base_local, path_local)}/focus_data_high_${String(index).padStart(5, "0")}.mp4`}
    : type === "nogifes_movie_card"   
    ? { filepath_server : `${base_server}${path_server}/movie_card_${String(index).padStart(5, "0")}.usme`, filepath_local : `${base_local}${path_local}/movie_card_${String(index).padStart(5, "0")}.mp4`}
    : type === "nogifes_movie_card_th"
    ? { filepath_server : `${base_server}${path_server}/movie_card_thumbnail_${String(index).padStart(5, "0")}.png`, filepath_local : `${base_local}${path_local}/movie_card_thumbnail_${String(index).padStart(5, "0")}.png`}
    : type === "nogifes_card"         
    ? { filepath_server : `${base_server}${path_server}/${String(index).padStart(6, "0")}0/card_l_${String(index).padStart(6, "0")}0`, filepath_local : `${base_local}${path_local}/card_l_${String(index).padStart(6, "0")}0.png`}
    : type === "nogikoi_sprites"      
    ? (() => { let url_local_server_list: ServerLocal[] = []; const seifuku: string[] = Array.from({ length: 11 }, (_, i) => String(i + 1).padStart(2, "0")); const pose: string[] = ["a", "b", "c", "d", "e", "f", "g"]; for (let a=0; a<seifuku.length; a++) { for (let b=0; b<pose.length; b++) { for (let c=0; c<n46_member_data.length; c++) { if (String(memberid) === n46_member_data[c].nogikoi) { url_local_server_list.push({ filepath_server : `${base_server}${path_server}/n${String(memberid).length <= 3 ? String(memberid) : String(memberid).slice(-3)}_${seifuku[a]}_v${String(index).length == 1 ? String(index) : String(index).slice(-1)}_${pose[b]}.png`, filepath_local : `${base_local}${path_local}/${n46_member_data[c].gen}. ${n46_member_data[c].name}/n${String(memberid).length <= 3 ? String(memberid) : String(memberid).slice(-3)}_${seifuku[a]}_v${String(index).length == 1 ? String(index) : String(index).slice(-1)}_${pose[b]}.png` })}}}}; return url_local_server_list;})()
    : zType1.safeParse(type).success
    ? { filepath_server : `${base_server}${path_server}${Number(String(star).charAt(0)) % 2 == 0 ? String(star).charAt(0).padEnd(2, "1") : String(star).charAt(0).padEnd(2, "0")}${index <= 10000 ? String(index).padStart(4, "0") : String(index).slice(0, 5)}.${type.includes("jpg") || type.includes("bg") ? "jpg" : "png"}`, filepath_local : `${base_local}${path_local}/${path_server.split("/").at(-1)}${Number(String(star).charAt(0)) % 2 == 0 ? String(star).charAt(0).padEnd(2, "1") : String(star).charAt(0).padEnd(2, "0")}${index <= 10000 ? String(index).padStart(4, "0") : String(index).slice(0, 5)}.${type.includes("jpg") || type.includes("bg") ? "jpg" : "png"}`}
    : type === "itsunogi_sprites"
    ? (() => { let url_local_server_list: ServerLocal[] = []; for (const a of n46_member_data) { if (String(memberid) === a["itsunogi"]) { url_local_server_list.push({ filepath_server : `${base_server}${path_server}/member_${memberid <= 100 ? String(memberid).padStart(3, "0") : "100"}_${seriesid <= 15 ? String(seriesid).padStart(3, "0") : "015"}/action_${memberid <= 100 ? String(memberid).padStart(3, "0") : "100"}_${seriesid <= 15 ? String(seriesid).padStart(3, "0") : "015"}_${index <= 17 ? String(index).padStart(3, "0") : "017"}.png`, filepath_local : `${base_local}${path_local}/${a.gen}. ${a.name}/action_${memberid <= 100 ? String(memberid).padStart(3, "0") : "100"}_${seriesid <= 15 ? String(seriesid).padStart(3, "0") : "015"}_${index <= 17 ? String(index).padStart(3, "0") : "017"}.png`})  }}; return url_local_server_list})()
    : type === "itsunogi_card"   
    ? (() => { let url_local_server_list: ServerLocal[] = []; const star_number: string[] = ["11", "21", "31", "41"]; const star_levels: string[] = ["001", "002"]; for (let a=0; a<star_number.length; a++) {for (let b=0; b<star_levels.length; b++) {for (let c=0; c<n46_member_data.length; c++) {if (String(memberid) == n46_member_data[c].itsunogi) {url_local_server_list.push({filepath_server: `${base_server}${path_server}/card_${star_number[a]}${String(index).length <= 3 ? String(index).padStart(3, "0") : String(index).slice(-3)}0${String(memberid).length <= 2 ? String(memberid).padEnd(2, "0") : String(memberid).slice(-2)}${star_levels[b]}.png`, filepath_local: `${base_local}${path_local}/${String(index).length <= 3 ? String(index).padStart(3, "0") : String(index).slice(-3)}0/${n46_member_data[c].gen}. ${n46_member_data[c].name}/card_${star_number[a]}${String(index).length <= 3 ? String(index).padStart(3, "0") : String(index).slice(-3)}0${String(memberid).length <= 2 ? String(memberid).padEnd(2, "0") : String(memberid).slice(-2)}${star_levels[b]}.png`})}}}}; return url_local_server_list;})()
    : type === "itsunogi_photo"  
    ? (() => { let url_local_server_list: ServerLocal[] = []; const star_number: string[] = ["11", "21", "31", "41"]; const star_levels: string[] = ["001", "002"]; for (let a=0; a<star_number.length; a++) {for (let b=0; b<star_levels.length; b++) {for (let c=0; c<n46_member_data.length; c++) {if (String(memberid) == n46_member_data[c].itsunogi) {url_local_server_list.push({filepath_server: `${base_server}${path_server}/photo_${star_number[a]}${String(index).length <= 3 ? String(index).padStart(3, "0") : String(index).slice(-3)}0${String(memberid).length <= 2 ? String(memberid).padEnd(2, "0") : String(memberid).slice(-2)}${star_levels[b]}.png`, filepath_local: `${base_local}${path_local}/${String(index).length <= 3 ? String(index).padStart(3, "0") : String(index).slice(-3)}0/${n46_member_data[c].gen}. ${n46_member_data[c].name}/photo_${star_number[a]}${String(index).length <= 3 ? String(index).padStart(3, "0") : String(index).slice(-3)}0${String(memberid).length <= 2 ? String(memberid).padEnd(2, "0") : String(memberid).slice(-2)}${star_levels[b]}.png`})}}}}; return url_local_server_list;})()
    //: z.union([zType6, zType7]).safeParse(type).success
    //? { filepath_server : `${base_server}${path_server}/000000000/Android`, filepath_local : `${base_local}${path_local}` }
    : { filepath_server : undefined, filepath_local : undefined };
  };
  auth_token = async (
    mode: "read"|"write"|"update",
    refresh_token?: RefreshToken, 
    access_token?: string
  ):Promise<
    BearerToken|void
  > => {
    const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
    if (mode === "read"  ) { const { refresh_token, access_token }: BearerToken = JSON.parse(fs.readFileSync(path.join(root_dir, process.env.CREDS_PATH!), "utf8"))[this.appname]; return { refresh_token, access_token };};
    if (mode === "write" ) { const config = JSON.parse(fs.readFileSync(path.join(root_dir, process.env.CREDS_PATH!), "utf8")); if (refresh_token) { if (!zRefreshToken.safeParse(refresh_token).success) { console.log(refreshTokenInvalid.replaceAll(":appname:", this.appname)); process.exit(1) }; config[this.appname].refresh_token = refresh_token}; if (access_token) { config[this.appname].access_token = access_token}; fs.writeFileSync(path.join(root_dir,  process.env.CREDS_PATH!), JSON.stringify(config, null, 2));};
    if (mode === "update") { const { refresh_token, access_token }: BearerToken = await new Getter(this.appname).auth_token("read") || { refresh_token: undefined, access_token: undefined }; try { const headers: ReqHeaders = await new Getter(this.appname).additional_headers(access_token!); const res = await axios.post(`${base_server}/update_token`, {"refresh_token": refresh_token}, { headers }); await new Getter(this.appname).auth_token("write", res.data.refresh_token, res.data.access_token); logging.info(accessTokenUpdated.replaceAll(":appname:", this.appname)); } catch (err: any) { if (!refresh_token) { console.log(refreshTokenUnavailable.replace(":appname:", this.appname)); logging.error(refreshTokenUnavailable.replace(":appname:", this.appname)); process.exit(1) }; if (!zRefreshToken.safeParse(refresh_token).success) { console.log(refreshTokenInvalid.replaceAll(":appname:", this.appname)); logging.error(refreshTokenInvalid.replaceAll(":appname:", this.appname)); process.exit(1) }; const errdata = { status: err.response.status, data: err.response.data }; logging.error(errdata); console.log(errdata) }}
  };
  additional_headers = async (
    access_token: string
  ):Promise<
    ReqHeaders
  > => {
    const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
    if (!base_server || !base_local) { logging.error(wrongAppname); console.log(wrongAppname); process.exit(1) }
    return /(blog|talk)/i.test(this.appname)
    ? {
        "Host"            : base_server!.replaceAll("https://", "").replaceAll("/v2", ""),
        "X-Talk-App-ID"   : `jp.co.sonymusic.communication.${this.appname.includes("nogi") ? "nogizaka" : this.appname.includes("saku") ? "sakurazaka" : this.appname.includes("hina") ? "keyakizaka" : "asukasaito" } 2.2`,
        "Authorization"   : `Bearer ${access_token}`,
        "User-Agent"      : `Dalvik/2.1.0 (Linux; U; Android 11; 2201117TY Build/RKQ1.211001.001)`,
        "Connection"      : `Keep-Alive`,
        "Content-Type"    : `application/json`,
        "Accept-Encoding" : `gzip, deflate`,
        "Accept-Language" : `ja-JP`,
        "TE"              : `gzip, deflate; q=0.5`
      }
    : (() => { console.log(reqHeadersUnnecessary.replace(":appname:", this.appname)); logging.error(reqHeadersUnnecessary.replace(":appname:", this.appname)); process.exit(1)})();
  };
  get_groups_members = async (
    mode: "groups"|"members"
  ):Promise<
    StatusData|void
  > => {
    return /(blog|talk)/i.test(this.appname)
    ? (async () => {
      try {
        const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
        const { refresh_token, access_token }: BearerToken = await new Getter(this.appname).auth_token("read") || { refresh_token: undefined, access_token: undefined };
        const headers: ReqHeaders = await new Getter(this.appname).additional_headers(access_token!); 
        const res = await axios.get(`${base_server}/${mode}`, { headers }); 
        logging.info({ status: res.status, data: getGroupsMembersSuccess.replaceAll(":appname:", this.appname).replaceAll(":mode:", mode) })
        return { status: res.status, data: res.data };
      } catch (err: any) {
        logging.error(err)
        if (err.response && err.response.status == 500) { const errdata = { status: err.response.status, data: err.response.data }; logging.error(errdata); return errdata }
        if (err.response && err.response.status == 401) { logging.error({ status: err.response.status, data: err.response.data }) ; await new Getter(this.appname).auth_token("update"); return await new Getter(this.appname).get_groups_members(mode)}
      }})()
    : (() => { console.log(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Getter().get_groups_members()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Getter().get_groups_members()")); process.exit(1)})();
  };
  get_message = async (
    mode: "timeline"|"past_messages",
    member: number,
    date?: DateType 
  ):Promise<
    StatusData|void
  > => {
    try {
      const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
      const { refresh_token, access_token }: BearerToken = await new Getter(this.appname).auth_token("read") || { refresh_token: undefined, access_token: undefined };
      const headers: ReqHeaders = await new Getter(this.appname).additional_headers(access_token!); 
      const res = await axios.get(`${base_server}/groups/${member}/${mode}${mode === "timeline" ? `?updated_from=${date}T00%3A00%3A00Z&sort=asc&count=100`: ""}`, { headers })
      return { status: res.status, data: res.data.messages }
    } catch (err: any) {
      logging.error(err)
      if (err.response && err.response.status == 500) { const errdata = { status: err.response.status, data: err.response.data }; logging.error(errdata); return errdata }
      if (err.response && err.response.status == 401) { logging.error({ status: err.response.status, data: err.response.data }) ; await new Getter(this.appname).auth_token("update"); return await new Getter(this.appname).get_message(mode, member, date)}
    };
  };
  get_messages = async (
    mode: "timeline"|"past_messages",
    members: Array<string|number>,
    dates: DateType[] = ["2022-03-22"]
  ):Promise<
    MessageType[]
  > => {
    const data: undefined|SakamichiMember[] = this.appname === "nogitalk" ? n46_member_data : this.appname === "sakutalk" ? s46_member_data : this.appname === "hinatalk" ? h46_member_data : this.appname === "asukatalk" ? asuka_member_data : undefined;
    if (!data) { console.log(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Getter().get_messages()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Getter().get_messages()")); process.exit(1) };
    let memberlist: number[] = []; for (let x=0; x < members.length; x++) { if (typeof members[x] === "number" && !memberlist.includes(Number(members[x]))) { memberlist.push(Number(members[x]))}; if (typeof members[x] === "string") { for (let y=0; y < data.length; y++) { const talkid = this.appname === "nogitalk" ? Number(data[y].nogimsg) : this.appname === "sakutalk" ? Number(data[y].sakumsg) : this.appname === "hinatalk" ? Number(data[y].hinamsg) : Number(data[y].asukamsg); if (members[x] == data[y].name.replace(" ", "") || Number(members[x]) == talkid && !memberlist.includes(talkid)) {memberlist.push(talkid)};}}}
    let datelist: DateType[] = []; const currentdate: Date = new Date(dates![0]); if (dates!.length == 1) { datelist.push(currentdate.toISOString().split("T")[0]) } else { while (currentdate <= new Date(dates![1])) { datelist.push(currentdate.toISOString().split("T")[0]); currentdate.setDate(currentdate.getDate() + 1)};};
    let messages: MessageType[] = [];
    for (let a=0; a<memberlist.length; a++) { for (let b=0; b<datelist.length; b++) { const res: any = await new Getter(this.appname).get_message(mode, memberlist[a], dates ? dates![b] : "") || { status: undefined, data: undefined }; if (res.data) { messages = messages.concat(res.data!.filter((message:any) => !messages.some((msg:any) => msg.id == message.id))) }}};
    if (!messages) { logging.error(messagesNotFound); console.log(messagesNotFound); process.exit(1)};
    return messages;
  };
};

export class Downloader {
  constructor(private appname: string) { this.appname = appname };
  downloaderMode1 = async (
    type: z.infer<typeof zType1 | typeof zType2>,
    fromindex: string,
    toindex: string,
    star?: string,
    memberid?: string
  ):Promise<
    void
  > => {
    if (!(this.appname.includes("nogifes") ? zType2 : this.appname.includes("nogikoi") ? zType1 : undefined)!.safeParse(type).success) { console.log(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode1()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode1()")); process.exit(1) };
    let urls: ServerLocal[] = [];
    for (let i: number = Number(fromindex); i <= Number(toindex); i++) { const url: ServerLocal|ServerLocal[] = await new Getter(this.appname).filepath_server_local(type, i, Number(star), Number(memberid)); if (Array.isArray(url)) { url.forEach(ur => { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === ur.filepath_server)) { urls.push(ur) };})} else { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === url.filepath_server)) {urls.push(url) };};}; 
    for (const link of urls) {
      const check = await fetch(link.filepath_server!);
      if (check.status != 200) { console.log(fileNotFound.replaceAll(":filename:", link.filepath_server!.split("/")!.at(-1)!.split(".")[0]!))};
      if (fs.existsSync(link.filepath_local!)) { console.log(fileAlreadyExist.replaceAll(":filename:", path.basename(link.filepath_local!).split(".")[0])) };
      if (check.status == 200 && !fs.existsSync(link.filepath_local!)) {
        if (!fs.existsSync(path.dirname(link.filepath_local!))) { fs.mkdirSync(path.dirname(link.filepath_local!), {recursive: true}) };
        try { execSync(`wget -N -q --show-progress ${link.filepath_server!} -P "${link.filepath_local!.split("/")!.slice(0, -1)!.join("/")}"`, {encoding: "utf8", stdio: "inherit"}); } catch (err) { console.log(depsNotInstalled); process.exit(1) };
      };
    };
  };
  downloaderMode2 = async (
    type: z.infer<typeof zType3>,
    fromindex: string,
    toindex: string
  ):Promise<
    void
  > => {
    if (!this.appname.includes("nogifes") || !zType3.safeParse(type).success) {console.log( methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode2()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode2()")); process.exit(1) };
    const key: number = this.appname.includes("nogifes") ? 0x0013F11BC5510101 : 0;
    let urls: ServerLocal[] = [];
    for (let i: number = Number(fromindex); i <= Number(toindex); i++) { const url: ServerLocal|ServerLocal[] = await new Getter(this.appname).filepath_server_local(type, i); if (Array.isArray(url)) { url.forEach(ur => { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === ur.filepath_server)) { urls.push(ur) };})} else { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === url.filepath_server)) {urls.push(url) };};}; 
    for (const link of urls) {
      const check = await fetch(link.filepath_server!);
      if (check.status != 200) { console.log(fileNotFound.replaceAll(":filename:", path.basename(link.filepath_server!).split(".")[0]!));}
      if (fs.existsSync(link.filepath_local!)) { console.log(fileAlreadyExist.replaceAll(":filename:", path.basename(link.filepath_local!).split(".")[0])) }
      if (check.status == 200 && !fs.existsSync(link.filepath_local!)) {
        if (!fs.existsSync(path.dirname(link.filepath_local!))) { fs.mkdirSync(path.dirname(link.filepath_local!), {recursive: true}) }
        console.log(`／ Downloading ${path.basename(link.filepath_local!).split(".")![0]} ＼`);
        try {
        execSync(`wget -N -q --show-progress -P ${temp_dir} ${link.filepath_server!}`, {encoding: "utf8", stdio: "inherit"});
        execSync(`${ process.platform === "win32" ? "python" : "python3" } ${deps_dir}/Downloader.py --type "${type}" --infile "${path.join(temp_dir, path.basename(link.filepath_server!))}" --outdir "${path.join(temp_dir, path.basename(link.filepath_server!).split(".")![0])}.demux" --key ${key}`, {encoding: "utf8", stdio: "ignore"}); console.log(`${path.basename(link.filepath_server!).split(".")![0]} demuxed!`);
          const tempvid: string|undefined = fs.readdirSync(path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`)).find(file => !file.endsWith("avi"));
          const tempaud: string|undefined = fs.readdirSync(path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`)).find(file => file.endsWith("avi"));
        execSync(`ffmpeg -n -i ${path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`, tempvid!)} ${type! === "nogifes_reward_movie" ? `-i ${path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`, tempaud!)}` : ``} -c:v copy ${type! === "nogifes_reward_movie" ? `-ab 320k -c:a:0 libmp3lame` : ``} "${link.filepath_local!}"`, {encoding: "utf8", stdio: "ignore"}); console.log(`${path.basename(link.filepath_server!).split(".")![0]} converted!`);
        fs.rmSync(temp_dir, {recursive: true, force: true})
        } catch (err) { console.log(depsNotInstalled); process.exit(1) }
        console.log(`＼ ${path.basename(link.filepath_local!).split(".")![0]} Downloaded! ／`);
      };
    };
  };
  downloaderMode3 = async (
    type: z.infer<typeof zType4>,
    fromindex: string,
    toindex: string
  ):Promise<
    void
  > => {
    if (!this.appname.includes("nogifes") || !zType4.safeParse(type).success) {console.log( methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode3()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode3()")); process.exit(1) };
    const key: number = this.appname.includes("nogifes") ? 0x0013F11BC5510101 : 0;
    let urls: ServerLocal[] = [];
    for (let i: number = Number(fromindex); i <= Number(toindex); i++) { const url: ServerLocal|ServerLocal[] = await new Getter(this.appname).filepath_server_local(type, i); if (Array.isArray(url)) { url.forEach(ur => { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === ur.filepath_server)) { urls.push(ur) };})} else { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === url.filepath_server)) {urls.push(url) };};}; 
    for (const link of urls) {
      const check = await fetch(link.filepath_server!);
      if (check.status != 200) { console.log(fileNotFound.replaceAll(":filename:", path.basename(link.filepath_server!).split(".")[0]!));}
      if (fs.existsSync(link.filepath_local!)) { console.log(fileAlreadyExist.replaceAll(":filename:", path.basename(link.filepath_local!).split(".")[0])) }
      if (check.status == 200 && !fs.existsSync(link.filepath_local!)) {
        if (!fs.existsSync(path.dirname(link.filepath_local!))) { fs.mkdirSync(path.dirname(link.filepath_local!), {recursive: true}) };
        console.log(`／ Downloading ${path.basename(link.filepath_local!).split(".")![0]} ＼`)
        try {
        execSync(`wget -N -q --show-progress -P ${temp_dir} ${link.filepath_server!}`, {encoding: "utf8", stdio: "inherit"})
        execSync(`${ process.platform === "win32" ? "python" : "python3" } ${deps_dir}/Downloader.py --type "${type}" --infile "${path.join(temp_dir, path.basename(link.filepath_server!))}" --outdir "${path.join(temp_dir, path.basename(link.filepath_server!).split(".")![0])}.demux" --key ${key}`, {encoding: "utf8", stdio: "ignore"}); console.log(`${path.basename(link.filepath_server!).split(".")![0]} demuxed!`);
        //execSync(`mv music ${path.join(temp_dir, path.basename(link.filepath_server!).split(".")![0])}.demux/music.acb && vgmstream-cli -o ${path.join(temp_dir, path.basename(link.filepath_server!).split(".")![0])}.demux/music.wav ${path.join(temp_dir, path.basename(link.filepath_server!).split(".")![0])}.demux/music.acb`, {encoding: "utf8", stdio: "ignore"}); console.log(`${path.basename(link.filepath_server!).split(".")![0]} demuxed!`);
          const tempvid: string|undefined = fs.readdirSync(path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`)).find(file => !file.endsWith("wav"));
          const tempaud: string|undefined = fs.readdirSync(path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`)).find(file => file.endsWith("wav"));
        execSync(`ffmpeg -n -i ${path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`, tempvid!)} -i ${path.join(temp_dir, `${path.basename(link.filepath_server!).split(".")![0]}.demux`, tempaud!)} -c:v copy -ab 320k -c:a:0 libmp3lame "${link.filepath_local!}"`, {encoding: "utf8", stdio: "ignore"}); console.log(`${path.basename(link.filepath_server!).split(".")![0]} converted!`);
        fs.rmSync(temp_dir, {recursive: true, force: true}); ["music", "movie"].forEach(file => fs.rmSync(path.join(process.cwd(), file), {force: true}));
        } catch (err) { console.log(depsNotInstalled); process.exit(1) }
        console.log(`＼ ${path.basename(link.filepath_local!).split(".")![0]} Downloaded! ／`)
      };
    };
  };
  downloaderMode4 = async (
    type: z.infer<typeof zType5>,
    fromindex: string,
    toindex: string,
    memberid: string = "0", 
    seriesid: string = "0"
  ):Promise<
    void
  > => {
    if (!/(nogifes|itsunogi)/i.test(this.appname) || !zType5.safeParse(type).success) { console.log( methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode4()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode4()")); process.exit(1) };
    let urls: ServerLocal[] = [];
    for (let i: number = Number(fromindex); i <= Number(toindex); i++) { const url: ServerLocal|ServerLocal[] = await new Getter(this.appname).filepath_server_local(type, i, 0, Number(memberid), Number(seriesid)); if (Array.isArray(url)) { url.forEach(ur => { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === ur.filepath_server)) { urls.push(ur) };})} else { if (!urls.some((urlx: ServerLocal) => urlx.filepath_server === url.filepath_server)) {urls.push(url) };};}; 
    for (const link of urls) {
      const check = await fetch(link.filepath_server!);
      if (check.status != 200) { console.log(fileNotFound.replaceAll(":filename:", path.basename(link.filepath_server!).split(".")[0]!));}
      if (fs.existsSync(link.filepath_local!)) { console.log(fileAlreadyExist.replaceAll(":filename:", path.basename(link.filepath_local!).split(".")[0])) }
      if (check.status == 200 && !fs.existsSync(link.filepath_local!)) {
        if (!fs.existsSync(path.dirname(link.filepath_local!))) { fs.mkdirSync(path.dirname(link.filepath_local!), {recursive: true}) }
        try { execSync(`${ process.platform === "win32" ? "python" : "python3" } ${deps_dir}/Downloader.py --type "${type}" --infile "${link.filepath_server!}" --outfile "${link.filepath_local!}"`, {encoding: "utf8", stdio: "inherit"}); } catch (err) { console.log(depsNotInstalled); process.exit(1) }
        console.log(`${path.basename(link.filepath_local!).split(".")![0]} Downloaded!`)
      };
    };
  };
  downloaderMode5 = async (
    type: z.infer<typeof zType6 | typeof zType7>, 
    fromindex: string = "0", 
    toindex: string = "0"
  ):Promise<
    void 
  > => {
    const memberdata: SakamichiMember[] = this.appname === "sakukoi" ? s46_member_data : this.appname === "hinakoi" ? h46_member_data : [];
    if (!z.union([zType6, zType7]).safeParse(type).success || !memberdata) {console.log( methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode5()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloaderMode5()")); process.exit(1) };
    const catalog = fs.readdirSync(ctlg_dir).filter(cata => cata.split("_")[0] === this.appname).pop(); if (!catalog) { console.log(catalogNotFound.replaceAll(":appname:", this.appname)); process.exit(1)};
    const { path_server, path_local }: ServerLocal = await new Getter(this.appname).path_server_local(type);
    try { execSync(`${ process.platform === "win32" ? "python" : "python3" } ${deps_dir}/Downloader.py --type "${type}" --memberdata '${JSON.stringify(memberdata)}' --catalog "${path.join(ctlg_dir, catalog!)}" --pathserver "${path_server}" --pathlocal "${path_local}" --fromindex ${fromindex} --toindex ${toindex}`, {encoding: "utf8", stdio: "inherit"}); } catch (err) { console.log(depsNotInstalled); process.exit(1) }
  };
  downloader_gm_tp = async (
    gm: "groups"|"members", 
    tp: "thumbnail"|"phone_image"
  ):Promise<
    void
  > => {
    if (!/(blog|talk)/i.test(this.appname)) { console.log( methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloader_gm_tp()")); logging.error(methodError.replace(":appname:", this.appname).replaceAll(":method:", "Downloader().downloader_gm_tp()")); process.exit(1) };
    const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
    const { status, data }: StatusData = await new Getter(this.appname).get_groups_members(gm) || { status: NaN, data: undefined };
    if (status == 200 && data) {
      if (!fs.existsSync(path.join(base_local!, gm, tp))) { fs.mkdirSync(path.join(base_local!, gm, tp), {recursive: true}) };
      for (let i=0; i < data!.length; i++) { if ((data[i] as GroupsMembers)[tp]) { execSync(`wget -N -q --show-progress -P "${path.join(base_local!, gm, tp)}" ${(data[i] as GroupsMembers)[tp]}`, {encoding: "utf8", stdio: "inherit"});}; };
    };
  };
  downloader_messages = async (
    mode: "timeline"|"past_messages",
    members: Array<number|string>, 
    dates: DateType[], 
    text: boolean = true
  ):Promise<
    void
  > => {
    const { base_server, base_local }: ServerLocal = await new Getter(this.appname).base_server_local();
    const data: SakamichiMember[] = this.appname === "nogitalk" ? n46_member_data : this.appname === "sakutalk" ? s46_member_data : this.appname === "hinatalk" ? h46_member_data : this.appname === "asukatalk" ? asuka_member_data : [];
    const messages: MessageType[] = await new Getter(this.appname).get_messages(mode, members, dates);
    for (const a of data) {
      for (const b of messages) {
        const talkid: number = this.appname === "nogitalk" ? Number(a.nogimsg) : this.appname === "sakutalk" ? Number(a.sakumsg) : this.appname === "hinatalk" ? Number(a.hinamsg) : this.appname === "asukatalk" ? Number(a.asukamsg) : NaN;
        if (b.group_id == talkid) {
          try {
          const folderpath: string = `${base_local}/${a.gen ? a.gen + ". " : ""}${a.name}/${b.published_at!.split("T")[0]!.replaceAll("-", ".")}`;
          if (!fs.existsSync(folderpath)) { fs.mkdirSync(folderpath, {recursive: true})}; 
          if (["picture", "video", "voice"].includes(b.type)) { const filename: string = b.file!.split("/").at(-1)!.split("?")[0]; if (!fs.existsSync(path.join(folderpath, filename))) { execSync(`wget -N -q --show-progress -O "${path.join(folderpath, filename)}" "${b.file}"`, {encoding: "utf8", stdio: "inherit"});}};
          if (b.text && text) { if (!fs.existsSync(folderpath)) { fs.mkdirSync(folderpath, {recursive: true})}; if (!fs.existsSync(`${folderpath}/${b.id!}-${b.published_at!.split("T")[0]!.replaceAll("-", "")}-${b.published_at!.split("T")[1]!.replaceAll(":", "").replace("Z", "")}.txt`)) { fs.writeFileSync(`${folderpath}/${b.id!}-${b.published_at!.split("T")[0]!.replaceAll("-", "")}-${b.published_at!.split("T")[1]!.replaceAll(":", "").replace("Z", "")}.txt`, b.text!, {flag: "a+"})} }
          } catch (err) { console.log(depsNotInstalled); process.exit(1) }
        };
      };
    }; 
  }; 
};
