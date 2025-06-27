from typing import Any
import logging

import httpx

# 设置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from langflow.custom.custom_component.component import Component
from langflow.field_typing.range_spec import RangeSpec
from langflow.io import (
    BoolInput,
    DropdownInput,
    IntInput,
    SliderInput,
    MessageTextInput,
    Output,
)

from langflow.services.database.models.config.crud import (
    get_config_value,
)
from langflow.services.database.service import DatabaseService
from langflow.services.deps import get_settings_service

from langflow.schema.data import Data
from langflow.schema.dotdict import dotdict
from langflow.schema.message import Message

# Define fields for each mode
MODE_FIELDS = {
    "URL": [
        "url_input",
        "method",
    ],
    "cURL": ["curl_input"],
}

# Fields that should always be visible
DEFAULT_FIELDS = ["mode"]

SEARCH_MODES = {
    '嵌入模式': 'embedding',
    '全文检索': 'fullTextRecall',
    '混合检索': 'mixedRecall',
}

# 全局变量存储知识库名称到ID的映射
GLOBAL_DATASET_NAME_TO_ID_MAP = {}


class KnowledgeBaseComponent(Component):
    display_name = "Knowledge Base"
    display_name_zh = "知识库"
    description = "Get possible answers from knowledge base."
    description_zh = "通过知识库获取可能的回答参考"
    icon = "Book"
    name = "KnowledgeBase"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 在初始化时输出一些日志到控制台，不使用组件日志系统
        print("=== KnowledgeBaseComponent 初始化 ===")

    inputs = [
        DropdownInput(
            name="searchMode",
            display_name="搜索模式",
            options=list(SEARCH_MODES.keys()),
            value="全文检索",
            info="选择要使用的搜索模式。",
            real_time_refresh=True,
        ),
        IntInput(
            name="limit",
            display_name="引用上限",
            value=20000,
            range_spec=RangeSpec(min=1, max=1000000, step=1),
            info="知识库检索结果最大token数量",
        ),
        SliderInput(
            name="similarity",
            display_name="检索相关度",
            value=0.1,
            info="检索结果与查询词的相似度",
            range_spec=RangeSpec(min=0, max=1, step=0.1),
            min_label="模糊",
            min_label_icon="palette",
            max_label="精准",
            max_label_icon="pencil-ruler",
        ),
        BoolInput(
            name="usingReRank",
            display_name="内容重排",
            info="是否使用内容重排，提高检索结果的准确性",
            value=True,
        ),
        BoolInput(
            name="datasetSearchUsingExtensionQuery",
            display_name="优化提问",
            info="是否使用优化提问，提高检索结果的准确性",
            value=True,
        ),
        DropdownInput(
            name="datasetIds",
            display_name="知识库选择",
            options=[],
            placeholder="请点击右侧刷新按钮加载知识库",
            value="",
            info="选择要使用的知识库。",
            refresh_button=True,
        ),
        MessageTextInput(
            name="text",
            display_name="问题输入",
        ),
    ]

    outputs = [
        Output(display_name="搜索结果", name="result", method="search_knowledge_base"),
    ]

    async def get_kb_config_value(self, key: str, default: str = None) -> str:
        """从配置表中获取配置值"""
        try:
            msg = f"尝试获取配置: {key}"
            print(msg)
            self.log(msg)
            
            # 获取设置服务
            settings_service = get_settings_service()
            msg = f"SettingsService 获取成功"
            print(msg)
            self.log(msg)
            
            db_service = DatabaseService(settings_service)
            msg = f"DatabaseService 创建成功"
            print(msg)
            self.log(msg)
            
            async with db_service.with_session() as session:
                msg = f"数据库会话创建成功，调用 get_config_value"
                print(msg)
                self.log(msg)
                
                value = await get_config_value(session, key, default)
                
                msg = f"配置值获取结果: key={key}, value={value}, default={default}"
                print(msg)
                self.log(msg)
                
                return value
        except Exception as e:
            msg = f"获取配置值失败 key={key}: {e}"
            print(msg)
            self.log(msg)
            import traceback
            msg = f"完整错误堆栈: {traceback.format_exc()}"
            print(msg)
            self.log(msg)
            return default

    def get_knowledge_base_list_sync(self) -> dict:
        """同步版本：获取知识库列表，返回名称列表和名称到ID的映射"""
        try:
            import httpx
            import asyncio
            
            # 在新线程中运行异步代码
            def run_async():
                return asyncio.run(self.get_knowledge_base_list())
            
            import threading
            result = {"options": []}
            exception = None
            
            def worker():
                nonlocal result, exception
                try:
                    result = asyncio.run(self.get_knowledge_base_list())
                except Exception as e:
                    exception = e
            
            thread = threading.Thread(target=worker)
            thread.start()
            thread.join(timeout=30)  # 30秒超时
            
            if exception:
                raise exception
            
            return result
            
        except Exception as e:
            msg = f"ERROR: Exception in get_knowledge_base_list_sync: {e}"
            print(msg)
            self.log(msg)
            return {"options": []}

    async def get_knowledge_base_list(self) -> dict:
        """获取知识库列表，返回名称列表和名称到ID的映射"""
        try:
            # 获取配置
            api_base_url = await self.get_kb_config_value("worldseek_kb_api_base_url", "http://uat.worldseek-ai.com:4000")
            api_key = await self.get_kb_config_value("worldseek_kb_api_key")
            
            # 同时使用 print 和 self.log 确保能看到输出
            msg = f"=== 知识库列表获取开始 ==="
            print(msg)
            self.log(msg)
            
            msg = f"API Base URL: {api_base_url}"
            print(msg)
            self.log(msg)
            
            msg = f"API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if api_key else 'None'}"
            print(msg)
            self.log(msg)
            
            if not api_key:
                msg = "ERROR: No API key found in configuration"
                print(msg)
                self.log(msg)
                return {"options": []}

            # 构建请求URL
            url = f"{api_base_url.rstrip('/')}/api/core/dataset/list?parentId="
            msg = f"Request URL: {url}"
            print(msg)
            self.log(msg)
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            msg = f"Request Headers: {headers}"
            print(msg)
            self.log(msg)

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=30)
                
                msg = f"Response Status: {response.status_code}"
                print(msg)
                self.log(msg)
                
                msg = f"Response Headers: {dict(response.headers)}"
                print(msg)
                self.log(msg)
                
                msg = f"Response Text: {response.text}"
                print(msg)
                self.log(msg)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log(f"Parsed JSON Data: {data}")
                    
                    # 根据API响应格式解析知识库列表
                    if isinstance(data, dict) and "data" in data:
                        datasets = data["data"]
                        self.log(f"Datasets from data field: {datasets}")
                    else:
                        datasets = data
                        self.log(f"Datasets direct: {datasets}")
                    
                    # 转换为下拉框选项格式，存储名称，并建立映射
                    options = []
                    name_to_id_map = {}
                    for i, dataset in enumerate(datasets):
                        if isinstance(dataset, dict):
                            # 获取ID和名称
                            dataset_id = str(dataset.get("_id", ""))
                            dataset_name = dataset.get("name", f"知识库 {dataset_id}")
                            
                            if dataset_id:  # 只有当ID不为空时才添加
                                options.append(dataset_name)  # 使用名称作为选项
                                name_to_id_map[dataset_name] = dataset_id  # 建立映射
                                print(f"知识库映射: {dataset_name} -> {dataset_id}")
                            else:
                                print(f"警告: 数据集 {dataset_name} 没有找到有效的ID字段")
                    
                    # 更新全局变量中的映射
                    global GLOBAL_DATASET_NAME_TO_ID_MAP
                    GLOBAL_DATASET_NAME_TO_ID_MAP = name_to_id_map
                    
                    self.log(f"Final options: {options}")
                    self.log(f"Name to ID mapping: {name_to_id_map}")
                    self.log(f"=== 知识库列表获取完成 ===")
                    
                    return {"options": options}
                else:
                    self.log(f"ERROR: Failed to get dataset list: {response.status_code}")
                    self.log(f"Error response: {response.text}")
                    return {"options": []}
                    
        except Exception as e:
            self.log(f"ERROR: Exception in get_knowledge_base_list: {e}")
            import traceback
            self.log(f"Full traceback: {traceback.format_exc()}")
            return {"options": []}

    async def get_dataset_id_by_name_async(self, dataset_name: str) -> str:
        """异步获取知识库ID，确保能获取到最新的映射"""
        try:
            # 每次都重新获取知识库列表来确保映射是最新的
            kb_data = await self.get_knowledge_base_list()
            
            # 从返回的数据中查找映射
            global GLOBAL_DATASET_NAME_TO_ID_MAP
            dataset_id = GLOBAL_DATASET_NAME_TO_ID_MAP.get(dataset_name, dataset_name)
            
            msg = f"异步映射知识库名称到ID: {dataset_name} -> {dataset_id}"
            print(msg)
            self.log(msg)
            
            return dataset_id
        except Exception as e:
            msg = f"异步获取数据集ID失败: {e}"
            print(msg)
            self.log(msg)
            return dataset_name

    def get_dataset_id_by_name(self, dataset_name: str) -> str:
        """根据知识库名称获取对应的ID"""
        global GLOBAL_DATASET_NAME_TO_ID_MAP
        
        msg = f"当前全局映射表内容: {GLOBAL_DATASET_NAME_TO_ID_MAP}"
        print(msg)
        self.log(msg)
        
        # 如果全局映射为空，重新获取
        if not GLOBAL_DATASET_NAME_TO_ID_MAP:
            msg = "全局映射表为空，重新获取知识库列表"
            print(msg)
            self.log(msg)
            
            try:
                kb_data = self.get_knowledge_base_list_sync()
                msg = f"重新获取后，全局映射表内容: {GLOBAL_DATASET_NAME_TO_ID_MAP}"
                print(msg)
                self.log(msg)
            except Exception as e:
                msg = f"重新获取知识库列表失败: {e}"
                print(msg)
                self.log(msg)
        
        dataset_id = GLOBAL_DATASET_NAME_TO_ID_MAP.get(dataset_name, dataset_name)
        msg = f"映射知识库名称到ID: {dataset_name} -> {dataset_id}"
        print(msg)
        self.log(msg)
        
        return dataset_id

    async def search_knowledge_base(self) -> Message:
        """执行知识库搜索"""
        try:
            # 获取配置
            api_base_url = await self.get_kb_config_value("worldseek_kb_api_base_url", "http://uat.worldseek-ai.com:4000")
            api_key = await self.get_kb_config_value("worldseek_kb_api_key")
            
            if not api_key:
                return Message(text="❌ 未找到API密钥配置，请在设置页面配置worldseek_kb_api_key")

            if not self.datasetIds or self.datasetIds in ["", "请点击刷新按钮加载知识库", "无可用知识库，请检查配置", "加载失败，请检查配置"]:
                return Message(text="❌ 请先点击刷新按钮加载知识库，然后选择一个知识库")

            if not self.text:
                return Message(text="❌ 请输入搜索文本")

            # 构建搜索请求
            search_url = f"{api_base_url.rstrip('/')}/api/core/dataset/searchTest"
            
            # 获取搜索模式对应的值
            search_mode_value = SEARCH_MODES.get(self.searchMode, "mixedRecall")
            
            # 根据知识库名称获取对应的ID
            dataset_id = await self.get_dataset_id_by_name_async(self.datasetIds)
            
            # 调试信息：检查映射结果
            msg = f"🔍 映射结果检查: 知识库名称='{self.datasetIds}' -> ID='{dataset_id}'"
            print(msg)
            self.log(msg)
            
            request_data = {
                "datasetId": dataset_id,
                "text": self.text,
                "limit": max(self.limit, 1),
                "similarity": max(0, min(self.similarity, 1)),  # 限制在0-1之间
                "searchMode": search_mode_value,
                "usingReRank": self.usingReRank,
                "datasetSearchUsingExtensionQuery": self.datasetSearchUsingExtensionQuery,
                "datasetSearchExtensionModel": getattr(self, 'datasetSearchExtensionModel', 'gpt-4o-mini'),
                "datasetSearchExtensionBg": getattr(self, 'datasetSearchExtensionBg', '')
            }

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # 详细的调试输出
            msg = f"🌐 完整请求信息:"
            print(msg)
            self.log(msg)
            msg = f"   URL: {search_url}"
            print(msg)
            self.log(msg)
            msg = f"   Request Data: {request_data}"
            print(msg)
            self.log(msg)

            # 配置HTTP客户端
            timeout_config = httpx.Timeout(30.0, connect=10.0)
            limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
            
            async with httpx.AsyncClient(timeout=timeout_config, limits=limits) as client:
                response = await client.post(
                    search_url, 
                    json=request_data, 
                    headers=headers
                )
                
                msg = f"📡 HTTP响应状态: {response.status_code}"
                print(msg)
                self.log(msg)
                
                if response.status_code == 200:
                    result_data = response.json()
                    msg = f"📡 API原始响应数据长度: {len(str(result_data))}"
                    print(msg)
                    self.log(msg)
                    
                    # 根据FastGPT API响应格式解析结果
                    search_results = []
                    if isinstance(result_data, dict):
                        if result_data.get("code") == 200:
                            # FastGPT返回的数据在data.list中
                            api_data = result_data.get("data", {})
                            if isinstance(api_data, dict) and "list" in api_data:
                                search_results = api_data["list"]
                            else:
                                search_results = result_data.get("data", [])
                        else:
                            return Message(text=f"API返回错误: {result_data.get('message', '未知错误')}")
                    else:
                        search_results = result_data if isinstance(result_data, list) else []

                    msg = f"🔍 解析后的搜索结果数量: {len(search_results)}"
                    print(msg)
                    self.log(msg)

                    # 格式化搜索结果 - 显示所有结果，不只是部分
                    formatted_results = []
                    for idx, item in enumerate(search_results):
                        if isinstance(item, dict):
                            # 处理score字段，可能是数组格式
                            score_value = 0
                            if "score" in item:
                                score_data = item["score"]
                                if isinstance(score_data, list) and len(score_data) > 0:
                                    score_value = score_data[0].get("value", 0)
                                elif isinstance(score_data, (int, float)):
                                    score_value = score_data
                            
                            formatted_result = {
                                "id": item.get("id", ""),
                                "question": item.get("q", ""),
                                "answer": item.get("a", ""),
                                "score": score_value,
                                "datasetId": item.get("datasetId", ""),
                                "collectionId": item.get("collectionId", ""),
                                "sourceName": item.get("sourceName", ""),
                                "sourceId": item.get("sourceId", ""),
                            }
                            formatted_results.append(formatted_result)
                            
                            # 记录每个结果的处理情况
                            msg = f"   处理结果 {idx + 1}: ID={formatted_result['id']}, Score={formatted_result['score']:.3f}"
                            print(msg)
                            self.log(msg)
                            
                    msg = f"🔍 最终格式化后的结果数量: {len(formatted_results)}"
                    print(msg)
                    self.log(msg)

                    # 构造返回的文本内容 - 显示所有结果，无字数限制
                    if formatted_results:
                        result_text = f"🔍 从知识库「{self.datasetIds}」中找到 {len(formatted_results)} 条相关结果:\n\n"
                        
                        msg = f"开始构造结果文本，总计 {len(formatted_results)} 条结果，无字数限制"
                        print(msg)
                        self.log(msg)
                        
                        for i, result in enumerate(formatted_results, 1):
                            msg = f"正在处理第 {i} 条结果，ID: {result['id']}"
                            print(msg)
                            self.log(msg)
                            
                            result_text += f"📋 结果 {i} (相关度: {result['score']:.3f})\n"
                            
                            if result['question']:
                                # 显示完整问题内容，不截断
                                result_text += f"❓ 问题: {result['question']}\n"
                            
                            if result['answer'] and result['answer'].strip():
                                # 显示完整答案内容，不截断
                                result_text += f"✅ 答案: {result['answer']}\n"
                            
                            if result['sourceName']:
                                result_text += f"📄 来源: {result['sourceName']}\n"
                            
                            result_text += "\n" + "─" * 50 + "\n\n"
                            
                            msg = f"第 {i} 条结果处理完成"
                            print(msg)
                            self.log(msg)
                        
                        final_length = len(result_text)
                        msg = f"最终结果文本长度: {final_length} 字符，包含所有 {len(formatted_results)} 条结果"
                        print(msg)
                        self.log(msg)
                    else:
                        result_text = f"❌ 在知识库「{self.datasetIds}」中未找到相关结果"

                    return Message(text=result_text)
                else:
                    error_message = f"❌ 搜索请求失败: HTTP {response.status_code}"
                    try:
                        error_detail = response.json()
                        if isinstance(error_detail, dict) and "message" in error_detail:
                            error_message += f" - {error_detail['message']}"
                    except:
                        error_message += f" - {response.text}"
                    
                    return Message(text=error_message)
                    
        except httpx.TimeoutException:
            return Message(text="❌ 请求超时，请检查网络连接或稍后重试")
        except httpx.ConnectError:
            return Message(text="❌ 无法连接到知识库服务器，请检查网络连接")
        except Exception as e:
            msg = f"搜索过程中发生错误: {e}"
            print(msg)
            self.log(msg)
            import traceback
            msg = f"完整错误堆栈: {traceback.format_exc()}"
            print(msg)
            self.log(msg)
            return Message(text=f"❌ 搜索过程中发生错误: {str(e)}")

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        """Update the build config and refresh knowledge base list if needed."""
        msg = f"=== update_build_config called ==="
        print(msg)
        self.log(msg)
        
        msg = f"field_name: {field_name}, field_value: {field_value}"
        print(msg)
        self.log(msg)
        
        # 当点击刷新按钮时，重新加载知识库列表
        if field_name == "datasetIds" or field_name is None:
            msg = "Refreshing knowledge base list..."
            print(msg)
            self.log(msg)
            
            try:
                # 同步调用获取知识库列表
                kb_data = self.get_knowledge_base_list_sync()
                
                msg = f"Retrieved kb_data: {kb_data}"
                print(msg)
                self.log(msg)
                
                # 更新下拉框选项
                if "datasetIds" in build_config:
                    if kb_data["options"]:
                        build_config["datasetIds"]["options"] = kb_data["options"]
                        msg = f"Updated options: {build_config['datasetIds']['options']}"
                        print(msg)
                        self.log(msg)
                    else:
                        build_config["datasetIds"]["options"] = ["无可用知识库，请检查配置"]
                        msg = "No options found, set placeholder message"
                        print(msg)
                        self.log(msg)
                        
            except Exception as e:
                msg = f"ERROR: Failed to refresh knowledge base list: {e}"
                print(msg)
                self.log(msg)
                import traceback
                msg = f"Full traceback: {traceback.format_exc()}"
                print(msg)
                self.log(msg)
                if "datasetIds" in build_config:
                    build_config["datasetIds"]["options"] = ["加载失败，请检查配置"]
        
        msg = f"=== update_build_config finished ==="
        print(msg)
        self.log(msg)
        return build_config
    
    def build_config(self):
        """Build the component configuration with knowledge base options."""
        # 获取初始的构建配置
        build_config = super().build_config()
        
        # 直接加载知识库列表
        try:
            kb_data = self.get_knowledge_base_list_sync()
            if "datasetIds" in build_config and kb_data["options"]:
                build_config["datasetIds"]["options"] = kb_data["options"]
        except Exception as e:
            msg = f"Failed to load knowledge base list in build_config: {e}"
            print(msg)
            self.log(msg)
            
        return build_config
