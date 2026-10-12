from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    damage_type: str  # e.g., "slashing", "piercing", "bludgeoning"
    properties: list[str]  # e.g., ["finesse", "light", "thrown"]
    one_handed_damage: str # e.g., "1d6", "1d8"
    two_handed_damage: str | None  # e.g., "1d8", "1d10"

scimitar = Weapon(
    name="Scimitar",
    damage_type="slashing",
    properties=["finesse", "light"],
    one_handed_damage="1d6",
    two_handed_damage=None
)

longsword = Weapon(
    name="Longsword",
    damage_type="slashing",
    properties=["versatile"],
    one_handed_damage="1d8",
    two_handed_damage="1d10"
)
