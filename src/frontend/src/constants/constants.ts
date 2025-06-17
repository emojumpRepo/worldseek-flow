// src/constants/constants.ts

import custom from "../customization/config-constants";
import { languageMap } from "../types/components";

/**
 * invalid characters for flow name
 * @constant
 */
export const INVALID_CHARACTERS = [
  " ",
  ",",
  ".",
  ":",
  ";",
  "!",
  "?",
  "/",
  "\\",
  "(",
  ")",
  "[",
  "]",
  "\n",
];

/**
 * regex to highlight the variables in the text
 * @constant regexHighlight
 * @type {RegExp}
 * @default
 * @example
 * {{variable}} or {variable}
 * @returns {RegExp}
 * @description
 * This regex is used to highlight the variables in the text.
 * It matches the variables in the text that are between {{}} or {}.
 */

export const regexHighlight = /\{\{(.*?)\}\}|\{([^{}]+)\}/g;
export const specialCharsRegex = /[!@#$%^&*()\-_=+[\]{}|;:'",.<>/?\\`´]/;

export const programmingLanguages: languageMap = {
  javascript: ".js",
  python: ".py",
  java: ".java",
  c: ".c",
  cpp: ".cpp",
  "c++": ".cpp",
  "c#": ".cs",
  ruby: ".rb",
  php: ".php",
  swift: ".swift",
  "objective-c": ".m",
  kotlin: ".kt",
  typescript: ".ts",
  go: ".go",
  perl: ".pl",
  rust: ".rs",
  scala: ".scala",
  haskell: ".hs",
  lua: ".lua",
  shell: ".sh",
  sql: ".sql",
  html: ".html",
  css: ".css",
  // add more file extensions here, make sure the key is same as language prop in CodeBlock.tsx component
};
/**
 * Number maximum of components to scroll on tooltips
 * @constant
 */
export const MAX_LENGTH_TO_SCROLL_TOOLTIP = 200;

export const MESSAGES_TABLE_ORDER = [
  "timestamp",
  "message",
  "text",
  "sender",
  "sender_name",
  "session_id",
  "files",
];

/**
 * Number maximum of components to scroll on tooltips
 * @constant
 */
export const MAX_WORDS_HIGHLIGHT = 79;

/**
 * Limit of items before show scroll on fields modal
 * @constant
 */
export const limitScrollFieldsModal = 10;

/**
 * The base text for subtitle of Export Dialog (Toolbar)
 * @constant
 */
export const EXPORT_DIALOG_SUBTITLE = "导出流程为JSON文件。";
/**
 * The base text for subtitle of Flow Settings (Menubar)
 * @constant
 */
export const SETTINGS_DIALOG_SUBTITLE =
  "自定义您的工作流细节和设置。";

/**
 * The base text for subtitle of Flow Logs (Menubar)
 * @constant
 */
export const LOGS_DIALOG_SUBTITLE =
  "查看组件之间事件和交互过程日志。";

/**
 * The base text for subtitle of Code Dialog (Toolbar)
 * @constant
 */
export const CODE_DIALOG_SUBTITLE =
  "导出您的工作流以便使用此代码进行集成";

/**
 * The base text for subtitle of Chat Form
 * @constant
 */
export const CHAT_FORM_DIALOG_SUBTITLE =
  "与您的 AI 进行交互。监控输入、输出和记忆数据。";

/**
 * The base text for subtitle of Edit Node Dialog
 * @constant
 */
export const EDIT_DIALOG_SUBTITLE =
  "调整组件设置并定义参数可见性。请注意保存您的更改。";

/**
 * The base text for subtitle of Code Dialog
 * @constant
 */
export const CODE_PROMPT_DIALOG_SUBTITLE =
  "编辑您的 Python 代码片段。有关如何编写自定义组件的更多信息，请参考 WorldSeek Agent 文档。";

export const CODE_DICT_DIALOG_SUBTITLE =
  "可根据自身需求对字典进行定制，添加或编辑键值对。同时，它支持添加新对象 `{}` 或者数组 `[]`。";

/**
 * The base text for subtitle of Prompt Dialog
 * @constant
 */
export const PROMPT_DIALOG_SUBTITLE =
  "创建您的提示词。提示词有助于引导语言模型的行为。使用花括号 `{}` 来引入变量。";

export const CHAT_CANNOT_OPEN_TITLE = "无法开启聊天";

export const CHAT_CANNOT_OPEN_DESCRIPTION = "这不是一个聊天工作流。";

export const FLOW_NOT_BUILT_TITLE = "工作流未构建";

export const FLOW_NOT_BUILT_DESCRIPTION =
  "请先构建工作流再进行聊天。";

/**
 * The base text for subtitle of Text Dialog
 * @constant
 */
export const TEXT_DIALOG_TITLE = "编辑文本内容";

/**
 * The base text for subtitle of Import Dialog
 * @constant
 */
export const IMPORT_DIALOG_SUBTITLE =
  "从 JSON 文件导入工作流，也能从现有的示例里进行挑选。";

/**
 * The text that shows when a tooltip is empty
 * @constant
 */
export const TOOLTIP_EMPTY = "未找到兼容的组件。";

export const CSVViewErrorTitle = "导出CSV文件";

export const CSVNoDataError = "没有数据可用";

export const PDFViewConstant = "展开查看 PDF";

export const CSVError = "加载 CSV 文件时出错";

export const PDFLoadErrorTitle = "加载 PDF 文件时出错";

export const PDFCheckFlow = "请检查您的工作流并重试";

export const PDFErrorTitle = "导出PDF文件";

export const PDFLoadError = "运行工作流以查看 PDF";

export const IMGViewConstant = "展开查看图片";

export const IMGViewErrorMSG =
  "运行工作流或提供有效的 URL 以查看图片";

export const IMGViewErrorTitle = "导出图片";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const EXPORT_CODE_DIALOG =
  "生成将工作流集成到外部应用程序的代码。";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const COLUMN_DIV_STYLE =
  " w-full h-full flex overflow-auto flex-col bg-muted px-16 ";

export const NAV_DISPLAY_STYLE =
  " w-full flex justify-between py-12 pb-2 px-6 ";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const DESCRIPTIONS: string[] = [
  "词语接龙，驭语言之术！",
  "语言架构师，匠心构筑中！",
  "赋能语言工程，激活智链未来。",
  "在此雕琢语言纽带，编织语义脉络。",
  "创作・连接・对话 —— 三维语言引擎启动。",
  "智能链构底层，智愈对话上层。",
  "桥接提示词，点亮语言灵光。",
  "语言模型已解缚，语义洪流任驰骋。",
  "文本生成中枢，尽在您的掌控。",
  "Prompt 即启，巧思天成！",
  "构筑语言迷宮，探索语义秘境。",
  "WorldSeek Agent: 创作・链联・沟通三位一体。",
  "连点成线，琢语成篇。",
  "交互式语言编织，经纬之间见智联。",
  "生成・革新・传意 —— 语言技术三角驱动。",
  "对话催化引擎：让交流迸发智核反应。",
  "语言链联大师，串起语义万维网。",
  "与 WorldSeek Agent 共设计，让对话成为交互艺术品。",
  "在此培育 NLP 节点，浇灌语义智能之树。",
  "对话绘图学已解锁，绘制交流认知图谱。",
  "设计・开发・对话化 —— 三步构建智能交互生态。",
];
export const BUTTON_DIV_STYLE =
  " flex gap-2 focus:ring-1 focus:ring-offset-1 focus:ring-ring focus:outline-none ";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const ADJECTIVES: string[] = [
  "钦佩的",
  "崇拜的",
  "焦虑的",
  "神奇的",
  "愤怒的",
  "令人敬畏的",
  "背叛的",
  "失控的",
  "巨大的",
  "无聊的",
  "聪明的",
  "自大的",
  "有同情心的",
  "轻蔑的",
  "易怒的",
  "绝望的",
  "坚定的",
  "分心的",
  "梦幻的",
  "醉酒的",
  "狂喜的",
  "高兴的",
  "优雅的",
  "邪恶的",
  "热情的",
  "专注的",
  "暴怒的",
  "庞大的",
  "阴郁的",
  "滑稽的",
  "庄重的",
  "快乐的",
  "高贵的",
  "有希望的",
  "饥饿的",
  "疯狂的",
  "愉快的",
  "友好的",
  "疯狂的",
  "孤独的",
  "喜爱的",
  "疯狂的",
  "谦虚的",
  "顽皮的",
  "恶心的",
  "怀旧的",
  "迂腐的",
  "沉思的",
  "尖锐的",
  "虔诚的",
  "浪漫的",
  "悲伤的",
  "宁静的",
  "锋利的",
  "恶心的",
  "愚蠢的",
  "困倦的",
  "微小的",
  "隐忍的",
  "震惊的",
  "可疑的",
  "温柔的",
  "渴望的",
  "极小的",
  "信任的",
  "活泼的",
  "迷人的",
  "愉快的",
  "滑稽的",
  "闪耀的",
  "欣喜的",
  "充满活力的",
  "热情的",
  "热心的",
  "兴高采烈的",
  "毛茸茸的",
  "友善的",
  "古怪的",
  "轻快的",
  "滑稽的",
  "欢快的",
  "愚蠢的",
  "优雅的",
  "笑嘻嘻的",
  "可笑的",
  "好奇的",
  "喜悦的",
  "欢呼的",
  "活跃的",
  "欢快的",
  "调皮的",
  "乐观的",
  "活泼的",
  "自信的",
  "淘气的",
  "古怪的",
  "灿烂的",
  "时髦的",
  "傻气的",
  "生机勃勃的",
  "敏捷的",
  "闪烁的",
  "积极向上的",
  "鲜艳的",
  "机智的",
  "荒唐的",
  "狂热的",
];
/**
 * Nouns for the name of the flow
 * @constant
 *
 */
export const NOUNS: string[] = [
  "阿尔巴塔尼",
  "艾伦",
  "阿尔梅达",
  "阿基米德",
  "阿德里安",
  "阿尔耶波多",
  "奥斯汀",
  "巴贝奇",
  "巴纳赫",
  "巴丁",
  "巴提克",
  "巴西",
  "贝尔",
  "巴巴",
  "巴什卡拉",
  "布莱克韦尔",
  "玻尔",
  "布斯",
  "博尔",
  "博斯",
  "博伊德",
  "布雷纳",
  "布雷特恩",
  "布朗",
  "卡森",
  "钱德拉塞卡",
  "科尔登",
  "科里",
  "克雷",
  "居里",
  "达尔文",
  "达维",
  "迪杰斯特拉",
  "杜比尼",
  "埃斯利",
  "爱因斯坦",
  "伊利翁",
  "恩格尔巴特",
  "欧几里得",
  "欧拉",
  "费马",
  "费米",
  "费恩曼",
  "富兰克林",
  "伽利略",
  "盖茨",
  "戈德堡",
  "戈尔德斯坦",
  "戈尔德瓦瑟",
  "戈勒克",
  "古德尔",
  "汉密尔顿",
  "霍金",
  "海森堡",
  "赫耶罗夫斯基",
  "霍奇金",
  "胡佛",
  "霍珀",
  "胡格勒",
  "希帕蒂娅",
  "张",
  "詹宁斯",
  "杰普森",
  "约里奥",
  "琼斯",
  "卡拉姆",
  "凯勒",
  "科勒",
  "科拉纳",
  "基尔比",
  "基尔",
  "克努斯",
  "科瓦列夫斯基",
  "拉兰德",
  "拉马尔",
  "莱基",
  "莱维特",
  "利特曼",
  "利斯科夫",
  "洛夫莱斯",
  "卢米埃尔",
  "马哈维拉",
  "迈耶",
  "麦卡锡",
  "麦克林",
  "麦克纳尔蒂",
  "麦克尼尔蒂",
  "迈特纳",
  "曼宁斯基",
  "梅斯特尔",
  "明斯基",
  "米尔扎哈尼",
  "摩尔斯",
  "穆德克",
  "牛顿",
  "诺贝尔",
  "诺特",
  "诺斯库特",
  "诺伊斯",
  "帕尼尼",
  "帕尔",
  "帕斯特",
  "佩恩",
  "佩尔曼",
  "皮克",
  "庞加莱",
  "波伊特拉斯",
  "托勒密",
  "拉曼",
  "拉马努金",
  "里德",
  "里奇",
  "伦琴",
  "罗莎琳",
  "萨哈",
  "萨姆梅特",
  "肖",
  "夏普利",
  "肖克利",
  "辛诺斯",
  "斯奈德",
  "斯普恩斯",
  "斯塔曼",
  "斯通布雷克",
  "斯旺森",
  "斯瓦茨",
  "斯威尔斯",
  "特斯拉",
  "汤普森",
  "托瓦兹",
  "图灵",
  "瓦拉哈米希拉",
  "维韦斯瓦拉",
  "沃尔哈德",
  "韦斯考夫",
  "威廉姆斯",
  "威尔逊",
  "韦恩",
  "沃兹尼亚克",
  "赖特",
  "亚洛",
  "约纳特",
  "库仑",
  "德格拉斯",
  "德威",
  "爱迪生",
  "埃拉托斯特尼",
  "法拉第",
  "高尔顿",
  "高斯",
  "赫歇尔",
  "哈勃",
  "焦耳",
  "卡库",
  "开普勒",
  "卡西尼",
  "拉瓦锡",
  "麦克斯韦",
  "孟德尔",
  "门捷列夫",
  "欧姆",
  "帕斯卡",
  "普朗克",
  "黎曼",
  "薛定谔",
  "萨根",
  "特斯拉",
  "泰森",
  "伏特",
  "瓦特",
  "韦伯",
  "维恩",
  "佐贝尔",
  "祖斯",
];

/**
 * Header text for user projects
 * @constant
 *
 */
export const USER_PROJECTS_HEADER = "我的收藏";

export const DEFAULT_FOLDER = "我的项目";
export const DEFAULT_FOLDER_DEPRECATED = "My Projects";

export const MAX_MCP_SERVER_NAME_LENGTH = 30;

/**
 * Header text for admin page
 * @constant
 *
 */
export const ADMIN_HEADER_TITLE = "管理员页面";

/**
 * Header description for admin page
 * @constant
 *
 */
export const ADMIN_HEADER_DESCRIPTION =
  "通过此部分高效管理所有应用用户。从这里，您可以无缝管理用户账户。";

export const BASE_URL_API = custom.BASE_URL_API || "/api/v1/";

export const BASE_URL_API_V2 = custom.BASE_URL_API_V2 || "/api/v2/";

/**
 * URLs excluded from error retries.
 * @constant
 *
 */
export const URL_EXCLUDED_FROM_ERROR_RETRIES = [
  `${BASE_URL_API}validate/code`,
  `${BASE_URL_API}custom_component`,
  `${BASE_URL_API}validate/prompt`,
  `${BASE_URL_API}/login`,
  `${BASE_URL_API}api_key/store`,
];

export const skipNodeUpdate = [
  "CustomComponent",
  "PromptTemplate",
  "ChatMessagePromptTemplate",
  "SystemMessagePromptTemplate",
  "HumanMessagePromptTemplate",
];

export const CONTROL_INPUT_STATE = {
  password: "",
  cnfPassword: "",
  username: "",
};

export const CONTROL_PATCH_USER_STATE = {
  password: "",
  cnfPassword: "",
  profilePicture: "",
  apikey: "",
};

export const CONTROL_LOGIN_STATE = {
  username: "",
  password: "",
};

export const CONTROL_NEW_USER = {
  username: "",
  password: "",
  is_active: false,
  is_superuser: false,
};

export const tabsCode = [];

export const FETCH_ERROR_MESSAGE = "无法建立连接。";
export const FETCH_ERROR_DESCRIPION =
  "请检查所有组件是否正常运行，然后重试。";

export const TIMEOUT_ERROR_MESSAGE =
  "服务器正在处理您的请求，请稍候片刻。";
export const TIMEOUT_ERROR_DESCRIPION = "服务器繁忙。";

export const SIGN_UP_SUCCESS = "账户创建成功！等待管理员激活。";

export const API_PAGE_PARAGRAPH =
  "您的WorldSeek Agent API密钥列表如下。请不要与他人分享您的API密钥，或将其暴露在浏览器或其他客户端代码中。";

export const API_PAGE_USER_KEYS =
  "此用户目前没有分配任何密钥。";

export const LAST_USED_SPAN_1 = "此密钥最近使用的时间。";

export const LAST_USED_SPAN_2 =
  "精确到最近使用时间的小时。";

export const LANGFLOW_SUPPORTED_TYPES = new Set([
  "str",
  "bool",
  "float",
  "code",
  "prompt",
  "file",
  "int",
  "dict",
  "NestedDict",
  "table",
  "link",
  "slider",
  "tab",
  "sortableList",
  "connect",
  "auth",
  "query",
  "mcp",
  "tools",
]);

export const FLEX_VIEW_TYPES = ["bool"];

export const priorityFields = new Set(["code", "template", "mode"]);

export const INPUT_TYPES = new Set([
  "ChatInput",
  // "TextInput",
  // "KeyPairInput",
  // "JsonInput",
  // "StringListInput",
]);
export const OUTPUT_TYPES = new Set([
  "ChatOutput",
  // "TextOutput",
  // "PDFOutput",
  // "ImageOutput",
  // "CSVOutput",
  // "JsonOutput",
  // "KeyPairOutput",
  // "StringListOutput",
  // "DataOutput",
  // "TableOutput",
]);

export const CHAT_FIRST_INITIAL_TEXT =
  "启动对话并点击智能体的记忆功能";

export const TOOLTIP_OUTDATED_NODE =
  "您的组件已过时。点击更新（数据可能丢失）";

export const CHAT_SECOND_INITIAL_TEXT = "查看历史消息。";

export const TOOLTIP_OPEN_HIDDEN_OUTPUTS = "展开结果";
export const TOOLTIP_HIDDEN_OUTPUTS = "折叠结果";

export const ZERO_NOTIFICATIONS = "没有新的通知";

export const SUCCESS_BUILD = "构建成功 ✨";

export const ALERT_SAVE_WITH_API =
  "警告：取消选中此框只会从专门指定用于 API 密钥的字段中删除 API 密钥。";

export const SAVE_WITH_API_CHECKBOX = "使用我的API密钥保存";
export const EDIT_TEXT_MODAL_TITLE = "编辑文本";
export const EDIT_TEXT_PLACEHOLDER = "在此输入消息。";
export const INPUT_HANDLER_HOVER = "可用的输入组件：";
export const OUTPUT_HANDLER_HOVER = "可用的输出组件：";
export const TEXT_INPUT_MODAL_TITLE = "输入";
export const OUTPUTS_MODAL_TITLE = "输出";
export const LANGFLOW_CHAT_TITLE = "WorldSeek Agent 聊天";
export const CHAT_INPUT_PLACEHOLDER =
  "没有找到聊天输入变量。点击运行您的工作流。";
export const CHAT_INPUT_PLACEHOLDER_SEND = "发送消息...";
export const EDIT_CODE_TITLE = "编辑代码";
export const MY_COLLECTION_DESC =
  "管理您的项目。下载和上传整个集合。";
export const STORE_DESC = "探索社区共享的工作流和组件。";
export const STORE_TITLE = "WorldSeek Agent 商店";
export const NO_API_KEY = "您没有API密钥。";
export const INSERT_API_KEY = "新建您的WorldSeek Agent API密钥。";
export const INVALID_API_KEY = "您的API密钥无效。";
export const CREATE_API_KEY = `没有API密钥？注册`;
export const STATUS_BUILD = "构建以验证状态。";
export const STATUS_INACTIVE = "执行被阻止";
export const STATUS_BUILDING = "构建中...";
export const SAVED_HOVER = "最后保存：";
export const RUN_TIMESTAMP_PREFIX = "最后运行：";
export const STARTER_FOLDER_NAME = "新手项目";
export const PRIORITY_SIDEBAR_ORDER = [
  "saved_components",
  "inputs",
  "outputs",
  "prompts",
  "data",
  "prompt",
  "models",
  "helpers",
  "vectorstores",
  "embeddings",
];

export const BUNDLES_SIDEBAR_FOLDER_NAMES = [
  "notion",
  "Notion",
  "AssemblyAI",
  "assemblyai",
  "LangWatch",
  "langwatch",
  "Youtube",
  "youtube",
];

export const AUTHORIZED_DUPLICATE_REQUESTS = [
  "/health",
  "/flows",
  "/logout",
  "/refresh",
  "/login",
  "/auto_login",
];

export const BROKEN_EDGES_WARNING =
  "部分连接因无效已被移除：";

export const SAVE_DEBOUNCE_TIME = 300;

export const IS_MAC =
  typeof navigator !== "undefined" &&
  navigator.userAgent.toUpperCase().includes("MAC");

export const defaultShortcuts = [
  {
    display_name: "控制",
    name: "高级设置",
    shortcut: "mod+shift+a",
  },
  {
    display_name: "侧边栏搜索组件",
    name: "侧边栏搜索组件",
    shortcut: "/",
  },
  {
    display_name: "最小化",
    name: "最小化",
    shortcut: "mod+.",
  },
  {
    display_name: "代码",
    name: "代码",
    shortcut: "space",
  },
  {
    display_name: "复制",
    name: "复制",
    shortcut: "mod+c",
  },
  {
    display_name: "复制（副本）",
    name: "复制（副本）",
    shortcut: "mod+d",
  },
  {
    display_name: "组件共享",
    name: "组件共享",
    shortcut: "mod+shift+s",
  },
  {
    display_name: "文档",
    name: "文档",
    shortcut: "mod+shift+d",
  },
  {
    display_name: "保存更改",
    name: "保存更改",
    shortcut: "mod+s",
  },
  {
    display_name: "保存组件",
    name: "保存组件",
    shortcut: "mod+alt+s",
  },
  {
    display_name: "删除",
    name: "删除",
    shortcut: "backspace",
  },
  {
    display_name: "打开游乐场",
    name: "打开游乐场",
    shortcut: "mod+k",
  },
  {
    display_name: "撤销",
    name: "撤销",
    shortcut: "mod+z",
  },
  {
    display_name: "重做",
    name: "重做",
    shortcut: "mod+y",
  },
  {
    display_name: "重做（替代）",
    name: "重做（替代）",
    shortcut: "mod+shift+z",
  },
  {
    display_name: "分组",
    name: "分组",
    shortcut: "mod+g",
  },
  {
    display_name: "剪切",
    name: "剪切",
    shortcut: "mod+x",
  },
  {
    display_name: "粘贴",
    name: "粘贴",
    shortcut: "mod+v",
  },
  {
    display_name: "API密钥",
    name: "API密钥",
    shortcut: "r",
  },
  {
    display_name: "下载",
    name: "下载",
    shortcut: "mod+j",
  },
  {
    display_name: "更新",
    name: "更新",
    shortcut: "mod+u",
  },
  {
    display_name: "冻结",
    name: "冻结",
    shortcut: "mod+shift+f",
  },
  {
    display_name: "工作流共享",
    name: "工作流共享",
    shortcut: "mod+shift+b",
  },
  {
    display_name: "运行",
    name: "运行",
    shortcut: "p",
  },
  {
    display_name: "输出检查",
    name: "输出检查",
    shortcut: "o",
  },
  {
    display_name: "工具模式",
    name: "工具模式",
    shortcut: "mod+shift+m",
  },
  {
    display_name: "切换侧边栏",
    name: "切换侧边栏",
    shortcut: "mod+b",
  },
];

export const DEFAULT_TABLE_ALERT_MSG = `哎呀！看起来现在没有数据可以显示。请稍后再试。`;

export const DEFAULT_TABLE_ALERT_TITLE = "没有数据";

export const NO_COLUMN_DEFINITION_ALERT_TITLE = "没有列定义";

export const NO_COLUMN_DEFINITION_ALERT_DESCRIPTION =
  "此表没有可用的列定义。";

export const LOCATIONS_TO_RETURN = ["/flow/", "/settings/"];

export const MAX_BATCH_SIZE = 50;

export const MODAL_CLASSES =
  "nopan nodelete nodrag  noflow fixed inset-0 bottom-0 left-0 right-0 top-0 z-50 overflow-auto bg-black/50 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0";

export const ALLOWED_IMAGE_INPUT_EXTENSIONS = ["png", "jpg", "jpeg"];

export const componentsToIgnoreUpdate = ["CustomComponent"];

export const FS_ERROR_TEXT =
  "请确保您的文件具有以下扩展名之一：";
export const SN_ERROR_TEXT = ALLOWED_IMAGE_INPUT_EXTENSIONS.join(", ");

export const ERROR_UPDATING_COMPONENT =
  "更新组件时发生意外错误。请重试。";
export const TITLE_ERROR_UPDATING_COMPONENT =
  "更新组件时出错";

export const EMPTY_INPUT_SEND_MESSAGE = "没有提供输入消息。";

export const EMPTY_OUTPUT_SEND_MESSAGE = "消息为空。";

export const TABS_ORDER = [
  "curl",
  "python api",
  "js api",
  "python code",
  "chat widget html",
];

export const LANGFLOW_ACCESS_TOKEN = "access_token_lf";
export const LANGFLOW_API_TOKEN = "apikey_tkn_lflw";
export const LANGFLOW_AUTO_LOGIN_OPTION = "auto_login_lf";
export const LANGFLOW_REFRESH_TOKEN = "refresh_token_lf";

export const LANGFLOW_ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 - 60 * 60 * 0.1;
export const LANGFLOW_ACCESS_TOKEN_EXPIRE_SECONDS_ENV =
  Number(process.env?.ACCESS_TOKEN_EXPIRE_SECONDS ?? 60) -
  Number(process.env?.ACCESS_TOKEN_EXPIRE_SECONDS ?? 60) * 0.1;
export const TEXT_FIELD_TYPES: string[] = ["str", "SecretStr"];
export const NODE_WIDTH = 384;
export const NODE_HEIGHT = NODE_WIDTH * 3;

export const SHORTCUT_KEYS = ["cmd", "ctrl", "mod", "alt", "shift"];

export const SERVER_HEALTH_INTERVAL = 10000;
export const REFETCH_SERVER_HEALTH_INTERVAL = 20000;
export const DRAG_EVENTS_CUSTOM_TYPESS = {
  genericnode: "genericNode",
  notenode: "noteNode",
  "text/plain": "text/plain",
};

export const NOTE_NODE_MIN_WIDTH = 324;
export const NOTE_NODE_MIN_HEIGHT = 324;
export const NOTE_NODE_MAX_HEIGHT = 800;
export const NOTE_NODE_MAX_WIDTH = 600;

export const COLOR_OPTIONS = {
  amber: "hsl(var(--note-amber))",
  neutral: "hsl(var(--note-neutral))",
  rose: "hsl(var(--note-rose))",
  blue: "hsl(var(--note-blue))",
  lime: "hsl(var(--note-lime))",
  transparent: null,
};

export const maxSizeFilesInBytes = 10 * 1024 * 1024; // 10MB in bytes
export const MAX_TEXT_LENGTH = 99999;

export const SEARCH_TABS = ["All", "Flows", "Components"];
export const PAGINATION_SIZE = 12;
export const PAGINATION_PAGE = 1;

export const STORE_PAGINATION_SIZE = 12;
export const STORE_PAGINATION_PAGE = 1;

export const PAGINATION_ROWS_COUNT = [12, 24, 48, 96];
export const STORE_PAGINATION_ROWS_COUNT = [12, 24, 48, 96];

export const GRADIENT_CLASS =
  "linear-gradient(to right, hsl(var(--background) / 0.3), hsl(var(--background)))";

export const GRADIENT_CLASS_DISABLED =
  "linear-gradient(to right, hsl(var(--muted) / 0.3), hsl(var(--muted)))";

export const RECEIVING_INPUT_VALUE = "接收输入";
export const SELECT_AN_OPTION = "选择一个选项";

export const ICON_STROKE_WIDTH = 1.5;

export const DEFAULT_PLACEHOLDER = "输入一些内容...";

export const DEFAULT_TOOLSET_PLACEHOLDER = "用作工具";

export const SAVE_API_KEY_ALERT = "API密钥保存成功";
export const PLAYGROUND_BUTTON_NAME = "游乐场";
export const POLLING_MESSAGES = {
  ENDPOINT_NOT_AVAILABLE: "端点不可用",
  STREAMING_NOT_SUPPORTED: "流式传输不支持",
} as const;

export const BUILD_POLLING_INTERVAL = 25;

export const IS_AUTO_LOGIN =
  !process?.env?.LANGFLOW_AUTO_LOGIN ||
  String(process?.env?.LANGFLOW_AUTO_LOGIN)?.toLowerCase() !== "false";

export const AUTO_LOGIN_RETRY_DELAY = 2000;
export const AUTO_LOGIN_MAX_RETRY_DELAY = 60000;

export const ALL_LANGUAGES = [
  { value: "en-US", name: "English (US)" },
  { value: "en-GB", name: "English (UK)" },
  { value: "it-IT", name: "Italian" },
  { value: "fr-FR", name: "French" },
  { value: "es-ES", name: "Spanish" },
  { value: "de-DE", name: "German" },
  { value: "ja-JP", name: "Japanese" },
  { value: "pt-BR", name: "Portuguese (Brazil)" },
  { value: "zh-CN", name: "中文 (简体)" },
  { value: "ru-RU", name: "Russian" },
  { value: "ar-SA", name: "Arabic" },
  { value: "hi-IN", name: "Hindi" },
];

export const DEBOUNCE_FIELD_LIST = [
  "SecretStrInput",
  "MessageTextInput",
  "TextInput",
  "MultilineInput",
  "SecretStrInput",
  "IntInput",
  "FloatInput",
  "SliderInput",
];

export const OPENAI_VOICES = [
  { name: "alloy", value: "alloy" },
  { name: "ash", value: "ash" },
  { name: "ballad", value: "ballad" },
  { name: "coral", value: "coral" },
  { name: "echo", value: "echo" },
  { name: "sage", value: "sage" },
  { name: "shimmer", value: "shimmer" },
  { name: "verse", value: "verse" },
];

export const DEFAULT_POLLING_INTERVAL = 5000;
export const DEFAULT_TIMEOUT = 30000;
export const DEFAULT_FILE_PICKER_TIMEOUT = 60000;
export const DISCORD_URL = "https://discord.com/invite/EqksyE2EX9";
export const GITHUB_URL = "https://github.com/langflow-ai/langflow";
export const TWITTER_URL = "https://x.com/langflow_ai";
export const DOCS_URL = "https://docs.langflow.org";
export const DATASTAX_DOCS_URL =
  "https://docs.datastax.com/en/langflow/index.html";

export const UUID_PARSING_ERROR = "uuid_parsing";
