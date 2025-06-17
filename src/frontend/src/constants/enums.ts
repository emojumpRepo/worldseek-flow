/**
 * enum for the different types of nodes
 * @enum
 */
export enum TypeModal {
  TEXT = 1,
  PROMPT = 2,
}

export enum BuildStatus {
  BUILDING = "构件中",
  TO_BUILD = "待构建",
  BUILT = "已构建",
  INACTIVE = "未激活",
  ERROR = "错误",
}

export enum InputOutput {
  INPUT = "输入",
  OUTPUT = "输出",
}

export enum IOInputTypes {
  TEXT = "文本输入",
  FILE_LOADER = "文件加载",
  KEYPAIR = "密钥对输入",
  JSON = "Json输入",
  STRING_LIST = "字符串列表输入",
}

export enum IOOutputTypes {
  TEXT = "文本输出",
  PDF = "PDF输出",
  CSV = "CSV输出",
  IMAGE = "图像输出",
  JSON = "Json输出",
  KEY_PAIR = "密钥对输出",
  STRING_LIST = "字符串列表输出",
  DATA = "数据输出",
}

export enum EventDeliveryType {
  STREAMING = "流式传输",
  POLLING = "轮询",
  DIRECT = "直接",
}
