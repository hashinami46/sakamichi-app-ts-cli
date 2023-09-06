import { z } from "zod";

const zServerLocal = z.object({
  base_server : z.string().optional(),
  base_local : z.string().optional(),
  path_server : z.string().optional(),
  path_local : z.string().optional(),
  filepath_server : z.string().optional(),
  filepath_local : z.string().optional(),
  folder_server : z.string().optional(),
  folder_local : z.string().optional()
});
export const zType1 = z.enum([
  "nogikoi_card_b_png",
  "nogikoi_card_p_png",
  "nogikoi_card_g_png",
  "nogikoi_card_b_png_bg",
  "nogikoi_card_p_png_bg",
  "nogikoi_card_g_png_bg",
  "nogikoi_card_p_jpg",
  "nogikoi_card_b_jpg",
  "nogikoi_card_g_jpg",
  "nogikoi_sprites"
]);
export const zType2 = z.enum([
  "nogifes_photo_common",
  "nogifes_movie_card_th"
]);
export const zType3 = z.enum([
  "nogifes_movie_card",
  "nogifes_reward_movie"
]);
export const zType4 = z.enum([
  "nogifes_focus_data_lo",
  "nogifes_focus_data_hi"
]);
export const zType5 = z.enum([
  "nogifes_card",
  "itsunogi_sprites",
  "itsunogi_card",
  "itsunogi_photo"
]);
export const zType6 = z.enum([
  "sakukoi_card",
  "hinakoi_card"
]);
export const zType7 = z.enum([
  "sakukoi_movie",
  "hinakoi_movie"
]);

const zDateType = z.string().regex(new RegExp(/^\d{4}-\d{2}-\d{2}$/))
export const zRefreshToken = z.union([z.string().regex(new RegExp(/^1\/\/[\w-]+$/)), z.string().regex(new RegExp(/^\d{10}:[A-Za-z0-9_-]+$/)), z.string().uuid(), z.string().regex(new RegExp(/^2/))]);
const zBearerToken = z.object({
  refresh_token : zRefreshToken.optional(),
  access_token  : z.string().optional()
});

export const zAssetTypes = z.union([zType1, zType2, zType3, zType4, zType5, zType6, zType7])
export type ServerLocal = z.infer<typeof zServerLocal>;
export type AssetTypes = z.infer<typeof zAssetTypes>;
export type SakamichiMember = {
  name : string,
  gen? : string,
  itsunogi? : string,
  nogikoi? : string,
  nogifes? : string,
  sakukoi? : string,
  hinakoi? : string,
  nogimsg? : string,
  sakumsg? : string,
  hinamsg? : string,
  asukamsg? : string,
};
export type RefreshToken = z.infer<typeof zRefreshToken>;
export type BearerToken = z.infer<typeof zBearerToken>;
export type ReqHeaders = {
  "Host"?            : string,
  "X-Talk-App-ID"?   : string,
  "Authorization"?   : string,
  "User-Agent"?      : string,
  "Connection"?      : "Keep-Alive" | "close",
  "Content-Type"?    : "application/json",
  "Accept-Encoding"? : string,
  "Accept-Language"? : string,
  "TE"?              : string
};
export type MessageType = {                                                                                                 
  id: number,                                                                                      
  group_id: number,                                                                                   
  member_id: number,
  state? : string,                                                                             
  type: "text"|"voice"|"video"|"picture",                                                                                   
  text? : string,
  file? : string,
  thumbnail? : string,
  is_silent: boolean,                                                                               
  is_favorite: boolean,                                                                             
  published_at? : string,                                                           
  updated_at? : string                                                            
};
export type GroupsMembers = {
  id: number,
  state: "open"|"close",
  name? : string,
  thumbnail? : string,
  phone_image? : string,
  priority? : number,
  is_letter_destination? : boolean,
  options? : {
    is_letter_open_notified? : boolean,
    is_message_commentable? : boolean,
    share_url? : string,
    sp_message_permission? : string
  },
  birthday? : string,
  updated_at? : string,
  subscription? : {
    type? : "free"|"paid",
    state? : "active"|"cancelled"|"expired",
    auto_renewing? : boolean,
    start_at? : string,
    end_at? : string
  },
  tags? : string[],
  groups? : number[]
};
export type StatusData = {
  status: number,
  data: string | MessageType[] | GroupsMembers[] | undefined
};
export type DateType = z.infer<typeof zDateType>;
export type Args = {
  app? : string,
  server? : "1" | "2",
  type? : string,
  membername? : string[],
  groupname : "n46"|"s46"|"h46"|"asuka"
  date? : DateType[],
  from? : string,
  to? : string,
  star? : string,
  memberid? : string,
  seriesid? : string,
  text? : boolean,
  upload? : boolean,
  cheatsheet? : "n46"|"s46"|"h46"|"asuka",
  h? : boolean
};