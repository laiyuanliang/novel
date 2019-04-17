import os
from time import strftime


class Config:
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_EXTENSION = '.md'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'can you guess it'
    DEBUG = True
    # sqlalchemy两个主要配置
    # ORM底层所访问数据库URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Root@mysql01@127.0.0.1/novel?charset=utf8'
    # 当关闭数据库是否自动提交事务
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        # app.logger.setLevel(logging.DEBUG)
        # app.logger.addHandler(get_handler)
        pass


class DevelopmentConfig(Config):
    """开发环境配置
    """

    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Root@mysql01@127.0.0.1/novel?charset=utf8'


class TestConfig(Config):
    """测试环境配置
    """

    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Root@mysql01@127.0.0.1/novel?charset=utf8'


class ProductionConfig(Config):
    """生产环境
    """
    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Root@mysql01@127.0.0.1/novel'


# 设置配置映射
config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
