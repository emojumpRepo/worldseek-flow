import { ENABLE_DATASTAX_LANGFLOW } from "@/customization/feature-flags";
import { useGenerateToken } from "@/customization/hooks/use-custom-generate-token";
import { useEffect, useRef, useState } from "react";
import { COPIED_NOTICE_ALERT } from "../../constants/alerts_constants";
import { createApiKey } from "../../controllers/API";
import useAlertStore from "../../stores/alertStore";
import { ApiKeyType } from "../../types/components";
import BaseModal from "../baseModal";
import { ContentRenderKey } from "./components/content-render";
import { FormKeyRender } from "./components/form-key-render";
import { HeaderRender } from "./components/header-render";

// Add this interface for the modal props
interface ModalConfigProps {
  title?: string;
  description?: string | React.ReactElement;
  inputLabel?: React.ReactNode;
  inputPlaceholder?: string;
  buttonText?: string;
  generatedKeyMessage?: string | React.ReactElement;
  showIcon?: boolean;
}

interface SecretKeyModalProps {
  userId?: string;
  size?: string;
  modalProps?: ModalConfigProps;
}

export default function SecretKeyModal({
  children,
  data,
  onCloseModal,
  modalProps,
}: ApiKeyType & { modalProps: SecretKeyModalProps }) {
  const [open, setOpen] = useState(false);
  const [apiKeyName, setApiKeyName] = useState(data?.apikeyname ?? "");
  const [apiKeyValue, setApiKeyValue] = useState("");
  const [renderKey, setRenderKey] = useState(false);
  const [textCopied, setTextCopied] = useState(true);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const generateToken = useGenerateToken();
  const modalConfigProps = modalProps?.modalProps ?? modalProps;

  useEffect(() => {
    if (open) {
      setRenderKey(false);
      resetForm();
    } else {
      onCloseModal?.();
    }
  }, [open]);

  function resetForm() {
    setApiKeyName("");
    setApiKeyValue("");
  }

  const handleCopyClick = async () => {
    if (!apiKeyValue) return;

    try {
      // 检查 Clipboard API 是否可用
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(apiKeyValue);
      } else {
        // 回退方案：使用传统的复制方法适用于HTTP环境
        const textArea = document.createElement('textarea');
        textArea.value = apiKeyValue;
        
        // 设置样式使其不可见但仍然可以被选中
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        textArea.style.opacity = '0';
        textArea.style.pointerEvents = 'none';
        textArea.style.zIndex = '-1';
        
        document.body.appendChild(textArea);
        
        // 确保元素获得焦点并选中文本
        textArea.focus();
        textArea.select();
        textArea.setSelectionRange(0, 99999); // 移动端兼容
        
        // 执行复制命令
        const successful = document.execCommand('copy');
        
        // 清理DOM
        document.body.removeChild(textArea);
        
        if (!successful) {
          throw new Error('复制失败');
        }
      }
      
      inputRef?.current?.focus();
      inputRef?.current?.select();
      setSuccessData({
        title: COPIED_NOTICE_ALERT,
      });
      setTextCopied(false);

      setTimeout(() => {
        setTextCopied(true);
      }, 3000);
    } catch (error) {
      console.error('复制到剪贴板失败:', error);
      // 可以添加错误提示
      setSuccessData({
        title: "复制失败，请手动复制",
      });
    }
  };

  function handleAddNewKey() {
    createApiKey(apiKeyName)
      .then((res) => {
        setApiKeyValue(res["api_key"]);
      })
      .catch((err) => {});
  }

  async function handleSubmitForm() {
    if (apiKeyValue) setOpen(false);
    if (ENABLE_DATASTAX_LANGFLOW) {
      handleDataStaxKey();
    } else {
      handleOSSKey();
    }
  }

  const handleDataStaxKey = async () => {
    try {
      const { token } = await generateToken();
      setApiKeyValue(token);
      setRenderKey(true);
    } catch (error) {
      console.error("Error generating token:", error);
    }
  };

  const handleOSSKey = () => {
    if (!renderKey) {
      setRenderKey(true);
      handleAddNewKey();
    } else {
      setOpen(false);
    }
  };

  return (
    <BaseModal
      onSubmit={handleSubmitForm}
      size={modalProps?.size ?? "small-h-full"}
      open={open}
      setOpen={setOpen}
    >
      <BaseModal.Trigger asChild>{children}</BaseModal.Trigger>
      <BaseModal.Header
        clampDescription={3}
        description={
          renderKey 
            ? (typeof modalConfigProps?.generatedKeyMessage === 'string' 
                ? modalConfigProps.generatedKeyMessage 
                : modalConfigProps?.generatedKeyMessage || null)
            : (typeof modalConfigProps?.description === 'string' 
                ? modalConfigProps.description 
                : modalConfigProps?.description || null)
        }
      >
        <HeaderRender
          title={modalConfigProps?.title}
          showIcon={modalConfigProps?.showIcon}
        />
      </BaseModal.Header>
      <BaseModal.Content>
        {renderKey ? (
          <ContentRenderKey
            inputLabel={String(modalConfigProps?.inputLabel ?? "")}
            inputRef={inputRef}
            apiKeyValue={apiKeyValue}
            handleCopyClick={handleCopyClick}
            textCopied={textCopied}
            renderKey={renderKey}
          />
        ) : ENABLE_DATASTAX_LANGFLOW ? (
          <></>
        ) : (
          <FormKeyRender
            modalProps={modalConfigProps}
            apiKeyName={apiKeyName}
            inputRef={inputRef}
            setApiKeyName={setApiKeyName}
          />
        )}
      </BaseModal.Content>
      <BaseModal.Footer
        submit={{
          label: renderKey ? "完成" : (modalConfigProps?.buttonText ?? ""),
        }}
      />
    </BaseModal>
  );
}
