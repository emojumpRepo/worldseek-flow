import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  useGetConfigValue,
  useSetConfigValue,
} from "@/controllers/API/queries/config/use-config-crud";
import useAlertStore from "@/stores/alertStore";
import { useEffect, useState } from "react";
import IconComponent, {
  ForwardedIconComponent,
} from "../../../../components/common/genericIconComponent";

export default function KnowledgeBasePage() {
  const [apiKey, setApiKey] = useState("");
  const [apiBaseUrl, setApiBaseUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  // 获取现有配置
  const { data: apiKeyData } = useGetConfigValue("worldseek_kb_api_key");
  const { data: apiBaseUrlData } = useGetConfigValue(
    "worldseek_kb_api_base_url",
  );

  const setConfigValue = useSetConfigValue();

  useEffect(() => {
    if (apiKeyData?.value) {
      setApiKey(apiKeyData.value);
    }
  }, [apiKeyData]);

  useEffect(() => {
    if (apiBaseUrlData?.value) {
      setApiBaseUrl(apiBaseUrlData.value);
    }
  }, [apiBaseUrlData]);

  const handleSaveConfig = async () => {
    if (!apiBaseUrl.trim() && !apiKey.trim()) {
      setErrorData({
        title: "保存失败",
        list: ["没有配置任何内容"],
      });
      return;
    }

    setIsLoading(true);
    try {
      // 保存API密钥（如果有输入）
      if (apiKey.trim()) {
        await setConfigValue.mutateAsync({
          key: "worldseek_kb_api_key",
          value: apiKey.trim(),
        });
      }

      if (apiBaseUrl.trim()) {
        await setConfigValue.mutateAsync({
          key: "worldseek_kb_api_base_url",
          value: apiBaseUrl.trim(),
        });
      }

      setSuccessData({
        title: "配置保存成功",
      });
    } catch (error: any) {
      setErrorData({
        title: "保存失败",
        list: [error?.response?.data?.detail || error.message],
      });
    } finally {
      setIsLoading(false);
    }
  };

  const maskApiKey = (key: string) => {
    if (!key || key.length <= 8) return key;
    return key.substring(0, 12) + "*".repeat(6) + key.substring(key.length - 4);
  };

  const hasApiKey = apiKeyData?.value && apiKeyData.value.trim().length > 0;

  return (
    <div className="flex h-full w-full flex-col gap-6">
      <div className="flex w-full items-start justify-between gap-6">
        <div className="flex w-full flex-col">
          <h2 className="flex items-center text-lg font-semibold tracking-tight">
            知识库
            <ForwardedIconComponent
              name="BookText"
              className="ml-2 h-5 w-5 text-primary"
            />
          </h2>
          <p className="text-sm text-muted-foreground">
            管理 WorldSeek Agent 中的知识库配置
          </p>
        </div>
      </div>

      <div className="grid w-full grid-cols-2 gap-6">
        {/* API密钥配置 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="api-key">API密钥</Label>
            {hasApiKey && (
              <div className="flex items-center gap-2 text-sm bg-green-50 rounded-md px-2 py-1">
                <span className="text-green-600">
                  已配置: {maskApiKey(apiKeyData?.value || "")}
                </span>
              </div>
            )}
          </div>
          <Input
            id="api-key"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="输入新的WorldSeek KB API密钥"
            disabled={isLoading}
          />
        </div>

        {/* API基础URL配置 */}
        <div className="space-y-2">
          <Label htmlFor="api-base-url">API基础URL（注意：只填写域名，不要带 "/" ）</Label>
          <Input
            id="api-base-url"
            value={apiBaseUrl}
            onChange={(e) => setApiBaseUrl(e.target.value)}
            placeholder="填入WorldSeek KB API基础URL，留空表示使用默认值"
            disabled={isLoading}
          />
        </div>
      </div>

      <div className="flex justify-end">
        {/* 保存按钮 */}
        <Button
          onClick={handleSaveConfig}
          loading={isLoading}
          className="btn-primary w-fit"
        >
          保存配置
        </Button>
      </div>
    </div>
  );
}
