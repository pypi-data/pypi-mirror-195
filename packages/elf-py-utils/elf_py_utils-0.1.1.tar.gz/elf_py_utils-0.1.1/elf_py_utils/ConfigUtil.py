"""
配置信息 工具类
"""
import configparser
import yaml

file_type_dict = {
    'ini': 'ini',
    'yaml': 'yaml',
    'xml': 'xml'
}


class ConfigReader:

    def __init__(self, config_path, config_type):
        self.config_path: str = config_path
        self.config_type: str = config_type
        self.config_dict: dict = self.__load_config()

    def load_config_ini(self) -> dict:
        """读取配置文件-ini

        :return: dict格式的配置信息
        """
        # 创建配置文件并获取内容
        config = configparser.ConfigParser()
        config.read(self.config_path, encoding="utf-8")
        # 遍历配置文件组装配置信息字典
        config_dict = {}
        for section in config.sections():
            config_dict[section] = dict(config.items(section, raw=True))

        return config_dict

    def load_config_yaml(self) -> dict:
        """读取配置文件-yaml

        :return: dict格式的配置信息
        """
        # 读取文件，获取字符串格式的配置信息
        config_file = open(self.config_path, 'r', encoding='utf-8')
        config = config_file.read()
        # 用yaml.load()方法将配置转化为字典
        config_dict = yaml.load(config, Loader=yaml.FullLoader)

        return config_dict

    config_type_dict = {
        'ini': load_config_ini,
        'yaml': load_config_yaml
    }

    def __load_config(self):
        function = self.config_type_dict.get(self.config_type)
        return function(self)

    def read_config(self, item_path: str):
        """
        根据配置项路径获取配置信息

        :param item_path: 配置项路径，以英文句号.分隔
        :return: 根据具体配置内容，决定返回体的类型
        """
        item_path_list = item_path.split('.')
        config_dict = self.config_dict
        for item in item_path_list:
            config_dict = config_dict[item]

        config_item = config_dict
        return config_item
