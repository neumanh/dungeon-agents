from dungeon_agents.common import game_state
from dungeon_agents.common.game_state import GameState
from dungeon_agents.common.weapon import longsword
from dungeon_agents.common.dice import Dice
from dungeon_agents.common.rules import resolve_attack
from dungeon_agents.common.npc import NPC
from dungeon_agents.common.character import Character
from dungeon_agents.common.turn_manager import TurnManager

def test_resolve_attack():
    # Create a GameState for testing
    target = NPC(name="Goblin 1", dexterity_modifier=2, ac=15, hp=20)
    game_state = GameState(combatants=[target])

    # Test case: Attack hits with a natural roll of 12 and an attack bonus of 4
    natural_roll = 12
    attack_bonus = 4
    hands_used = 1

    actual_damage = resolve_attack(game_state, target, longsword, hands_used, natural_roll, attack_bonus)

    # Check actual damage is within the expected range for a longsword one-handed attack (1d8)
    assert 1 <= actual_damage <= 8

    # Check that the NPC's HP has decreased appropriately
    assert target.hp == 20 - actual_damage


def test_resolve_attack_misses(monkeypatch):
    # Create a GameState for testing
    target = NPC(name="Goblin 1", dexterity_modifier=2, ac=15, hp=20)
    game_state = GameState(combatants=[target])

    # Test case: Attack misses with a natural roll of 10 and an attack bonus of 2
    natural_roll = 10
    attack_bonus = 2
    hands_used = 1

    actual_damage = resolve_attack(game_state, target, longsword, hands_used, natural_roll, attack_bonus)

    # Check that no damage is dealt
    assert actual_damage == 0

    # Check that the NPC's HP remains unchanged
    assert target.hp == 20


def test_resolve_attack_overkill(monkeypatch):
    # Create a GameState for testing
    target = NPC(name="Goblin 1", dexterity_modifier=2, ac=15, hp=3)
    game_state = GameState(combatants=[target])

    # Define a fake roll_damage function to control the damage output
    def fake_roll_damage(damage_dice):
        return 7

    # Use monkeypatch to replace the roll_damage method in Dice with our fake function
    monkeypatch.setattr(
        Dice,
        "roll_damage",
        fake_roll_damage,
    )

    actual_damage = resolve_attack(game_state, target,longsword, 1, 12, 4)

    assert actual_damage == 3
    assert target.hp == 0


def test_resolve_attack_misses_does_not_roll_damage(monkeypatch):
    # Create a GameState for testing
    target = NPC(name="Goblin 1", dexterity_modifier=2, ac=15, hp=20)
    game_state = GameState(combatants=[target])
    
    # Validate no dice is rolled when the attack misses
    def fail_if_called(damage_dice):
        raise AssertionError("Damage should not be rolled on a miss")

    monkeypatch.setattr(
        Dice,
        "roll_damage",
        fail_if_called,
    )

    actual_damage = resolve_attack(game_state, target,longsword, 1, 10, 2)

    # Check that no damage is dealt
    assert actual_damage == 0

    # Check that the NPC's HP remains unchanged
    assert target.hp == 20


def test_attacks_between_character_and_npc():
    # Create a GameState for testing
    npc = NPC(name="Goblin 1", dexterity_modifier=2, ac=15, hp=20)
    character = Character(name="Hero", dexterity_modifier=3, ac=16, hp=30)
    game_state = GameState(combatants=[npc, character])

    # Test case: Hero attacks Goblin 1 with a natural roll of 12 and an attack bonus of 4
    natural_roll = 12
    attack_bonus = 4
    hands_used = 2

    actual_damage = resolve_attack(game_state, npc, longsword, hands_used, natural_roll, attack_bonus)

    # Check actual damage is within the expected range for a longsword two-handed attack (1d10)
    assert 1 <= actual_damage <= 10

    # Check that the NPC's HP has decreased appropriately
    assert npc.hp == 20 - actual_damage

    # Test case: Goblin 1 attacks Hero with a natural roll of 15 and an attack bonus of 2
    natural_roll = 15
    attack_bonus = 2
    hands_used = 1

    actual_damage = resolve_attack(game_state, character, longsword, hands_used, natural_roll, attack_bonus)

    # Check actual damage is within the expected range for a longsword one-handed attack (1d8)
    assert 1 <= actual_damage <= 8

    # Check that the character's HP has decreased appropriately
    assert character.hp == 30 - actual_damage

def test_get_live_combatants():
    # Create a GameState for testing
    npc1 = NPC(name="Goblin 1", dexterity_modifier=2, ac=15, hp=0)  # Dead
    npc2 = NPC(name="Goblin 2", dexterity_modifier=2, ac=15, hp=10)  # Alive
    character = Character(name="Hero", dexterity_modifier=3, ac=16, hp=30)  # Alive
    game_state = GameState(combatants=[npc1, npc2, character])

    alive_combatants = game_state.get_alive_combatants()

    # Check that only the alive combatants are returned and that the dead combatant kept in game_state
    assert len(alive_combatants) == 2
    assert npc2 in alive_combatants
    assert character in alive_combatants
    assert npc1 not in alive_combatants
    assert len(game_state.combatants) == 3
    assert npc1 in game_state.combatants

def test_set_initiative_order(monkeypatch):
    # Create a GameState for testing
    npc1 = NPC(name="Goblin 1", dexterity_modifier=0, ac=15, hp=10)
    npc2 = NPC(name="Goblin 2", dexterity_modifier=0, ac=15, hp=0)
    character = Character(name="Hero", dexterity_modifier=0, ac=16, hp=30)
    game_state = GameState(combatants=[npc1, npc2, character])

    # Create a fake dice roll of 5, 10, 15 using an iterator to simulate the rolls for each combatant
    rolls = iter([5, 10])  # For npc1, character, no npc2 (dead)
    def fake_roll_dice(sides):
        if sides != 20:
            raise ValueError(f"Expected to roll a d20, but got d{sides}")
        return next(rolls)

    # Use monkeypatch to replace the roll_dice method in Dice with our fake function
    monkeypatch.setattr(
        Dice,
        "roll_dice",
        fake_roll_dice,
    )

    turn_manager = TurnManager(game_state)
    turn_manager.set_initiative_order()

    # Check that the initiative order is sorted in descending order of initiative rolls
    initiative_values = [initiative for _, initiative in turn_manager.initiative_order]
    assert initiative_values == sorted(initiative_values, reverse=True)

    # Check that all alive combatants are included in the initiative order
    initiative_names = [combatant.name for combatant, _ in turn_manager.initiative_order]
    expected_names = [character.name, npc1.name]  # npc2 is dead and should not be included
    expected_values = [10, 5]  # Corresponding initiative values for character and npc1
    assert initiative_names == expected_names
    assert initiative_values == expected_values


