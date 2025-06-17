import { UniqueInputsComponents } from "../types";

export const getDisabledTooltip = (
  SBItemName: string,
  uniqueInputsComponents: UniqueInputsComponents,
) => {
  if (SBItemName === "ChatInput" && uniqueInputsComponents.chatInput) {
    return "聊天输入组件已添加";
  }
  if (SBItemName === "Webhook" && uniqueInputsComponents.webhookInput) {
    return "Webhook 已添加";
  }
  return "";
};
