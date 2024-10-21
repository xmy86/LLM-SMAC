from openai import OpenAI
from LLM.call_llm_api.call_llm import TextChatbot
import config
import re

class LLMPlanner:

    def __init__(self):
        
        self.planner_bot = TextChatbot("planner")

        self.system_content = '''
You are a StarCraft II player and a helpful assistant and you are facing the micro-management tasks.
I will describe the map and the units on the map. You should not build any new buildings or new units. 
You may focus on micro-management tactics to win the combat. 
You should provide me the tactics in the format below:
### Tactic 1: Tactic 1' name
**Condition to use:**
**Tactic Skeleton**

### Tactic 2: Tactic 2' name
**Condition to use:**
**Tactic Skeleton**

Meanwhile, I will tell you history taken tactics, you may add new tactics onto the history tactics by adding new tactic in the list or try a new tactic. 
'''

        self.task_content = config.task_config + '''
You should provide me with less than at most 3 most important tactics and describe the chosen tactic skeleton in detail according to the situations of your unit and enemy units.
You should also indicate the condition to use this tactic. Make sure the conditions are not conflict with each other.
'''

        self.tactic_history = {}



    def plan(self, message=None):

        if not message==None:
            # The keys of message dictionary are:
            # {"win": 0, "tie": 0, "lose": 10, "score": 50, "damage": 276.8, "damage_taken": 147, "damage_shield": 160}

            if type(message) == str:
                result = '''The generated code has bug which might not be the reason from you. '''
            else:
                result = '''
You win {} times, tie {} times, and lose {} times out of {} combats. There are {} units and {} enemy units left. You achieve {} scores, give {} damages to the enemy, take {} damage on health, and take {} damage on shield on average.
'''.format(message["win"], message["tie"], message["lose"], message["times"], message["units_num"], message["enemy_num"], message["score"], message["damage"], message["damage_taken"], message["damage_shield"])


            history = 'The history strategy and the results are: '
            for k, v in self.tactic_history.items():
                history += '[{}]: {} scores, '.format(k, v[0])

            result_message = result + ' ' + history + 'To improve the winning rates, you may change a new tactic or add a new tactics based on one of the history strategies.'


        response = self.planner_bot.query(self.system_content, self.task_content if message==None else result_message, maintain_history=True)

        return response
    


    def update_history(self, name, score):
        if name not in self.tactic_history:
            self.tactic_history[name] = (score, 1)
        else:
            avg_score = self.tactic_history[name][0]
            times = self.tactic_history[name][1]
            new_score = (avg_score * times + score) / (times + 1) 
            self.tactic_history[name] = (new_score, times+1)

    def retrival_information(self, tactic):
        retrived_name = re.findall(r'### Tactic (.*?)\n', tactic, re.DOTALL)
        return [t.split(': ')[1] for t in retrived_name]
