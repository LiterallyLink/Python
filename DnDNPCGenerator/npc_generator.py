# npc_generator.py
import random

def generate_alignment():
    alignments = [
        'Lawful Good', 'Lawful Neutral', 'Lawful Evil',
        'Neutral Good', 'Neutral', 'Neutral Evil',
        'Chaotic Good', 'Chaotic Neutral', 'Chaotic Evil'
    ]

    return random.choice(alignments)

def generate_class():
    classes = [
        'Fighter', 'Wizard', 'Cleric', 'Bard', 'Druid',
        'Rogue', 'Ranger', 'Paladin', 'Barbarian',
        'Monk', 'Sorcerer', 'Warlock', "Artificer"
    ]
    return random.choice(classes)

npc_alignment = generate_alignment()
npc_class = generate_class()

print(f"Class: {npc_class}")
print(f"Alignment: {npc_alignment}")