# llm_api_config.py

class LLMModelConfig:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def __repr__(self):
        # 隐藏完整的 API 密钥，只显示前 6 个字符
        masked_api_key = self.api_key[:6] + "*" * (len(self.api_key) - 6)
        return f"LLMModelConfig(api_key='{masked_api_key}', base_url='{self.base_url}')"

class LLMAPIConfig:
    # LLM 配置
    MODELS = {
        "deepseek-chat": LLMModelConfig(
            api_key="sk-9b13a70fa21a4595b233134c523dcb9e",
            base_url="https://api.deepseek.com"
        ),
        "deepseek-coder": LLMModelConfig(
            api_key="Your API key here.",
            base_url="Base URL here."
        ),
        "gpt-4": LLMModelConfig(
            api_key="Your API key here.",
            base_url="Base URL here."
        ),
        "Qwen2.5-72B-Instruct": LLMModelConfig(
            api_key="Your API key here.",
            base_url="Base URL here."
        ),
        "claude-3-5-sonnet-20240620": LLMModelConfig(
            api_key="Your API key here.",
            base_url="Base URL here."
        ),
    }
    """
    test
    """
    
    TASK_MODELS = {
        "planner": "deepseek-chat",
        "coder": "deepseek-chat",
        "summarizer": "deepseek-chat"
    }
    @classmethod
    def get_model_config(cls, model_name):
        return cls.MODELS.get(model_name)

    @classmethod
    def get_task_model(cls, task):
        model_name = cls.TASK_MODELS.get(task)
        return cls.get_model_config(model_name)

if __name__ == '__main__':
    config = LLMAPIConfig()
    print("Model config for deepseek_chat:")
    print(config.get_model_config("deepseek_chat"))
    print("\nModel config for planner task:")
    print(config.get_task_model("planner"))