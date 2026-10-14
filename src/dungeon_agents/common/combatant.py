from dataclasses import dataclass


@dataclass
class Combatant:
    name: str
    dexterity_modifier: int
    ac: int
    hp: int
