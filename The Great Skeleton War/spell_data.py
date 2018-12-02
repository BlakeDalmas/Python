#new spelldata

spells = []

# Creating the Spells and Skills
# The two things in the art array:
# 0: The image for the spell itself.
# 1: The image for the skill nodes for that spell.
# 2: The color representing the spell.

art = ["images/UI/fire/fire.png", "images/UI/fire/node.png", (210, 30, 30)]
skills = []
skills.append(["Blistering", "Enemies hit by the beam are lit on fire."])
skills.append(["Searing", "Deals additional damage to enemies that are on fire."])
skills.append(["Hyper", "Increases damage and projectile speed of the beam."])
skills.append(["Reflective", "Beam has a small chance to reflect instead of expiring."])
ultimate = ["Plasma", "Beam penetrates an unlimited amount of enemies."]
spells.append(["fire", "Beam", "Shoots a beam of fire that penetrates enemies.", skills, ultimate, art])

skills = []
skills.append(["Fire Blast", "Fireball explodes on contact."])
skills.append(["Volcanic", "Fire lasts longer."])
skills.append(["Potent", "Increased impact damage."])
skills.append(["Velocity", "Increases the projectile speed."])
ultimate = ["Melting", "Enemies that die from the fireball explode."]
spells.append(["fire", "Fireball", "Throw a high damage fireball that ignites enemies.", skills, ultimate, art])

skills = []
skills.append(["Fueled", "Fire lasts longer."])
skills.append(["Decay", "The longer the enemy stands in the fire the more damage they take."])
skills.append(["Consuming", "Enemies killed in the fire extend its duration."])
skills.append(["Ash", "Fire does more damage."])
ultimate = ["Wildfire", "Fire length is extended to 9 blocks and lasts longer."]
spells.append(["fire", "Inferno", "Sets off a fire in front of you.", skills, ultimate, art])

art = ["images/UI/shock/shock.png", "images/UI/shock/node.png", (62, 167, 224)]
skills = []
skills.append(["Voltage", "Higher impact damage."])
skills.append(["Amplitude", "Increases velocity and damage."])
skills.append(["Energized", "For each enemy hit returns 20% of mana used when it was cast."])
skills.append(["Rapid", "Increases casting speed."])
ultimate = ["Chain", "Lightning has 80% chance to chain to another target."]
spells.append(["shock", "Lightning", "Shoot lightning out of your hands.", skills, ultimate, art])

skills = []
skills.append(["Stabilized", "Path of the energy ball is more stable."])
skills.append(["Energetic", "Shocks enemies more rapidly."])
skills.append(["Static", "Increases damage of the shock."])
skills.append(["Scorn", "Allows two orbs to exist at the same time."])
ultimate = ["Quantum", "Orb has a small chance to teleport and send enemies back to spawn."]
spells.append(["shock", "Orb", "Fires an unstable orb of some strange electric force.", skills, ultimate, art])

skills = []
skills.append(["Powerful", "Increases area of explosion."])
skills.append(["Supercell", "Small chance to strike again."])
skills.append(["Smiting", "Increases damage of strike."])
skills.append(["Fiery", "Small chance to light enemies on fire."])
ultimate = ["Disintegrate", "Has a small chance to deal x5 damage."]
spells.append(["shock", "Thunderstrike", "Spawns a lightning strike that does devastating damage.", skills, ultimate, art])

art = ["images/UI/poison/poison.png", "images/UI/poison/node.png", (15, 210, 40)]
skills = []
skills.append(["Debilitating", "Poison does more damage."])
skills.append(["Paralyzing", "Poison has chance to paralyze the enemy for the duration of the poison."])
skills.append(["Venom", "Poison lasts longer."])
skills.append(["Penetrating", "Dart has a chance to penetrate an enemy."])
ultimate = ["Lethal", "25% chance for enemy to instantly die."]
spells.append(["poison", "Dart", "Shoots a powerful dart.", skills, ultimate, art])

