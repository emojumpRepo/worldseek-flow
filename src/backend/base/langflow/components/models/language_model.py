from typing import Any
import asyncio

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from langflow.base.models.anthropic_constants import ANTHROPIC_MODELS
from langflow.base.models.google_generative_ai_constants import GOOGLE_GENERATIVE_AI_MODELS
from langflow.base.models.model import LCModelComponent
from langflow.base.models.openai_constants import OPENAI_MODEL_NAMES
from langflow.field_typing import LanguageModel
from langflow.field_typing.range_spec import RangeSpec
from langflow.inputs.inputs import BoolInput
from langflow.io import DropdownInput, MessageInput, MultilineInput, SecretStrInput, SliderInput
from langflow.schema.dotdict import dotdict


def get_worldseek_models_sync() -> list[str]:
    """同步方式获取WorldSeek模型名称列表"""
    try:
        from langflow.services.deps import get_db_service
        from langflow.services.database.models.model.crud import get_models
        import threading
        import queue
        
        db_service = get_db_service()
        
        # 使用线程来避免事件循环冲突
        result_queue = queue.Queue()
        
        def run_async():
            async def _get_models():
                try:
                    async with db_service.with_session() as session:
                        models = await get_models(session, skip=0, limit=1000)
                        return [model.name for model in models if model.name]
                except Exception as e:
                    # print(f"数据库查询错误: {e}")
                    return []
            
            try:
                # 在新线程中创建新的事件循环
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(_get_models())
                result_queue.put(result)
            except Exception as e:
                # print(f"异步执行错误: {e}")
                result_queue.put([])
            finally:
                loop.close()
        
        # 在新线程中运行异步代码
        thread = threading.Thread(target=run_async)
        thread.start()
        thread.join(timeout=5)  # 5秒超时
        
        if thread.is_alive():
            # print("获取模型列表超时")
            return []
        
        try:
            return result_queue.get_nowait()
        except queue.Empty:
            return []
            
    except Exception as e:
        # print(f"获取WorldSeek模型列表失败: {e}")
        return []


def get_worldseek_model_config_sync(model_name: str) -> dict:
    """根据模型名称获取模型配置"""
    try:
        from langflow.services.deps import get_db_service
        from langflow.services.database.models.model.crud import get_model_by_name
        import threading
        import queue

        db_service = get_db_service()
        
        # 使用线程来避免事件循环冲突
        result_queue = queue.Queue()
        
        def run_async():
            async def _get_model_config():
                try:
                    async with db_service.with_session() as session:
                        model = await get_model_by_name(session, model_name)
                        if model:
                            return {
                                "id": model.id,
                                "name": model.name,
                                "model_id": getattr(model, 'model_id', ''),
                                "api_path": model.api_path,
                                "api_key": model.api_key
                            }
                        return {}
                except Exception as e:
                    # print(f"数据库查询错误: {e}")
                    return {}
            
            try:
                # 在新线程中创建新的事件循环
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(_get_model_config())
                result_queue.put(result)
            except Exception as e:
                # print(f"异步执行错误: {e}")
                result_queue.put({})
            finally:
                loop.close()
        
        # 在新线程中运行异步代码
        thread = threading.Thread(target=run_async)
        thread.start()
        thread.join(timeout=5)  # 5秒超时
        
        if thread.is_alive():
            # print("获取模型配置超时")
            return {}
        
        try:
            return result_queue.get_nowait()
        except queue.Empty:
            return {}
            
    except Exception as e:
        # print(f"获取WorldSeek模型配置失败: {e}")
        return {}


