
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
        colossus = self.units(UnitTypeId.COLOSSUS).first
        stalkers = self.units(UnitTypeId.STALKER)
        zealots = self.units(UnitTypeId.ZEALOT)

        # Get enemy units
        enemy_colossus = self.enemy_units(UnitTypeId.COLOSSUS).first
        enemy_stalkers = self.enemy_units(UnitTypeId.STALKER)
        enemy_zealots = self.enemy_units(UnitTypeId.ZEALOT)

        # Define the initial position of our Stalkers
        initial_stalker_position = Point2((9, 16))

        # If our Colossus is alive, focus on kiting enemy Zealots
        if colossus:
            enemy_zealots_in_range = self.enemy_units.filter(
                lambda unit: unit.type_id == UnitTypeId.ZEALOT and unit.distance_to(colossus) <= 7
            )
            if enemy_zealots_in_range:
                # Move away from enemy Zealots while attacking
                colossus.move(colossus.position.towards(initial_stalker_position, -7))
                colossus.attack(enemy_zealots_in_range.closest_to(colossus))
            else:
                # Attack the closest enemy unit
                closest_enemy = self.enemy_units.closest_to(colossus)
                if closest_enemy:
                    colossus.attack(closest_enemy)

        # Control Stalkers to focus on enemy Colossus
        if stalkers:
            if enemy_colossus:
                for stalker in stalkers:
                    stalker.attack(enemy_colossus)
            else:
                # If no enemy Colossus, attack the closest enemy unit
                for stalker in stalkers:
                    closest_enemy = self.enemy_units.closest_to(stalker)
                    if closest_enemy:
                        stalker.attack(closest_enemy)

        # Control Zealots to engage enemy Stalkers
        if zealots:
            if enemy_stalkers:
                for zealot in zealots:
                    zealot.attack(enemy_stalkers.closest_to(zealot))
            else:
                # If no enemy Stalkers, attack the closest enemy unit
                for zealot in zealots:
                    closest_enemy = self.enemy_units.closest_to(zealot)
                    if closest_enemy:
                        zealot.attack(closest_enemy)

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
