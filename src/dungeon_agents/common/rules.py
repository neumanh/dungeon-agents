from dungeon_agents.common.game_state import GameState
from dungeon_agents.common.combatant import Combatant
from dungeon_agents.common.weapon import Weapon
from dungeon_agents.common.dice import Dice


def calculate_damage(weapon: Weapon, hands_used: int) -> int:
    """
    Calculate the damage dealt by a weapon based on the number of hands used.

    Args:
        weapon (Weapon): The weapon being used.
        hands_used (int): The number of hands used to wield the weapon.

    Returns:
        int: The total damage dealt by the weapon.
    """
    if hands_used < 1 or hands_used > 2:
        raise ValueError("hands_used must be either 1 or 2.")

    # Determine the appropriate damage dice based on hands used
    if hands_used == 2 and weapon.two_handed_damage is not None:
        damage_dice = weapon.two_handed_damage
    else:
        # According to D&D 5e, one-hand weapons can be used with two hands with the same damage
        damage_dice = weapon.one_handed_damage
    
    # Rolling the dice to calculate total damage
    return Dice.roll_damage(damage_dice)


def resolve_attack(
    game_state: GameState,
    target: Combatant,
    weapon: Weapon,
    hands_used: int,
    natural_roll: int,
    attack_bonus: int,
) -> int:
    """
    Resolve an attack against the target, applying damage if the attack hits.

    Args:
        game_state (GameState): The current state of the game.
        target (Combatant): The combatant being attacked.
        weapon (Weapon): The weapon being used for the attack.
        hands_used (int): The number of hands used to wield the weapon.
        natural_roll (int): The natural roll of the d20 for the attack.
        attack_bonus (int): The attack bonus to be added to the natural roll.

    Returns:
        int: The actual damage dealt to the target. Returns 0 if the attack misses.
    """
    # Check attack success
    attack_result = game_state.check_attack(target, natural_roll, attack_bonus)

    if not attack_result:
        return 0  # Attack missed, no damage dealt

    # Calculate damage based on weapon and hands used
    rolled_damage = calculate_damage(weapon, hands_used)

    # Apply damage to the NPC's HP
    actual_damage = game_state.apply_damage(target, rolled_damage)

    return actual_damage



if __name__ == "__main__":
    from dungeon_agents.common.weapon import scimitar, longsword
    target_example = Combatant(name="Goblin 1", hp=15, ac=13)
    print(f"{calculate_damage(longsword, 1)=}")  # Example: Calculate damage for longsword with one hand
    print(f"{calculate_damage(longsword, 2)=}")  # Example: Calculate damage for longsword with two hands
    print(f"{calculate_damage(scimitar, 1)=}")  # Example: Calculate damage for scimitar with one hand
    print(f"{calculate_damage(scimitar, 2)=}")   # Example: Calculate damage for scimitar with two hands
