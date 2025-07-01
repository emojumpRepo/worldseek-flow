import { useQueryFunctionType } from "@/types/api";
import { UseMutationResult, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

// 配置项类型定义
export interface Config {
  id: number;
  key: string;
  value: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

// 获取配置值
export const useGetConfigValue = (key: string, defaultValue?: string) => {
  const { query } = UseRequestProcessor();

  const getConfigValueFn = async (): Promise<{ key: string; value: string | null }> => {
    const queryParams = new URLSearchParams();
    if (defaultValue) queryParams.append("default", defaultValue);
    
    const url = `${getURL("CONFIG")}/value/${key}?${queryParams.toString()}`;
    const response = await api.get<{ key: string; value: string | null }>(url);
    return response.data;
  };

  return query(
    ["useGetConfigValue", key, defaultValue],
    getConfigValueFn,
    {
      enabled: !!key,
      refetchOnWindowFocus: false,
    }
  );
};

// 设置配置值
export const useSetConfigValue = (): UseMutationResult<Config, Error, { key: string; value: string }> => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ key, value }: { key: string; value: string }): Promise<Config> => {
      const response = await api.post<Config>(`${getURL("CONFIG")}/value/${key}`, { value });
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["useGetConfigValue", variables.key] });
    },
  });
}; 