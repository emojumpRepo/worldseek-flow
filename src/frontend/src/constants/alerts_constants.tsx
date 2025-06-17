// ERROR
export const MISSED_ERROR_ALERT = "哎呀！看来你漏掉了一些内容哦～";
export const INCOMPLETE_LOOP_ERROR_ALERT =
  "工作流有一个不完整的循环。检查您的连接并重试。";
export const INVALID_FILE_ALERT =
  "请选择一个有效的文件。只允许这些文件类型：";
export const CONSOLE_ERROR_MSG = "上传文件时发生错误";
export const CONSOLE_SUCCESS_MSG = "文件上传成功";
export const INFO_MISSING_ALERT =
  "哎呀！看来你漏掉了一些必填信息哦～";
export const FUNC_ERROR_ALERT = "您的函数中存在错误";
export const IMPORT_ERROR_ALERT = "您的导入中存在错误";
export const BUG_ALERT = "出错了，请重试";
export const CODE_ERROR_ALERT =
  "代码中存在一些问题，请检查一下";
export const CHAT_ERROR_ALERT = "请先构建工作流，再使用聊天功能。";
export const MSG_ERROR_ALERT = "发送消息时发生错误";
export const PROMPT_ERROR_ALERT =
  "提示词中存在一些问题，请检查一下";
export const API_ERROR_ALERT =
  "保存API密钥时发生错误，请重试。";
export const USER_DEL_ERROR_ALERT = "删除用户时发生错误";
export const USER_EDIT_ERROR_ALERT = "编辑用户时发生错误";
export const USER_ADD_ERROR_ALERT = "添加新用户时发生错误";
export const SIGNIN_ERROR_ALERT = "登录时发生错误";
export const DEL_KEY_ERROR_ALERT = "删除密钥时发生错误";
export const DEL_KEY_ERROR_ALERT_PLURAL = "删除密钥时发生错误";
export const UPLOAD_ERROR_ALERT = "上传文件时发生错误";
export const WRONG_FILE_ERROR_ALERT = "无效的文件类型";
export const UPLOAD_ALERT_LIST = "请上传一个JSON文件";
export const INVALID_SELECTION_ERROR_ALERT = "无效的选择";
export const EDIT_PASSWORD_ERROR_ALERT = "更改密码时发生错误";
export const EDIT_PASSWORD_ALERT_LIST = "密码不匹配";
export const SAVE_ERROR_ALERT = "保存更改时发生错误";
export const PROFILE_PICTURES_GET_ERROR_ALERT =
  "获取个人资料图片时发生错误";
export const SIGNUP_ERROR_ALERT = "注册时发生错误";
export const APIKEY_ERROR_ALERT = "API密钥错误";
export const NOAPI_ERROR_ALERT =
  "您没有API密钥。请添加一个以使用WorldSeek Agent商店。";
export const INVALID_API_ERROR_ALERT =
  "您的API密钥无效。请添加一个有效的API密钥以使用WorldSeek Agent商店。";
export const COMPONENTS_ERROR_ALERT = "获取组件时发生错误。";

// NOTICE
export const NOCHATOUTPUT_NOTICE_ALERT =
  "工作流中没有ChatOutput组件。";
export const API_WARNING_NOTICE_ALERT =
  "警告：关键数据，JSON文件可能包含API密钥。";
export const COPIED_NOTICE_ALERT = "API密钥已复制！";
export const TEMP_NOTICE_ALERT = "您的模板没有变量。";

// SUCCESS
export const CODE_SUCCESS_ALERT = "代码已准备好运行";
export const PROMPT_SUCCESS_ALERT = "提示词已准备好";
export const API_SUCCESS_ALERT = "成功！您的API密钥已保存。";
export const USER_DEL_SUCCESS_ALERT = "成功！用户已删除！";
export const USER_EDIT_SUCCESS_ALERT = "成功！用户已编辑！";
export const USER_ADD_SUCCESS_ALERT = "成功！新用户已添加！";
export const DEL_KEY_SUCCESS_ALERT = "成功！密钥已删除！";
export const DEL_KEY_SUCCESS_ALERT_PLURAL = "成功！密钥已删除！";
export const FLOW_BUILD_SUCCESS_ALERT = `工作流构建成功`;
export const SAVE_SUCCESS_ALERT = "更改已保存！";
export const INVALID_FILE_SIZE_ALERT = (maxSizeMB) => {
  return `文件太大。请选择小于${maxSizeMB}的文件。`;
};
