import useFlowsManagerStore from "@/stores/flowsManagerStore";
import { useTypesStore } from "@/stores/typesStore";
import { APIObjectType, useQueryFunctionType } from "../../../../types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

export const useGetTypes: useQueryFunctionType<
  undefined,
  any,
  { checkCache?: boolean }
> = (options) => {
  const { query } = UseRequestProcessor();
  const setLoading = useFlowsManagerStore((state) => state.setIsLoading);
  const setTypes = useTypesStore((state) => state.setTypes);

  const getTypesFn = async (checkCache = false) => {
    try {
      if (checkCache) {
        const data = useTypesStore.getState().types;
        if (data && Object.keys(data).length > 0) {
          return data;
        }
      }

      const response = await api.get<APIObjectType>(
        `${getURL("ALL")}?force_refresh=true`,
      );
      const data = response?.data; 
      // 过滤数据
      if (data) {
        // 删除不需要的顶级对象
        delete data.embeddings;
        delete data.memories;
        delete data.vectorstores;
        
        // 过滤models对象，只保留指定的组件
        if (data.models) {
          const filteredModels: { [key: string]: any } = {};
          filteredModels.OpenAIModel = data.models.OpenAIModel;
          filteredModels.LanguageModelComponent = data.models.LanguageModelComponent;
          data.models = filteredModels;
        }

        if (data.tools) {
          const filteredTools: { [key: string]: any } = {};
          filteredTools.MCPTools = data.tools.MCPTools;
          filteredTools.CalculatorTool = data.tools.CalculatorTool;
          filteredTools.CalculatorComponent = data.tools.CalculatorComponent;
          filteredTools.GoogleSearchAPI = data.tools.GoogleSearchAPI;
          filteredTools.GoogleSearchAPICore = data.tools.GoogleSearchAPICore;
          filteredTools.BingSearchAPI = data.tools.BingSearchAPI;
          data.tools = filteredTools;
        }
      }
      
      setTypes(data);
      return data;
    } catch (error) {
      console.error("[Types] Error fetching types:", error);
      setLoading(false); 
      throw error;
    }
  };

  const queryResult = query(
    ["useGetTypes"],
    () => getTypesFn(options?.checkCache),
    {
      refetchOnWindowFocus: false,
      ...options,
    },
  );

  return queryResult;
};
