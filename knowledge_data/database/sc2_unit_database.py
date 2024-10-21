import json
import logging
import os
from typing import Dict, List, Any, Optional

import yaml

"""
星际争霸2单位数据库
yaml是索引文件，包含了所有单位的文件名和路径
json文件包含了单位的详细信息
测试代码在最下面,与LLM的联合测试在test_llm_use_database.py
"""
# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SC2UnitDatabase:
    def __init__(self, yaml_file: str):
        self.yaml_file = os.path.abspath(yaml_file)
        self.data: Dict[str, Dict[str, Dict[str, str]]] = {}
        self.unit_cache: Dict[str, Dict[str, Any]] = {}
        self.load_yaml()

    def load_yaml(self):
        """加载YAML索引文件"""
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
            logging.info(f"Successfully loaded YAML file: {self.yaml_file}")
        except FileNotFoundError:
            logging.error(f"YAML file not found: {self.yaml_file}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file: {e}")
            raise

    def get_units_by_race(self, race: str) -> List[str]:
        """获取特定种族的单位列表"""
        return list(self.data.get(race, {}).keys())

    def get_all_units_by_race(self) -> Dict[str, List[str]]:
        """获取所有单位（按种族分组）"""
        return {race: list(units.keys()) for race, units in self.data.items()}

    def get_all_unit_names(self) -> List[str]:
        """获取所有单位名称"""
        return [unit for race_units in self.data.values() for unit in race_units]

    def unit_exists(self, unit_name: str) -> bool:
        """检查特定单位是否存在"""
        unit_name_lower = unit_name.lower()
        return any(unit_name_lower == name.lower() for race_units in self.data.values() for name in race_units)

    def get_unit_info(self, unit_name: str) -> Dict[str, Any]:
        """获取特定单位的详细信息"""
        if unit_name in self.unit_cache:
            return self.unit_cache[unit_name]

        for race, units in self.data.items():
            unit_name_lower = unit_name.lower()
            for unit_key, unit_data in units.items():
                if unit_name_lower == unit_key.lower():
                    file_path = unit_data['file_path']  # 这里应该已经是绝对路径
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                unit_info = json.load(file)
                            self.unit_cache[unit_name] = unit_info
                            logging.info(f"Loaded unit info for: {unit_name}")
                            return unit_info
                        except json.JSONDecodeError as e:
                            logging.error(f"Error parsing JSON file for unit {unit_name}: {e}")
                    else:
                        logging.error(f"JSON file not found for unit {unit_name}: {file_path}")
                        return {}

        logging.warning(f"Unit information not found for: {unit_name}")
        return {}

    def search_units(self, query: str) -> List[Dict[str, str]]:
        """搜索单位"""
        results = []
        for race, units in self.data.items():
            for unit_name, unit_data in units.items():
                if query.lower() in unit_name.lower():
                    results.append({
                        "race": race,
                        "name": unit_name,
                        "file_name": unit_data['file_name']
                    })
        return results

    def get_all_races(self) -> List[str]:
        """获取所有种族列表"""
        return list(self.data.keys())

    def get_unit_attribute(self, unit_name: str, attribute: str) -> Any:
        """获取单位的特定属性"""
        unit_info = self.get_unit_info(unit_name)
        if not unit_info:
            logging.warning(f"No information found for unit: {unit_name}")
            return None
        if attribute not in unit_info:
            logging.warning(f"Attribute '{attribute}' not found for unit: {unit_name}")
            return None
        return unit_info.get(attribute)

    # 以下是特定属性获取方法
    def get_unit_cost(self, unit_name: str) -> Optional[Dict[str, Any]]:
        """获取单位的成本信息"""
        return self.get_unit_attribute(unit_name, "Cost")

    def get_unit_attack_info(self, unit_name: str) -> Optional[Dict[str, Any]]:
        """获取单位的攻击信息"""
        return self.get_unit_attribute(unit_name, "Attack")

    def get_unit_stats(self, unit_name: str) -> Optional[Dict[str, Any]]:
        """获取单位的统计信息"""
        return self.get_unit_attribute(unit_name, "Unit stats")

    def get_unit_strengths(self, unit_name: str) -> Optional[List[str]]:
        """获取单位的优势对象列表"""
        return self.get_unit_attribute(unit_name, "Strong against")

    def get_unit_weaknesses(self, unit_name: str) -> Optional[List[str]]:
        """获取单位的劣势对象列表"""
        return self.get_unit_attribute(unit_name, "Weak against")

    def get_unit_ability(self, unit_name: str) -> Optional[str]:
        """获取单位的特殊能力"""
        return self.get_unit_attribute(unit_name, "Ability")

    def get_unit_upgrade(self, unit_name: str) -> Optional[Dict[str, Any]]:
        """获取单位的升级信息"""
        return self.get_unit_attribute(unit_name, "Upgrade")

    def get_unit_competitive_usage(self, unit_name: str) -> Optional[Dict[str, str]]:
        """获取单位的竞技使用信息"""
        return self.get_unit_attribute(unit_name, "Competitive Usage")


