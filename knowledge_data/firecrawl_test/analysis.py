import os
import json
from bs4 import BeautifulSoup


def extract_info(soup, field_name):
    field = soup.find('div', class_='infobox-cell-2', string=field_name)
    if field:
        value = field.find_next_sibling('div').text.strip()
        return ' '.join(value.split())  # 处理多余的空格，包括不间断空格
    return "Not found"


def extract_list(soup, field_name):
    field = soup.find('div', class_='infobox-cell-2', string=field_name)
    if field:
        items = field.find_next_sibling('div').find_all('li')
        return [' '.join(item.text.strip().split()) for item in items]
    return []


def extract_full_description(soup):
    description_section = soup.find('span', class_='mw-headline', id='Description')
    if description_section:
        description = ""
        for sibling in description_section.parent.next_siblings:
            if sibling.name == 'p':
                description += sibling.text.strip() + " "
            elif sibling.name == 'h2':
                break
        return description.strip()
    return "Not found"


def extract_cost(soup):
    cost_field = soup.find('div', class_='infobox-cell-2', string='Cost:')
    if cost_field:
        cost_value = cost_field.find_next_sibling('div').text.strip()
        cost_parts = cost_value.split()
        if len(cost_parts) == 4:
            return {
                "mineral": int(cost_parts[0]) if cost_parts[0].isdigit() else 0,
                "vespene": int(cost_parts[1]) if cost_parts[1].isdigit() else 0,
                "game_time": float(cost_parts[2]) if cost_parts[2].replace('.', '').isdigit() else 0,
                "supply": int(cost_parts[3]) if cost_parts[3].isdigit() else 0
            }
    return "Cost information not found or in unexpected format"


def extract_competitive_usage(soup):
    competitive_usage = {}
    competitive_usage_section = soup.find('span', class_='mw-headline', id='Competitive_Usage')
    if competitive_usage_section:
        current_section = None
        for elem in competitive_usage_section.parent.next_siblings:
            if elem.name == 'h3':
                current_section = elem.find('span', class_='mw-headline').text.strip()
                competitive_usage[current_section] = ""
            elif elem.name in ['p', 'ul'] and current_section:
                competitive_usage[current_section] += elem.text.strip() + " "
            elif elem.name == 'h2':
                break

        # 清理每个部分的文本
        for section, content in competitive_usage.items():
            competitive_usage[section] = ' '.join(content.split())

    return competitive_usage if competitive_usage else "Competitive Usage information not found"


def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html_content = data['html']
    soup = BeautifulSoup(html_content, 'html.parser')

    unit_info = {
        "Type": extract_info(soup, "Type:"),
        "Description": extract_full_description(soup),
        "Built From": extract_info(soup, "Built From:"),
        "Requirements": extract_info(soup, "Requirements:"),
        "Cost": extract_cost(soup),
        "Hotkey": extract_info(soup, "Hotkey:"),
        "Attack": {
            "Targets": extract_info(soup, "Targets:"),
            "Damage": extract_info(soup, "Damage:"),
            "DPS": extract_info(soup, "DPS:"),
            "Cooldown": extract_info(soup, "Cooldown:"),
            "Bonus": extract_info(soup, "Bonus:"),
            "Bonus DPS": extract_info(soup, "Bonus DPS:"),
            "Range": extract_info(soup, "Range:")
        },
        "Unit stats": {
            "Defense": extract_info(soup, "Defense:"),
            "Attributes": extract_info(soup, "Attributes:"),
            "Sight": extract_info(soup, "Sight:"),
            "Speed": extract_info(soup, "Speed:"),
            "Cargo size": extract_info(soup, "Cargo size:")
        },
        "Strong against": extract_list(soup, "Strong against:"),
        "Weak against": extract_list(soup, "Weak against:")
    }

    # 提取ability
    ability_section = soup.find('span', class_='mw-headline', id='Ability')
    if ability_section:
        ability_div = ability_section.find_next('div', class_='wikitable')
        ability_name = ability_div.find('div', id='Cliff_Walk').text.strip() if ability_div.find('div',
                                                                                                 id='Cliff_Walk') else "Not found"
        ability_description = ability_div.find('div', style='clear:both').text.strip() if ability_div.find('div',
                                                                                                           style='clear:both') else "Not found"
        unit_info["Ability"] = f"{ability_name}: {ability_description}"
    else:
        unit_info["Ability"] = "No ability found"

    # 提取upgrade
    upgrade_section = soup.find('span', class_='mw-headline', id='Upgrade')
    if upgrade_section:
        upgrade_div = upgrade_section.find_next('div', class_='wikitable')
        upgrade_name = upgrade_div.find('div', id='Extended_Thermal_Lance').text.strip() if upgrade_div.find('div',
                                                                                                             id='Extended_Thermal_Lance') else "Not found"
        upgrade_details = upgrade_div.find_all('div', style='padding:2px 10px')
        upgrade_description = upgrade_div.find('div', style='clear:both').text.strip() if upgrade_div.find('div',
                                                                                                           style='clear:both') else "Not found"
        unit_info["Upgrade"] = {
            "Name": upgrade_name,
            "Details": [detail.text.strip() for detail in upgrade_details],
            "Description": upgrade_description
        }
    else:
        unit_info["Upgrade"] = "No upgrade found"

    # 提取Competitive Usage部分
    unit_info["Competitive Usage"] = extract_competitive_usage(soup)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unit_info, f, indent=2, ensure_ascii=False)


def main():
    input_dir = r"D:\pythoncode\vlm_attention_starcraft2-main\vlm_attention\knowledge_data\firecrawl_test\sc2_unit_info"
    output_dir = r"D:\pythoncode\vlm_attention_starcraft2-main\vlm_attention\knowledge_data\firecrawl_test\sc2_unit_info_processed"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            print(f"Processing {filename}...")
            process_file(input_file, output_file)
            print(f"Finished processing {filename}")


if __name__ == "__main__":
    main()