import logging
from typing import List, Dict, Optional
from sc2_unit_database import SC2UnitDatabase
from LLM.call_llm_api.call_llm import TextChatbot

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

"""
测试代码,用于联合测试LLM和数据库.确保检索和生成的信息是正确的
"""
class SC2UnitAnalyzer:
    def __init__(self, yaml_file: str, llm_model: str = "summarizer"):
        self.db = SC2UnitDatabase(yaml_file)
        self.text_bot = TextChatbot(llm_model)

    def get_unit_info(self, unit_names: List[str]) -> Dict[str, Dict]:
        """从数据库获取指定单位的信息"""
        return {unit: info for unit in unit_names if (info := self.db.get_unit_info(unit))}

    def summarize_units(self, unit_names: List[str]) -> Optional[str]:
        """总结指定单位的信息"""
        unit_info = self.get_unit_info(unit_names)
        if not unit_info:
            logger.warning(f"未找到任何单位信息: {', '.join(unit_names)}")
            return None

        summary_prompt = self._create_summary_prompt(unit_info)
        return self.text_bot.query("You are a StarCraft 2 expert. Summarize the following unit information concisely:",
                                   summary_prompt)

    def compare_units(self, unit_names: List[str]) -> Optional[str]:
        """比较指定单位的信息"""
        unit_info = self.get_unit_info(unit_names)
        if len(unit_info) < 2:
            logger.warning(f"需要至少两个有效单位进行比较。找到的有效单位: {', '.join(unit_info.keys())}")
            return None

        compare_prompt = self._create_comparison_prompt(unit_info)
        return self.text_bot.query("You are a StarCraft 2 expert. Compare and analyze the following units:",
                                   compare_prompt)

    def _create_summary_prompt(self, unit_info: Dict[str, Dict]) -> str:
        return "\n\n".join(
            f"单位：{unit}\n" +
            f"描述：{info.get('Description', 'N/A')}\n" +
            f"优势：{', '.join(info.get('Strong against', ['N/A']))}\n" +
            f"劣势：{', '.join(info.get('Weak against', ['N/A']))}\n" +
            f"特殊能力：{info.get('Ability', 'N/A')}"
            for unit, info in unit_info.items()
        )

    def _create_comparison_prompt(self, unit_info: Dict[str, Dict]) -> str:
        return self._create_summary_prompt(unit_info)


def main():
    analyzer = SC2UnitAnalyzer("sc2_unit_data_index.yaml")

    # 测试用例1: 获取和总结多个单位信息
    test_units = ["zealot", "stalker", "archon"]
    logger.info(f"测试用例1: 获取和总结单位信息 - {', '.join(test_units)}")
    summary = analyzer.summarize_units(test_units)
    if summary:
        logger.info(f"单位信息总结:\n{summary}")

    # 测试用例2: 获取不存在的单位信息
    non_existent_unit = "non_existent_unit"
    logger.info(f"测试用例2: 尝试获取不存在的单位信息 - {non_existent_unit}")
    summary = analyzer.summarize_units([non_existent_unit])
    if summary is None:
        logger.info("正确地未找到不存在的单位信息")

    # 测试用例3: 使用LLM生成单位对比分析
    compare_units = ["stalker", "marauder"]
    logger.info(f"测试用例3: 使用LLM生成单位对比分析 - {', '.join(compare_units)}")
    comparison = analyzer.compare_units(compare_units)
    if comparison:
        logger.info(f"单位对比分析:\n{comparison}")


if __name__ == "__main__":
    main()
