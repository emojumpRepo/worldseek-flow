import { createFileUpload } from "@/helpers/create-file-upload";
import { getObjectsFromFilelist } from "@/helpers/get-objects-from-filelist";
import useFlowStore from "@/stores/flowStore";
import { FlowType } from "@/types/flow";
import { processDataFromFlow } from "@/utils/reactflowUtils";
import useAddFlow from "./use-add-flow";

const useUploadFlow = () => {
  const addFlow = useAddFlow();
  const paste = useFlowStore((state) => state.paste);

  const getFlowsFromFiles = async ({
    files,
  }: {
    files: File[];
  }): Promise<FlowType[]> => {
    const objectList = await getObjectsFromFilelist<any>(files);
    const flows: FlowType[] = [];
    objectList.forEach((object) => {
      if (object.flows) {
        object.flows.forEach((flow: FlowType) => {
          flows.push(flow);
        });
      } else {
        flows.push(object as FlowType);
      }
    });
    return flows;
  };

  const getFlowsToUpload = async ({
    files,
  }: {
    files?: File[];
  }): Promise<FlowType[]> => {
    if (!files) {
      files = await createFileUpload();
    }
    if (!files.every((file) => file.type === "application/json")) {
      throw new Error("无效的文件类型");
    }
    return await getFlowsFromFiles({
      files,
    });
  };

  const uploadFlow = async ({
    files,
    isComponent,
    position,
  }: {
    files?: File[];
    isComponent?: boolean;
    position?: { x: number; y: number };
  }): Promise<void> => {
    try {
      let flows = await getFlowsToUpload({ files });
      for (const flow of flows) {
        await processDataFromFlow(flow);
      }

      if (
        isComponent !== undefined &&
        flows.every(
          (fileData) =>
            (!fileData.is_component && isComponent === true) ||
            (fileData.is_component !== undefined &&
              fileData.is_component !== isComponent),
        )
      ) {
        throw new Error(
          "不能将组件作为工作流上传，反之亦然",
        );
      } else {
        let currentPosition = position;
        for (const flow of flows) {
          if (flow.data) {
            if (currentPosition) {
              paste(flow.data, currentPosition);
              currentPosition = {
                x: currentPosition.x + 50,
                y: currentPosition.y + 50,
              };
            } else {
              await addFlow({ flow });
            }
          } else {
            throw new Error("无效的工作流数据");
          }
        }
      }
    } catch (e) {
      throw e;
    }
  };

  return uploadFlow;
};

export default useUploadFlow;
