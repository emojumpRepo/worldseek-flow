from typing import Any
import asyncio
from loguru import logger

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

# 验证缓存 - 避免重复验证相同的API连接
import time
_verification_cache = {}
_cache_ttl = 300  # 缓存5分钟


def _get_cache_key(api_base: str, api_key: str, model_name: str) -> str:
    """生成缓存键"""
    return f"{api_base}:{api_key[:10]}:{model_name}"


def _is_cache_valid(cache_key: str) -> bool:
    """检查缓存是否有效"""
    if cache_key not in _verification_cache:
        return False
    cached_time, cached_result = _verification_cache[cache_key]
    return time.time() - cached_time < _cache_ttl


def _set_cache(cache_key: str, result: bool):
    """设置缓存"""
    _verification_cache[cache_key] = (time.time(), result)


def get_worldseek_models_sync() -> list[str]:
    """同步获取WorldSeek模型列表"""
    try:
        from langflow.services.deps import get_db_service
        from langflow.services.database.models.model.crud import get_models
        import threading
        import queue
        import gc  # 添加垃圾回收
        
        db_service = get_db_service()
        
        result_queue = queue.Queue()
        
        def run_async():
            async def _get_models():
                try:
                    async with db_service.with_session() as session:
                        models = await get_models(session, skip=0, limit=1000)
                        return [model.name for model in models if model.name]
                except Exception as e:
                    logger.error(f"数据库查询错误: {e}")
                    return []
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(_get_models())
                result_queue.put(result)
            except Exception as e:
                logger.error(f"异步执行错误: {e}")
                result_queue.put([])
            finally:
                loop.close()
                # 强制垃圾回收释放内存
                gc.collect()
        
        thread = threading.Thread(target=run_async)
        thread.start()
        # 将超时时间从5秒增加到15秒，以适应线上环境
        thread.join(timeout=15)
        
        if thread.is_alive():
            logger.warning("获取模型列表超时")
            # 强制清理线程资源
            try:
                thread.join(timeout=5)  # 再给5秒时间
            except:
                pass
            return []
        
        try:
            return result_queue.get_nowait()
        except queue.Empty:
            logger.warning("获取模型列表时队列为空")
            return []
            
    except Exception as e:
        logger.error(f"获取WorldSeek模型列表失败: {e}")
        return []
    finally:
        # 确保内存清理
        import gc
        gc.collect()


def get_worldseek_model_config_sync(model_name: str) -> dict:
    """根据模型名称获取模型配置"""
    try:
        from langflow.services.deps import get_db_service
        from langflow.services.database.models.model.crud import get_model_by_name
        import threading
        import queue
        import gc

        db_service = get_db_service()
        
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
                        logger.warning(f"在数据库中未找到模型: {model_name}")
                        return {}
                except Exception as e:
                    logger.error(f"数据库查询错误: {e}")
                    return {}
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(_get_model_config())
                result_queue.put(result)
            except Exception as e:
                logger.error(f"异步执行错误: {e}")
                result_queue.put({})
            finally:
                loop.close()
                gc.collect()
        
        thread = threading.Thread(target=run_async)
        thread.start()
        # 将超时时间从5秒增加到15秒
        thread.join(timeout=15)
        
        if thread.is_alive():
            logger.warning(f"获取模型 '{model_name}' 的配置超时")
            # 强制清理线程资源
            try:
                thread.join(timeout=5)
            except:
                pass
            return {}
        
        try:
            return result_queue.get_nowait()
        except queue.Empty:
            logger.warning(f"获取模型 '{model_name}' 配置时队列为空")
            return {}
            
    except Exception as e:
        logger.error(f"获取WorldSeek模型 '{model_name}' 配置失败: {e}")
        return {}
    finally:
        import gc
        gc.collect()


