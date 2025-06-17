import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import ToolsComponent from "@/components/core/parameterRenderComponent/components/ToolsComponent";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs-button";
import {
  DEFAULT_FOLDER,
  DEFAULT_FOLDER_DEPRECATED,
  MAX_MCP_SERVER_NAME_LENGTH,
} from "@/constants/constants";
import { createApiKey } from "@/controllers/API";
import {
  useGetFlowsMCP,
  usePatchFlowsMCP,
} from "@/controllers/API/queries/mcp";
import { useGetInstalledMCP } from "@/controllers/API/queries/mcp/use-get-installed-mcp";
import { usePatchInstallMCP } from "@/controllers/API/queries/mcp/use-patch-install-mcp";
import useTheme from "@/customization/hooks/use-custom-theme";
import { customGetMCPUrl } from "@/customization/utils/custom-mcp-url";
import { useIsLocalConnection } from "@/hooks/useIsLocalConnection";
import useAlertStore from "@/stores/alertStore";
import useAuthStore from "@/stores/authStore";
import { useFolderStore } from "@/stores/foldersStore";
import { MCPSettingsType } from "@/types/mcp";
import { parseString } from "@/utils/stringManipulation";
import { cn, getOS } from "@/utils/utils";
import { memo, ReactNode, useCallback, useState } from "react";
import { useParams } from "react-router-dom";
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";

// Define interface for MemoizedCodeTag props
interface MemoizedCodeTagProps {
  children: ReactNode;
  isCopied: boolean;
  copyToClipboard: () => void;
  isAutoLogin: boolean | null;
  apiKey: string;
  isGeneratingApiKey: boolean;
  generateApiKey: () => void;
}

// Memoized CodeTag to prevent re-renders when parent components re-render
const MemoizedCodeTag = memo(
  ({
    children,
    isCopied,
    copyToClipboard,
    isAutoLogin,
    apiKey,
    isGeneratingApiKey,
    generateApiKey,
  }: MemoizedCodeTagProps) => (
    <div className="relative bg-background text-[13px]">
      <div className="absolute right-4 top-4 flex items-center gap-6">
        {!isAutoLogin && (
          <Button
            unstyled
            className="flex items-center gap-2 font-sans text-muted-foreground hover:text-foreground"
            disabled={apiKey !== ""}
            loading={isGeneratingApiKey}
            onClick={generateApiKey}
          >
            <ForwardedIconComponent
              name={"key"}
              className="h-4 w-4"
              aria-hidden="true"
            />
            <span>
              {apiKey === "" ? "生成 API 密钥" : "API 密钥已生成"}
            </span>
          </Button>
        )}
        <Button
          unstyled
          size="icon"
          className={cn("h-4 w-4 text-muted-foreground hover:text-foreground")}
          onClick={copyToClipboard}
        >
          <ForwardedIconComponent
            name={isCopied ? "check" : "copy"}
            className="h-4 w-4"
            aria-hidden="true"
          />
        </Button>
      </div>
      <div className="overflow-x-auto p-4">
        <span>{children}</span>
      </div>
    </div>
  ),
);
MemoizedCodeTag.displayName = "MemoizedCodeTag";

const autoInstallers = [
  {
    name: "cursor",
    title: "Cursor",
    icon: "Cursor",
  },
  {
    name: "claude",
    title: "Claude",
    icon: "Claude",
  },
];

const operatingSystemTabs = [
  {
    name: "macoslinux",
    title: "macOS/Linux",
    icon: "FaApple",
  },
  {
    name: "windows",
    title: "Windows",
    icon: "FaWindows",
  },
  {
    name: "wsl",
    title: "WSL",
    icon: "FaLinux",
  },
];