import unittest


class TestSC2UnitDatabase(unittest.TestCase):
    def setUp(self):
        self.yaml_file = 'sc2_unit_data_index.yaml'
        self.db = SC2UnitDatabase(self.yaml_file)

    def test_load_yaml(self):
        self.assertIsNotNone(self.db.data)
        self.assertGreater(len(self.db.data), 0)

    def test_get_units_by_race(self):
        protoss_units = self.db.get_units_by_race("Protoss")
        self.assertIn("stalker", protoss_units)
        self.assertIn("archon", protoss_units)
        self.assertIn("zealot", protoss_units)
        terran_units = self.db.get_units_by_race("Terran")
        self.assertIn("banshee", terran_units)
        self.assertIn("ghost", terran_units)

    def test_get_all_units_by_race(self):
        all_units = self.db.get_all_units_by_race()
        self.assertIn("Protoss", all_units)
        self.assertIn("Terran", all_units)
        self.assertIn("stalker", all_units["Protoss"])
        self.assertIn("banshee", all_units["Terran"])

    def test_get_all_unit_names(self):
        all_names = self.db.get_all_unit_names()
        self.assertIn("stalker", all_names)
        self.assertIn("archon", all_names)
        self.assertIn("zealot", all_names)
        self.assertIn("banshee", all_names)
        self.assertIn("ghost", all_names)

    def test_unit_exists(self):
        self.assertTrue(self.db.unit_exists("stalker"))
        self.assertTrue(self.db.unit_exists("archon"))
        self.assertTrue(self.db.unit_exists("zealot"))
        self.assertTrue(self.db.unit_exists("banshee"))
        self.assertTrue(self.db.unit_exists("ghost"))
        self.assertFalse(self.db.unit_exists("nonexistentunit"))

    def test_get_unit_info(self):
        stalker_info = self.db.get_unit_info("stalker")
        self.assertIsNotNone(stalker_info)
        self.assertIn("Description", stalker_info)

    def test_search_units(self):
        results = self.db.search_units("banshee")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["name"], "banshee")
        self.assertEqual(results[0]["race"], "Terran")

    def test_get_all_races(self):
        races = self.db.get_all_races()
        self.assertIn("Protoss", races)
        self.assertIn("Terran", races)

    def test_get_unit_attribute(self):
        cost = self.db.get_unit_attribute("zealot", "Cost")
        self.assertIsNotNone(cost)
        self.assertIn("mineral", cost)

    def test_get_unit_cost(self):
        cost = self.db.get_unit_cost("stalker")
        self.assertIsNotNone(cost)
        self.assertIn("mineral", cost)

    def test_get_unit_attack_info(self):
        attack_info = self.db.get_unit_attack_info("ghost")
        self.assertIsNotNone(attack_info)

    def test_get_unit_stats(self):
        stats = self.db.get_unit_stats("archon")
        self.assertIsNotNone(stats)

    def test_get_unit_strengths(self):
        strengths = self.db.get_unit_strengths("banshee")
        self.assertIsNotNone(strengths)

    def test_get_unit_weaknesses(self):
        weaknesses = self.db.get_unit_weaknesses("zealot")
        self.assertIsNotNone(weaknesses)

    def test_get_unit_ability(self):
        ability = self.db.get_unit_ability("ghost")
        self.assertIsNotNone(ability)

    def test_get_unit_upgrade(self):
        upgrade = self.db.get_unit_upgrade("stalker")
        self.assertIsNotNone(upgrade)

    def test_get_unit_competitive_usage(self):
        usage = self.db.get_unit_competitive_usage("archon")
        self.assertIsNotNone(usage)


if __name__ == "__main__":
    unittest.main()


