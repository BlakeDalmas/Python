import arcade
import random
import globalvars
import spell_data

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

        self.lines_x = {}
        self.lines_y = {}

        self.old_tier = 0

        self.spells = spell_data.spells

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
        self.box_subtitle = ""
        self.box_title_color = None
        self.box_ultfix = False

        # Select two random casting spells and one random passive spell to show up in the menu:
        # source_pool = self.spells.copy()
        source_pool = []
        passive_spells = []

        for i in range(len(self.spells)):
            if self.spells[i][0] == "passive":
                passive_spells.append(self.spells[i])
            else:
                source_pool.append(self.spells[i])

        choice = random.choice(passive_spells)

        for i in range(3):
            item = Node()
            item.tier = 0
            item.data = arcade.load_texture(choice[5][0])
            item.type = choice[0]

            item.xpos = self.calc_source_pos("x", i + 1)
            item.ypos = self.calc_source_pos("y", i + 1)
            item.quadrant = i + 1
            item.st_x = item.xpos
            item.st_y = item.ypos
            item.unlocked = True
            item.purchased = False
            item.radius = 16
            item.ultimate = False
            item.complete = False
            item.nodes = []

            item.spell_index = 0
            item.title = choice[1]
            item.desc = choice[2]

            item.ult_data = arcade.load_texture("images/UI/ultimate.png")
            item.ult_title = choice[4][0]
            item.ult_desc = choice[4][1]

            item.spell_ref = choice

            self.sources.append(item)

            choice = random.choice(source_pool)
            source_pool.remove(choice)

        # For these three spells, set up their skills.
        for cur_spell in self.sources:
            local_tier = 0

            skill_pool = cur_spell.spell_ref[3].copy()

            for i in range(random.randint(3, 4)):
                local_tier += 1

                node = Node()
                node.quadrant = cur_spell.quadrant
                node.st_x = 0
                node.st_y = 0
                node.data = arcade.load_texture(cur_spell.spell_ref[5][1])
                node.type = cur_spell.type
                # node.tier = local_tier
                node.xpos = 200
                node.ypos = 200
                node.unlocked = False
                node.purchased = False
                node.radius = 8
                node.ultimate = False
                node.source_spell = cur_spell

                cur_spell.nodes.append(node)
                self.calc_node_pos(node, cur_spell)

                selected = random.choice(skill_pool)
                node.title = selected[0]
                node.desc = selected[1]
                skill_pool.remove(selected)

        # Add source to the line lists
        for source in self.sources:
            self.lines_x[source.title] = [source.xpos]
            self.lines_y[source.title] = [source.ypos]

    def already_exists(self, chosen_spell):
        exists = False

        for source in self.sources:
            for node in source.nodes:
                if node.title == chosen_spell[0]:
                    exists = True

        return exists

    def add_line_data(self, title, xpos, ypos):
        self.lines_x[title].append(xpos)
        self.lines_y[title].append(ypos)

    def draw_connection(self, element_x, element_y):
        for i in range(len(element_x)):
            if i < len(element_x) - 1:
                arcade.draw_line(element_x[i], element_y[i], element_x[i+1], element_y[i+1], arcade.color.WHITE)

    def draw(self):
        # Draw backgrounds, etc.
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - 50, 60, 60, self.exit_button)
        arcade.draw_text(str(globalvars.player.skillpoints), 39, SCREEN_HEIGHT - 120, (73, 42, 230), 32)

        # If hovering over a node, display information.
        if self.display_box:
            arcade.draw_text(str(self.box_title), 49, 110, self.box_title_color, 32)

            char_calc = round(16 - (len(self.box_message) / 6))
            if char_calc < 0:
                char_calc = 0

            size = 14 + char_calc
            arcade.draw_text(str(self.box_message), 50, 75, (255, 255, 255), size)

            local_subtitle = self.box_subtitle[0].upper() + self.box_subtitle[1:]

            arcade.draw_text(local_subtitle, 50, 40, self.box_title_color, 16)

        # Draw lines between the nodes.
        for line_type in self.lines_x:
            self.draw_connection(self.lines_x[line_type], self.lines_y[line_type])

        # Draw the nodes
        for source in self.sources:
            if source.ultimate:
                arcade.draw_circle_filled(source.xpos, source.ypos, 18, (122, 18, 130, random.randint(0, 255)))
                arcade.draw_texture_rectangle(source.xpos, source.ypos, 32, 32, source.data)

                if self.box_ultfix:
                    self.box_title_color = (122, 18, 130, random.randint(100, 255))
            else:
                if globalvars.skills_ultimate and source.complete:
                    arcade.draw_texture_rectangle(source.xpos, source.ypos, 32, 32, source.ult_data)
                else:
                    arcade.draw_texture_rectangle(source.xpos, source.ypos, 32, 32, source.data)

            if not source.purchased:
                arcade.draw_circle_filled(source.xpos, source.ypos, 16, (200, 200, 200, 100))

            for node in source.nodes:
                if source.ultimate:
                    arcade.draw_circle_filled(node.xpos, node.ypos, 10, (177, 32, 188, random.randint(0, 255)))

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
                    if (source.xpos - source.radius) < x < (source.xpos + source.radius) and (source.ypos - source.radius) < y < (source.ypos + source.radius):
                        if globalvars.skills_ultimate and source.complete and source.purchased:
                            source.ultimate = True
                            globalvars.player.skillpoints -= 1
                            globalvars.emit_sound("ult_choose.ogg")
                            globalvars.player.give_skill(source.ult_title)
                            globalvars.skills_ultimate = False

                            if globalvars.player.player_has_skill("Vitality") and globalvars.player.player_has_skill("Fleet"):
                                globalvars.player.speed += 1

                            if globalvars.player.player_has_skill("Vitality") and globalvars.player.player_has_skill("City"):
                                globalvars.population *= 2
                                globalvars.max_population *= 2

                            if globalvars.player.player_has_skill("Vitality") and globalvars.player.player_has_skill("Mage"):
                                globalvars.player.mana_cap = int(globalvars.player.mana_cap * 1.5)
                                globalvars.player.mana = globalvars.player.mana_cap

                        elif not source.purchased:
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
                                globalvars.population *= 2
                                globalvars.max_population *= 2

                            if node.title == "Mage":
                                globalvars.player.mana_cap = int(globalvars.player.mana_cap * 1.5)
                                globalvars.player.mana = globalvars.player.mana_cap

                            node.purchased = True
                            self.add_line_data(source.title, node.xpos, node.ypos)
                            if i < len(source.nodes) - 1:
                                source.nodes[i + 1].unlocked = True
                            else:
                                source.complete = True
                if globalvars.skills_ultimate and globalvars.player.skillpoints <= 0:
                    globalvars.skills_ultimate = False

    def move_mouse(self, x, y):
        self.display_box = False

        local_ultfix = False

        for source in self.sources:
            rad = source.radius * 1.5

            if (source.xpos - rad) < x < (source.xpos + rad) and (source.ypos - rad) < y < (source.ypos + rad):
                self.display_box = True

                if source.ultimate:
                    self.box_title = "Ultimate " + source.title
                    self.box_message = source.ult_desc
                    local_ultfix = True
                elif globalvars.skills_ultimate and source.complete:
                    self.box_title = source.ult_title
                    self.box_message = source.ult_desc
                    self.box_title_color = (122, 18, 130, 255)
                else:
                    self.box_title = source.title
                    self.box_message = source.desc
                    self.box_title_color = source.spell_ref[5][2]

                self.box_subtitle = source.type + " spell"

            for i in range(len(source.nodes)):
                node = source.nodes[i]
                rad = node.radius * 1.5
                if (node.xpos - rad) < x < (node.xpos + rad) and (node.ypos - rad) < y < (node.ypos + rad) and node.unlocked:
                    self.display_box = True
                    self.box_title = node.title
                    self.box_message = node.desc
                    self.box_title_color = node.source_spell.spell_ref[5][2]
                    self.box_subtitle = node.type + " skill"
                    local_ultfix = False

        self.box_ultfix = local_ultfix