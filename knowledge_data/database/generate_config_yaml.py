import os
import yaml
import sys
"""
生成数据库所用的config.yaml文件,注意,每次安装的时候都需要运行这个脚本
"""
def get_project_root():
    """返回项目根目录的路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..', '..'))

def scan_unit_files(folder_path):
    unit_data = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                parts = filename.split('_')
                if len(parts) >= 2:
                    race = parts[0]
                    unit_name = '_'.join(parts[1:]).rsplit('.', 1)[0]
                    file_path = os.path.join(folder_path, filename)
                    if race not in unit_data:
                        unit_data[race] = {}
                    unit_data[race][unit_name] = {
                        'file_name': filename,
                        'file_path': os.path.abspath(file_path)  # 使用绝对路径
                    }
    except FileNotFoundError:
        print(f"错误：找不到文件夹 '{folder_path}'")
        sys.exit(1)
    except PermissionError:
        print(f"错误：没有权限访问文件夹 '{folder_path}'")
        sys.exit(1)
    return unit_data

def save_to_yaml(data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
    except IOError as e:
        print(f"错误：无法保存到文件 '{output_file}': {e}")
        sys.exit(1)

def main():
    project_root = get_project_root()
    relative_folder_path = os.path.join('knowledge_data', 'firecrawl_test', 'sc2_unit_info_processed')
    folder_path = os.path.join(project_root, relative_folder_path)
    output_file = os.path.join(project_root, 'knowledge_data', 'database', 'sc2_unit_data_index.yaml')

    unit_data = scan_unit_files(folder_path)
    save_to_yaml(unit_data, output_file)

    total_units = sum(len(race_units) for race_units in unit_data.values())
    print(f"扫描了 {total_units} 个单位文件。")
    print(f"数据索引已保存到 {output_file}")

    # 打印简要摘要
    for race, units in unit_data.items():
        print(f"\n{race} 单位 ({len(units)}):")
        for unit_name in units:
            print(f"  - {unit_name}")

if __name__ == "__main__":
    main()