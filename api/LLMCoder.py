from openai import OpenAI
from LLM.call_llm_api.call_llm import TextChatbot
from LLM.call_llm_api.call_llm import main_logger
import config
import os
import re
import subprocess
from multiprocessing import Process, Queue


class LLMCoder:

    def __init__(self):

        self.coder_bot = TextChatbot("coder")
        

        self.system_content = '''
You are a StarCraft II player and a helpful assistant and you are facing the micro-management tasks.
I will describe the map and the units on the map. You should not build any new buildings or new units or expand your base. 
You should concentrate on the micro-management strategy.
I will give you the strategy in JSON array format. The keys are 'tactic_name' and 'tactic_description'.
You should implement the strategy in python with burnysc2/pythonsc2 package.
You should concentrate on implementing the 'def async on_step(self, iteration: int):' function.
The result should be surrounded in the '```python' and '```' structure. 
'''

        # TODO: 1) The description of the units should be injected by database crawled from liquipedia.
        # Hard-coding here first.
        self.base_task_content = config.task_config + '''
You should not use the await keyword. Make sure to check whether the list variables are empty or not.
'''

        self.prefix_code = config.prefix_code
        self.post_code = config.post_code


    def generate_code(self, tactic, promotion=''):

        prompt = self.base_task_content +'\n'+promotion+'\n The tactic is: ' + str(tactic) + '\nPlease implement the code.'

        
        response = self.coder_bot.query(self.system_content, prompt, maintain_history=True)

        if 'async def on_step(self, iteration: int):' not in response:
            return None
        elif 'async def on_step(self, iteration: int):' in response:
            code = re.search(r'async def on_step\(self, iteration: int\):(.*?)```', response, re.DOTALL).group(1)
        elif 'def on_step(self, iteration: int):':
            code = re.search(r'def on_step\(self, iteration: int\):(.*?)```', response, re.DOTALL).group(1)
        
        total_code = self.prefix_code + '\n    async def on_step(self, iteration: int):\n' + code + self.post_code

        with open('res-temp.py', 'w') as writer:
            writer.write(total_code)

        return response






    def test_code(self, plan_idx, iter_idx):

        main_logger.debug('Start Testing')
        print('Start Testing')
        running = subprocess.Popen('python res-temp.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        invoke_result = running.stdout.read().decode('utf-8')
        

        units_num = 0
        enemy_num = 0
        v = 0
        d = 0
        t = 0

        score = 0
        damage_dealt = 0
        damage_taken = 0
        damage_shield = 0

        times = 10

        if 'Traceback' in invoke_result or 'Error' in invoke_result:
            # BUG
            print('-------------------BUG!!!--------------------')
            print(invoke_result)
            os.popen('mv res-temp.py res-{}-{}-temp{}-{}.py'.format('X', times, plan_idx, iter_idx))
            return {'type': 'bug', 'message': invoke_result}

        elif invoke_result == '':

            os.popen('mv res-temp.py res-{}-{}-temp{}-{}.py'.format('X', times, plan_idx, iter_idx))
            return {'type': 'bug', 'message': 'code incomplete'}

        else:
            

            q = Queue()

            process_list = []
            
            for _ in range(times):
                p = Process(target=run_game, args=(q,))
                p.start()
                process_list.append(p)

            for i in range(times):
                process_list[i].join()
            
            for _ in range(times):
                data = q.get()
                code_result = data['result']
                if code_result == 'bug':
                    os.popen('mv res-temp.py res-{}-{}-temp{}-{}.py'.format('X', times, plan_idx, iter_idx))
                    return {'type': 'bug', 'message': data['content']} 
                u, eu, r, s, dd, dt, ds = data['content']
                if r == 'v':
                    v += 1
                elif r == 'd':
                    d += 1
                else:
                    t += 1
                score += s
                damage_dealt += dd
                damage_taken += dt
                damage_shield += ds

                units_num += u
                enemy_num += eu

            score /= times
            damage_dealt /= times
            damage_taken /= times
            damage_shield /= times

            units_num /= times
            enemy_num /= times

            print('You Win {}, Tie {}, and Lose {} out of {} times. There are {} units and {} enemy units left.'.format(v, t, d, times, units_num, enemy_num))
            print('You achieve {} scores, give {} damages to the enemy, take {} damage on health, and take {} damage on shield on average.'.format(score, damage_dealt, damage_taken, damage_shield))
            main_logger.info('You Win {}, Tie {}, and Lose {} out of {} times. There are {} units and {} enemy units left.'.format(v, t, d, times, units_num, enemy_num) + 
            'You achieve {} scores, give {} damages to the enemy, take {} damage on health, and take {} damage on shield on average.'.format(score, damage_dealt, damage_taken, damage_shield)
                )


            os.popen('mv res-temp.py res-{}-{}-temp{}-{}.py'.format(v, times, plan_idx, iter_idx))

            for p in process_list:
                p.close()

            return {'type': 'result', 'message': {"win": v, "tie": t, "lose": d, "times": times, "score": score, "damage": damage_dealt, "damage_taken": damage_taken, "damage_shield": damage_shield, "units_num": units_num, "enemy_num": enemy_num}}


def run_game(q):

    r = ''

    running = subprocess.Popen('python res-temp.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = running.stdout.read().decode('utf-8')
    if 'Traceback' in result or 'Error' in result:
        q.put({'result': 'bug', 'content':result})
        return
    cells = result.split('\n')
    score = float(cells[1])
    damage_dealt = float(cells[2])
    damage_taken = float(cells[3])
    damage_shield = float(cells[4])
    unit_num = float(cells[5])
    enemy_unit_num = float(cells[6])
    if 'Result.Victory' in result:
        r = 'v'
        enemy_unit_num = 0
    elif 'Result.Defeat' in result:
        r = 'd'
        unit_num = 0
    else: 
        r = 't'
    q.put({'result': 'data', 'content':(unit_num, enemy_unit_num, r, score, damage_dealt, damage_taken, damage_shield)})
