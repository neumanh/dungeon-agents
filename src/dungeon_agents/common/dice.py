from random import randint

class Dice:

    valid_sides = [4, 6, 8, 10, 12, 20]

    @classmethod
    def roll_dice(cls, sides: int) -> int:
        if sides not in cls.valid_sides:
            raise ValueError(f"Invalid number of sides: {sides}. Valid options are {cls.valid_sides}.")
        
        return randint(1, sides)

    @classmethod
    def roll_damage(cls, damage_dice: str) -> int:
        # Extract the number of roll and the dice type
        string_parts = damage_dice.lower().split('d')

        # Validate the format
        if len(string_parts) != 2:
            raise ValueError(f"Invalid damage dice format: {damage_dice}. Expected format is 'XdY'.")

        dice_count, dice_type = string_parts

        # Validate that both parts are integers
        try:
            dice_count, dice_type = int(dice_count), int(dice_type)
        except ValueError as e:
            raise ValueError(
                f"Invalid damage dice format: {damage_dice}. Both X and Y must be integers."
            ) from e

        if dice_count < 1:
            raise ValueError(f"Dice count must be at least 1. Got: {dice_count}.")

        # Roll
        damage_total = 0
        for _ in range(dice_count):
            damage_total += cls.roll_dice(dice_type)

        return damage_total
        
        


if __name__ == "__main__":
    # Example usage
    print(f"Rolling a 4d20: {Dice.roll_damage('4d20')}")
    print(f"Rolling a 2d6: {Dice.roll_damage('2d6')}")
