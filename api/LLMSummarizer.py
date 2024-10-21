from openai import OpenAI
import config
from LLM.call_llm_api.call_llm import TextChatbot

class LLMSummarizer:

    def __init__(self):

        self.summarizer_bot = TextChatbot("summarizer")

        self.system_content = '''
You are a StarCraft II player and a helpful assistant and you are facing the micro-management tasks.
You are now working as a critic.
I will describe the map and the units on the map. You should not build any new buildings or new units. 
After that, I will provide you the tactic and the python script which is the implementation of this tactic.
You should concentrate on the micro-management strategy to kill more enemy and preserve more units of yourself.
I will also provide you the result of the code, which might be the bug stacktrace or the combat results.
You should analyse why the code leads to the result and tell me the potential method to improve the performance based on the code. 
You can suggest improve the current tactic or delete some tactic based on the current code.
You do not need to provide me the refinement code.
After that you should provide me a suggestion from ```[Change Tactic]``` or ```[Improve Tactic]```
'''

    def summarize(self, code, result):
        
        if type(result) == dict:
            result = '''
You win {} times, tie {} times, and lose {} times out of {} combats. There are {} units and {} enemy units left. You achieve {} scores, give {} damages to the enemy, take {} damage on health, and take {} damage on shield on average.
'''.format(result["win"], result["tie"], result["lose"], result["times"], result["units_num"], result["enemy_num"], result["score"], result["damage"], result["damage_taken"], result["damage_shield"])


        task_content = config.task_config + '''

The code is: 
{}

The result is: 
{}

You should check whether the api you invoked follows the burnysc2/python-sc2 package.
Please summarize why the code cause the result.
Meanwhile, please briefly provide me 1 most important refinement of the tactic aiming at killing more enemy units and cause more damage.
Do not show the revised code to me.
'''.format(code, result)

    
        response = self.summarizer_bot.query(self.system_content, task_content, maintain_history=False)


        return response
    

