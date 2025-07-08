"""
警告抑制配置
用于抑制已知的无害警告，让日志更清洁
"""

import warnings
from sqlalchemy.exc import SAWarning
from langchain_core._api.deprecation import LangChainDeprecationWarning


def setup_warning_filters():
    """设置警告过滤器，抑制已知的无害警告"""
    
    # 1. 抑制SQLAlchemy外键约束警告（SQLite特有的正常警告）
    warnings.filterwarnings(
        "ignore",
        message=r".*SQL-parsed foreign key constraint.*could not be located in PRAGMA foreign_keys.*",
        category=SAWarning
    )
    
    # 2. 抑制LangChain的pydantic v1兼容性警告
    warnings.filterwarnings(
        "ignore",
        message=r".*langchain\.pydantic_v1.*",
        category=LangChainDeprecationWarning
    )
    
    # 3. 抑制Gunicorn worker相关的信息日志
    warnings.filterwarnings(
        "ignore",
        message=r".*Worker.*was sent.*",
        category=UserWarning
    )
    
    # 4. 抑制第三方库的语法警告
    warnings.filterwarnings(
        "ignore",
        message=r".*assertion is always true.*",
        category=SyntaxWarning
    )
    
    # 5. 抑制LangChain配置相关的弃用警告
    warnings.filterwarnings(
        "ignore",
        message=r".*Support for class-based.*config.*is deprecated.*",
        category=DeprecationWarning
    )
    
    warnings.filterwarnings(
        "ignore", 
        message=r".*Valid config keys have changed in V2.*",
        category=UserWarning
    )


def setup_clean_logging():
    """设置清洁的日志输出"""
    import logging
    
    # 设置第三方库的日志级别
    logging.getLogger("gunicorn.error").setLevel(logging.WARNING)
    logging.getLogger("gunicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)
    logging.getLogger("alembic.runtime.migration").setLevel(logging.WARNING)
    
    # 设置langchain相关日志级别
    logging.getLogger("langchain").setLevel(logging.WARNING)
    logging.getLogger("langchain_core").setLevel(logging.WARNING)
    logging.getLogger("langchain_community").setLevel(logging.WARNING)
    
    # 设置第三方集成的日志级别
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


# 在模块导入时自动设置
# setup_warning_filters()
# setup_clean_logging() 