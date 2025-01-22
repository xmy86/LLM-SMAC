
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
        colossus = self.units(UnitTypeId.COLOSSUS).first
        stalkers = self.units(UnitTypeId.STALKER)
        zealots = self.units(UnitTypeId.ZEALOT)

        # Enemy position
        enemy_position = Point2((23, 16))

        # Colossus micro: Stay behind Stalkers and Zealots, attack enemy units
        if colossus:
            if stalkers:
                colossus_position = stalkers.center.towards(enemy_position, -4)
                self.do(colossus.move(colossus_position))
            if self.enemy_units.closer_than(7, colossus):
                self.do(colossus.attack(self.enemy_units.closest_to(colossus)))

        # Stalker micro: Kite enemy units, focus fire on enemy Colossus
        for stalker in stalkers:
            if self.enemy_units.closer_than(6, stalker):
                closest_enemy = self.enemy_units.closest_to(stalker)
                if closest_enemy.type_id == UnitTypeId.COLOSSUS:
                    self.do(stalker.attack(closest_enemy))
                else:
                    self.do(stalker.move(stalker.position.towards(enemy_position, -4)))
            else:
                self.do(stalker.attack(enemy_position))

        # Zealot micro: Tank damage, focus on enemy Zealots and Stalkers
        for zealot in zealots:
            if self.enemy_units.closer_than(0.1, zealot):
                closest_enemy = self.enemy_units.closest_to(zealot)
                if closest_enemy.type_id in {UnitTypeId.ZEALOT, UnitTypeId.STALKER}:
                    self.do(zealot.attack(closest_enemy))
                else:
                    self.do(zealot.move(zealot.position.towards(enemy_position, 2)))
            else:
                self.do(zealot.move(enemy_position))

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
