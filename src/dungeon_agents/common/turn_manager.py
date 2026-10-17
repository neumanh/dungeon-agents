from dungeon_agents.common.game_state import GameState
from dungeon_agents.common.dice import Dice
from dungeon_agents.common.combatant import Combatant

class TurnManager:
    def __init__(self, game_state: GameState):
        self.game_state: GameState = game_state
        self.initiative_order: list[tuple[Combatant, int]] = []

    def set_initiative_order(self):
        # This method does 3 things:
        # 1. Rolls initiative for each combatant
        # 2. Sorts the combatants based on their initiative rolls + dexterity modifier
        # 3. Stores the sorted order in self.initiative_order

        # 1. Roll a d20 for initiative and add the dexterity modifier
        initiative_rolls = []
        alive_combatants = self.game_state.get_alive_combatants()
        for combatant in alive_combatants:
            current_initiative = Dice.roll_dice(20) + combatant.dexterity_modifier
            initiative_rolls.append((combatant, current_initiative)) 

        # 2. Sort the combatants based on their initiative rolls in descending order
        initiative_rolls.sort(key=lambda x: x[1], reverse=True)

        # 3. Store the sorted combatants in self.initiative_order
        self.initiative_order = initiative_rolls