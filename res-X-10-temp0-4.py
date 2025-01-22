
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

        enemy_colossus = self.enemy_units(UnitTypeId.COLOSSUS)
        enemy_stalkers = self.enemy_units(UnitTypeId.STALKER)
        enemy_zealots = self.enemy_units(UnitTypeId.ZEALOT)

        # Define the enemy position
        enemy_position = Point2((23, 16))

        # Colossus micro: Focus on enemy Zealots and Stalkers
        if colossus:
            colossus_unit = colossus.first
            if enemy_zealots or enemy_stalkers:
                closest_enemy = colossus_unit.find_closest(enemy_zealots | enemy_stalkers)
                if closest_enemy:
                    colossus_unit.attack(closest_enemy)

        # Stalker micro: Kite enemy units
        if stalkers:
            for stalker in stalkers:
                if enemy_zealots or enemy_stalkers:
                    closest_enemy = stalker.find_closest(enemy_zealots | enemy_stalkers)
                    if closest_enemy:
                        if stalker.distance_to(closest_enemy) < 6:  # Stalker attack range is 6
                            stalker.move(stalker.position.towards(closest_enemy, -4))  # Move away
                        else:
                            stalker.attack(closest_enemy)

        # Zealot micro: Engage in close combat
        if zealots:
            for zealot in zealots:
                if enemy_zealots or enemy_stalkers:
                    closest_enemy = zealot.find_closest(enemy_zealots | enemy_stalkers)
                    if closest_enemy:
                        zealot.attack(closest_enemy)

        # If no enemies are in range, move towards the enemy position
        if not (enemy_zealots or enemy_stalkers or enemy_colossus):
            if colossus:
                colossus.first.attack(enemy_position)
            if stalkers:
                for stalker in stalkers:
                    stalker.attack(enemy_position)
            if zealots:
                for zealot in zealots:
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
