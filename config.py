map_config = '''The map is a 32*32 sized square map. 
The available area of x axis is from 0 to 32, and the y axis is from 7 to 25.
The enemy units are at (23, 16) point and your Stalker units are at (9, 16) point initially.
The ememy controls all the enemy units to move and attack towards (9, 16) point along the way.
There is no terrain advantages nor choke points in this map. You cannot get back to the enemy units.
'''

unit_config = '''The map is 1c3s5z.
You can control 1 Colossus unit, 3 Stalker units and 5 Zealot Units.
The enemy also controls 1 Colossus unit, 3 Stalker units and 5 Zealot Units
The Colossus unit has 200 health, 150 shield, 1 defense, 7 attacking range, 3.15 speed, 10*2 damage with 18.7 DPS.
The Stalker unit has 80 health, 80 shield, 1 defense, 6 attacking range, 4.13 speed, 13 damage with 9.7 DPS.
The Zealot unit has 100 health, 50 shield, 1 defense, 0.1 attacking range, 3.15 speed, 8*2 damage with 18.6 DPS.
All the units has no abilities such as blinking or equipments. The hate value will directly change to other units in range after retreat.
'''


task_config = unit_config + map_config

map_name = '1c3s5z'


prefix_code = '''
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race, Difficulty
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
import math
import random

class MarineBot(BotAI):
'''

post_code = '''
if __name__ == '__main__':
    bot = MarineBot()
    result = run_game(maps.get('{}'), [Bot(Race.Random, bot), Computer(Race.Random, Difficulty.VeryHard)], realtime=False)
    print(result)
    print(bot.state.score.score)
    print(bot.state.score.total_damage_dealt_life)
    print(bot.state.score.total_damage_taken_life)
    print(bot.state.score.total_damage_taken_shields)
    print(len(bot.units))
    print(len(bot.enemy_units)+ len(bot.enemy_structures))
'''.format(map_name)

    
