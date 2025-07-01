import {
  useCreateModel,
  useUpdateModel,
} from "@/controllers/API/queries/models/use-models-crud";
import { Model } from "@/controllers/API/queries/models/use-models-crud";
import { useEffect, useState } from "react";

import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import BaseModal from "@/modals/baseModal";
import useAlertStore from "@/stores/alertStore";
import { ResponseErrorDetailAPI } from "@/types/api";
import InputComponent from "../parameterRenderComponent/components/inputComponent";

export default function ModelModal({
  children,
  asChild,
  initialData,
  open: myOpen,
  setOpen: mySetOpen,
  disabled = false,
}: {
  children?: JSX.Element;
  asChild?: boolean;
  initialData?: Model;
  open?: boolean;
  setOpen?: (a: boolean | ((o?: boolean) => boolean)) => void;
  disabled?: boolean;
}): JSX.Element {
  const [modelId, setModelId] = useState(initialData?.model_id ?? "");
  const [name, setName] = useState(initialData?.name ?? "");
  const [apiPath, setApiPath] = useState(initialData?.api_path ?? "");
  const [apiKey, setApiKey] = useState(initialData?.api_key ?? "");
  
  // 当initialData改变时更新状态
  useEffect(() => {
    if (initialData) {
      setModelId(initialData.model_id || "");
      setName(initialData.name || "");
      setApiPath(initialData.api_path || "");
      setApiKey(initialData.api_key || "");
    } else {
      setModelId("");
      setName("");
      setApiPath("");
      setApiKey("");
    }
  }, [initialData]);
  const [open, setOpen] =
    mySetOpen !== undefined && myOpen !== undefined
      ? [myOpen, mySetOpen]
      : useState(false);
  
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  
  const { mutate: mutateCreateModel } = useCreateModel();
  const { mutate: mutateUpdateModel } = useUpdateModel();

  function handleSaveModel() {
    const data = {
      name: name.trim(),
      model_id: modelId.trim(),
      api_path: apiPath.trim(),
      api_key: apiKey.trim(),
    };

    if (!data.name || !data.model_id || !data.api_path || !data.api_key) {
      setErrorData({
        title: "表单验证失败",
        list: ["请填写所有必填字段"],
      });
      return;
    }

    if (initialData?.id) {
      // 更新模型
      mutateUpdateModel(
        { id: initialData.id, model: data },
        {
          onSuccess: (res) => {
            setModelId("");
            setName("");
            setApiPath("");
            setApiKey("");
            setOpen(false);
            setSuccessData({
              title: `模型 ${res.name} 更新成功`,
            });
          },
          onError: (error) => {
            let responseError = error as unknown as ResponseErrorDetailAPI;
            setErrorData({
              title: "模型更新失败",
              list: [
                responseError?.response?.data?.detail ?? "模型更新失败，请重试。",
              ],
            });
          },
        }
      );
    } else {
      // 创建模型
      mutateCreateModel(data, {
        onSuccess: (res) => {
          setModelId("");
          setName("");
          setApiPath("");
          setApiKey("");
          setOpen(false);
          setSuccessData({
            title: `模型 ${res.name} 创建成功`,
          });
        },
        onError: (error) => {
          let responseError = error as unknown as ResponseErrorDetailAPI;
          setErrorData({
            title: "模型创建失败",
            list: [
              responseError?.response?.data?.detail ?? "模型创建失败，请重试。",
            ],
          });
        },
      });
    }
  }

  const isFormValid = modelId.trim() && name.trim() && apiPath.trim() && apiKey.trim();

  return (
    <BaseModal
      open={open}
      setOpen={setOpen}
      size="x-small"
      onSubmit={handleSaveModel}
      disable={disabled || !isFormValid}
    >
      <BaseModal.Header description="使用指定的模型提供者运行语言模型。">
        <ForwardedIconComponent
          name="models"
          className="h-6 w-6 pr-1 text-primary mr-2"
          aria-hidden="true"
        />
        {initialData ? "更新模型" : "语言模型"}
      </BaseModal.Header>
      <BaseModal.Trigger disable={disabled} asChild={asChild}>
        {children}
      </BaseModal.Trigger>
      <BaseModal.Content>
        <div className="flex h-full w-full flex-col gap-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Label htmlFor="model-id" className="text-sm font-medium">
                  模型ID
                </Label>
                <p className="text-xs text-muted-foreground">实际请求的模型名称</p>
              </div>
              <Input
                id="model-id"
                value={modelId}
                onChange={(e) => setModelId(e.target.value)}
                placeholder="deepseek-v3"
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Label htmlFor="model-name" className="text-sm font-medium">
                  模型名称
                </Label>
                <p className="text-xs text-muted-foreground">模型的显示名称</p>
              </div>
              <Input
                id="model-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Deepseek-V3"
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Label htmlFor="api-path" className="text-sm font-medium">
                  模型链接
                </Label>
                <p className="text-xs text-muted-foreground">模型提供者的访问链接</p>
              </div>
              <Input
                id="api-path"
                value={apiPath}
                onChange={(e) => setApiPath(e.target.value)}
                placeholder="http://localhost:1234/v1"
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Label htmlFor="api-key" className="text-sm font-medium">
                  API Key
                </Label>
                <p className="text-xs text-muted-foreground">模型提供者的API密钥</p>
              </div>
              <InputComponent
                id="api-key"
                password
                value={apiKey}
                onChange={(e) => setApiKey(e)}
                placeholder="输入API密钥..."
                nodeStyle
                className="w-full"
              />
            </div>
          </div>
        </div>
      </BaseModal.Content>
      <BaseModal.Footer
        submit={{
          label: initialData ? "更新" : "保存",
          dataTestId: "save-model-btn",
        }}
      />
    </BaseModal>
  );
} 