
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

        # Update unit references
        self.colossus = self.units(UnitTypeId.COLOSSUS).first
        self.stalkers = self.units(UnitTypeId.STALKER)
        self.zealots = self.units(UnitTypeId.ZEALOT)

        enemy_colossus = self.enemy_units(UnitTypeId.COLOSSUS).first
        enemy_stalkers = self.enemy_units(UnitTypeId.STALKER)
        enemy_zealots = self.enemy_units(UnitTypeId.ZEALOT)

        # Tactic 1: Colossus Focus Fire
        if enemy_colossus and self.colossus.distance_to(enemy_colossus) <= 7:
            self.colossus.attack(enemy_colossus)
            for stalker in self.stalkers:
                if stalker.distance_to(enemy_colossus) <= 6:
                    stalker.attack(enemy_colossus)
            for zealot in self.zealots:
                if zealot.distance_to(enemy_zealots.closest_to(zealot)) <= 0.1:
                    zealot.attack(enemy_zealots.closest_to(zealot))

        # Tactic 2: Stalker Kiting
        elif enemy_zealots and self.stalkers:
            for stalker in self.stalkers:
                closest_enemy_zealot = enemy_zealots.closest_to(stalker)
                if stalker.distance_to(closest_enemy_zealot) <= 6:
                    stalker.move(stalker.position.towards(self.colossus, 4))
                    stalker.attack(closest_enemy_zealot)
            if self.colossus:
                self.colossus.attack(enemy_zealots.closest_to(self.colossus))
            for zealot in self.zealots:
                if zealot.distance_to(enemy_zealots.closest_to(zealot)) <= 0.1:
                    zealot.attack(enemy_zealots.closest_to(zealot))

        # Tactic 3: Zealot Rush
        elif enemy_stalkers and self.zealots:
            for zealot in self.zealots:
                closest_enemy_stalker = enemy_stalkers.closest_to(zealot)
                if zealot.distance_to(closest_enemy_stalker) <= 0.1:
                    zealot.attack(closest_enemy_stalker)
            if self.colossus:
                self.colossus.attack(enemy_stalkers.closest_to(self.colossus))
            for stalker in self.stalkers:
                if stalker.distance_to(enemy_zealots.closest_to(stalker)) <= 6:
                    stalker.attack(enemy_zealots.closest_to(stalker))

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
