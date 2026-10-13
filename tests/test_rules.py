from dungeon_agents.common.game_state import GameState
from dungeon_agents.common.weapon import longsword
from dungeon_agents.common.dice import Dice
from dungeon_agents.common.rules import resolve_attack

def test_resolve_attack():
    # Create a GameState for testing
    game_state = GameState(npc_hp=20, npc_ac=15)

    # Test case: Attack hits with a natural roll of 12 and an attack bonus of 4
    natural_roll = 12
    attack_bonus = 4
    hands_used = 1

    actual_damage = resolve_attack(game_state, longsword, hands_used, natural_roll, attack_bonus)

    # Check actual damage is within the expected range for a longsword one-handed attack (1d8)
    assert 1 <= actual_damage <= 8

    # Check that the NPC's HP has decreased appropriately
    assert game_state.npc_hp == 20 - actual_damage


def test_resolve_attack_misses():
    # Create a GameState for testing
    game_state = GameState(npc_hp=20, npc_ac=15)

    # Test case: Attack misses with a natural roll of 10 and an attack bonus of 2
    natural_roll = 10
    attack_bonus = 2
    hands_used = 1

    actual_damage = resolve_attack(game_state, longsword, hands_used, natural_roll, attack_bonus)

    # Check that no damage is dealt
    assert actual_damage == 0

    # Check that the NPC's HP remains unchanged
    assert game_state.npc_hp == 20


def test_resolve_attack_overkill(monkeypatch):
    # Create a GameState for testing
    game_state = GameState(npc_hp=3, npc_ac=15)

    # Define a fake roll_damage function to control the damage output
    def fake_roll_damage(damage_dice):
        return 7

    # Use monkeypatch to replace the roll_damage method in Dice with our fake function
    monkeypatch.setattr(
        Dice,
        "roll_damage",
        fake_roll_damage,
    )

    actual_damage = resolve_attack(
        game_state, longsword, 1, 12, 4
    )

    assert actual_damage == 3
    assert game_state.npc_hp == 0