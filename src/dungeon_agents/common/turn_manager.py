from dungeon_agents.common.game_state import GameState
from dungeon_agents.common.dice import Dice
from dungeon_agents.common.combatant import Combatant

class TurnManager:
    def __init__(self, game_state: GameState):
        self.game_state: GameState = game_state
        self.initiative_order: list[tuple[Combatant, int]] = []
        self.current_turn_index = 0

    def set_initiative_order(self) -> None:
        # This method does 3 things:
        # 1. Rolls initiative for each combatant
        # 2. Sorts the combatants based on their initiative rolls + dexterity modifier
        # 3. Stores the sorted order in self.initiative_order

        self.current_turn_index = 0

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

    def advance_turn(self) -> None:
        # Move to the next live combatant in the initiative order
        if not self.initiative_order:
            raise ValueError("Initiative order is empty. Please set the initiative order first.")
        
        # If all combatants gone - dont advance
        alive_combatants = self.game_state.get_alive_combatants()
        if not alive_combatants:
            return None

        # Get next alive player
        next_index = (self.current_turn_index + 1) % len(self.initiative_order)
        loop_index = 0
        while loop_index < len(self.initiative_order):
            if self.initiative_order[next_index][0].hp > 0:
                self.current_turn_index = next_index
                break

            next_index = (next_index + 1) % len(self.initiative_order)
            loop_index += 1
    
    def get_next_player(self) -> Combatant | None:
        # Return the combatant whose turn it is next

        # If initiative_order is not set - return None
        if not self.initiative_order:
            return None

        # If all combatants gone - return None
        alive_combatants = self.game_state.get_alive_combatants()
        if not alive_combatants:
            return None

        if (self.current_turn_index >= len(self.initiative_order)) or (self.current_turn_index < 0):
            # Raise a value error
            raise ValueError("The current index is larger than the number of combatants.")
        
        current_player = self.initiative_order[self.current_turn_index][0]

        if current_player.hp > 0:
            return current_player
        return None
