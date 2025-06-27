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
            # 获取设置服务
            settings_service = get_settings_service()
            db_service = DatabaseService(settings_service)
            
            async with db_service.with_session() as session:
                value = await get_config_value(session, key, default)
                return value
        except Exception as e:
            msg = f"获取配置值失败 key={key}: {e}"
            print(msg)
            self.log(msg)
            return default

    def get_knowledge_base_list_sync(self) -> dict:
        """同步版本：获取知识库列表，返回名称列表和名称到ID的映射"""
        try:
            import httpx
            import asyncio
            
            # 在新线程中运行异步代码
            result = {"options": []}
            exception = None
            
            def worker():
                nonlocal result, exception
                try:
                    result = asyncio.run(self.get_knowledge_base_list())
                except Exception as e:
                    exception = e
            
            import threading
            thread = threading.Thread(target=worker)
            thread.start()
            thread.join(timeout=30)  # 30秒超时
            
            if exception:
                raise exception
            
            return result
            
        except Exception as e:
            msg = f"同步获取知识库列表失败: {e}"
            print(msg)
            self.log(msg)
            return {"options": []}

    async def get_knowledge_base_list(self) -> dict:
        """获取知识库列表，返回名称列表和名称到ID的映射"""
        try:
            # 获取配置
            api_base_url = await self.get_kb_config_value("worldseek_kb_api_base_url", "http://uat.worldseek-ai.com:4000")
            api_key = await self.get_kb_config_value("worldseek_kb_api_key")
            
            if not api_key:
                msg = "ERROR: 未找到API密钥配置"
                print(msg)
                self.log(msg)
                return {"options": []}

            # 构建请求URL
            url = f"{api_base_url.rstrip('/')}/api/core/dataset/list?parentId="
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 根据API响应格式解析知识库列表
                    if isinstance(data, dict) and "data" in data:
                        datasets = data["data"]
                    else:
                        datasets = data
                    
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
                            else:
                                print(f"警告: 数据集 {dataset_name} 没有找到有效的ID字段")
                    
                    # 更新全局变量中的映射
                    global GLOBAL_DATASET_NAME_TO_ID_MAP
                    GLOBAL_DATASET_NAME_TO_ID_MAP = name_to_id_map
                    
                    msg = f"成功获取 {len(options)} 个知识库"
                    print(msg)
                    self.log(msg)
                    
                    return {"options": options}
                else:
                    msg = f"获取知识库列表失败: HTTP {response.status_code}"
                    print(msg)
                    self.log(msg)
                    return {"options": []}
                    
        except Exception as e:
            msg = f"知识库列表获取异常: {e}"
            print(msg)
            self.log(msg)
            return {"options": []}

    async def get_dataset_id_by_name_async(self, dataset_name: str) -> str:
        """异步获取知识库ID，确保能获取到最新的映射"""
        try:
            # 每次都重新获取知识库列表来确保映射是最新的
            kb_data = await self.get_knowledge_base_list()
            
            # 从返回的数据中查找映射
            global GLOBAL_DATASET_NAME_TO_ID_MAP
            dataset_id = GLOBAL_DATASET_NAME_TO_ID_MAP.get(dataset_name, dataset_name)
            
            return dataset_id
        except Exception as e:
            msg = f"异步获取数据集ID失败: {e}"
            print(msg)
            self.log(msg)
            return dataset_name

    def get_dataset_id_by_name(self, dataset_name: str) -> str:
        """根据知识库名称获取对应的ID"""
        global GLOBAL_DATASET_NAME_TO_ID_MAP
        
        # 如果全局映射为空，重新获取
        if not GLOBAL_DATASET_NAME_TO_ID_MAP:
            try:
                kb_data = self.get_knowledge_base_list_sync()
            except Exception as e:
                msg = f"重新获取知识库列表失败: {e}"
                print(msg)
                self.log(msg)
        
        dataset_id = GLOBAL_DATASET_NAME_TO_ID_MAP.get(dataset_name, dataset_name)
        
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

            # 配置HTTP客户端
            timeout_config = httpx.Timeout(30.0, connect=10.0)
            limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
            
            async with httpx.AsyncClient(timeout=timeout_config, limits=limits) as client:
                response = await client.post(
                    search_url, 
                    json=request_data, 
                    headers=headers
                )
                
                if response.status_code == 200:
                    result_data = response.json()
                    
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

                    msg = f"知识库搜索完成: 找到 {len(search_results)} 条结果"
                    print(msg)
                    self.log(msg)

                    # 格式化搜索结果
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

                    # 构造返回的文本内容
                    if formatted_results:
                        result_text = f"🔍 从知识库「{self.datasetIds}」中找到 {len(formatted_results)} 条相关结果:\n\n"
                        
                        for i, result in enumerate(formatted_results, 1):
                            result_text += f"📋 结果 {i} (相关度: {result['score']:.3f})\n"
                            
                            if result['question']:
                                result_text += f"❓ 问题: {result['question']}\n"
                            
                            if result['answer'] and result['answer'].strip():
                                result_text += f"✅ 答案: {result['answer']}\n"
                            
                            if result['sourceName']:
                                result_text += f"📄 来源: {result['sourceName']}\n"
                            
                            result_text += "\n" + "─" * 50 + "\n\n"
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
            return Message(text=f"❌ 搜索过程中发生错误: {str(e)}")

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        """Update the build config and refresh knowledge base list if needed."""
        
        # 当点击刷新按钮时，重新加载知识库列表
        if field_name == "datasetIds" or field_name is None:
            try:
                # 同步调用获取知识库列表
                kb_data = self.get_knowledge_base_list_sync()
                
                # 更新下拉框选项
                if "datasetIds" in build_config:
                    if kb_data["options"]:
                        build_config["datasetIds"]["options"] = kb_data["options"]
                        msg = f"知识库刷新成功: 加载了 {len(kb_data['options'])} 个选项"
                        print(msg)
                        self.log(msg)
                    else:
                        build_config["datasetIds"]["options"] = ["无可用知识库，请检查配置"]
                        
            except Exception as e:
                msg = f"知识库刷新失败: {e}"
                print(msg)
                self.log(msg)
                if "datasetIds" in build_config:
                    build_config["datasetIds"]["options"] = ["加载失败，请检查配置"]
        
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
            msg = f"构建配置时加载知识库列表失败: {e}"
            print(msg)
            self.log(msg)
            
        return build_config
