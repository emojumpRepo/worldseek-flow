import { useQueryFunctionType, useMutationFunctionType } from "@/types/api";
import { UseMutationResult } from "@tanstack/react-query";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";
import useAuthStore from "@/stores/authStore";

// 模型配置类型定义
export interface Model {
  id: number;
  name: string;
  model_id: string;
  api_path: string;
  api_key: string;
  created_at: string;
  updated_at: string;
}

export interface ModelCreate {
  name: string;
  model_id: string;
  api_path: string;
  api_key: string;
}

export interface ModelUpdate {
  name?: string;
  model_id?: string;
  api_path?: string;
  api_key?: string;
}

// 获取模型配置列表
export const useGetModels = (
  skip: number = 0,
  limit: number = 100,
  nameFilter?: string
) => {
  const { query } = UseRequestProcessor();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const getModelsFn = async (): Promise<Model[]> => {
    if (!isAuthenticated) return [];
    
    const queryParams = new URLSearchParams();
    queryParams.append("skip", skip.toString());
    queryParams.append("limit", limit.toString());
    if (nameFilter) queryParams.append("name_filter", nameFilter);
    
    const url = `${getURL("MODELS")}/?${queryParams.toString()}`;
    const res = await api.get(url);
    return res.data;
  };

  return query(
    ["useGetModels", skip, limit, nameFilter],
    getModelsFn,
    {
      refetchOnWindowFocus: false,
    }
  );
};

// 根据ID获取模型配置
export const useGetModel = (modelId: number) => {
  const { query } = UseRequestProcessor();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const getModelFn = async (): Promise<Model> => {
    if (!isAuthenticated) throw new Error("User not authenticated");
    
    const res = await api.get(`${getURL("MODELS")}/${modelId}`);
    return res.data;
  };

  return query(
    ["useGetModel", modelId],
    getModelFn,
    {
      enabled: !!modelId && isAuthenticated,
      refetchOnWindowFocus: false,
    }
  );
};

// 根据名称获取模型配置
export const useGetModelByName = (name: string) => {
  const { query } = UseRequestProcessor();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const getModelByNameFn = async (): Promise<Model> => {
    if (!isAuthenticated) throw new Error("User not authenticated");
    
    const res = await api.get(`${getURL("MODELS")}/name/${name}`);
    return res.data;
  };

  return query(
    ["useGetModelByName", name],
    getModelByNameFn,
    {
      enabled: !!name && isAuthenticated,
      refetchOnWindowFocus: false,
    }
  );
};

// 创建模型配置
export const useCreateModel: useMutationFunctionType<undefined, ModelCreate> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const createModelFn = async (model: ModelCreate): Promise<Model> => {
    const res = await api.post(`${getURL("MODELS")}/`, model);
    return res.data;
  };

  return mutate(["useCreateModel"], createModelFn, {
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["useGetModels"] });
    },
    ...options,
  });
};

// 更新模型配置
export const useUpdateModel: useMutationFunctionType<undefined, { id: number; model: ModelUpdate }> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const updateModelFn = async ({ id, model }: { id: number; model: ModelUpdate }): Promise<Model> => {
    const res = await api.put(`${getURL("MODELS")}/${id}`, model);
    return res.data;
  };

  return mutate(["useUpdateModel"], updateModelFn, {
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["useGetModels"] });
    },
    ...options,
  });
};

// 删除模型配置
export const useDeleteModel: useMutationFunctionType<undefined, number> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const deleteModelFn = async (modelId: number): Promise<void> => {
    const res = await api.delete(`${getURL("MODELS")}/${modelId}`);
    return res.data;
  };

  return mutate(["useDeleteModel"], deleteModelFn, {
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["useGetModels"] });
    },
    ...options,
  });
}; 