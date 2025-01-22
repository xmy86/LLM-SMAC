
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

        # Get all your units
        colossus: Units = self.units(UnitTypeId.COLOSSUS)
        stalkers: Units = self.units(UnitTypeId.STALKER)
        zealots: Units = self.units(UnitTypeId.ZEALOT)

        # Get enemy units
        enemy_colossus: Units = self.enemy_units(UnitTypeId.COLOSSUS)
        enemy_stalkers: Units = self.enemy_units(UnitTypeId.STALKER)
        enemy_zealots: Units = self.enemy_units(UnitTypeId.ZEALOT)

        # If no units are available, do nothing
        if not colossus or not stalkers or not zealots:
            return

        # Colossus micro: Focus on enemy Zealots first, then Stalkers
        if colossus:
            colossus_unit: Unit = colossus.first
            if enemy_zealots:
                colossus_unit.attack(enemy_zealots.closest_to(colossus_unit))
            elif enemy_stalkers:
                colossus_unit.attack(enemy_stalkers.closest_to(colossus_unit))
            else:
                colossus_unit.attack(enemy_colossus.closest_to(colossus_unit))

        # Stalker micro: Kite enemy Zealots and focus on enemy Stalkers
        if stalkers:
            for stalker in stalkers:
                if enemy_zealots:
                    closest_enemy_zealot = enemy_zealots.closest_to(stalker)
                    if stalker.distance_to(closest_enemy_zealot) < 6:
                        stalker.move(stalker.position.towards(closest_enemy_zealot, -4))
                    else:
                        stalker.attack(closest_enemy_zealot)
                elif enemy_stalkers:
                    closest_enemy_stalker = enemy_stalkers.closest_to(stalker)
                    stalker.attack(closest_enemy_stalker)
                else:
                    stalker.attack(enemy_colossus.closest_to(stalker))

        # Zealot micro: Tank damage and focus on enemy Zealots, then Stalkers
        if zealots:
            for zealot in zealots:
                if enemy_zealots:
                    zealot.attack(enemy_zealots.closest_to(zealot))
                elif enemy_stalkers:
                    zealot.attack(enemy_stalkers.closest_to(zealot))
                else:
                    zealot.attack(enemy_colossus.closest_to(zealot))

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