skills = []
skills.append(["Expansive", "Increases area of poison cloud."])
skills.append(["Venomous", "Poison lingers for longer after they walk out of the cloud."])
skills.append(["Noxious", "Increased damage while enemies are in the cloud."])
skills.append(["Caustic", "Enemies exposed to the poison are lit on fire."])
ultimate = ["Plague", "Enemies killed by a cloud place another cloud."]
spells.append(["poison", "Cloud", "Creates a plume of toxin that poisons enemies as they walk through it.", skills, ultimate, art])

skills = []
skills.append(["Lasting", "Poison lasts longer."])
skills.append(["Necrotic Siphon", "Enemies killed by the poison regen your mana."])
skills.append(["Frailty", "Deals additional damage equal to 2% of the enemies max health."])
skills.append(["Hebenon", "Poison slows the enemy down."])
ultimate = ["Eternal", "The venom stays on your sword forever."]
spells.append(["poison", "Venomblade", "Poisons your sword, your next slash will apply poison as well.", skills, ultimate, art])

art = ["images/UI/sorcery/sorcery.png", "images/UI/sorcery/node.png", (245, 255, 66)]
skills = []
skills.append(["Broaden", "Increased area of effect."])
skills.append(["Enduring", "Slowness lasts longer."])
skills.append(["Slug", "Increased slow amount."])
skills.append(["Diminishing", "Slow amount increases on high speed enemies."])
ultimate = ["Freezing", "Enemies hit directly are paralyzed for some time."]
spells.append(["sorcery", "Burden", "Projectile that slows down the enemy in a small area.", skills, ultimate, art])

skills = []
skills.append(["Overcharged", "Missile power increases the fuller your mana bar is."])
skills.append(["Concentrate", "Increases missile speed."])
skills.append(["Devastating", "Increases base damage."])
skills.append(["Incendiary", "Enemies hit by the missiles are ignited."])
skills.append(["Blast", "Adds a blast radius."])
skills.append(["Barrage", "Decreases cast time for magic missiles."])
ultimate = ["Devour", "Magic Missiles are larger, and casting it while a missile already exists no longer removes it. Instead, it increases its power."]
spells.append(["sorcery", "Magic Missile", "Control explosive shock orbs with your mind.", skills, ultimate, art])

skills = []
skills.append(["Protostar", "Increases the strength of low mana starblasts."])
skills.append(["Singularity", "Enemies close to the center take additional damage."])
skills.append(["Radioactive", "Enemies in the blast range are poisoned."])
skills.append(["Gamma Rays", "The blast launches beams in random directions."])
skills.append(["Red Giant", "Increases the blast range."])
ultimate = ["Dark Energy", "Starblast only consumes 25% of your current mana instead of 100%."]
spells.append(["sorcery", "Starblast", "Focus all your mana into a single devastating spell.", skills, ultimate, art])

art = ["images/UI/passive/passive.png", "images/UI/passive/node.png", (191, 255, 247)]
skills = []
skills.append(["Siphon", "Melee damage regens mana."])
skills.append(["Beserk", "Melee damage increased."])
skills.append(["Frenzy", "Decreases delay between melee swings."])
skills.append(["Spellcaster", "Decreases delay between spells."])
skills.append(["Mastery", "Reduces mana cost of all spells."])
skills.append(["Fleet", "Faster movement speed"])
skills.append(["Lucrative", "You gain additional money from kills."])
skills.append(["Bargain", "You get more money back from selling towers."])
skills.append(["Necromancy", "You regain a population at the start of every wave."])
skills.append(["Affinity", "Base mana regen rate increased."])
skills.append(["City", "Doubles the population of your village."])
skills.append(["Mage", "1.5x max mana"])
skills.append(["Fury", "Your melee attacks can hit multiple enemies at once."])
ultimate = ["Vitality", "Increases the power of all passive skills."]
spells.append(["passive", "Passive", "Passive abilities that improve various things.", skills, ultimate, art])