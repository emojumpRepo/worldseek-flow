import { MCPServerType } from "@/types/mcp";

/**
 * Extracts the first MCP server from a JSON string or object.
 * Supports:
 * 1. { mcpServers: { ... } }
 * 2. { ... } (object with server keys)
 * 3. a single server object
 * Returns: { name, server } or throws an error.
 */
export function extractFirstMcpServerFromJson(json: string | object): {
  name: string;
  server: Omit<MCPServerType, "name">;
} {
  let parsed: any = json;
  if (typeof json === "string") {
    try {
      parsed = JSON.parse(json);
    } catch (e) {
      throw new Error("无效的 JSON 格式。");
    }
  }

  let serverEntries: [string, Omit<MCPServerType, "name">][] = [];

  // Case 1: { mcpServers: { ... } }
  if (
    parsed &&
    typeof parsed === "object" &&
    parsed.mcpServers &&
    typeof parsed.mcpServers === "object"
  ) {
    serverEntries = Object.entries(parsed.mcpServers) as [
      string,
      Omit<MCPServerType, "name">,
    ][];
  }
  // Case 2: { ... } (object with server keys)
  else if (
    parsed &&
    typeof parsed === "object" &&
    Object.values(parsed).some(
      (v) =>
        v &&
        typeof v === "object" &&
        "command" in v &&
        Array.isArray((v as any).args),
    )
  ) {
    serverEntries = Object.entries(parsed).filter(
      ([, v]) =>
        v &&
        typeof v === "object" &&
        "command" in v &&
        Array.isArray((v as any).args),
    ) as [string, Omit<MCPServerType, "name">][];
  }
  // Case 3: single server object
  else if (
    parsed &&
    typeof parsed === "object" &&
    "command" in parsed &&
    Array.isArray((parsed as any).args)
  ) {
    serverEntries = [["server", parsed]];
  }

  if (serverEntries.length === 0) {
    throw new Error("未找到有效的 MCP 服务。");
  }
  const [name, server] = serverEntries[0];
  if (!server.command || !Array.isArray(server.args)) {
    throw new Error(
      "每个 MCP 服务必须有一个 'command' 和一个 'args' 数组。",
    );
  }
  return { name, server };
}

/**
 * Extracts all MCP servers from a JSON string or object.
 * Supports:
 * 1. { mcpServers: { ... } }
 * 2. { ... } (object with server keys)
 * 3. a single server object
 * Returns: Array<MCPServerType> or throws an error.
 */
export function extractMcpServersFromJson(
  json: string | object,
): MCPServerType[] {
  let parsed: any = json;
  if (typeof json === "string") {
    try {
      parsed = JSON.parse(json);
    } catch (e) {
      try {
        parsed = JSON.parse(`{${json}}`);
      } catch (e) {
        throw new Error("无效的 JSON 格式。");
      }
    }
  }

  let serverEntries: [string, any][] = [];

  // Case 1: { mcpServers: { ... } }
  if (
    parsed &&
    typeof parsed === "object" &&
    parsed.mcpServers &&
    typeof parsed.mcpServers === "object"
  ) {
    serverEntries = Object.entries(parsed.mcpServers);
  }
  // Case 2: { ... } (object with server keys)
  else if (
    parsed &&
    typeof parsed === "object" &&
    Object.values(parsed).some(
      (v) =>
        v &&
        typeof v === "object" &&
        "command" in v &&
        Array.isArray((v as any).args),
    )
  ) {
    serverEntries = Object.entries(parsed).filter(
      ([, v]) =>
        v &&
        typeof v === "object" &&
        "command" in v &&
        Array.isArray((v as any).args),
    );
  }
  // Case 3: single server object
  else if (
    parsed &&
    typeof parsed === "object" &&
    "command" in parsed &&
    Array.isArray((parsed as any).args)
  ) {
    serverEntries = [["server", parsed]];
  }

  if (serverEntries.length === 0) {
    throw new Error("未找到有效的 MCP 服务。");
  }
  // Validate and map all servers
  const validServers = serverEntries.filter(
    ([, server]) => server.command && Array.isArray(server.args),
  );
  if (validServers.length === 0) {
    throw new Error("未找到有效的 MCP 服务。");
  }
  return validServers.map(([name, server]) => ({
    name: name.slice(0, 30),
    command: server.command,
    args: server.args,
    env: server.env && typeof server.env === "object" ? server.env : {},
    url: server.url,
  }));
}
