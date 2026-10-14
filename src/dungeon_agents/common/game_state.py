from dataclasses import dataclass

from dungeon_agents.common.combatant import Combatant


@dataclass
class GameState:
    combatants: list[Combatant]

    def get_combatant_by_name(self, name: str) -> Combatant:
        """Retrieve a combatant by name from the list of combatants."""
        for combatant in self.combatants:
            if combatant.name == name:
                return combatant
        raise ValueError(f"Combatant with name '{name}' not found.")

    def check_attack(self, target: Combatant, natural_roll: int, attack_bonus: int) -> bool:
        """Check if the attack roll hits the target based on its armor class."""

        if natural_roll < 1 or natural_roll > 20:
            raise ValueError("Natural roll must be between 1 and 20.")
        
        if natural_roll == 20:
            # Critical hit always hits
            return True
       
        if natural_roll == 1:
            # Critical miss always misses
            return False
        
        return (natural_roll + attack_bonus) >= target.ac

    def apply_damage(self, target: Combatant, damage: int) -> int:
        """Apply damage to the combatant's HP, ensuring it doesn't go below zero."""
        if damage < 0:
            raise ValueError("Damage cannot be negative.")
        new_hp = max(0, target.hp - damage)

        # Calculate the actual damage applied (in case of overkill)
        actual_damage = target.hp - new_hp
        target.hp = new_hp
        return actual_damage

    def is_combatant_alive(self, combatant: Combatant) -> bool:
        """Check if the combatant is still alive."""
        return combatant.hp > 0

    def get_alive_combatants(self) -> list[Combatant]:
        """Return a list of combatants that are still alive."""
        return [combatant for combatant in self.combatants if self.is_combatant_alive(combatant)]
