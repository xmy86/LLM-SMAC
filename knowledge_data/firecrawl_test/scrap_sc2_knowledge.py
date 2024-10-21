import json
from firecrawl import FirecrawlApp
import os
from datetime import datetime
import time
import requests
from knowledge_data import url
"""
根据liquidpedia上的星际争霸2单位信息，使用Firecrawl爬虫库爬取单位信息
url.py 文件中包含了单位的 URL 信息

需要设置proxy.
"""
# 配置
CONFIG = {
    "api_key": "fc-96cdb2de30954131b1a9e6cc8bb34d65",
    "proxy": {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    },
    "scrape_params": {
        "formats": ["markdown", "html"]
    },
    "output_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "sc2_unit_info"),
    "max_retries": 5,
    "retry_delay": 15,  # 秒
    "error_log_file": "scraping_errors.log"
}


def setup_proxy(proxy_config):
    for protocol, url in proxy_config.items():
        os.environ[f'{protocol.upper()}_PROXY'] = url


def save_result(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {filename}")


def log_error(message):
    with open(CONFIG["error_log_file"], 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")


def scrape_unit_with_retry(app, race, unit_name, unit_url):
    for attempt in range(CONFIG["max_retries"]):
        try:
            print(f"Scraping unit: {unit_name} (Attempt {attempt + 1})")
            scrape_status = app.scrape_url(unit_url, params=CONFIG["scrape_params"])

            # 保存单个单位的信息
            unit_filename = os.path.join(CONFIG["output_dir"], f"{race}_{unit_name}.json")
            save_result(scrape_status, unit_filename)

            return {unit_name: scrape_status}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limit exceeded. Waiting for {CONFIG['retry_delay']} seconds before retrying...")
                time.sleep(CONFIG['retry_delay'])
            elif e.response.status_code == 404:
                error_msg = f"URL not found for {unit_name}: {unit_url}"
                print(error_msg)
                log_error(error_msg)
                return {unit_name: {"error": "404 Not Found"}}
            else:
                error_msg = f"HTTP error occurred for {unit_name}: {e}"
                print(error_msg)
                log_error(error_msg)
                if attempt == CONFIG["max_retries"] - 1:
                    return {unit_name: {"error": str(e)}}
        except Exception as e:
            error_msg = f"An error occurred while scraping {unit_name}: {e}"
            print(error_msg)
            log_error(error_msg)
            if attempt == CONFIG["max_retries"] - 1:
                return {unit_name: {"error": str(e)}}

        time.sleep(CONFIG['retry_delay'])

    error_msg = f"Failed to scrape {unit_name} after {CONFIG['max_retries']} attempts"
    print(error_msg)
    log_error(error_msg)
    return {unit_name: {"error": "Max retries reached"}}


def main():
    app = FirecrawlApp(api_key=CONFIG["api_key"])
    setup_proxy(CONFIG["proxy"])

    # 创建输出目录
    os.makedirs(CONFIG["output_dir"], exist_ok=True)

    all_units_data = {}

    for race, units in url.knowledge_url["Unit"].items():
        print(f"Processing {race} units:")
        all_units_data[race] = {}
        for unit_name, unit_url in units.items():
            unit_data = scrape_unit_with_retry(app, race, unit_name, unit_url)
            all_units_data[race].update(unit_data)
            time.sleep(2)  # 在每次请求之间增加延迟

    # 保存所有单位的汇总信息
    consolidated_filename = os.path.join(CONFIG["output_dir"],
                                         f"all_units_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    save_result(all_units_data, consolidated_filename)

    print(f"Scraping completed. Check {CONFIG['error_log_file']} for any errors.")


if __name__ == "__main__":
    main()