async def verify_model_connection(api_base: str, api_key: str, model_name: str) -> bool:
    """
    验证模型连接是否有效 - 快速检测各种错误情况
    
    Args:
        api_base: API基础URL  
        api_key: API密钥
        model_name: 模型名称
        
    Returns:
        bool: 连接是否有效
        
    Raises:
        ValueError: 当检测到具体错误时立即抛出，避免长时间等待
    """
    # 🚀 检查缓存，避免重复验证
    cache_key = _get_cache_key(api_base, api_key, model_name)
    if _is_cache_valid(cache_key):
        cached_result = _verification_cache[cache_key][1]
        logger.debug(f"使用缓存的验证结果: {cache_key} -> {cached_result}")
        if cached_result:
            return True
        else:
            # 缓存中是失败结果，立即抛出错误
            raise ValueError(f"模型 '{model_name}' 连接验证失败 (缓存结果)")
    
    try:
        import httpx
        import asyncio
        
        # 🔥 关键：使用极短的超时，让线上环境快速检测错误
        timeout = httpx.Timeout(
            connect=3.0,    # 连接超时3秒
            read=5.0,       # 读取超时5秒  
            write=3.0,      # 写入超时3秒
            pool=3.0        # 连接池超时3秒
        )
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Langflow/1.0"
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            # 步骤1：快速测试基础连接 🔌
            try:
                base_url = api_base.rstrip('/') + '/models'
                logger.debug(f"测试基础连接: {base_url}")
                
                response = await client.get(base_url, headers=headers)
                
                # 🚨 立即检测常见错误并抛出具体异常
                if response.status_code == 401:
                    error_msg = f"Error code: 401 - API密钥无效或已过期: {api_key[:10]}..."
                    _set_cache(cache_key, False)  # 缓存失败结果
                    raise ValueError(error_msg)
                elif response.status_code == 403:
                    error_msg = f"Error code: 403 - API密钥权限不足"
                    _set_cache(cache_key, False)
                    raise ValueError(error_msg)
                elif response.status_code == 404:
                    error_msg = f"Error code: 404 - API端点不存在: {base_url}"
                    _set_cache(cache_key, False)
                    raise ValueError(error_msg)
                elif response.status_code == 429:
                    error_msg = f"Error code: 429 - API请求频率限制"
                    # 不缓存429错误，可能是临时的
                    raise ValueError(error_msg)
                elif response.status_code >= 500:
                    error_msg = f"Error code: {response.status_code} - 服务器错误"
                    # 不缓存服务器错误，可能是临时的
                    raise ValueError(error_msg)
                    
            except httpx.ConnectError as e:
                error_msg = f"Error building Component: 无法连接到API服务器 {api_base}. 请检查网络连接和URL是否正确"
                _set_cache(cache_key, False)
                raise ValueError(error_msg) from e
            except httpx.TimeoutException as e:
                error_msg = f"Error building Component: 连接超时 {api_base}. 请检查网络连接"
                _set_cache(cache_key, False)
                raise ValueError(error_msg) from e
            except httpx.RequestError as e:
                error_msg = f"Error building Component: 网络请求错误 {str(e)}"
                _set_cache(cache_key, False)
                raise ValueError(error_msg) from e
            
            # 步骤2：验证模型是否存在 🤖  
            if response.status_code == 200:
                try:
                    models_data = response.json()
                    available_models = []
                    
                    # 解析不同API格式的模型列表
                    if isinstance(models_data, dict):
                        if 'data' in models_data:
                            # OpenAI格式: {"data": [{"id": "model1"}, ...]}
                            available_models = [model.get('id', '') for model in models_data['data']]
                        elif 'models' in models_data:
                            # 其他格式: {"models": ["model1", "model2", ...]}
                            available_models = models_data['models']
                    elif isinstance(models_data, list):
                        # 直接的模型列表: ["model1", "model2", ...]
                        available_models = models_data
                    
                    # 🔍 检查模型是否存在
                    if available_models and model_name not in available_models:
                        available_str = ', '.join(available_models[:5])  # 显示前5个可用模型
                        if len(available_models) > 5:
                            available_str += f" (还有{len(available_models)-5}个模型...)"
                        error_msg = f"Error code: 404 - 模型 '{model_name}' 不存在. 可用模型: {available_str}"
                        _set_cache(cache_key, False)
                        raise ValueError(error_msg)
                    
                    logger.info(f"✅ 模型验证成功: {model_name}")
                    _set_cache(cache_key, True)  # 缓存成功结果
                    return True
                    
                except (ValueError, KeyError, TypeError) as e:
                    # JSON解析失败，但连接成功，可能是兼容性问题
                    logger.warning(f"模型列表解析失败，但API连接正常: {e}")
                    _set_cache(cache_key, True)  # 认为连接有效
                    return True
            
            # 其他状态码认为连接有效但可能有其他问题
            logger.warning(f"API响应状态码: {response.status_code}, 但连接正常")
            _set_cache(cache_key, True)
            return True
                
    except ValueError:
        # 重新抛出ValueError，这些是我们想要立即暴露给用户的错误
        raise
    except Exception as e:
        # 其他未预期的错误
        logger.warning(f"模型连接验证失败: {e}")
        _set_cache(cache_key, False)
        raise ValueError(f"Error building Component: 模型连接验证失败: {str(e)}") from e


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
                timeout=30,  # 添加超时设置
                max_retries=2,  # 限制重试次数
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
                timeout=30,
                max_retries=2,
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
                request_timeout=30,
                max_retries=2,
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
            logger.info(f"WorldSeek API - 模型: {actual_model}, API端点: {api_base}")
            
            # 🔥 快速验证连接，失败时立即抛出错误
            # 这是解决线上环境Worker超时问题的关键
            try:
                import httpx
                
                logger.info(f"🔍 验证WorldSeek API连接: {api_base}")
                
                # 使用同步验证逻辑，避免asyncio问题
                def _verify_connection_sync():
                    # 检查缓存
                    cache_key = _get_cache_key(api_base, self.api_key, actual_model)
                    if _is_cache_valid(cache_key):
                        cached_result = _verification_cache[cache_key][1]
                        if cached_result:
                            return True
                        else:
                            raise ValueError(f"模型 '{actual_model}' 连接验证失败 (缓存结果)")
                    
                    # 极短超时设置
                    timeout = httpx.Timeout(connect=3.0, read=5.0, write=3.0, pool=3.0)
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "Langflow/1.0"
                    }
                    
                    # 使用同步Client
                    with httpx.Client(timeout=timeout) as client:
                        try:
                            base_url = api_base.rstrip('/') + '/models'
                            response = client.get(base_url, headers=headers)
                            
                            # 立即检测错误
                            if response.status_code == 401:
                                _set_cache(cache_key, False)
                                raise ValueError(f"Error code: 401 - API密钥无效或已过期: {self.api_key[:10]}...")
                            elif response.status_code == 403:
                                _set_cache(cache_key, False)
                                raise ValueError(f"Error code: 403 - API密钥权限不足")
                            elif response.status_code == 404:
                                _set_cache(cache_key, False)
                                raise ValueError(f"Error code: 404 - API端点不存在: {base_url}")
                            elif response.status_code == 429:
                                raise ValueError(f"Error code: 429 - API请求频率限制")
                            elif response.status_code >= 500:
                                raise ValueError(f"Error code: {response.status_code} - 服务器错误")
                            
                            # 验证成功
                            _set_cache(cache_key, True)
                            return True
                            
                        except httpx.ConnectError as e:
                            _set_cache(cache_key, False)
                            raise ValueError(f"无法连接到API服务器 {api_base}. 请检查网络连接和URL是否正确") from e
                        except httpx.TimeoutException as e:
                            _set_cache(cache_key, False)
                            raise ValueError(f"连接超时 {api_base}. 请检查网络连接") from e
                        except httpx.RequestError as e:
                            _set_cache(cache_key, False)
                            raise ValueError(f"网络请求错误 {str(e)}") from e
                
                # 执行同步验证
                _verify_connection_sync()
                
                logger.info(f"✅ WorldSeek API连接验证成功")
                
            except ValueError as e:
                # 重新抛出验证错误，让用户立即看到具体错误信息
                logger.error(f"❌ WorldSeek API连接验证失败: {e}")
                raise  # 直接抛出，不再继续创建模型
            except Exception as e:
                # 其他异常也转换为ValueError并抛出
                error_msg = f"连接验证过程出错: {str(e)}"
                logger.error(f"❌ {error_msg}")
                raise ValueError(error_msg) from e
            
            # 构建额外参数，处理特定模型的要求
            extra_kwargs = {}
            
            # 对于某些模型（如DeepSeek），在非流式调用时需要设置enable_thinking=false
            if not self.stream:
                extra_kwargs['extra_body'] = {'enable_thinking': False}
            
            try:
                return ChatOpenAI(
                    model=actual_model,
                    temperature=temperature,
                    streaming=stream,
                    openai_api_key=self.api_key,
                    openai_api_base=api_base,
                    request_timeout=30,  # 添加30秒超时
                    max_retries=2,  # 限制重试次数防止资源泄漏
                    **extra_kwargs
                )
            except Exception as e:
                logger.error(f"创建WorldSeek模型实例失败: {e}")
                # 提供更友好的错误信息
                if "connection" in str(e).lower() or "timeout" in str(e).lower():
                    raise ValueError(f"无法连接到WorldSeek API，请检查网络连接和API配置。错误: {e}")
                else:
                    raise ValueError(f"WorldSeek模型配置错误: {e}")
        
        msg = f"Unknown provider: {provider}"
        raise ValueError(msg)

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        if field_name == "provider":
            build_config["model_name"]["placeholder"] = "请选择模型"
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