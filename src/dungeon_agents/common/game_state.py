from dataclasses import dataclass


@dataclass
class GameState:
    npc_hp: int = 20
    npc_ac: int = 15

    def check_attack(self, natural_roll: int, attack_bonus: int) -> bool:
        """Check if the attack roll hits the NPC based on its armor class."""
        if natural_roll < 1 or natural_roll > 20:
            raise ValueError("Natural roll must be between 1 and 20.")
        
        if natural_roll == 20:
            # Critical hit always hits
            return True
       
        if natural_roll == 1:
            # Critical miss always misses
            return False
        
        return (natural_roll + attack_bonus) >= self.npc_ac

    def apply_damage(self, damage: int) -> None:
        """Apply damage to the NPC's HP, ensuring it doesn't go below zero."""
        if damage < 0:
            raise ValueError("Damage cannot be negative.")

        self.npc_hp = max(0, self.npc_hp - damage)

    def is_npc_alive(self) -> bool:
        """Check if the NPC is still alive."""
        return self.npc_hp > 0

if __name__ == "__main__":
    # Example usage
    state = GameState()

    state.apply_damage(6)
    assert state.npc_hp == 14
    assert state.is_npc_alive()

    state.apply_damage(100)
    assert state.npc_hp == 0
    assert not state.is_npc_alive()
    print("All tests passed!")