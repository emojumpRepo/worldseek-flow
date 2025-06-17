import BaseModal from "@/modals/baseModal";
import useFlowsManagerStore from "@/stores/flowsManagerStore";
import { CardData } from "@/types/templates/types";
import memoryChatbot from "../../../../assets/temp-pat-1.png";
import vectorRag from "../../../../assets/temp-pat-2.png";
import multiAgent from "../../../../assets/temp-pat-3.png";
import memoryChatbotHorizontal from "../../../../assets/temp-pat-m-1.png";
import vectorRagHorizontal from "../../../../assets/temp-pat-m-2.png";
import multiAgentHorizontal from "../../../../assets/temp-pat-m-3.png";

import TemplateGetStartedCardComponent from "../TemplateGetStartedCardComponent";

export default function GetStartedComponent() {
  const examples = useFlowsManagerStore((state) => state.examples);

  // Define the card data
  const cardData: CardData[] = [
    {
      bgImage: memoryChatbot,
      bgHorizontalImage: memoryChatbotHorizontal,
      icon: "MessagesSquare",
      category: "提示词",
      flow: examples.find((example) => example.name === "基础提示词"),
    },
    {
      bgImage: multiAgent,
      bgHorizontalImage: multiAgentHorizontal,
      icon: "Bot",
      category: "智能体",
      flow: examples.find((example) => example.name === "简易智能体"),
    },
  ];

  return (
    <div className="flex flex-1 flex-col gap-4 md:gap-8">
      <BaseModal.Header description="从模板开始，展示 WorldSeek Agent 的基础提示词工作流和 Agent 用例。">
        开始
      </BaseModal.Header>
      <div className="grid flex-1 grid-cols-2 gap-4">
        {cardData.map((card, index) => (
          <TemplateGetStartedCardComponent key={index} {...card} />
        ))}
      </div>
    </div>
  );
}