class LanguageModelComponent(LCModelComponent):
    display_name = "Language Model"
    display_name_zh = "语言模型"
    description = "Runs a language model given a specified provider. "
    description_zh = "使用指定的模型提供者运行语言模型。"
    icon = "brain-circuit"
    category = "models"
    priority = 0  # Set priority to 0 to make it appear first

    inputs = [
        DropdownInput(
            name="provider",
            display_name="模型提供商",
            options=["OpenAI", "Anthropic", "Google", "WorldSeek API"],
            value="OpenAI",
            info="选择模型提供商",
            real_time_refresh=True,
            options_metadata=[{"icon": "OpenAI"}, {"icon": "Anthropic"}, {"icon": "GoogleGenerativeAI"}, {"icon": "WorldSeek"}],
        ),
        DropdownInput(
            name="model_name",
            display_name="模型名称",
            options=OPENAI_MODEL_NAMES,
            value=OPENAI_MODEL_NAMES[0],
            info="选择要使用的模型",
            real_time_refresh=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="API密钥",
            info="模型提供商的API密钥",
            required=False,
            show=True,
            real_time_refresh=True,
        ),
        MessageInput(
            name="input_value",
            display_name="输入",
            info="要发送给模型的输入文本",
        ),
        MultilineInput(
            name="system_message",
            display_name="系统消息",
            info="帮助设置助手行为的系统消息",
            advanced=True,
        ),
        BoolInput(
            name="stream",
            display_name="流式输出",
            info="是否流式输出响应",
            value=False,
            advanced=True,
        ),
        SliderInput(
            name="temperature",
            display_name="温度",
            value=0.1,
            info="控制响应的随机性",
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
    ]

    def build_model(self) -> LanguageModel:
        provider = self.provider
        model_name = self.model_name
        temperature = self.temperature
        stream = self.stream

        if provider == "OpenAI":
            if not self.api_key:
                msg = "OpenAI API Key 是使用OpenAI提供商时必需的"
                raise ValueError(msg)
            return ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                streaming=stream,
                openai_api_key=self.api_key,
            )
        if provider == "Anthropic":
            if not self.api_key:
                msg = "Anthropic API Key 是使用Anthropic提供商时必需的"
                raise ValueError(msg)
            return ChatAnthropic(
                model=model_name,
                temperature=temperature,
                streaming=stream,
                anthropic_api_key=self.api_key,
            )
        if provider == "Google":
            if not self.api_key:
                msg = "Google API Key 是使用Google提供商时必需的"
                raise ValueError(msg)
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                streaming=stream,
                google_api_key=self.api_key,
            )
        if provider == "WorldSeek API":
            if not self.api_key:
                msg = "WorldSeek API Key 是使用WorldSeek API提供商时必需的"
                raise ValueError(msg)
            
            # 重新获取模型配置以确保获得最新的api_path和model_id
            model_config = get_worldseek_model_config_sync(model_name)
            
            # 使用配置中的api_path，如果没有则使用默认值
            raw_api_path = model_config.get('api_path', 'https://api.worldseek.com/v1') if model_config else 'https://api.worldseek.com/v1'
            
            # ChatOpenAI会自动在api_base后面添加/chat/completions，所以我们需要移除末尾的这部分
            # 避免路径重复拼接
            if raw_api_path.endswith('/chat/completions'):
                api_base = raw_api_path[:-len('/chat/completions')]
            elif raw_api_path.endswith('/v1/chat/completions'):
                api_base = raw_api_path[:-len('/v1/chat/completions')] + '/v1'
            else:
                api_base = raw_api_path
            
            # 使用配置中的model_id作为实际请求的模型名称，如果没有则使用model_name
            actual_model = model_config.get('model_id', model_name) if model_config else model_name
            
            # 保留关键调试信息
            print(f"WorldSeek API - 模型: {actual_model}, API端点: {api_base}")
            
            # 构建额外参数，处理特定模型的要求
            extra_kwargs = {}
            
            # 对于某些模型（如DeepSeek），在非流式调用时需要设置enable_thinking=false
            if not self.stream:
                extra_kwargs['extra_body'] = {'enable_thinking': False}
            
            return ChatOpenAI(
                model=actual_model,
                temperature=temperature,
                streaming=stream,
                openai_api_key=self.api_key,
                openai_api_base=api_base,
                **extra_kwargs
            )
        msg = f"Unknown provider: {provider}"
        raise ValueError(msg)

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        if field_name == "provider":
            if field_value == "OpenAI":
                build_config["model_name"]["refresh_button"] = False
                build_config["api_key"]["value"] = ""
                build_config["model_name"]["options"] = OPENAI_MODEL_NAMES
                build_config["model_name"]["value"] = OPENAI_MODEL_NAMES[0]
                build_config["api_key"]["display_name"] = "OpenAI API Key"
            elif field_value == "Anthropic":
                build_config["model_name"]["refresh_button"] = False
                build_config["api_key"]["value"] = ""
                build_config["model_name"]["options"] = ANTHROPIC_MODELS
                build_config["model_name"]["value"] = ANTHROPIC_MODELS[0]
                build_config["api_key"]["display_name"] = "Anthropic API Key"
            elif field_value == "Google":
                build_config["model_name"]["refresh_button"] = False
                build_config["api_key"]["value"] = ""
                build_config["model_name"]["options"] = GOOGLE_GENERATIVE_AI_MODELS
                build_config["model_name"]["value"] = GOOGLE_GENERATIVE_AI_MODELS[0]
                build_config["api_key"]["display_name"] = "Google API Key"
            elif field_value == "WorldSeek API":
                # 展示刷新按钮
                build_config["model_name"]["refresh_button"] = True
                # 获取WorldSeek模型列表
                worldseek_models = get_worldseek_models_sync()
                # 如果获取到模型列表，则展示模型列表
                if worldseek_models:
                    build_config["model_name"]["options"] = worldseek_models
                    build_config["model_name"]["value"] = worldseek_models[0]
                    # 获取模型配置
                    model_config = get_worldseek_model_config_sync(build_config["model_name"]["value"])
                    if model_config:
                        if "api_key" in model_config and model_config["api_key"]:
                            build_config["api_key"]["value"] = model_config["api_key"]
                # 如果获取不到模型列表，则展示空列表
                else:
                    build_config["model_name"]["options"] = []
                    build_config["model_name"]["placeholder"] = "请先在设置面板中配置模型"
                    build_config["model_name"]["value"] = ""
                build_config["api_key"]["display_name"] = "WorldSeek API Key"
        elif field_name == "model_name":
            if build_config["provider"]["value"] == "WorldSeek API" and field_value:
                model_config = get_worldseek_model_config_sync(field_value)
                if model_config:
                    # 同时设置build_config和组件属性
                    if "api_key" in build_config and "api_key" in model_config:
                        build_config["api_key"]["value"] = model_config["api_key"]              
                else:
                    pass  # 未找到配置时保持静默
        return build_config
