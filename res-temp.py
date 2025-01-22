
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

        # Get all our units
        colossus = self.units(UnitTypeId.COLOSSUS)
        stalkers = self.units(UnitTypeId.STALKER)
        zealots = self.units(UnitTypeId.ZEALOT)

        # Get enemy units
        enemy_colossus = self.enemy_units(UnitTypeId.COLOSSUS)
        enemy_stalkers = self.enemy_units(UnitTypeId.STALKER)
        enemy_zealots = self.enemy_units(UnitTypeId.ZEALOT)

        # Target position for kiting
        target_position = Point2((9, 16))

        # Colossus micro: Focus on enemy Zealots and Stalkers
        if colossus:
            colossus_unit = colossus.first
            if enemy_zealots:
                colossus_unit.attack(enemy_zealots.closest_to(colossus_unit))
            elif enemy_stalkers:
                colossus_unit.attack(enemy_stalkers.closest_to(colossus_unit))
            else:
                colossus_unit.attack(target_position)

        # Stalker micro: Kite enemy units
        if stalkers:
            for stalker in stalkers:
                if enemy_zealots:
                    closest_enemy = enemy_zealots.closest_to(stalker)
                    if stalker.distance_to(closest_enemy) < 6:
                        stalker.move(stalker.position.towards(target_position, -4))
                    else:
                        stalker.attack(closest_enemy)
                elif enemy_stalkers:
                    closest_enemy = enemy_stalkers.closest_to(stalker)
                    if stalker.distance_to(closest_enemy) < 6:
                        stalker.move(stalker.position.towards(target_position, -4))
                    else:
                        stalker.attack(closest_enemy)
                else:
                    stalker.attack(target_position)

        # Zealot micro: Tank and attack closest enemy
        if zealots:
            for zealot in zealots:
                if enemy_zealots:
                    zealot.attack(enemy_zealots.closest_to(zealot))
                elif enemy_stalkers:
                    zealot.attack(enemy_stalkers.closest_to(zealot))
                elif enemy_colossus:
                    zealot.attack(enemy_colossus.closest_to(zealot))
                else:
                    zealot.attack(target_position)

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
