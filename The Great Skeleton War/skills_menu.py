import arcade
import random
import globalvars

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 768

# The skills
class Node():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.data = None
        self.type = "fire"
        self.tier = 0
        self.quadrant = 0
        self.st_x = 0
        self.st_y = 0
        self.unlocked = False
        self.purchased = False
        self.radius = 0
        self.spell_title = ""
        self.spell_desc = ""
        self.ultimate = False

class Menu():
    def __init__(self):
        super().__init__()
        self.background = None
        self.exit_button = None
        self.sources = []
        self.display_box = False
        self.box_title = ""
        self.box_message = ""
        self.box_title_color = None

        self.lines_fire_x = []
        self.lines_fire_y = []
        self.lines_shock_x = []
        self.lines_shock_y = []
        self.lines_poison_x = []
        self.lines_poison_y = []
        self.lines_sorcery_x = []
        self.lines_sorcery_y = []
        self.old_tier = 0

        # Spell Data
        self.spell_ultimate_fire_1 = ["Plasma", "Beam penetrates an unlimited amount of enemies."]
        self.spell_ultimate_fire_2 = ["Melting", "Enemies that die from the fireball explode."]
        self.spell_ultimate_fire_3 = ["Wildfire", "Fire length is extended to 9 blocks."]
        self.spell_ultimates_fire = [self.spell_ultimate_fire_1, self.spell_ultimate_fire_2, self.spell_ultimate_fire_3]

        self.spell_ultimate_poison_1 = ["Lethal", "10% chance for enemy to instantly die."]
        self.spell_ultimate_poison_2 = ["Plague", "You can place up to three clouds at once."]
        self.spell_ultimate_poison_3 = ["Eternal", "Poison only needs to be reapplied every 3 hits."]
        self.spell_ultimates_poison = [self.spell_ultimate_poison_1, self.spell_ultimate_poison_2, self.spell_ultimate_poison_3]

        self.spell_ultimate_shock_1 = ["Chain", "Lightning has 80% chance to chain to another target."]
        self.spell_ultimate_shock_2 = ["Quantum", "Orb has a small chance to teleport and send enemies back to spawn."]
        self.spell_ultimate_shock_3 = ["Disintegrate", "Has a small chance to deal x5 damage."]
        self.spell_ultimates_shock = [self.spell_ultimate_shock_1, self.spell_ultimate_shock_2, self.spell_ultimate_shock_3]

        self.spell_ultimate_sorcery_1 = ["Affinity", "Base mana regen rate increased."]
        self.spell_ultimate_sorcery_2 = ["Freezing", "Enemy hit directly is paralyzed for some time."]
        self.spell_ultimate_sorcery_3 = ["City", "Max population increased to 20."]
        self.spell_ultimates_sorcery = [self.spell_ultimate_sorcery_1, self.spell_ultimate_sorcery_2, self.spell_ultimate_sorcery_3]

        self.major_spell_fire_1 = ["Beam", "Shoots a beam of fire that penetrates enemies."]
        self.major_spell_fire_2 = ["Fireball", "Throw a high damage fireball that ignites enemies."]
        self.major_spell_fire_3 = ["Inferno", "Sets off a fire in front of you."]
        self.major_spells_fire = [self.major_spell_fire_1, self.major_spell_fire_2, self.major_spell_fire_3]

        self.major_spell_poison_1 = ["Dart", "Shoots a powerful dart."]
        self.major_spell_poison_2 = ["Cloud", "Creates a plume of toxin that poisons enemies as they walk through it."]
        self.major_spell_poison_3 = ["Venomblade", "Poisons your sword, your next slash will apply poison as well."]
        self.major_spells_poison = [self.major_spell_poison_1, self.major_spell_poison_2, self.major_spell_poison_3]

        self.major_spell_shock_1 = ["Lightning", "Shoot lightning out of your hands."]
        self.major_spell_shock_2 = ["Orb", "Fires an unstable orb of some strange electric force."]
        self.major_spell_shock_3 = ["Thunderstrike", "Spawns a lightning strike that does devastating damage."]
        self.major_spells_shock = [self.major_spell_shock_1, self.major_spell_shock_2, self.major_spell_shock_3]

        self.major_spell_sorcery_1 = ["Battlemage", "Passive abilities that improve melee and magic."]
        self.major_spell_sorcery_2 = ["Burden", "Projectile that slows down the enemy in a small area."]
        self.major_spell_sorcery_3 = ["Mysticism", "Passive abilities that influence random things."]
        self.major_spells_sorcery = [self.major_spell_sorcery_1, self.major_spell_sorcery_2, self.major_spell_sorcery_3]

        # Minor
        self.minor_spell_fire_1_1 = ["Blistering", "Enemies hit by the beam are lit on fire."]
        self.minor_spell_fire_1_2 = ["Searing", "Deals additional damage to enemies that are on fire."]
        self.minor_spell_fire_1_3 = ["Hyper", "Increases damage and projectile speed of the beam."]
        self.minor_spell_fire_1_4 = ["Reflective", "Beam has a small chance to reflect instead of expiring."]
        self.minor_spells_fire_1 = [self.minor_spell_fire_1_1, self.minor_spell_fire_1_2, self.minor_spell_fire_1_3, self.minor_spell_fire_1_4]
        self.minor_spell_fire_2_1 = ["Fire Blast", "Fireball explodes on contact."]
        self.minor_spell_fire_2_2 = ["Volcanic", "Fire lasts longer."]
        self.minor_spell_fire_2_3 = ["Potent", "Increased impact damage."]
        self.minor_spell_fire_2_4 = ["Velocity", "Increases the projectile speed."]
        self.minor_spells_fire_2 = [self.minor_spell_fire_2_1, self.minor_spell_fire_2_2, self.minor_spell_fire_2_3, self.minor_spell_fire_2_4]
        self.minor_spell_fire_3_1 = ["Fueled", "Fire lasts longer."]
        self.minor_spell_fire_3_2 = ["Decay", "The longer the enemy stands in the fire the more damage they take."]
        self.minor_spell_fire_3_3 = ["Consuming", "Enemies killed in the fire extend its duration."]
        self.minor_spell_fire_3_4 = ["Ash", "Fire does more damage."]
        self.minor_spells_fire_3 = [self.minor_spell_fire_3_1, self.minor_spell_fire_3_2, self.minor_spell_fire_3_3, self.minor_spell_fire_3_4]
        self.minor_spells_fire = [self.minor_spells_fire_1, self.minor_spells_fire_2, self.minor_spells_fire_3]

        self.minor_spell_poison_1_1 = ["Debilitating", "Poison does more damage."]
        self.minor_spell_poison_1_2 = ["Paralyzing", "Poison has chance to paralyze the enemy for the duration of the poison."]
        self.minor_spell_poison_1_3 = ["Venom", "Poison lasts longer."]
        self.minor_spell_poison_1_4 = ["Penetrating", "Dart has a chance to penetrate an enemy."]
        self.minor_spells_poison_1 = [self.minor_spell_poison_1_1, self.minor_spell_poison_1_2, self.minor_spell_poison_1_3, self.minor_spell_poison_1_4]
        self.minor_spell_poison_2_1 = ["Expansive", "Increases area of poison cloud."]
        self.minor_spell_poison_2_2 = ["Venomous", "Poison lingers for longer after they walk out of the cloud."]
        self.minor_spell_poison_2_3 = ["Noxious", "Increased damage while enemies are in the cloud."]
        self.minor_spell_poison_2_4 = ["Caustic", "Enemies exposed to the poison are lit on fire."]
        self.minor_spells_poison_2 = [self.minor_spell_poison_2_1, self.minor_spell_poison_2_2, self.minor_spell_poison_2_3, self.minor_spell_poison_2_4]
        self.minor_spell_poison_3_1 = ["Lasting", "Poison lasts longer."]
        self.minor_spell_poison_3_2 = ["Necrotic Siphon", "Enemies killed by the poison regen your mana."]
        self.minor_spell_poison_3_3 = ["Frailty", "Deals additional damage equal to 2% of the enemies max health."]
        self.minor_spell_poison_3_4 = ["Hebenon", "Poison slows the enemy down."]
        self.minor_spells_poison_3 = [self.minor_spell_poison_3_1, self.minor_spell_poison_3_2, self.minor_spell_poison_3_3, self.minor_spell_poison_3_4]
        self.minor_spells_poison = [self.minor_spells_poison_1, self.minor_spells_poison_2, self.minor_spells_poison_3]

        self.minor_spell_shock_1_1 = ["Voltage", "Higher impact damage."]
        self.minor_spell_shock_1_2 = ["Amplitude", "Increases velocity and damage."]
        self.minor_spell_shock_1_3 = ["Energized", "For each enemy hit returns 20% of mana used when it was cast."]
        self.minor_spell_shock_1_4 = ["Rapid", "Increases casting speed."]
        self.minor_spells_shock_1 = [self.minor_spell_shock_1_1, self.minor_spell_shock_1_2, self.minor_spell_shock_1_3, self.minor_spell_shock_1_4]
        self.minor_spell_shock_2_1 = ["Stabilized", "Path of the energy ball is more stable."]
        self.minor_spell_shock_2_2 = ["Energetic", "Shocks enemies more rapidly."]
        self.minor_spell_shock_2_3 = ["Static", "Increases damage of the shock."]
        self.minor_spell_shock_2_4 = ["Scorn", "Allows two orbs to exist at the same time."]
        self.minor_spells_shock_2 = [self.minor_spell_shock_2_1, self.minor_spell_shock_2_2, self.minor_spell_shock_2_3, self.minor_spell_shock_2_4]
        self.minor_spell_shock_3_1 = ["Powerful", "Increases area of explosion."]
        self.minor_spell_shock_3_2 = ["Supercell", "Small chance to strike again."]
        self.minor_spell_shock_3_3 = ["Smiting", "Increases damage of strike."]
        self.minor_spell_shock_3_4 = ["Fiery", "Small chance to light enemies on fire."]
        self.minor_spells_shock_3 = [self.minor_spell_shock_3_1, self.minor_spell_shock_3_2, self.minor_spell_shock_3_3, self.minor_spell_shock_3_4]
        self.minor_spells_shock = [self.minor_spells_shock_1, self.minor_spells_shock_2, self.minor_spells_shock_3]

        self.minor_spell_sorcery_1_1 = ["Siphon", "Melee damage regens mana."]
        self.minor_spell_sorcery_1_2 = ["Beserk", "Melee damage increased."]
        self.minor_spell_sorcery_1_3 = ["Frenzy", "Decreases delay between spell casts and melee swings."]
        self.minor_spell_sorcery_1_4 = ["Mastery", "Reduces mana cost of all spells."]
        self.minor_spells_sorcery_1 = [self.minor_spell_sorcery_1_1, self.minor_spell_sorcery_1_2, self.minor_spell_sorcery_1_3, self.minor_spell_sorcery_1_4]
        self.minor_spell_sorcery_2_1 = ["Broaden", "Increased area of effect."]
        self.minor_spell_sorcery_2_2 = ["Enduring", "Slowness lasts longer."]
        self.minor_spell_sorcery_2_3 = ["Slug", "Increased slow amount."]
        self.minor_spell_sorcery_2_4 = ["Diminishing", "Slow amount increases on high speed enemies."]
        self.minor_spells_sorcery_2 = [self.minor_spell_sorcery_2_1, self.minor_spell_sorcery_2_2, self.minor_spell_sorcery_2_3, self.minor_spell_sorcery_2_4]
        self.minor_spell_sorcery_3_1 = ["Fleet", "Faster movement speed"]
        self.minor_spell_sorcery_3_2 = ["Lucrative", "You gain additional money from kills."]
        self.minor_spell_sorcery_3_3 = ["Bargain", "You get more money back from selling towers."]
        self.minor_spell_sorcery_3_4 = ["Necromancy", "You regain a population at the start of every wave."]
        self.minor_spells_sorcery_3 = [self.minor_spell_sorcery_3_1, self.minor_spell_sorcery_3_2, self.minor_spell_sorcery_3_3, self.minor_spell_sorcery_3_4]
        self.minor_spells_sorcery = [self.minor_spells_sorcery_1, self.minor_spells_sorcery_2, self.minor_spells_sorcery_3]

        self.minor_spells = [self.minor_spells_fire, self.minor_spells_poison, self.minor_spells_shock, self.minor_spells_sorcery]
        self.major_spells = [self.major_spells_fire, self.major_spells_poison, self.major_spells_shock, self.major_spells_sorcery]
        self.ultimates = [self.spell_ultimates_fire, self.spell_ultimates_poison, self.spell_ultimates_shock, self.spell_ultimates_sorcery]
        self.spells = [self.major_spells, self.minor_spells, self.ultimates]

        self.setup()

    def calc_source_pos(self, axis, index):
        # 2 1
        # 3 4
        value = 0
        center_x = int(SCREEN_WIDTH / 2)
        center_y = int(SCREEN_HEIGHT / 2)
        drift_x = 300
        drift_y = 100
        spacing = 50

        if axis == "x":
            if index == 1:
                value = random.randint(center_x + spacing, center_x + drift_x + spacing)
            elif index == 2:
                value = random.randint(center_x - drift_x - spacing, center_x - spacing)
            elif index == 3:
                value = random.randint(center_x - drift_x - spacing, center_x - spacing)
            elif index == 4:
                value = random.randint(center_x + spacing, center_x + drift_x + spacing)
        elif axis == "y":
            if index == 1:
                value = random.randint(center_y + spacing, center_y + spacing + drift_y)
            elif index == 2:
                value = random.randint(center_y + spacing, center_y + spacing + drift_y)
            elif index == 3:
                value = random.randint(center_y - spacing - drift_y, center_y - spacing)
            elif index == 4:
                value = random.randint(center_y - spacing - drift_y, center_y - spacing)
        return value

    def calc_node_pos(self, node, source):
        pattern_x = [1, -1, -1, 1]
        pattern_y = [1, 1, -1, -1]
        range_x = [32, 64]
        range_y = range_x

        if node.tier != self.old_tier:
            self.old_tier = node.tier
            pattern_x = [-1, 1, 1, -1]

        for i in range(4):
            if node.quadrant == i + 1:
                source.st_x += (random.randint(range_x[0], range_x[1]) * pattern_x[i])
                source.st_y += (random.randint(range_y[0], range_y[1]) * pattern_y[i])
                node.xpos = source.st_x
                node.ypos = source.st_y

    def setup(self):
        self.background = arcade.load_texture("new_spacebg.jpg", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.exit_button = arcade.load_texture("images/UI/buttons/exit_button.png")
        self.display_box = False
        self.box_title = ""
        self.box_message = ""
        self.box_title_color = None

        source = []
        rands = [1, 2, 3, 4]
        for i in range(4):
            choice = random.choice(rands)
            source.append(choice)
            rands.remove(choice)

        for i in range(len(source)):
            item = Node()
            item.tier = 0
            if i == 0:
                item.data = arcade.load_texture("images/UI/fire/fire.png")
                item.type = "fire"
            elif i == 1:
                item.data = arcade.load_texture("images/UI/shock/shock.png")
                item.type = "shock"
            elif i == 2:
                item.data = arcade.load_texture("images/UI/poison/poison.png")
                item.type = "poison"
            elif i == 3:
                item.data = arcade.load_texture("images/UI/sorcery/sorcery.png")
                item.type = "sorcery"

            item.xpos = self.calc_source_pos("x", source[i])
            item.ypos = self.calc_source_pos("y", source[i])
            item.quadrant = source[i]
            item.st_x = item.xpos
            item.st_y = item.ypos
            item.unlocked = True
            item.purchased = False
            item.radius = 16
            item.ultimate = False
            item.nodes = []

            item.spell_index = 0
            item.title = ""
            item.desc = ""

            item.spell_index = random.randint(0, len(self.major_spells_fire) - 1)
            if item.type == "fire":
                temp = self.major_spells_fire[item.spell_index]
            elif item.type == "poison":
                temp = self.major_spells_poison[item.spell_index]
            elif item.type == "shock":
                temp = self.major_spells_shock[item.spell_index]
            elif item.type == "sorcery":
                temp = self.major_spells_sorcery[item.spell_index]
            else:
                print("What happened?")
            item.title = temp[0]
            item.desc = temp[1]

            self.sources.append(item)

        self.sources.pop(random.randint(0, len(self.sources) - 1))

        for source in self.sources:
            local_tier = 0
            # Generate regular nodes
            for i in range(random.randint(2, 4)):
                local_tier += 1

                node = Node()
                node.quadrant = source.quadrant
                node.st_x = 0
                node.st_y = 0
                node.data = arcade.load_texture("images/UI/" + source.type + "/node.png")
                node.type = source.type
                # node.tier = local_tier
                node.xpos = 200
                node.ypos = 200
                node.unlocked = False
                node.purchased = False
                node.radius = 8
                node.ultimate = False

                source.nodes.append(node)
                self.calc_node_pos(node, source)

                node.title = ""
                node.desc = ""
                temp_1 = None
                if node.type == "fire":
                    temp_1 = self.minor_spells_fire[source.spell_index]
                    # temp_1 = random.choice(self.minor_spells_fire)
                elif node.type == "poison":
                    temp_1 = self.minor_spells_poison[source.spell_index]
                elif node.type == "shock":
                    temp_1 = self.minor_spells_shock[source.spell_index]
                elif node.type == "sorcery":
                    temp_1 = self.minor_spells_sorcery[source.spell_index]
                else:
                    print("What happened?")

                selected = random.choice(temp_1)
                error_count = 0
                while self.already_exists(selected):
                    selected = random.choice(temp_1)
                    error_count += 1
                    if error_count > 100:
                        print("Something went horribly wrong!")
                        break

                node.title = selected[0]
                node.desc = selected[1]

            # Generate ultimates
            if random.randint(1 + local_tier, 7) == 7:
                node = Node()
                node.quadrant = source.quadrant
                node.st_x = 0
                node.st_y = 0
                node.data = arcade.load_texture("images/UI/ultimate.png")
                node.type = source.type
                # node.tier = source.nodes[-1].tier + 1
                node.xpos = 200
                node.ypos = 200
                node.unlocked = False
                node.purchased = False
                node.radius = 8
                node.ultimate = True

                node.title = ""
                node.desc = ""
                if node.type == "fire":
                    # temp = random.choice(self.spell_ultimates_fire)
                    temp = self.spell_ultimates_fire[source.spell_index]
                elif node.type == "poison":
                    temp = self.spell_ultimates_poison[source.spell_index]
                elif node.type == "shock":
                    temp = self.spell_ultimates_shock[source.spell_index]
                elif node.type == "sorcery":
                    temp = self.spell_ultimates_sorcery[source.spell_index]
                else:
                    print("What happened?")
                node.title = temp[0]
                node.desc = temp[1]

                source.nodes.append(node)
                self.calc_node_pos(node, source)



        # Add source to the line lists
        for source in self.sources:
            if source.type == "fire":
                self.lines_fire_x.append(source.xpos)
                self.lines_fire_y.append(source.ypos)
            if source.type == "shock":
                self.lines_shock_x.append(source.xpos)
                self.lines_shock_y.append(source.ypos)
            if source.type == "poison":
                self.lines_poison_x.append(source.xpos)
                self.lines_poison_y.append(source.ypos)
            if source.type == "sorcery":
                self.lines_sorcery_x.append(source.xpos)
                self.lines_sorcery_y.append(source.ypos)

    def already_exists(self, chosen_spell):
        exists = False

        for source in self.sources:
            for node in source.nodes:
                if node.title == chosen_spell[0]:
                    exists = True

        return exists

    def add_line_data(self, element, xpos, ypos):
        if element == "fire":
            self.lines_fire_x.append(xpos)
            self.lines_fire_y.append(ypos)
        if element == "shock":
            self.lines_shock_x.append(xpos)
            self.lines_shock_y.append(ypos)
        if element == "poison":
            self.lines_poison_x.append(xpos)
            self.lines_poison_y.append(ypos)
        if element == "sorcery":
            self.lines_sorcery_x.append(xpos)
            self.lines_sorcery_y.append(ypos)

    def draw_connection(self, element_x, element_y):
        for i in range(len(element_x)):
            if i < len(element_x) - 1:
                arcade.draw_line(element_x[i], element_y[i], element_x[i+1], element_y[i+1], arcade.color.WHITE)

    def draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - 50, 60, 60, self.exit_button)
        arcade.draw_text(str(globalvars.player.skillpoints), 39, SCREEN_HEIGHT - 120, (73, 42, 230), 32)

        if self.display_box:
            arcade.draw_text(str(self.box_title), 50, 100, self.box_title_color, 32)
            char_calc = round(16 - (len(self.box_message) / 6))
            if char_calc < 0:
                char_calc = 0
            size = 14 + char_calc
            arcade.draw_text(str(self.box_message), 50, 50, (255, 255, 255), size)

        self.draw_connection(self.lines_fire_x, self.lines_fire_y)
        self.draw_connection(self.lines_shock_x, self.lines_shock_y)
        self.draw_connection(self.lines_poison_x, self.lines_poison_y)
        self.draw_connection(self.lines_sorcery_x, self.lines_sorcery_y)

        for source in self.sources:
            arcade.draw_texture_rectangle(source.xpos, source.ypos, 32, 32, source.data)
            if not source.purchased:
                arcade.draw_circle_filled(source.xpos, source.ypos, 16, (200, 200, 200, 100))
            for node in source.nodes:
                if node.unlocked:
                    arcade.draw_texture_rectangle(node.xpos, node.ypos, 16, 16, node.data)
                    if not node.purchased:
                        arcade.draw_circle_filled(node.xpos, node.ypos, 8, (200, 200, 200, 100))


    def mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if 10 < x < 80 and SCREEN_HEIGHT - 70 < y < SCREEN_HEIGHT - 10:
                globalvars.emit_sound("click.ogg")
                globalvars.skills_opened = False

            for source in self.sources:
                if globalvars.player.skillpoints > 0:
                    if (source.xpos - source.radius) < x < (source.xpos + source.radius) and (source.ypos - source.radius) < y < (source.ypos + source.radius) and not source.purchased:
                        source.purchased = True
                        source.nodes[0].unlocked = True
                        globalvars.player.skillpoints -= 1
                        globalvars.emit_sound("source_select.ogg")
                        globalvars.player.give_spell(source.title)
                    for i in range(len(source.nodes)):
                        node = source.nodes[i]
                        if (node.xpos - node.radius) < x < (node.xpos + node.radius) and (node.ypos - node.radius) < y < (node.ypos + node.radius) and not node.purchased and node.unlocked:
                            globalvars.player.skillpoints -= 1
                            globalvars.emit_sound("skill_select.ogg")
                            globalvars.player.give_skill(node.title)

                            if node.title == "Fleet":
                                globalvars.player.speed += 1

                            if node.title == "City":
                                globalvars.population = 20
                                globalvars.max_population = 20

                            node.purchased = True
                            self.add_line_data(node.type, node.xpos, node.ypos)
                            if i < len(source.nodes) - 1:
                                source.nodes[i + 1].unlocked = True

    def move_mouse(self, x, y):
        self.display_box = False
        for source in self.sources:
            rad = source.radius * 1.5
            if (source.xpos - rad) < x < (source.xpos + rad) and (source.ypos - rad) < y < (source.ypos + rad):
                self.display_box = True
                self.box_title = source.title
                self.box_message = source.desc

                color = (255, 255, 255)
                if source.type == "fire":
                    color = (210, 30, 30)
                elif source.type == "shock":
                    color = (62, 167, 224)
                elif source.type == "poison":
                    color = (15, 210, 40)
                elif source.type == "sorcery":
                    color = (245, 255, 66)
                self.box_title_color = color
            for i in range(len(source.nodes)):
                node = source.nodes[i]
                rad = node.radius * 1.5
                if (node.xpos - rad) < x < (node.xpos + rad) and (node.ypos - rad) < y < (node.ypos + rad) and node.unlocked:
                    self.display_box = True
                    self.box_title = node.title
                    self.box_message = node.desc

                    color = (255, 255, 255)
                    if node.ultimate:
                        color = (122, 18, 130, random.randint(200, 255))
                    else:
                        if node.type == "fire":
                            color = (210, 30, 30)
                        elif node.type == "shock":
                            color = (62, 167, 224)
                        elif node.type == "poison":
                            color = (15, 210, 40)
                        elif node.type == "sorcery":
                            color = (245, 255, 66)
                    self.box_title_color = color

"""
Every game the following shows up in the galaxy (it's completely random)
One major skill from 3 random categories
2-4 minor skills for that major skill
10% for an ultimate to show up for that major skill
"""




