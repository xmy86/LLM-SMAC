# LLM-SMAC

<p align="center">
  <img src="asset/3m.gif" width="250"/>
  <img src="asset/2m_vs_1z.gif" width="250"/>
  <img src="asset/3s5z.gif" width="250"/><br/>
  <img src="asset/bane_vs_bane.gif" width="250"/>
  <img src="asset/3s_vs_3z.gif" width="250"/>
  <img src="asset/1c3s5z.gif" width="250"/><br/>
  <img src="asset/2c_vs_64zg.gif" width="250"/>
  <img src="asset/MMM.gif" width="250"/>
  <img src="asset/corridor.gif" width="250"/><br/>
  <img src="asset/10m_vs_11m.gif" width="250"/>
  <img src="asset/so_many_baneling.gif" width="250"/>
  <img src="asset/27m_vs_30m.gif" width="250"/><br/>
  <i>Demos of LLM-SMAC tasks</i>
</p>



## Quick Start Guide

### Get StarCraft II

LLM-SMAC depends on the full StarCraft II game and works with version of burnysc2/python-sc2 package.

#### Linux

Follow Blizzard's [documentation](https://github.com/Blizzard/s2client-proto#downloads) to
get the linux version. By default, LLM-SMAC expects the game to live in
`~/StarCraftII/`. You can override this path by setting the `SC2PATH`
environment variable or creating your own run_config.

#### Windows/MacOS

Install of the game as normal from [Battle.net](https://battle.net). Even the
[Starter Edition](http://battle.net/sc2/en/legacy-of-the-void/) will work.
If you used the default install location LLM-SMAC should find the latest binary.
If you changed the install location, you might need to set the `SC2PATH`
environment variable with the correct location.

 Note that the version of StarCraft II on Linux platform supports upto 4.10, however, the latest version on Windows/Macos is upto 5.0.13. Therefore, the results across the operating system might not be consistent.

### Get LLM-SMAC

Download the LLM-SMAC code from this github page.

Use pip install to initialize the environment:

```shell
$ conda create --name YOUR_ENV_NAME python==3.10
$ conda activate YOUR_ENV_NAME
$ pip install -r requirements.txt
```

### Replace sc2 Folder and Maps

1. The sc2 folder is modified according to the SMAC task. We modified the log level as 'CRITICAL' and modify the bot_ai_internal.py of sc2 file because the start_location and the enemy_start_locations cannot be acquired without the 'townhall'. 
2. We modify the maps of original SMAC tasks and add the victory, tie, and defeat judgments. We also set a timeout mechanism to solve the problem of unfinished tasks. 


### Replace your API key

You may fill your api key to the file 'configs\llm_api_config.py'

    class LLMAPIConfig:
        # LLM 配置
        MODELS = {
            "deepseek-chat": LLMModelConfig(
                api_key="Your API key here.",
                base_url="Base URL here."
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

### Customize the planner, coder, and critic model

You may customize the models from DeepSeek to other models by applying the corresponding API key in 'configs\llm_api_config.py'

~~~
TASK_MODELS = {
        "planner": "gpt-4",
        "coder": "gpt-4",
        "summarizer": "claude-3-5-sonnet-20240620"
    }
~~~


### How to run

```shell
# Change the information in the config.py, then
$ python main.py
```

After applying the command, there should be a log file in the root directory which can be modified in the file 'LLM\call\_llm_api\call_llm.py'

The generated scripts are also in the root directory, which named as 'res-Victory_Times-Test_Times-Planning_Round-Coding_Round'. When new experiments are conducted, the previously generated Python scripts will be **REMOVED**, so make sure you have store the results.

