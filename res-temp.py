
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

    async def on_step(self, iteration: int):

        # Define your units
        colossus: Units = self.units(UnitTypeId.COLOSSUS)
        stalkers: Units = self.units(UnitTypeId.STALKER)
        zealots: Units = self.units(UnitTypeId.ZEALOT)

        # Define enemy units
        enemy_units: Units = self.enemy_units
        enemy_colossus: Units = enemy_units(UnitTypeId.COLOSSUS)
        enemy_stalkers: Units = enemy_units(UnitTypeId.STALKER)
        enemy_zealots: Units = enemy_units(UnitTypeId.ZEALOT)

        # Define positions
        enemy_position: Point2 = Point2((23, 16))
        my_position: Point2 = Point2((9, 16))

        # Micro for Colossus
        if colossus:
            for col in colossus:
                if enemy_colossus:
                    col.attack(enemy_colossus.closest_to(col))
                elif enemy_stalkers:
                    col.attack(enemy_stalkers.closest_to(col))
                else:
                    col.attack(enemy_position)

        # Micro for Stalkers
        if stalkers:
            for stalker in stalkers:
                if enemy_stalkers:
                    if stalker.distance_to(enemy_stalkers.closest_to(stalker)) > 6:
                        stalker.attack(enemy_stalkers.closest_to(stalker))
                    else:
                        stalker.move(stalker.position.towards(my_position, 3))
                elif enemy_zealots:
                    if stalker.distance_to(enemy_zealots.closest_to(stalker)) > 6:
                        stalker.attack(enemy_zealots.closest_to(stalker))
                    else:
                        stalker.move(stalker.position.towards(my_position, 3))
                else:
                    stalker.attack(enemy_position)

        # Micro for Zealots
        if zealots:
            for zealot in zealots:
                if enemy_zealots:
                    zealot.attack(enemy_zealots.closest_to(zealot))
                elif enemy_stalkers:
                    zealot.attack(enemy_stalkers.closest_to(zealot))
                else:
                    zealot.attack(enemy_position)

if __name__ == '__main__':
    bot = MarineBot()
    result = run_game(maps.get('1c3s5z'), [Bot(Race.Random, bot), Computer(Race.Random, Difficulty.VeryHard)], realtime=False)
    print(result)
    print(bot.state.score.score)
    print(bot.state.score.total_damage_dealt_life)
    print(bot.state.score.total_damage_taken_life)
    print(bot.state.score.total_damage_taken_shields)
    print(len(bot.units))
    print(len(bot.enemy_units)+ len(bot.enemy_structures))