const McpServerTab = ({ folderName }: { folderName: string }) => {
  const isDarkMode = useTheme().dark;
  const { folderId } = useParams();
  const myCollectionId = useFolderStore((state) => state.myCollectionId);
  const projectId = folderId ?? myCollectionId ?? "";
  const [isCopied, setIsCopied] = useState(false);
  const [apiKey, setApiKey] = useState<string>("");
  const [isGeneratingApiKey, setIsGeneratingApiKey] = useState(false);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  const { data: flowsMCP } = useGetFlowsMCP({ projectId });
  const { mutate: patchFlowsMCP } = usePatchFlowsMCP({ project_id: projectId });
  const { mutate: patchInstallMCP } = usePatchInstallMCP({
    project_id: projectId,
  });

  const { data: installedMCP } = useGetInstalledMCP({ projectId });

  const [selectedPlatform, setSelectedPlatform] = useState(
    operatingSystemTabs.find((tab) => tab.name.includes(getOS() || "windows"))
      ?.name,
  );

  const isAutoLogin = useAuthStore((state) => state.autoLogin);

  // Check if the current connection is local
  const isLocalConnection = useIsLocalConnection();

  const [selectedMode, setSelectedMode] = useState(
    isLocalConnection ? "Auto install" : "JSON",
  );

  const handleOnNewValue = (value) => {
    const flowsMCPData: MCPSettingsType[] = value.value.map((flow) => ({
      id: flow.id,
      action_name: flow.name,
      action_description: flow.description,
      mcp_enabled: flow.status,
    }));
    patchFlowsMCP(flowsMCPData);
  };

  const flowsMCPData = flowsMCP?.map((flow) => ({
    id: flow.id,
    name: flow.action_name,
    description: flow.action_description,
    display_name: flow.name,
    display_description: flow.description,
    status: flow.mcp_enabled,
    tags: [flow.name],
  }));

  const syntaxHighlighterStyle = {
    "hljs-string": {
      color: isDarkMode ? "hsla(158, 64%, 52%, 1)" : "#059669", // Accent Green
    },
    "hljs-attr": {
      color: isDarkMode ? "hsla(329, 86%, 70%, 1)" : "#DB2777", // Accent Pink
    },
  };

  const apiUrl = customGetMCPUrl(projectId);

  const MCP_SERVER_JSON = `{
  "mcpServers": {
    "lf-${parseString(folderName === DEFAULT_FOLDER_DEPRECATED ? DEFAULT_FOLDER : (folderName ?? "project"), ["snake_case", "no_blank", "lowercase"]).slice(0, MAX_MCP_SERVER_NAME_LENGTH - 4)}": {
      "command": "${selectedPlatform === "windows" ? "cmd" : selectedPlatform === "wsl" ? "wsl" : "uvx"}",
      "args": [
        ${
          selectedPlatform === `windows`
            ? `"/c",
        "uvx",
        `
            : selectedPlatform === "wsl"
              ? `"uvx",
        `
              : ""
        }"mcp-proxy",${
          isAutoLogin
            ? ""
            : `
        "--headers",
        "x-api-key",
        "${apiKey || "YOUR_API_KEY"}",`
        }
        "${apiUrl}"
      ]
    }
  }
}`;

  const MCP_SERVER_TUTORIAL_LINK =
    "https://docs.langflow.org/mcp-server#connect-clients-to-use-the-servers-actions";

  const MCP_SERVER_DEPLOY_TUTORIAL_LINK =
    "https://docs.langflow.org/mcp-server#deploy-your-server-externally";

  const copyToClipboard = useCallback(() => {
    navigator.clipboard
      .writeText(MCP_SERVER_JSON)
      .then(() => {
        setIsCopied(true);
        setTimeout(() => {
          setIsCopied(false);
        }, 1000);
      })
      .catch((err) => console.error("Failed to copy text: ", err));
  }, [MCP_SERVER_JSON]);

  const generateApiKey = useCallback(() => {
    setIsGeneratingApiKey(true);
    createApiKey(`MCP Server ${folderName}`)
      .then((res) => {
        setApiKey(res["api_key"]);
      })
      .catch((err) => {})
      .finally(() => {
        setIsGeneratingApiKey(false);
      });
  }, [folderName]);

  const [loadingMCP, setLoadingMCP] = useState<string[]>([]);

  return (
    <div>
      <div className="pb-2 text-sm font-medium" data-testid="mcp-server-title">
        MCP 服务
      </div>
      <div className="pb-4 text-mmd text-muted-foreground">
        将您的项目中的工作流作为 MCP 服务器中的操作。了解更多信息，请参阅
        <a
          className="text-accent-pink-foreground"
          href={MCP_SERVER_DEPLOY_TUTORIAL_LINK}
          target="_blank"
          rel="noreferrer"
        >
        {" "}MCP 服务器指南。
        </a>
      </div>
      <div className="flex flex-col justify-between gap-8 xl:flex-row">
        <div className="w-full xl:w-2/5">
          <div className="flex flex-row justify-between">
            <ShadTooltip
              content="您项目中的工作流可以作为 MCP 服务器中的可调用操作。"
              side="right"
            >
              <div className="flex items-center text-mmd font-medium hover:cursor-help">
                工作流/操作
                <ForwardedIconComponent
                  name="info"
                  className="ml-1.5 h-4 w-4 text-muted-foreground"
                  aria-hidden="true"
                />
              </div>
            </ShadTooltip>
          </div>
          <div className="flex flex-row flex-wrap gap-2 pt-2">
            <ToolsComponent
              value={flowsMCPData}
              title="MCP 服务操作"
              description="选择要添加到此服务器的操作"
              handleOnNewValue={handleOnNewValue}
              id="mcp-server-tools"
              button_description="编辑操作"
              editNode={false}
              isAction
              disabled={false}
            />
          </div>
        </div>
        <div className="flex flex-1 flex-col gap-4 overflow-hidden">
          <div className="flex flex-col">
            <div className="flex flex-row justify-start border-b border-border">
              {[{ name: "Auto install" }, { name: "JSON" }].map(
                (item, index) => (
                  <Button
                    unstyled
                    key={item.name}
                    className={`flex h-6 flex-row items-end gap-2 text-nowrap border-b-2 border-border border-b-transparent !py-1 font-medium ${
                      selectedMode === item.name
                        ? "border-b-2 border-black dark:border-b-white"
                        : "text-muted-foreground hover:text-foreground"
                    } px-3 py-2 text-[13px]`}
                    onClick={() => setSelectedMode(item.name)}
                  >
                    <span>{item.name === "Auto install" ? "一键安装" : "JSON"}</span>
                  </Button>
                ),
              )}
            </div>
          </div>
          {selectedMode === "JSON" && (
            <>
              <div className="flex flex-col gap-4">
                <Tabs
                  value={selectedPlatform}
                  onValueChange={setSelectedPlatform}
                >
                  <TabsList>
                    {operatingSystemTabs.map((tab, index) => (
                      <TabsTrigger
                        className="flex items-center gap-2"
                        key={index}
                        value={tab.name}
                      >
                        <ForwardedIconComponent
                          name={tab.icon}
                          aria-hidden="true"
                        />
                        {tab.title}
                      </TabsTrigger>
                    ))}
                  </TabsList>
                </Tabs>
                <div className="overflow-hidden rounded-lg border border-border">
                  <SyntaxHighlighter
                    style={syntaxHighlighterStyle}
                    CodeTag={({ children }) => (
                      <MemoizedCodeTag
                        isCopied={isCopied}
                        copyToClipboard={copyToClipboard}
                        isAutoLogin={isAutoLogin}
                        apiKey={apiKey}
                        isGeneratingApiKey={isGeneratingApiKey}
                        generateApiKey={generateApiKey}
                      >
                        {children}
                      </MemoizedCodeTag>
                    )}
                    language="json"
                  >
                    {MCP_SERVER_JSON}
                  </SyntaxHighlighter>
                </div>
              </div>
              <div className="px-2 text-mmd text-muted-foreground">
                将此配置添加到您选择的客户端。需要帮助？请参阅
                <a
                  href={MCP_SERVER_TUTORIAL_LINK}
                  target="_blank"
                  rel="noreferrer"
                  className="text-accent-pink-foreground"
                >
                  设置指南
                </a>
                .
              </div>
            </>
          )}
          {selectedMode === "Auto install" && (
            <div className="flex flex-col gap-1">
              {!isLocalConnection && (
                <div className="mb-2 rounded-md bg-amber-50 px-3 py-2 text-sm text-amber-800 dark:bg-amber-950 dark:text-amber-200">
                  <div className="flex items-center gap-3">
                    <ForwardedIconComponent
                      name="AlertTriangle"
                      className="h-4 w-4 shrink-0"
                    />
                    <span>
                      一键安装已禁用，因为 WorldSeek Agent 服务器未在您的本地机器上运行。使用 JSON 选项卡手动配置您的客户端。
                    </span>
                  </div>
                </div>
              )}
              {autoInstallers.map((installer) => (
                <Button
                  variant="ghost"
                  className="flex items-center justify-between disabled:text-foreground disabled:opacity-50"
                  disabled={
                    installedMCP?.includes(installer.name) ||
                    loadingMCP.includes(installer.name) ||
                    !isLocalConnection
                  }
                  onClick={() => {
                    setLoadingMCP([...loadingMCP, installer.name]);
                    patchInstallMCP(
                      {
                        client: installer.name,
                      },
                      {
                        onSuccess: () => {
                          setSuccessData({
                            title: `MCP 服务已成功安装在 ${installer.title} 上`,
                          });
                          setLoadingMCP(
                            loadingMCP.filter(
                              (name) => name !== installer.name,
                            ),
                          );
                        },
                        onError: (e) => {
                          setErrorData({
                            title: `在 ${installer.title} 上安装 MCP 服务失败`,
                            list: [e.message],
                          });
                          setLoadingMCP(
                            loadingMCP.filter(
                              (name) => name !== installer.name,
                            ),
                          );
                        },
                      },
                    );
                  }}
                >
                  <div className="flex items-center gap-4 text-sm font-medium">
                    <ForwardedIconComponent
                      name={installer.icon}
                      className={cn("h-5 w-5")}
                      aria-hidden="true"
                    />
                    {installer.title}
                  </div>

                  <ForwardedIconComponent
                    name={
                      installedMCP?.includes(installer.name)
                        ? "Check"
                        : loadingMCP.includes(installer.name)
                          ? "Loader2"
                          : "Plus"
                    }
                    className={cn(
                      "h-4 w-4",
                      loadingMCP.includes(installer.name) && "animate-spin",
                    )}
                  />
                </Button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default McpServerTab;
