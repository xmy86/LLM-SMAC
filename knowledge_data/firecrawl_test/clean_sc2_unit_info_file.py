import json
import os
from bs4 import BeautifulSoup
from typing import Dict, List, Any

"""
将从Liquipedia爬取的StarCraft II单位信息文件进行处理，提取有用的信息并保存到新的JSON文件中。
处理后的每个json文件的数据格式为:
{
  "Type": "Ground Unit",
    "Description": "T.....",
  "Built From": "Not found",
  "Requirements": "Not found",
  "Cost": {
    "mineral": 0,
    "vespene": 0,
    "game_time": 8.57,
    "supply": 4
  },
  "Hotkey": "Not found",
  "Attack": {
    "Targets": "Ground / Air",
    "Damage": "25 (+3) (Splash)",
    "DPS": "Not found",
    "Cooldown": "Not found",
    "Bonus": "+10 (+1) vs Biological",
    "Bonus DPS": "+8 (+0.8) vs Biological",
    "Range": "Not found"
  },
  "Unit stats": {
    "Defense": "10 350 0 (+1)",
    "Attributes": "Psionic, Massive",
    "Sight": "9",
    "Speed": "3.94",
    "Cargo size": "4"
  },
  "Strong against": [
    "Marine",
    "Mutalisk",
    "Adept"
  ],
  "Weak against": [
    "Thor",
    "Hydralisk",
    "Immortal"
  ],
  "Ability": "No ability found",
  "Upgrade": "No upgrade found",
  "Competitive Usage": {
    "General": "",
    "vs. Protoss": "",
    "vs. Terran": "",
    "vs. Zerg": ""
}
"""
class UnitInfoExtractor:
    def __init__(self, input_directory: str, output_directory: str):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.ensure_output_directory()

    def ensure_output_directory(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def extract_info_from_file(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        html_content = data.get('html', '')
        soup = BeautifulSoup(html_content, 'html.parser')

        unit_info = {
            'name': self.extract_name(soup),
            'description': self.extract_description(soup),
            'abilities': self.extract_abilities(soup),
            'competitive_usage': self.extract_competitive_usage(soup)
        }

        return unit_info

    def extract_name(self, soup: BeautifulSoup) -> str:
        name_element = soup.find('h1', id='firstHeading')
        return name_element.text.strip() if name_element else 'N/A'

    def extract_description(self, soup: BeautifulSoup) -> str:
        description_element = soup.find('div', class_='infobox-description')
        return description_element.text.strip() if description_element else 'N/A'

    def extract_abilities(self, soup: BeautifulSoup) -> List[str]:
        abilities_section = soup.find('span', id='Abilities')
        abilities = []
        if abilities_section:
            ability_divs = abilities_section.find_next('h2').find_next_siblings('div', class_='table-responsive')
            for div in ability_divs:
                ability_name = div.find('div', id=True)
                if ability_name:
                    abilities.append(ability_name.text.strip())
        return abilities

    def extract_competitive_usage(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        competitive_usage = {}
        usage_section = soup.find('span', id='Competitive_Usage')
        if usage_section:
            current_section = None
            for sibling in usage_section.find_next().find_next_siblings():
                if sibling.name == 'h3':
                    current_section = sibling.text.strip()
                    competitive_usage[current_section] = []
                elif sibling.name == 'ul' and current_section:
                    competitive_usage[current_section].extend([li.text.strip() for li in sibling.find_all('li')])
                elif sibling.name == 'h2':
                    break
        return competitive_usage

    def process_all_files(self):
        for filename in os.listdir(self.input_directory):
            if filename.endswith('.json'):
                input_path = os.path.join(self.input_directory, filename)
                output_path = os.path.join(self.output_directory, filename)

                unit_info = self.extract_info_from_file(input_path)

                with open(output_path, 'w', encoding='utf-8') as outfile:
                    json.dump(unit_info, outfile, ensure_ascii=False, indent=2)

                print(f"Processed: {filename}")


def main():
    input_dir = (r'C:\python_code\vlm_attention_starcraft2-main\vlm_attention\knowledge_data\firecrawl_test'
                 r'\sc2_unit_info')
    output_dir = (r'C:\python_code\vlm_attention_starcraft2-main\vlm_attention\knowledge_data\firecrawl_test'
                  r'\sc2_unit_info_processed')

    extractor = UnitInfoExtractor(input_dir, output_dir)
    extractor.process_all_files()


if __name__ == "__main__":
    main()