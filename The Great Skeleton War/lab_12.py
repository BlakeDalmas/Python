import arcade
import random
import sys
import gamedata
import globalvars
import player
import os
import math
import skills_menu

# Sources can be found in sources.txt

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 768

class MyApplication(arcade.Window):
    def __init__(self, width, height):

        super().__init__(width, height)

    def setup(self):
        # General
        self.player = arcade.Sprite()
        self.main_menu_open = True
        self.game_started = False
        self.options_opened = False
        self.key_listening = False
        self.selected_key = 0
        self.instructions = 0
        self.crash_detection = 0
        self.current_mouse_x = 0
        self.current_mouse_y = 0
        self.button_start = arcade.load_texture("images/TD/GUI/button_start.png")
        self.button_instructions = arcade.load_texture("images/TD/GUI/button_instructions.png")
        self.button_exit = arcade.load_texture("images/TD/GUI/button_exit.png")
        self.button_generate = arcade.load_texture("images/TD/GUI/button_generate.png")
        self.button_new_start = arcade.load_texture("images/TD/GUI/new_button_start.png")
        self.button_new_generate = arcade.load_texture("images/TD/GUI/new_button_generate.png")
        self.button_difficulty = arcade.load_texture("images/TD/GUI/difficulty.png")
        self.button_diff_min = arcade.load_texture("images/TD/GUI/diff_min.png")
        self.button_diff_max = arcade.load_texture("images/TD/GUI/diff_max.png")
        self.game_background = arcade.load_texture("images/TD/grass_bg_new.jpg")
        self.skeleton_texture = arcade.load_texture("images/TD/entities/skeleton_test.png")
        self.error_box = arcade.load_texture("images/UI/error_box.png")
        self.options_screen = arcade.load_texture("images/UI/options.png")
        self.win_screen = arcade.load_texture("images/UI/win_screen.png")
        self.lose_screen = arcade.load_texture("images/UI/lose_screen.png")
        self.cos_math = 175
        self.cos_dir = "down"
        self.curtime = 0
        self.title_image = arcade.load_texture("images/title.png")
        self.lose_switch = False
        self.death_floaters = []
        self.paused = False
        self.bck_x = int(SCREEN_WIDTH / 2)
        self.bck_y = int(SCREEN_HEIGHT / 2)
        self.diff_open = True
        self.enemy_list_debug = False

        # Backgrounds
        self.bg_switch = False
        self.draw_timer = 0
        self.bg_x_timer = 0
        self.bg_x = []
        self.backgrounds = []
        path = "images/backgrounds"
        temp_bg = os.listdir(path)
        for bg in temp_bg:
            self.backgrounds.append(arcade.load_texture(path + "/" + bg))

        for i in range(len(self.backgrounds)):
            self.bg_x.append((i * 1440) - 720)


        # Skills menu
        globalvars.skills_opened = False
        self.menu_skill = skills_menu.Menu()

        # Spell select menu
        self.spell_select_open = False

        # Errorbox
        self.errorbox_message = ""
        self.errorbox_timer = 0

        # Cheat menu
        self.cheat_menu = False
        self.cheat_text = ""
        self.cheating = False

        # Gui
        self.go_button = arcade.load_texture("images/TD/GUI/go_button.png")
        self.tower_menu_main = arcade.load_texture("images/TD/GUI/tower_gui.png")
        self.tower_menu_max = arcade.load_texture("images/TD/GUI/tower_gui_maxbutton.png")
        self.tower_menu_age_blank = arcade.load_texture("images/TD/GUI/age_button_blank.png")
        self.tower_menu_win_blank = arcade.load_texture("images/TD/GUI/win_button_blank.png")
        self.tower_menu_age = arcade.load_texture("images/TD/GUI/age_button.png")
        self.tower_menu_age2 = arcade.load_texture("images/TD/GUI/age_button_2.png")
        self.tower_menu_age3 = arcade.load_texture("images/TD/GUI/age_button_3.png")
        self.village_stone = arcade.load_texture("images/TD/village_stone.png")
        self.village_medieval = arcade.load_texture("images/TD/village_medieval.png")
        self.village_industrial = arcade.load_texture("images/TD/village_industrial.png")
        self.tower_menu_button_stone = []
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_1.png"))
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_2.png"))
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_3.png"))
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_4.png"))
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_5.png"))
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_6.png"))
        self.tower_menu_button_stone.append(arcade.load_texture("images/TD/GUI/tower_button_7.png"))
        self.tower_menu_button_medieval = []
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_1.png"))
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_2.png"))
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_3.png"))
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_4.png"))
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_5.png"))
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_6.png"))
        self.tower_menu_button_medieval.append(arcade.load_texture("images/TD/GUI/medieval_button_7.png"))
        self.tower_menu_button_industrial = []
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_1.png"))
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_2.png"))
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_3.png"))
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_4.png"))
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_5.png"))
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_6.png"))
        self.tower_menu_button_industrial.append(arcade.load_texture("images/TD/GUI/industrial_button_7.png"))
        self.skills_button = arcade.load_texture("images/UI/buttons/skills_button.png")
        self.spells_button = arcade.load_texture("images/UI/buttons/spells_button.png")
        self.gear_button = arcade.load_texture("images/UI/buttons/gear.png")

        # Wave Logic
        self.enemy_queue = []
        self.enemy_delay = 0
        self.wave = 0
        self.countdown = 61
        self.countdown_bound = 61
        self.countdown_logic = 0
        self.spawn_logic = 0

        self.win = False

        # Sprites
        self.instruction_screen = []

        for i in range(1, 6):
            self.instruction_screen.append(arcade.load_texture("images/instructions/" + str(i) + ".png"))

        self.towers_stone = []
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/deadfall_set.png"))
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/clubman_default.png"))
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/caveman_default.png"))
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/caveman_blowgun.png"))
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/boulder.png"))
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/caveman_money_default.png"))
        self.towers_stone.append(arcade.load_texture("images/TD/entities/towers/stone/atlatl_default.png"))

        self.towers_medieval = []
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/spikes_default.png"))
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/knight_default.png"))
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/jav_default.png"))
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/archer/archer_ready.png"))
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_1.png"))
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/farm.png"))
        self.towers_medieval.append(arcade.load_texture("images/TD/entities/towers/medieval/mage/mage_idle_1.png"))

        self.towers_industrial = []
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/landmine_unlit.png"))
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/shotgun/shotgun_idle.png"))
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/ar2/idle.png"))
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/sniper/idle.png"))
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/plane.png"))
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/oil_1.png"))
        self.towers_industrial.append(arcade.load_texture("images/TD/entities/towers/industrial/tank_base.png"))

        self.skeletons_normal = []
        self.skeletons_normal.append("images/TD/entities/skeletons/skeleton_axe.png")
        self.skeletons_normal.append("images/TD/entities/skeletons/skeleton_bow.png")
        self.skeletons_normal.append("images/TD/entities/skeletons/skeleton_sword.png")

        self.skeletons_armored = []
        self.skeletons_armored.append("images/TD/entities/skeletons/armored_skeleton_axe.png")
        self.skeletons_armored.append("images/TD/entities/skeletons/armored_skeleton_sword.png")

        self.skeletons_hyper = []
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_base.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_1.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_2.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_3.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_4.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_5.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_6.png"))
        self.skeletons_hyper.append(arcade.load_texture("images/TD/entities/skeletons/skeleton_test.png"))

        self.skeletons_lich_shield = []
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/shield_1.png"))
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/shield_2.png"))
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/shield_3.png"))
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/shield_4.png"))
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/shield_5.png"))
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/lich_shield_hit.png"))
        self.skeletons_lich_shield.append(arcade.load_texture("images/TD/entities/skeletons/lich_shield/lich_hit.png"))

        arcade.set_background_color(arcade.color.WHITE)

        self.setup_towerdata("stone")

    def setup_towerdata(self, age):
        self.tower_data = []
        tw_temp = None
        if age == "stone":
            tw_temp = gamedata.Tower_Stone_Trap("images/TD/entities/towers/stone/deadfall_set.png")
            tw_temp.attack_radius = 25
            tw_temp.damage = 200
            tw_temp.fire_rate = 10
            tw_temp.price = 50
            tw_temp.sellable = False
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/deadfall_used.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Person_1("images/TD/entities/towers/stone/clubman_default.png")
            tw_temp.attack_radius = 50
            tw_temp.damage = 75
            tw_temp.fire_rate = 1.65
            tw_temp.price = 75
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/clubman_attack_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/clubman_attack_2.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Person_2("images/TD/entities/towers/stone/caveman_default.png")
            tw_temp.attack_radius = 150
            tw_temp.damage = 25
            tw_temp.fire_rate = 1.0
            tw_temp.price = 125
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/caveman_throw.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Person_3("images/TD/entities/towers/stone/caveman_blowgun.png")
            tw_temp.attack_radius = 500
            tw_temp.damage = 100
            tw_temp.fire_rate = 6.65
            tw_temp.price = 250
            tw_temp.sellable = True
            tw_temp.anims = []
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Boulder("images/TD/entities/towers/stone/boulder.png")
            tw_temp.attack_radius = 30
            tw_temp.damage = 10
            tw_temp.fire_rate = 1.0
            tw_temp.price = 300
            tw_temp.sellable = True
            tw_temp.anims = []
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Money("images/TD/entities/towers/stone/caveman_money_default.png")
            tw_temp.attack_radius = 50
            tw_temp.damage = 1
            tw_temp.fire_rate = 1.0
            tw_temp.price = 300
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/caveman_money_1.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Person_1("images/TD/entities/towers/stone/atlatl_default.png")
            tw_temp.attack_radius = 250
            tw_temp.damage = 100
            tw_temp.fire_rate = 1.5
            tw_temp.price = 500
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/atlatl_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/stone/atlatl_2.png"))
            self.tower_data.append(tw_temp)
        elif age == "medieval":
            tw_temp = gamedata.Tower_Medieval_Trap("images/TD/entities/towers/medieval/spikes_default.png")
            tw_temp.attack_radius = 25
            tw_temp.damage = 200
            tw_temp.fire_rate = 5
            tw_temp.price = 100
            tw_temp.sellable = False
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/spikes_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/spikes_2.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/spikes_3.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Medieval_Person_1("images/TD/entities/towers/medieval/knight_default.png")
            tw_temp.attack_radius = 50
            tw_temp.damage = 100
            tw_temp.fire_rate = 1
            tw_temp.price = 150
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/knight_1.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Medieval_Person_2("images/TD/entities/towers/medieval/jav_default.png")
            tw_temp.attack_radius = 175
            tw_temp.damage = 100
            tw_temp.fire_rate = 1.5
            tw_temp.price = 350
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/jav_1.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Medieval_Person_3("images/TD/entities/towers/medieval/archer/archer_ready.png")
            tw_temp.attack_radius = 250
            tw_temp.damage = 100
            tw_temp.fire_rate = 1.5
            tw_temp.price = 500
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/archer/archer_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/archer/archer_fired.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/archer/archer_empty.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/archer/archer_reload.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Medieval_Special("images/TD/entities/towers/medieval/horse_1.png")
            tw_temp.attack_radius = 45
            tw_temp.damage = 10
            tw_temp.fire_rate = 1.0
            tw_temp.price = 750
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_2.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_3.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_4.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_5.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_6.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_7.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/horse_8.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Money("images/TD/entities/towers/medieval/farm.png")
            tw_temp.attack_radius = 50
            tw_temp.damage = 3
            tw_temp.fire_rate = 1.0
            tw_temp.price = 900
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/farm.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Medieval_Super("images/TD/entities/towers/medieval/mage/mage_attack.png")
            tw_temp.attack_radius = 250
            tw_temp.damage = 50
            tw_temp.fire_rate = .25
            tw_temp.price = 1500
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/medieval/mage/mage_attack.png"))
            for i in range(10):
                txt_str = "images/TD/entities/towers/medieval/mage/mage_idle_" + str(i + 1) + ".png"
                tw_temp.anims.append(arcade.load_texture(txt_str))
            self.tower_data.append(tw_temp)
        elif age == "industrial":
            tw_temp = gamedata.Tower_Industrial_Trap("images/TD/entities/towers/industrial/landmine_unlit.png")
            tw_temp.attack_radius = 25
            tw_temp.damage = 20
            tw_temp.fire_rate = 1
            tw_temp.price = 200
            tw_temp.sellable = False
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/landmine_lit.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Industrial_Person_1("images/TD/entities/towers/industrial/shotgun/shotgun_idle.png")
            tw_temp.attack_radius = 125
            tw_temp.damage = 24
            tw_temp.fire_rate = 1.28
            tw_temp.price = 750
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/shotgun/shotgun_shoot.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/shotgun/shotgun_pump.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/shotgun/reload_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/shotgun/reload_2.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Industrial_Person_2("images/TD/entities/towers/industrial/ar2/idle.png")
            tw_temp.attack_radius = 225
            tw_temp.damage = 25
            tw_temp.fire_rate = .1
            tw_temp.price = 1500
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/ar2/shoot.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/ar2/reload_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/ar2/reload_2.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Industrial_Person_3("images/TD/entities/towers/industrial/sniper/idle.png")
            tw_temp.attack_radius = 1000
            tw_temp.damage = 1000
            tw_temp.fire_rate = 5
            tw_temp.price = 2000
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/sniper/shoot.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/sniper/reload_1.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/sniper/reload_2.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Medieval_Special("images/TD/entities/towers/industrial/plane.png")
            tw_temp.attack_radius = 64
            tw_temp.damage = 60
            tw_temp.fire_rate = 1.0
            tw_temp.price = 2000
            tw_temp.sellable = True
            tw_temp.anims = []
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Stone_Money("images/TD/entities/towers/industrial/oil_1.png")
            tw_temp.attack_radius = 50
            tw_temp.damage = 9
            tw_temp.fire_rate = 1.0
            tw_temp.price = 2500
            tw_temp.sellable = True
            tw_temp.anims = []
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/oil_2.png"))
            tw_temp.anims.append(arcade.load_texture("images/TD/entities/towers/industrial/oil_3.png"))
            self.tower_data.append(tw_temp)

            tw_temp = gamedata.Tower_Industrial_Super("images/TD/entities/towers/industrial/tank_base.png")
            tw_temp.attack_radius = 500
            tw_temp.damage = 500
            tw_temp.fire_rate = 5
            tw_temp.price = 10000
            tw_temp.sellable = False
            tw_temp.anims = []
            self.tower_data.append(tw_temp)

    def create_map(self):
        print("map created")
        # Logic
        self.curtime = 0
        self.curtime_logic = 0
        self.ghost_timer = 0
        self.ghost_x = 0
        self.ghost_y = 0
        self.enemy_timer = 0
        self.age = "stone"

        # Sprite lists
        self.all_sprites_list = None
        self.floor_list = None
        self.wall_list = None

        # Create Map
        self.useless = 0
        self.doorpos = 3
        self.direction = "right"
        self.tilesize = 48
        self.tilesize_half = 24
        self.blocks_length_x = 31
        self.blocks_length_y = 17
        self.blocks_created = 0

        # Snake Logic
        self.snake_counter = 0
        self.node_graph_x = [1, 2, 3]
        self.node_graph_y = [self.doorpos, self.doorpos, self.doorpos]
        self.node_direction = [[True for self.useless in range(self.blocks_length_y + 5)] for self.useless in range(self.blocks_length_x + 5)]
        self.node_direction[0][self.doorpos] = "right"
        self.node_direction[1][self.doorpos] = "right"
        self.node_direction[2][self.doorpos] = "right"
        self.node_direction[3][self.doorpos] = "right"
        self.r_warn = 5
        self.l_warn = 5
        self.u_warn = 5
        self.d_warn = 5
        self.clean_count_r = 0
        self.clean_count_l = 0
        self.clean_count_u = 0
        self.clean_count_d = 0

        # Changing these variables will influence the snake generation algorithm, higher numbers = less likely to happen
        # The following demonstrates the general idea of how each penalty works:
        """
            x = path (aka, body of snake)
            M = edge of map
            || = where it's trying to place path
            o = head of snake (most recently placed path)
            A = air
            
            Clean Three Intersection:
                           x 
                x x x x o |x|
                           x
                                
            "Dirty" Non-Clean Intersection:
                           x 
                x x x x o |x|
            
            Incoming:
                x x x x x o |A| x
                
            Double:
                x x x x x o |A| x x
                
            Map:
                x x x x x o |A| M
                 
            Adjacdent:
                x x x x x o |A|
                             x   
                              
            Diagonal:
                x x x x x o |A|
                                x
        """

        self.penalty_clean = -1  # Penalty for a clean intersection, set to negative to encourage it
        self.penalty_nonclean = 2  # Penalty for a non-clean intersection
        self.penalty_map = 3  # Penalty for getting close to edges of map (increases exponentially the closer you get)
        self.penalty_incoming = 1  # Penalty for going towards a previously placed path
        self.penalty_double = 1  # Penalty for going towards a double
        self.penalty_adjacent = 0  # Penalty for trying to place a path adjacent to another path
        self.penalty_diagonal = 1  # Penalty for trying to place a path diagonal to another path

        # GUI
        self.tower_menu_open = True
        self.placing_tower = False
        self.selected_tower = 0
        self.valid_tower_spot = False

        # Other
        self.debug_x = 0
        self.debug_y = 0
        self.old_dir = "right"
        self.crash_detection = 0
        self.village_pos_y = 0
        # self.level_text = arcade.create_text("0", [50, 64, 200], 24)

        self.all_sprites_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        # globalvars.enemy_list = arcade.SpriteList()
        self.tower_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        def cords_inside_map(cord_x, cord_y):
            inside_map = False
            if self.blocks_length_x > cord_x > 0 and self.blocks_length_y > cord_y > 0:
                inside_map = True
            return inside_map

        def cd_clean_three_check(ctc_x, ctc_y, ctc_dir):
            is_clean = False
            # Clean intersection - right
            if ctc_dir == "right":
                if cords_inside_map(ctc_x, ctc_y + 1) and cords_inside_map(ctc_x, ctc_y - 1):
                    if blocks[ctc_x][ctc_y + 1] and blocks[ctc_x][ctc_y - 1]:
                        if cords_inside_map(ctc_x + 1, ctc_y + 1) and cords_inside_map(ctc_x + 1, ctc_y - 1):
                            if not blocks[ctc_x + 1][ctc_y + 1] and not blocks[ctc_x + 1][ctc_y - 1] and not blocks[ctc_x + 1][ctc_y]:
                                is_clean = True
                                self.r_warn -= self.penalty_clean

            # Clean intersection left
            if ctc_dir == "left":
                if cords_inside_map(ctc_x, ctc_y + 1) and cords_inside_map(ctc_x, ctc_y - 1):
                    if blocks[ctc_x][ctc_y + 1] and blocks[ctc_x][ctc_y - 1]:
                        if cords_inside_map(ctc_x - 1, ctc_y + 1) and cords_inside_map(ctc_x - 1, ctc_y - 1):
                            if not blocks[ctc_x - 1][ctc_y + 1] and not blocks[ctc_x - 1][ctc_y - 1] and not blocks[ctc_x - 1][ctc_y]:
                                is_clean = True
                                self.l_warn -= self.penalty_clean

            # Clean intersection up
            if ctc_dir == "up":
                if cords_inside_map(ctc_x + 1, ctc_y) and cords_inside_map(ctc_x - 1, ctc_y):
                    if blocks[ctc_x + 1][ctc_y] and blocks[ctc_x - 1][ctc_y]:
                        if cords_inside_map(ctc_x + 1, ctc_y + 1) and cords_inside_map(ctc_x - 1, ctc_y + 1):
                            if not blocks[ctc_x + 1][ctc_y + 1] and not blocks[ctc_x - 1][ctc_y + 1] and not blocks[ctc_x][ctc_y + 1]:
                                is_clean = True
                                self.u_warn -= self.penalty_clean

            # Clean intersection down
            if ctc_dir == "down":
                if cords_inside_map(ctc_x + 1, ctc_y) and cords_inside_map(ctc_x - 1, ctc_y):
                    if blocks[ctc_x + 1][ctc_y] and blocks[ctc_x - 1][ctc_y]:
                        if cords_inside_map(ctc_x + 1, ctc_y - 1) and cords_inside_map(ctc_x - 1, ctc_y - 1):
                            if not blocks[ctc_x + 1][ctc_y - 1] and not blocks[ctc_x - 1][ctc_y - 1] and not blocks[ctc_x][ctc_y - 1]:
                                is_clean = True
                                self.d_warn -= self.penalty_clean

            return is_clean

        def cd_incoming_block_check(ibc_x, ibc_y, ibc_dir):
            if ibc_dir == "right":
                # Excessive map boundary - right
                if ibc_x == self.blocks_length_x:
                    self.r_warn -= 100
                    self.l_warn += 100
                    self.clean_count_l = 3
                # Map boundary - right
                if ibc_x + 3 >= self.blocks_length_x:
                    local_penalty = ((ibc_x + 3) - self.blocks_length_x) * self.penalty_map
                    self.r_warn -= local_penalty
                if cords_inside_map(ibc_x + 2, ibc_y):
                    # Non_clean - right
                    if not blocks[ibc_x][ibc_y]:
                        self.r_warn -= self.penalty_nonclean
                    # Incoming block close - right
                    if not blocks[ibc_x+1][ibc_y]:
                        self.r_warn -= self.penalty_incoming
                    # Incoming block far - right
                    if not blocks[ibc_x+2][ibc_y]:
                        self.r_warn -= self.penalty_incoming
                    # Double incoming block - right
                    if not blocks[ibc_x+1][ibc_y] and not blocks[ibc_x+2][ibc_y]:
                        self.r_warn -= self.penalty_double

            if ibc_dir == "left":
                # Excessive map boundary
                if ibc_x == 1:
                    self.l_warn -= 100
                    self.r_warn += 100
                    self.clean_count_r = 3
                # Map boundary
                if ibc_x - 3 <= 1:
                    local_penalty = (1 - (ibc_x - 3)) * self.penalty_map
                    self.l_warn -= local_penalty
                if cords_inside_map(ibc_x - 2, ibc_y):
                    # Non-clean - left
                    if not blocks[ibc_x][ibc_y]:
                        self.l_warn -= self.penalty_nonclean
                    # Incoming - left
                    if not blocks[ibc_x-1][ibc_y]:
                        self.l_warn -= self.penalty_incoming
                    # Incoming - left
                    if not blocks[ibc_x-2][ibc_y]:
                        self.l_warn -= self.penalty_incoming
                    # Double incoming - left
                    if not blocks[ibc_x-1][ibc_y] and not blocks[ibc_x-2][ibc_y]:
                        self.l_warn -= self.penalty_double

            if ibc_dir == "up":
                # Excessive map - up
                if ibc_y == self.blocks_length_y:
                    self.u_warn -= 100
                    self.d_warn += 100
                    self.clean_count_d = 3
                # Map boundary - up
                if ibc_y + 3 >= self.blocks_length_y:
                    local_penalty = ((ibc_y + 3) - self.blocks_length_y) * self.penalty_map
                    self.u_warn -= local_penalty
                if cords_inside_map(ibc_x, ibc_y + 2):
                    # Nonclean - up
                    if not blocks[ibc_x][ibc_y]:
                        self.u_warn -= self.penalty_nonclean
                    # Incoming - up
                    if not blocks[ibc_x][ibc_y+1]:
                        self.u_warn -= self.penalty_incoming
                    # Incoming - up
                    if not blocks[ibc_x][ibc_y+2]:
                        self.u_warn -= self.penalty_incoming
                    # Double incoming - up
                    if not blocks[ibc_x][ibc_y+1] and not blocks[ibc_x][ibc_y+2]:
                        self.u_warn -= self.penalty_double

            if ibc_dir == "down":
                # Excessive map boundary - down
                if ibc_y == 1:
                    self.d_warn -= 100
                    self.u_warn += 100
                    self.clean_count_u = 3
                # Map boundary - down
                if ibc_y - 3 <= 1:
                    local_penalty = (1 - (ibc_y - 3)) * self.penalty_map
                    self.d_warn -= local_penalty
                if cords_inside_map(ibc_x, ibc_y - 2):
                    # Nonclean - down
                    if not blocks[ibc_x][ibc_y]:
                        self.d_warn -= self.penalty_nonclean
                    # Incmoing - down
                    if not blocks[ibc_x][ibc_y-1]:
                        self.d_warn -= self.penalty_incoming
                    # Incoming - down
                    if not blocks[ibc_x][ibc_y-2]:
                        self.d_warn -= self.penalty_incoming
                    # Double incoming - down
                    if not blocks[ibc_x][ibc_y-1] and not blocks[ibc_x][ibc_y-2]:
                        self.d_warn -= self.penalty_double

        def cd_diagonal_block_check(dbc_x, dbc_y, dbc_dir):
            if dbc_dir == "right":
                # Adjacent penalty - right
                if cords_inside_map(dbc_x, dbc_y + 1) and cords_inside_map(dbc_x, dbc_y - 1):
                    if not blocks[dbc_x][dbc_y + 1]:
                        self.r_warn -= self.penalty_adjacent
                    if not blocks[dbc_x][dbc_y - 1]:
                        self.r_warn -= self.penalty_adjacent
                # Diagonal penalty - right
                if cords_inside_map(dbc_x + 1, dbc_y + 1) and cords_inside_map(dbc_x + 1, dbc_y - 1):
                    if not blocks[dbc_x + 1][dbc_y + 1]:
                        self.r_warn -= self.penalty_diagonal
                    if not blocks[dbc_x + 1][dbc_y - 1]:
                        self.r_warn -= self.penalty_diagonal

            if dbc_dir == "left":
                # Adjacent penalty - left
                if cords_inside_map(dbc_x, dbc_y + 1) and cords_inside_map(dbc_x, dbc_y - 1):
                    if not blocks[dbc_x][dbc_y + 1]:
                        self.l_warn -= self.penalty_adjacent
                    if not blocks[dbc_x][dbc_y - 1]:
                        self.l_warn -= self.penalty_adjacent
                # Diagonal penalty - left
                if cords_inside_map(dbc_x - 1, dbc_y + 1) and cords_inside_map(dbc_x - 1, dbc_y - 1):
                    if not blocks[dbc_x - 1][dbc_y + 1]:
                        self.l_warn -= self.penalty_diagonal
                    if not blocks[dbc_x - 1][dbc_y - 1]:
                        self.l_warn -= self.penalty_diagonal

            if dbc_dir == "up":
                # Adjacent penalty - up
                if cords_inside_map(dbc_x + 1, dbc_y) and cords_inside_map(dbc_x - 1, dbc_y):
                    if not blocks[dbc_x + 1][dbc_y]:
                        self.u_warn -= self.penalty_adjacent
                    if not blocks[dbc_x - 1][dbc_y]:
                        self.u_warn -= self.penalty_adjacent
                # Diagonal penalty - up
                if cords_inside_map(dbc_x + 1, dbc_y + 1) and cords_inside_map(dbc_x - 1, dbc_y + 1):
                    if not blocks[dbc_x + 1][dbc_y + 1]:
                        self.u_warn -= self.penalty_diagonal
                    if not blocks[dbc_x - 1][dbc_y + 1]:
                        self.u_warn -= self.penalty_diagonal

            if dbc_dir == "down":
                # Adjacent penalty - down
                if cords_inside_map(dbc_x + 1, dbc_y) and cords_inside_map(dbc_x - 1, dbc_y):
                    if not blocks[dbc_x + 1][dbc_y]:
                        self.d_warn -= self.penalty_adjacent
                    if not blocks[dbc_x - 1][dbc_y]:
                        self.d_warn -= self.penalty_adjacent
                # Diagonal penalty - down
                if cords_inside_map(dbc_x + 1, dbc_y - 1) and cords_inside_map(dbc_x - 1, dbc_y - 1):
                    if not blocks[dbc_x + 1][dbc_y - 1]:
                        self.d_warn -= self.penalty_diagonal
                    if not blocks[dbc_x - 1][dbc_y - 1]:
                        self.d_warn -= self.penalty_diagonal


        def choose_next_direction(pos_x, pos_y):
            # Check all the penalties based on the current position and where the block wants to go:
            self.r_warn = 5
            self.l_warn = 5
            self.u_warn = 5
            self.d_warn = 5
            ghost_x = pos_x
            ghost_y = pos_y

            if self.clean_count_r > 0:
                self.clean_count_r -= 1
            if self.clean_count_l > 0:
                self.clean_count_l -= 1
            if self.clean_count_d > 0:
                self.clean_count_d -= 1
            if self.clean_count_u > 0:
                self.clean_count_u -= 1

            if self.direction == "right":
                if cd_clean_three_check(ghost_x + 1, ghost_y, "right"):
                    self.clean_count_r = 2

            if self.direction == "left":
                if cd_clean_three_check(ghost_x - 1, ghost_y, "left"):
                    self.clean_count_l = 2

            if self.direction == "up":
                if cd_clean_three_check(ghost_x, ghost_y + 1, "up"):
                    self.clean_count_u = 2

            if self.direction == "down":
                if cd_clean_three_check(ghost_x, ghost_y - 1, "down"):
                    self.clean_count_d = 2

            if self.clean_count_r < 1:
                cd_incoming_block_check(ghost_x + 1, ghost_y, "right")
                cd_diagonal_block_check(ghost_x + 1, ghost_y, "right")

            if self.clean_count_l < 1:
                cd_incoming_block_check(ghost_x - 1, ghost_y, "left")
                cd_diagonal_block_check(ghost_x - 1, ghost_y, "left")

            if self.clean_count_u < 1:
                cd_incoming_block_check(ghost_x, ghost_y + 1, "up")
                cd_diagonal_block_check(ghost_x, ghost_y + 1, "up")

            if self.clean_count_d < 1:
                cd_incoming_block_check(ghost_x, ghost_y - 1, "down")
                cd_diagonal_block_check(ghost_x, ghost_y - 1, "down")

            local_new_dir = "right"
            local_total_equal = 0
            local_valid_options = []
            temp_arr = [self.r_warn, self.l_warn, self.u_warn, self.d_warn]
            local_highest = max(temp_arr)
            if self.r_warn == local_highest:
                local_total_equal += 1
                local_valid_options.append("right")

            if self.l_warn == local_highest:
                local_total_equal += 1
                local_valid_options.append("left")

            if self.u_warn == local_highest:
                local_total_equal += 1
                local_valid_options.append("up")

            if self.d_warn == local_highest:
                local_total_equal += 1
                local_valid_options.append("down")

            # If this runs the generation is stuck, so force it to go right.
            if local_total_equal == 4:
                self.r_warn = 0

            if local_total_equal == 3:
                local_chance = random.randint(1, 5)
                if local_chance == 2:
                    if len(local_valid_options) > 0:
                        local_new_dir = random.choice(local_valid_options)
                    else:
                        local_new_dir = self.direction
                        print("Error: Array Size")
                else:
                    local_new_dir = self.direction

            if local_total_equal < 3:
                if len(local_valid_options) > 0:
                    local_new_dir = random.choice(local_valid_options)
                else:
                    local_new_dir = self.direction
                    print("Error: Array Size")

            # Prevents overly-complicated maps from forming by forcing it to go right after a limit.
            if self.blocks_created > 150:
                local_new_dir = "right"

            self.direction = local_new_dir

        # Initialize double array
        blocks = [[True for self.useless in range(self.blocks_length_y)] for self.useless in range(self.blocks_length_x)]

        blocks[1][self.doorpos] = True
        blocks[2][self.doorpos] = False
        blocks[3][self.doorpos] = False
        x = 3
        y = self.doorpos
        stop = False
        while not stop:    # While the snake isn't on the extend of the right
            choose_next_direction(x, y)
            if self.direction == "right":   # Move the snake in the correct direction
                x += 1
            if self.direction == "left":
                x -= 1
            if self.direction == "up":
                y += 1
            if self.direction == "down":
                y -= 1

            # If snake ends up out of map force it back in
            if x < 1:
                x += 1
                self.clean_count_r = 3
                self.direction = "right"
            if y < 1:
                y += 1
                self.clean_count_u = 3
                self.direction = "up"
            if y > (self.blocks_length_y - 1):
                y -= 1
                self.clean_count_d = 3
                self.direction = "down"

            blocks[x][y] = False
            self.node_graph_x.append(x)
            self.node_graph_y.append(y)
            self.snake_counter += 1
            self.blocks_created += 1
            if self.node_direction[x][y] == True:
                self.node_direction[x][y] = self.direction

            self.crash_detection += 1

            if self.crash_detection > 1000:
                self.crash_detection = 0
                print("Map generation attempt failed! Restarting...")
                stop = True
                self.setup()
                self.create_map()

            if x >= 28 and self.snake_counter > 50:
                blocks[x+1][y] = True
                self.node_graph_x.append(x+1)
                self.node_graph_y.append(y)
                self.node_direction[x+1][y] = self.direction
                blocks[self.blocks_length_x - 1][y] = "DOOR"
                stop = True

        node_track = [[True for self.useless in range(self.blocks_length_y)] for self.useless in range(self.blocks_length_x)]
        for i in range(len(self.node_graph_x)):
            local_dir = self.node_direction[self.node_graph_x[i]][self.node_graph_y[i]]
            next_dir = "right"
            if i < len(self.node_graph_x) - 1:
                next_dir = self.node_direction[self.node_graph_x[i+1]][self.node_graph_y[i+1]]

            if node_track[self.node_graph_x[i]][self.node_graph_y[i]] == True:
                floor = arcade.Sprite("images/TD/dirt_test_2.png", 1)
                if local_dir == "right" and next_dir == "right":
                    floor = arcade.Sprite("images/TD/paths/pathLR.png", 1)
                    # print("place LR")
                if local_dir == "left" and next_dir == "left":
                    floor = arcade.Sprite("images/TD/paths/pathLR.png", 1)
                    # print("place LR")
                if local_dir == "up" and next_dir == "up":
                    floor = arcade.Sprite("images/TD/paths/pathUD.png", 1)
                    # print("place UD")
                if local_dir == "down" and next_dir == "down":
                    floor = arcade.Sprite("images/TD/paths/pathUD.png", 1)
                    # print("place UD")

                if local_dir == "right" and next_dir == "up":
                    floor = arcade.Sprite("images/TD/paths/pathDR.png", 1)
                    # print("place DR")
                if local_dir == "right" and next_dir == "down":
                    floor = arcade.Sprite("images/TD/paths/pathRU.png", 1)
                    # print("place RU")

                if local_dir == "up" and next_dir == "left":
                    floor = arcade.Sprite("images/TD/paths/pathRU.png", 1)
                    # print("place RU")
                if local_dir == "up" and next_dir == "right":
                    floor = arcade.Sprite("images/TD/paths/pathLU.png", 1)
                    # print("place LU")

                if local_dir == "down" and next_dir == "left":
                    floor = arcade.Sprite("images/TD/paths/pathDR.png", 1)
                    # print("place DR")
                if local_dir == "down" and next_dir == "right":
                    floor = arcade.Sprite("images/TD/paths/pathLD.png", 1)
                    # print("place LD")

                if local_dir == "left" and next_dir == "down":
                    floor = arcade.Sprite("images/TD/paths/pathLU.png", 1)
                    # print("place LU")
                if local_dir == "left" and next_dir == "up":
                    floor = arcade.Sprite("images/TD/paths/pathLD.png", 1)
                    # print("place LD")
                node_track[self.node_graph_x[i]][self.node_graph_y[i]] = False

                floor.center_x = (self.node_graph_x[i] * self.tilesize) - self.tilesize_half
                floor.center_y = (self.node_graph_y[i] * self.tilesize) - self.tilesize_half
                self.all_sprites_list.append(floor)
                self.floor_list.append(floor)
            else:
                if local_dir == "right" or local_dir == "left":
                    floor = arcade.Sprite("images/TD/paths/path_connect_LR_2.png", 1)
                    floor.center_x = (self.node_graph_x[i] * self.tilesize) - self.tilesize_half
                    floor.center_y = (self.node_graph_y[i] * self.tilesize) - self.tilesize_half
                    self.all_sprites_list.append(floor)
                    self.floor_list.append(floor)
                else:
                    floor = arcade.Sprite("images/TD/paths/path_connect_UD_2.png", 1)
                    floor.center_x = (self.node_graph_x[i] * self.tilesize) - self.tilesize_half
                    floor.center_y = (self.node_graph_y[i] * self.tilesize) - self.tilesize_half
                    self.all_sprites_list.append(floor)
                    self.floor_list.append(floor)

        for x in range(len(blocks)):
            for y in range(len(blocks[0])):
                if blocks[x][y] == "DOOR":
                    self.village_pos_y = y * 48

        wall = arcade.Sprite("images/TD/graves.png", 1)
        wall.center_x = self.tilesize_half
        wall.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
        self.all_sprites_list.append(wall)
        self.wall_list.append(wall)

    def on_draw(self):
        arcade.start_render()

        if self.main_menu_open:
            for i in range(len(self.backgrounds)):
                arcade.draw_texture_rectangle(self.bg_x[i], int(SCREEN_HEIGHT / 2), SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds[i])

            self.draw_timer += 1
            if self.draw_timer > self.bg_x_timer:
                for k in range(len(self.bg_x)):
                    if self.bg_x[k] <= -720:
                        self.bg_x[k] = max(self.bg_x) + SCREEN_WIDTH
                    self.bg_x[k] -= 1

                if max(self.bg_x) % 720 == 0:
                    self.bg_switch = not self.bg_switch
                    if not self.bg_switch:
                        self.bg_x_timer = self.draw_timer + 200

            arcade.draw_texture_rectangle(300, 500, 478, 141, self.button_start)
            arcade.draw_texture_rectangle(300, 300, 478, 141, self.button_instructions)
            arcade.draw_texture_rectangle(300, 100, 478, 141, self.button_exit)
            arcade.draw_texture_rectangle(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, self.gear_button)
            arcade.draw_texture_rectangle(475, 675, 900, 100, self.title_image)
        else:
            arcade.draw_texture_rectangle(self.bck_x, self.bck_y, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_background)

        if not self.main_menu_open and not self.game_started:
            self.all_sprites_list.draw()

            if self.diff_open:
                arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - 25, 42, 16, self.button_diff_min)

                arcade.draw_texture_rectangle(150, SCREEN_HEIGHT - 350, 190, 350, self.button_difficulty)

                difficulty = ""
                color = (0, 0, 0)
                if self.blocks_created >= 150:
                    difficulty = "Easy"
                    color = (46, 232, 52)
                if self.blocks_created < 150:
                    difficulty = "Normal"
                    color = (214, 211, 32)
                if self.blocks_created < 100:
                    difficulty = "Hard"
                    color = (237, 151, 23)
                if self.blocks_created < 60:
                    difficulty = "Very Hard"
                    color = (209, 20, 20)

                arcade.draw_text("Map Difficulty:", 25, 700, (0, 0, 0), 24)
                arcade.draw_text(difficulty, 235, 700, color, 24)

                arcade.draw_text("War Difficulty:", 25, 650, (0, 0, 0), 24)

                arcade.draw_text("Select War Difficulty", 22, 600, (75, 0, 0), 24, bold=True)

                diff_text = "Normal"
                color = (214, 211, 32)

                if globalvars.difficulty == 1:
                    diff_text = "Hard"
                    color = (237, 151, 23)
                elif globalvars.difficulty == 2:
                    diff_text = "NIGHTMARE"
                    color = (209, 20, 20)

                arcade.draw_text(diff_text, 235, 650, color, 24)
            else:
                arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - 25, 42, 16, self.button_diff_max)

            arcade.draw_circle_filled(self.debug_x - self.tilesize_half, self.debug_y - self.tilesize_half, 16, (50, 50, 200, 175))
            arcade.draw_texture_rectangle(int(SCREEN_WIDTH / 2) + 150, 75, 200, 100, self.button_new_start)
            arcade.draw_texture_rectangle(int(SCREEN_WIDTH / 2) - 150, 75, 200, 100, self.button_new_generate)
        if not self.main_menu_open and self.game_started:
            self.floor_list.draw()
            self.wall_list.draw()
            self.bullet_list.draw()
            self.tower_list.draw()
            globalvars.enemy_list.draw()
            self.player.draw()

            # By commenting out globalvars.enemy_list.draw() and placing enemy.draw in the Damage Floaters loop, you could save some
            # efficiency. However, this will force the following two situations:
            # A) Have all the enemies render above the player
            # B) Have all the damage floaters render under the player
            # In order to have both of these render above the player, it must be done this way:

            # Damage Floaters
            for enemy in globalvars.enemy_list:
                floater = enemy.cur_floater

                if floater is not None:
                    arcade.render_text(floater, floater.x_pos, floater.y_pos)
                    floater.die_time -= .1

                    if floater.die_time <= 0:
                        enemy.cur_floater = None

            # Death Floaters
            for floater in self.death_floaters:
                arcade.render_text(floater, floater.x_pos, floater.y_pos)
                floater.die_time -= .1

                if floater.die_time <= 0:
                    self.death_floaters.remove(floater)

            arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - 50, 60, 60, self.skills_button)
            arcade.draw_texture_rectangle(50, SCREEN_HEIGHT - 120, 60, 60, self.spells_button)

            # Spell Select Display
            if len(self.player.spell_icon_list) > 0:
                if self.spell_select_open:
                    for i in range(len(self.player.spell_icon_list)):
                        arcade.draw_texture_rectangle(50, (SCREEN_HEIGHT - 190) - (i * 70), 60, 60, self.player.spell_icon_list[i])
                elif self.player.current_spell_icon is not None:
                    arcade.draw_texture_rectangle(125, SCREEN_HEIGHT - 120, 60, 60, self.player.current_spell_icon)

            # If player has available skillpoints put a flashing number on the skills button.
            if self.player.skillpoints > 0:
                if self.cos_dir == "up":
                    self.cos_math += 1
                elif self.cos_dir == "down":
                    self.cos_math -= 1

                if self.cos_math <= 175:
                    self.cos_dir = "up"
                    self.cos_math = 175
                elif self.cos_math >= 255:
                    self.cos_dir = "down"
                    self.cos_math = 255

                arcade.draw_text(str(self.player.skillpoints), 40, SCREEN_HEIGHT - 60, (28 + (self.cos_math - 175), 101 + (self.cos_math - 175), 219, self.cos_math), 32)

            # Draw Mana Bar
            x_pos = 100
            y_pos = 730

            adjust = 0
            if self.player.mana_cap > 0:
                adjust = self.player.mana / self.player.mana_cap

            right = x_pos + (144 * adjust)
            arcade.draw_lrtb_rectangle_filled(x_pos, right, y_pos + 4, y_pos - 4, (165, 43, 157))
            arcade.draw_rectangle_outline(x_pos + 72, y_pos, 144, 8, (0, 0, 0))
            arcade.draw_text(str(round(self.player.mana_cap)), x_pos + 150, y_pos - 7, (165, 43, 157), 18)

            if self.player.level < 10:
                arcade.render_text(globalvars.level_text, SCREEN_WIDTH - 104, SCREEN_HEIGHT - 50)

                right = 1272 + (144 * (self.player.exp_cur / self.player.exp_cap))

                if right < 1272:
                    right = 1272

                arcade.draw_lrtb_rectangle_filled(1272, right, 748, 740, (50, 64, 200))
                for i in range(9):
                    arcade.draw_rectangle_outline(SCREEN_WIDTH - 160 + (16 * i), SCREEN_HEIGHT - 24, 16, 8, (0, 0, 0))
            else:
                arcade.render_text(globalvars.level_text, SCREEN_WIDTH - 112, SCREEN_HEIGHT - 42)

            if self.countdown < self.countdown_bound:
                arcade.draw_texture_rectangle((SCREEN_WIDTH / 2) - 24, SCREEN_HEIGHT - 128, 128, 24, self.go_button)

            arcade.draw_text("Wave " + str(self.wave), (SCREEN_WIDTH / 2) - 64, SCREEN_HEIGHT - 25, (0, 0, 50, 255), 20)
            if self.countdown < self.countdown_bound:
                arcade.draw_text(str(self.countdown), (SCREEN_WIDTH / 2) - 24 - (24 * len(str(self.countdown))), SCREEN_HEIGHT - 100, (200, 50, 50, 200), 64)

            if self.age == "stone":
                arcade.draw_texture_rectangle(SCREEN_WIDTH - 48, self.village_pos_y - 24, 64, 64, self.village_stone)
            elif self.age == "medieval":
                arcade.draw_texture_rectangle(SCREEN_WIDTH - 48, self.village_pos_y - 8, 64, 64, self.village_medieval)
            elif self.age == "industrial":
                arcade.draw_texture_rectangle(SCREEN_WIDTH - 48, self.village_pos_y - 24, 64, 64, self.village_industrial)

            if not self.placing_tower:
                for towers in self.tower_list:
                    if towers.sellable:
                        mx = self.current_mouse_x
                        my = self.current_mouse_y
                        if (mx - 20) < int(towers.center_x) < (mx + 20) and (my - 20) < int(towers.center_y) < (my + 20):
                            amount = int(towers.price / 4)

                            if self.player.player_has_skill("Bargain"):
                                amount = int(towers.price / 2)

                                if self.player.player_has_skill("Vitality"):
                                    amount = towers.price - int(towers.price / 10)

                            arcade.draw_text("$"+str(amount), mx, my, (0, 100, 0), 12)

            if self.placing_tower:
                local_current_tile_x = int((self.current_mouse_x + 48) / self.tilesize)
                local_current_tile_y = int((self.current_mouse_y + 48) / self.tilesize)
                if self.selected_tower == 0:
                    self.valid_tower_spot = False
                    local_circle_color = (255, 0, 0, 50)
                else:
                    self.valid_tower_spot = True
                    local_circle_color = (0, 255, 0, 50)
                for check in range(len(self.node_graph_x)):
                    if local_current_tile_x == self.node_graph_x[check] and local_current_tile_y == self.node_graph_y[check]:
                        if self.selected_tower == 0:
                            self.valid_tower_spot = True
                            local_circle_color = (0, 255, 0, 50)
                        else:
                            local_circle_color = (255, 0, 0, 50)
                            self.valid_tower_spot = False

                for towers in self.tower_list:
                    c_range = 32
                    if towers.center_x - c_range < self.current_mouse_x < towers.center_x + c_range and towers.center_y - c_range < self.current_mouse_y < towers.center_y + c_range:
                        self.valid_tower_spot = False
                        local_circle_color = (255, 0, 0, 50)

                if globalvars.money < self.tower_data[self.selected_tower].price:
                    self.valid_tower_spot = False
                    local_circle_color = (255, 0, 0, 50)

                if self.age == "stone":
                    arcade.draw_texture_rectangle(self.current_mouse_x, self.current_mouse_y, 32, 32, self.towers_stone[self.selected_tower])
                elif self.age == "medieval":
                    arcade.draw_texture_rectangle(self.current_mouse_x, self.current_mouse_y, 32, 32, self.towers_medieval[self.selected_tower])
                elif self.age == "industrial":
                    arcade.draw_texture_rectangle(self.current_mouse_x, self.current_mouse_y, 32, 32, self.towers_industrial[self.selected_tower])

                if self.age == "industrial" and self.selected_tower == 4:
                    local_circle_color = (0, 255, 0, 50)
                    self.valid_tower_spot = True
                    if globalvars.money < self.tower_data[self.selected_tower].price:
                        self.valid_tower_spot = False
                        local_circle_color = (255, 0, 0, 50)
                    radius = 150
                    arcade.draw_ellipse_outline(self.current_mouse_x - radius, self.current_mouse_y, 150, 100, local_circle_color, 10)
                    arcade.draw_ellipse_outline(self.current_mouse_x + radius, self.current_mouse_y, 150, 100, local_circle_color, 10)
                else:
                    radius = self.tower_data[self.selected_tower].attack_radius
                    arcade.draw_circle_filled(self.current_mouse_x, self.current_mouse_y, radius, local_circle_color)
                arcade.draw_text("Press Right Click to Cancel", 100, 50, (200, 20, 36), 25)

            if self.tower_menu_open and not self.placing_tower and (self.countdown != self.countdown_bound or self.wave == 0):
                arcade.draw_texture_rectangle(int(SCREEN_WIDTH / 2), 64, SCREEN_WIDTH, 128, self.tower_menu_main)

                # new age button
                if self.age == "industrial":
                    arcade.draw_texture_rectangle(SCREEN_WIDTH - 375, 54, 160, 80, self.tower_menu_win_blank)
                else:
                    arcade.draw_texture_rectangle(SCREEN_WIDTH - 375, 54, 160, 80, self.tower_menu_age_blank)

                local_age_money = 0

                if self.age == "stone":
                    local_age_money = globalvars.dv_stoneage[globalvars.difficulty]

                    for stone in range(len(self.tower_data)):
                        arcade.draw_texture_rectangle(64 + (64 * stone) + (64 * stone), 64, 48, 64, self.tower_menu_button_stone[stone])
                        if self.tower_data[stone].price > globalvars.money:
                            arcade.draw_rectangle_filled(64 + (64 * stone) + (64 * stone), 64, 48, 64, (180, 20, 40, 100))
                if self.age == "medieval":
                    local_age_money = globalvars.dv_midage[globalvars.difficulty]

                    for stone in range(len(self.tower_data)):
                        loc_x = 64 + (64 * stone) + (64 * stone)
                        txt_x = loc_x - 16
                        if len(str(self.tower_data[stone].price)) > 3:
                            txt_x = txt_x - len(str(self.tower_data[stone].price))
                        arcade.draw_texture_rectangle(loc_x, 64, 48, 64, self.tower_menu_button_medieval[stone])
                        arcade.draw_text("$"+str(self.tower_data[stone].price), txt_x, 34, (0, 0, 0, 255), 11)
                        if self.tower_data[stone].price > globalvars.money:
                            arcade.draw_rectangle_filled(64 + (64 * stone) + (64 * stone), 64, 48, 64, (180, 20, 40, 100))
                if self.age == "industrial":
                    local_age_money = globalvars.dv_win[globalvars.difficulty]

                    for stone in range(len(self.tower_data)):
                        loc_x = 64 + (64 * stone) + (64 * stone)
                        txt_x = loc_x - 16
                        if len(str(self.tower_data[stone].price)) > 3:
                            txt_x = txt_x - len(str(self.tower_data[stone].price))
                        arcade.draw_texture_rectangle(loc_x, 64, 48, 64, self.tower_menu_button_industrial[stone])
                        arcade.draw_text("$"+str(self.tower_data[stone].price), txt_x, 34, (0, 0, 0, 255), 11)
                        if self.tower_data[stone].price > globalvars.money:
                            arcade.draw_rectangle_filled(64 + (64 * stone) + (64 * stone), 64, 48, 64, (180, 20, 40, 100))

                arcade.draw_text("$" + str(local_age_money), SCREEN_WIDTH - 445, 27, (0, 0, 0, 255), 20, align="left")

            elif not self.placing_tower and (self.countdown != self.countdown_bound or self.wave == 0):
                arcade.draw_texture_rectangle(67, 13, 134, 26, self.tower_menu_max)
            arcade.draw_text("$" + str(globalvars.money), SCREEN_WIDTH - 270, 60, (10, 0, 0), 20)
            arcade.draw_text("Population: " + str(globalvars.population), SCREEN_WIDTH - 270, 30, (10, 0, 0), 20)

        if globalvars.skills_opened:
            self.menu_skill.draw()

        if self.errorbox_timer > self.curtime:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, 50, 360, 60, self.error_box)
            arcade.draw_text(self.errorbox_message, (SCREEN_WIDTH / 2) - 160, 45, (0, 0, 0), 18)

        if self.cheat_menu:
            x_pos = 250
            y_pos = 650
            arcade.draw_rectangle_filled(x_pos, y_pos, 400, 150, (0, 0, 0))
            arcade.draw_rectangle_outline(x_pos, y_pos, 400, 150, (255, 255, 255))
            arcade.draw_text(str(self.cheat_text), x_pos - 180, y_pos + 50, (255, 255, 255), 12)

        if self.cheating:
            arcade.draw_text("CHEATER", SCREEN_WIDTH - 350, SCREEN_HEIGHT - 40, (200, 20, 20), 32)

        if globalvars.population <= 0:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.lose_screen)

        if self.win:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.win_screen)

        if globalvars.population <= 0 or self.win:
            x_pos = 800
            color = (181, 0, 0)
            size = 32
            dmg = 0
            if globalvars.stats_total_dmg > 0:
                dmg = round((globalvars.stats_player_dmg / globalvars.stats_total_dmg) * 100)

            arcade.draw_text(str(globalvars.stats_kills), x_pos, 410, color, size)
            arcade.draw_text(str(globalvars.stats_money), x_pos, 344, color, size)
            arcade.draw_text(str(globalvars.stats_waves), x_pos, 278, color, size)
            arcade.draw_text(str(globalvars.population), x_pos, 212, color, size)
            arcade.draw_text(str(dmg) + "%", x_pos, 146, color, size)

        if self.instructions > len(self.instruction_screen):
            self.instructions = 0

        if self.instructions > 0:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.instruction_screen[self.instructions - 1])

        if self.options_opened:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 960, 512, self.options_screen)

            # If the number has an ASCII value find its associated key, otherwise see if the number represents a key in an array I made.
            for i in range(len(globalvars.keys)):
                seq = globalvars.keys[i]
                result = ""
                for num in seq:
                    char = self.get_key_string(num)

                    if len(result) > 0:
                        result = result + " / " + char
                    else:
                        result = result + char

                # Display the keys bound
                if i < 6:
                    arcade.draw_text(result, 455, 585 - (i * 54), (255, 255, 255), 16)
                else:
                    arcade.draw_text(result, 750, 585 - ((i - 6) * 54), (255, 255, 255), 16)

            if self.key_listening:
                arcade.draw_text("Press the key you want to bind this to", (SCREEN_WIDTH / 2) - 190, 170, (255, 255, 255), 18)

            for item in globalvars.keys:
                if len(item) < 1:
                    arcade.draw_text("You cannot apply until all keys have been bound!", (SCREEN_WIDTH / 2) - 190, 200, (255, 30, 30), 18)

        if self.paused:
            arcade.draw_text("[PAUSED]", (SCREEN_WIDTH / 2) - 140, (SCREEN_HEIGHT / 2), (163, 22, 17), 50)
            arcade.draw_text("Press " + str(self.get_key_string(globalvars.keys[9][0])).upper() + " To Resume", (SCREEN_WIDTH / 2) - 140, (SCREEN_HEIGHT / 2) - 50, (0, 0, 0), 25)

        # if self.enemy_list_debug:
        #     ex_debug = 0
        #
        #     if len(globalvars.enemy_list) > 0:
        #         lch = globalvars.enemy_list[0]
        #         arcade.draw_rectangle_filled(lch.center_x, lch.center_y, 32, 32, (0, 100, 0, 100))
        #
        #     for enemy in globalvars.enemy_list:
        #         arcade.draw_text(str(enemy.health) + " -> " + str(enemy), 250, 650 - (ex_debug * 15), (0, 0, 0), 16)
        #         ex_debug += 1
        #
        #     ex_index = 0
        #
        #     for enemy in globalvars.enemy_list:
        #         arcade.draw_text(str(ex_index), enemy.center_x, enemy.center_y - 16, (0, 0, 0), 16)
        #         ex_index += 1

    def get_key_string(self, num):
        char = ""
        use_library = False

        try:
            char = chr(int(num))
            if int(num) > 200:
                use_library = True
        except:
            char = ""

        if num == "32":
            char = "SPACEBAR"

        if use_library:
            for k in range(len(globalvars.library_number)):
                if globalvars.library_number[k] == num:
                    char = globalvars.library_key[k]

        return char

    def display_errorbox(self, message):
        self.errorbox_timer = self.curtime + 30
        self.errorbox_message = message

    def cheat_code(self, code):
        # I use the try and excepts here in case it tries to convert a letter into an integer
        if code == "quit":
            sys.exit()
        elif code == "win":
            self.win = True
            self.cheating = True
        elif code == "lose":
            globalvars.population = 0
        elif code == "restart":
            self.restart()
        elif code == "restoremana":
            self.cheating = True
            self.player.mana = self.player.mana_cap
        elif code == "nextage":
            if self.age != "industrial":
                if self.age == "stone":
                    self.age = "medieval"
                else:
                    self.age = "industrial"
        elif code == "killall":
            self.cheating = True

            nearby_enemies = self.player.getNearbyEnemies(self.player, 19208)

            for enemy in nearby_enemies:
                enemy.health = 0
                enemy.on_take_damage(10, False)
                enemy.kill()
        elif code == "detectiontest":
            globalvars.enemy_list[0].kill()
        elif code == "endwave":
            self.cheating = True
            self.enemy_queue = []
        elif code == "spawndata":
            self.display_errorbox(str(len(self.enemy_queue)) + " enemies in the queue")
        elif code == "where the wild things are":
            self.cheating = True
            self.player.center_x = random.randint(0, SCREEN_WIDTH)
            self.player.center_y = random.randint(0, SCREEN_HEIGHT)
            self.player.angle += random.randint(1, 360)
            self.player.speed *= -5
            random.shuffle(self.node_graph_x)
            random.shuffle(self.node_graph_y)
            for sound in globalvars.sound_list:
                globalvars.emit_sound(random.choice(globalvars.sound_list))
            for sprite in self.all_sprites_list:
                sprite.angle = random.randint(1, 360)
                sprite.center_x = random.randint(0, SCREEN_WIDTH)
                sprite.center_y = random.randint(0, SCREEN_HEIGHT)
            for enemy in globalvars.enemy_list:
                enemy.speed = 10
                enemy.angle = random.randint(1, 360)
                enemy.center_x = self.player.center_x
                enemy.center_y = self.player.center_y
            for tower in self.tower_list:
                tower.center_x = random.randint(100, SCREEN_WIDTH - 100)
                tower.center_y = random.randint(100, SCREEN_HEIGHT - 100)
                tower.angle = random.randint(1, 360)
            for bullet in self.bullet_list:
                bullet.center_x = SCREEN_WIDTH / 2
                bullet.center_y = SCREEN_HEIGHT / 2
        elif code == "tgm":
            self.cheating = True
            self.player.level = 10
            self.player.mana_cap = 10000
            self.player.mana = 10000
            self.player.skillpoints = 9
            self.player.speed = 5
            globalvars.money = 1000000
            globalvars.population = 1000000
        elif code == "enemy debug":
            self.enemy_list_debug = not self.enemy_list_debug
        elif code[:14] == "player.levelup":
            self.cheating = True
            level = code[15:]
            if level == "":
                self.player.give_exp(self.player.exp_cap - self.player.exp_cur)
            else:
                try:
                    for i in range(int(level)):
                        self.player.give_exp(self.player.exp_cap - self.player.exp_cur)
                except:
                    self.display_errorbox("Cannot set level to " + level)
        elif code[:16] == "player.givespell":
            self.cheating = True
            spell = code[17:]
            spell = spell.title()
            self.player.give_spell(spell)
        elif code[:16] == "player.giveskill":
            self.cheating = True
            skill = code[17:]
            skill = skill.title()
            self.player.give_skill(skill)
        elif code[:14] == "player.setmana":
            self.cheating = True
            mana = code[15:]
            try:
                self.player.mana = int(mana)
            except:
                self.display_errorbox("Cannot set mana to " + mana)
        elif code[:17] == "player.setmaxmana":
            self.cheating = True
            cap = code[18:]
            try:
                self.player.mana_cap = int(cap)
            except:
                self.display_errorbox("Cannot set mana cap to " + cap)
        elif code[:13] == "player.givexp":
            self.cheating = True
            xp = code[14:]
            try:
                self.player.give_exp(int(xp))
            except:
                self.display_errorbox("Cannot give " + xp)
        elif code[:15] == "player.setspeed":
            self.cheating = True
            speed = code[16:]
            try:
                self.player.speed = int(speed)
            except:
                self.display_errorbox("Cannot set speed to " + speed)
        elif code[:18] == "game.setpopulation":
            self.cheating = True
            population = code[19:]
            try:
                globalvars.population = int(population)
            except:
                self.display_errorbox("Cannot set population to " + population)
        elif code[:12] == "game.setwave":
            self.cheating = True
            wave = code[12:]
            try:
                self.wave = int(wave)
            except:
                self.display_errorbox("Cannot set wave to " + wave)
        elif code[:14] == "game.givemoney":
            self.cheating = True
            money = code[14:]
            try:
                globalvars.money += int(money)
            except:
                self.display_errorbox("Cannot set money to " + money)
        elif code[:11] == "game.setage":
            self.cheating = True
            age = code[12:]
            if age == "1" or age == "stone":
                self.age = "stone"
            elif age == "2" or age == "medieval":
                self.age = "medieval"
            elif age == "3" or age == "industrial":
                self.age = "industrial"
        elif code[:15] == "game.spawnenemy":
            self.cheating = True
            name = code[16:]
            if name == "skeleton" or name == "hyperskeleton" or name == "raptor" or name == "lich" or name == "armoredskeleton" or name == "skeletonlord":
                self.enemy_queue.append(name)
            else:
                self.display_errorbox("Invalid enemy type: " + name)

    def on_mouse_motion(self, x, y, dx, dy):
        if globalvars.skills_opened:
            self.menu_skill.move_mouse(x, y)
        if self.game_started:
            self.current_mouse_x = x
            self.current_mouse_y = y
            self.player.current_mouse_x = x
            self.player.current_mouse_y = y

    def on_key_press(self, key, modifiers):
        if self.key_listening:
            self.key_listening = False
            globalvars.keys[self.selected_key].append(str(key))

        if self.game_started:
            if not self.cheat_menu:
                for item in globalvars.keys[9]:
                    if str(item) == str(key):
                        self.paused = not self.paused

                if not self.paused:
                    self.player.key_press(key, modifiers)
            else:
                if key == 65293:    # If Enter insert the code
                    self.cheat_code(self.cheat_text)
                    self.cheat_menu = False
                else:
                    if key != 65505:    # If the key isn't Shift (Shift would be hard to implement and it's not needed.)
                        if key == 65288:   # If backspace remove the last character of the string
                            if len(self.cheat_text) > 0:
                                self.cheat_text = self.cheat_text[:-1]
                        else:
                            # Add buttons you're pressing to the string.
                            self.cheat_text = self.cheat_text + str(chr(key))

            if key == 96:  # If you press Tilde toggle the cheat menu.
                self.cheat_menu = not self.cheat_menu
                self.cheat_text = ""

    def on_key_release(self, key, modifiers):
        if self.game_started:
            self.player.key_release(key, modifiers)

    def restart(self):
        self.setup()
        self.main_menu_open = True
        globalvars.money = globalvars.dv_startingmoney[globalvars.difficulty]
        globalvars.max_population = globalvars.dv_population[globalvars.difficulty]
        globalvars.population = globalvars.max_population
        globalvars.enemy_list = arcade.SpriteList()
        self.player = None
        globalvars.level_text = arcade.create_text("0", [50, 64, 200], 24)
        self.lose_switch = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.paused:
            return None

        if globalvars.population <= 0 or self.win:
            if SCREEN_WIDTH - 250 < x < SCREEN_WIDTH - 150 and 50 < y < 150:
                self.restart()

        if globalvars.skills_opened:
            self.menu_skill.mouse_press(x, y, button, modifiers)
        else:
            if button == arcade.MOUSE_BUTTON_RIGHT:
                if self.placing_tower:
                    self.placing_tower = False
                else:
                    for towers in self.tower_list:
                        if towers.sellable:
                            mx = self.current_mouse_x
                            my = self.current_mouse_y
                            if (mx - 20) < int(towers.center_x) < (mx + 20) and (my - 20) < int(towers.center_y) < (my + 20):
                                globalvars.emit_sound("tower_sell.ogg")
                                towers.kill()
                                buyback = int(towers.price / 4)

                                if self.player.player_has_skill("Bargain"):
                                    buyback = int(towers.price / 2)

                                    if self.player.player_has_skill("Vitality"):
                                        buyback = towers.price - int(towers.price / 10)

                                globalvars.money += buyback

            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.game_started:
                    # Start wave button
                    if self.countdown != self.countdown_bound:
                        if 632 < x < 760 and 628 < y < 652:
                            globalvars.emit_sound("startwave.ogg")
                            self.countdown = 0

                    # Spell Menu
                    if self.spell_select_open:
                        for i in range(len(self.player.spell_icon_list)):
                            local_bounds = 10 < x < 80 and (SCREEN_HEIGHT - 150) - ((i + 1) * 70) < y < (SCREEN_HEIGHT - 85) - ((i + 1) * 70)

                            if local_bounds:
                                globalvars.emit_sound("click.ogg")

                                adj_list = self.player.spell_list.copy()
                                local_done = False

                                while not local_done:
                                    local_finished = True

                                    for item in adj_list:
                                        if item[0] == "passive":
                                            adj_list.remove(item)
                                            local_finished = False
                                            break

                                    local_done = local_finished

                                self.player.selected_spell = adj_list[i]
                                self.player.current_spell_icon = self.player.spell_icon_list[i]
                                self.spell_select_open = False

                    # Skills and spells buttons
                    if not self.placing_tower:
                        if 10 < x < 80 and SCREEN_HEIGHT - 70 < y < SCREEN_HEIGHT - 10:
                            # Open skills screen
                            globalvars.emit_sound("skill_open.ogg")
                            globalvars.skills_opened = True
                        elif 10 < x < 80 and SCREEN_HEIGHT - 150 < y < SCREEN_HEIGHT - 85:
                            # Open spell menu
                            globalvars.emit_sound("click.ogg")
                            self.spell_select_open = not self.spell_select_open

                    # Placing tower
                    if self.placing_tower and self.countdown != self.countdown_bound:
                        if self.valid_tower_spot:
                            if globalvars.money >= self.tower_data[self.selected_tower].price:
                                globalvars.emit_sound("place_sound.ogg")
                                globalvars.money -= self.tower_data[self.selected_tower].price
                                self.create_tower(self.selected_tower)

                    # Tower menu buttons
                    if self.tower_menu_open and not self.placing_tower:
                        # Minimize button
                        if 0 < x < 128 and 100 < y < 128:
                            globalvars.emit_sound("click.ogg")
                            self.tower_menu_open = False

                        # Next age buttons
                        if 980 < x < 1150 and 0 < y < 128:
                            if self.age == "industrial":
                                if globalvars.money >= globalvars.dv_win[globalvars.difficulty]:
                                    globalvars.emit_sound("victory.ogg")
                                    self.win = True
                            if self.age == "medieval":
                                if globalvars.money >= globalvars.dv_midage[globalvars.difficulty]:
                                    globalvars.emit_sound("next_age.ogg")
                                    self.age = "industrial"
                                    globalvars.money -= globalvars.dv_midage[globalvars.difficulty]
                                    self.setup_towerdata("industrial")
                            if self.age == "stone":
                                if globalvars.money >= globalvars.dv_stoneage[globalvars.difficulty]:
                                    globalvars.emit_sound("next_age.ogg")
                                    self.age = "medieval"
                                    globalvars.money -= globalvars.dv_stoneage[globalvars.difficulty]
                                    self.setup_towerdata("medieval")

                        # Tower buttons
                        for select in range(1, 8):
                            center_pos = ((64 * select) + (64 * select)) - 64
                            if (center_pos - 24) < x < (center_pos + 24) and 32 < y < 96 and not self.placing_tower:
                                globalvars.emit_sound("click.ogg")
                                self.selected_tower = select - 1
                                if self.tower_data[self.selected_tower].price <= globalvars.money:
                                    self.placing_tower = True
                                else:
                                    self.selected_tower = 0
                                break
                    else:
                        if 0 < x < 134 and 0 < y < 30:
                            globalvars.emit_sound("click.ogg")
                            self.tower_menu_open = True

                # If you're on the main screen.
                if self.main_menu_open:
                    # Options menu
                    if SCREEN_WIDTH - 100 < x < SCREEN_WIDTH and SCREEN_HEIGHT - 100 < y < SCREEN_HEIGHT:
                        globalvars.emit_sound("click.ogg")
                        self.options_opened = not self.options_opened

                    # Start game button
                    if 100 < x < 500 and 440 < y < 570 and self.instructions < 1 and not self.options_opened:
                        globalvars.emit_sound("button.ogg")
                        self.main_menu_open = False
                        self.create_map()
                        self.game_started = False

                    # Exit button
                    if 100 < x < 500 and 40 < y < 170 and self.instructions < 1 and not self.options_opened:
                        globalvars.emit_sound("button.ogg")
                        sys.exit("Thanks for playing!")

                    # Instructions button
                    if 100 < x < 500 and 240 < y < 370 and not self.options_opened:
                        globalvars.emit_sound("button.ogg")
                        self.instructions += 1

                    # Buttons in the instructions screen
                    if self.instructions > 0:
                        if 100 < x < 200 and 50 < y < 150:
                            globalvars.emit_sound("click.ogg")
                            self.instructions -= 1

                        if SCREEN_WIDTH - 200 < x < SCREEN_WIDTH - 100 and 50 < y < 150:
                            globalvars.emit_sound("click.ogg")
                            self.instructions += 1

                    # Buttons in the options menu
                    if self.options_opened:
                        # Key buttons and delete buttons
                        for i in range(6):
                            if 320 < x < 440 and 575 - (i * 54) < y < 615 - (i * 54):
                                globalvars.emit_sound("click.ogg")
                                self.key_listening = True
                                self.selected_key = i
                            elif 275 < x < 310 and 575 - (i * 54) < y < 615 - (i * 54):
                                globalvars.emit_sound("click2.ogg")
                                globalvars.keys[i] = []

                        # Select Spell 1-3 Buttons
                        # 1 = 49, 2 = 50, 3 = 51
                        for i in range(4):
                            if 620 < x < 725 and 575 - (i * 54) < y < 615 - (i * 54):
                                globalvars.emit_sound("click.ogg")
                                self.key_listening = True
                                self.selected_key = i + 6
                            elif 570 < x < 600 and 575 - (i * 54) < y < 615 - (i * 54):
                                globalvars.emit_sound("click2.ogg")
                                globalvars.keys[i + 6] = []

                        # Reset to defaults button
                        if 255 < x < 475 and 230 < y < 280:
                            globalvars.emit_sound("click.ogg")
                            globalvars.up_keys = ["119", "65362"]
                            globalvars.down_keys = ["115", "65364"]
                            globalvars.left_keys = ["97", "65361"]
                            globalvars.right_keys = ["100", "65363"]
                            globalvars.slash_keys = ["32"]
                            globalvars.spell_keys = ["65513", "65514"]
                            globalvars.switch1_keys = ["49"]
                            globalvars.switch2_keys = ["50"]
                            globalvars.switch3_keys = ["51"]
                            globalvars.pause_keys = ["112"]

                            globalvars.keys = [globalvars.up_keys, globalvars.down_keys, globalvars.left_keys,
                                               globalvars.right_keys, globalvars.slash_keys, globalvars.spell_keys,
                                               globalvars.switch1_keys, globalvars.switch2_keys, globalvars.switch3_keys,
                                               globalvars.pause_keys]

                        # Apply button
                        if 255 < x < 415 and 160 < y < 210:
                            can_apply = True
                            for item in globalvars.keys:
                                if len(item) < 1:
                                    can_apply = False

                            if can_apply:
                                globalvars.emit_sound("click.ogg")
                                open("config.txt").close()  # Delete old binds

                                # Write new binds
                                to_write = ""
                                for item in globalvars.keys:
                                    line = ""
                                    for i in range(len(item)):
                                        line = line + str(item[i]) + "."
                                    to_write = to_write + line + "\n"
                                file = open("config.txt", 'w')
                                file.write(str(to_write))

                                self.options_opened = False

                # If you're in the map preview screen
                if not self.main_menu_open and not self.game_started:
                    # Hide Button (Difficulty Menu)
                    local_y = SCREEN_HEIGHT - 15
                    if 30 < x < 75 and local_y - 20 < y < local_y:
                        globalvars.emit_sound("click.ogg")
                        self.diff_open = not self.diff_open

                    # Difficulty Menu
                    if self.diff_open:
                        if 50 < x < 250 and 525 < y < 575:
                            globalvars.emit_sound("click.ogg")
                            globalvars.difficulty = 0

                        if 50 < x < 250 and 400 < y < 470:
                            globalvars.emit_sound("click.ogg")
                            globalvars.difficulty = 1

                        if 50 < x < 250 and 250 < y < 325:
                            globalvars.emit_sound("click.ogg")
                            globalvars.difficulty = 2

                    # If the user clicks the Generate button.
                    if 475 < x < 650 and 25 < y < 125:
                        globalvars.emit_sound("click.ogg")
                        self.create_map()

                    # If the user clicks the start button.
                    if 775 < x < 950 and 25 < y < 125:
                        globalvars.emit_sound("startgame.ogg")

                        globalvars.money = globalvars.dv_startingmoney[globalvars.difficulty]
                        globalvars.max_population = globalvars.dv_population[globalvars.difficulty]
                        globalvars.population = globalvars.max_population
                        self.game_started = True
                        self.countdown = self.countdown_bound + 5

                        # Create the player
                        self.player = player.Player("images/char/stand/down/1.png", 1)
                        self.player.center_x = SCREEN_WIDTH - 16
                        self.player.center_y = self.village_pos_y - 16
                        self.player.speed = 1.5
                        self.player.melee_damage = 10
                        self.player.anim_count = 0
                        self.player.anim_delay = 0
                        self.player.direction = "down"
                        self.player.curtime = 0
                        self.player.cast_delay = 0
                        self.player.slash_delay = 0
                        self.player.animation_list = []
                        self.player.anim_rate = 0
                        self.player.rendering_animation = False
                        self.player.attacking = False
                        self.player.level = 0
                        self.player.exp_cur = 0
                        self.player.exp_cap = 20
                        self.player.debug = 0
                        self.player.walk_delay = 0
                        self.player.old_direction = "right"
                        self.player.enemy_list = globalvars.enemy_list
                        self.player.skillpoints = 0
                        self.player.spell_list = []
                        self.player.skill_list = []
                        self.player.spell_icon_list = []
                        self.player.current_spell_icon = None
                        self.player.selected_spell = ""
                        self.player.bullet_list = self.bullet_list
                        self.player.mana = 0
                        self.player.mana_cap = 0
                        self.player.mana_regen_delay = 0
                        self.player.window_ref = self
                        self.player.inferno_list = []
                        self.player.sword_poisoned = False
                        self.player.cloud_list = []
                        self.player.orb_list = []
                        self.player.surged = False
                        self.player.step_switch = False
                        self.player.current_mouse_x = 0
                        self.player.current_mouse_y = 0
                        self.player.active_mm = None
                        self.player.pcloud = None

                        # Manually setting up the idle animations
                        self.player.append_texture(arcade.load_texture("images/char/stand/left/1.png"))
                        self.player.append_texture(arcade.load_texture("images/char/stand/right/1.png"))
                        self.player.append_texture(arcade.load_texture("images/char/stand/up/1.png"))

                        # Automatically setting up the rest of the animations
                        # Goes through all the animations in the char folder and appends them to the player's textures.
                        char_anim_list = os.listdir("images/char")
                        for k in range(len(char_anim_list)):
                            direction_list = os.listdir("images/char" + "/" + str(char_anim_list[k]))
                            for v in range(len(direction_list)):
                                number_list = os.listdir("images/char" + "/" + str(char_anim_list[k]) + "/" + str(direction_list[v]))
                                for w in range(len(number_list)):
                                    filepath = "images/char/" + str(char_anim_list[k]) + "/" + str(direction_list[v]) + "/" + str(w + 1) + ".png"
                                    self.player.append_texture(arcade.load_texture(filepath))

    # Enemy stats
    def spawn_enemy(self, enemy_name):
        if enemy_name == "skeleton":
            enemy = gamedata.Skeleton(self.skeletons_normal[random.randint(0, 2)])
            enemy.name = enemy_name
            enemy.speed = 1
            enemy.set_speed = 1
            enemy.health = 100
            enemy.center_x = 48
            enemy.worth = globalvars.dv_worth_skeleton[globalvars.difficulty]
            enemy.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
            enemy.ng_x = self.node_graph_x
            enemy.ng_y = self.node_graph_y
            enemy.node_tracker = 1
            enemy.ticks_until_tile = 0
            enemy.node_direction = self.node_direction
            enemy.cur_floater = None
            enemy.death_floaters = self.death_floaters
            enemy.floater_randpos_x = random.randint(-16, 16)
            enemy.floater_randpos_y = random.randint(-16, 16)
            enemy.ignite = 0
            enemy.ignite_timer = 0
            enemy.fire_weakness = 1
            enemy.invincible = False
            enemy.anim_timer = 0
            enemy.enemy_list = globalvars.enemy_list
            enemy.poisoned = None
            globalvars.enemy_list.append(enemy)
        elif enemy_name == "armored_skeleton":
            enemy = gamedata.Skeleton(self.skeletons_armored[random.randint(0, 1)])
            enemy.name = enemy_name
            enemy.speed = .75
            enemy.set_speed = .75
            enemy.health = 300
            enemy.center_x = 48
            enemy.worth = globalvars.dv_worth_armoredskeleton[globalvars.difficulty]
            enemy.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
            enemy.ng_x = self.node_graph_x
            enemy.ng_y = self.node_graph_y
            enemy.node_tracker = 1
            enemy.ticks_until_tile = 0
            enemy.node_direction = self.node_direction
            enemy.cur_floater = None
            enemy.death_floaters = self.death_floaters
            enemy.floater_randpos_x = random.randint(-16, 16)
            enemy.floater_randpos_y = random.randint(-16, 16)
            enemy.ignite = 0
            enemy.ignite_timer = 0
            enemy.fire_weakness = 1
            enemy.invincible = False
            enemy.poisoned = None
            globalvars.enemy_list.append(enemy)
        elif enemy_name == "hyperskeleton":
            enemy = gamedata.Hyperskeleton("images/TD/entities/skeletons/hyperskeleton/hyperskeleton_base.png")
            enemy.name = enemy_name
            local_speed = 1
            local_tiles = 0
            for unused in self.floor_list:
                local_tiles += 1

            local_speed = local_tiles / 10
            enemy.speed = local_speed
            enemy.set_speed = enemy.speed
            # enemy.tiles = int(local_tiles / 2) + random.randint(-3, 3)
            enemy.tiles = int(local_tiles / globalvars.dv_hyperdist[globalvars.difficulty]) - random.randint(1, 5)
            enemy.invincible = True
            enemy.health = globalvars.dv_health_hyperskeleton[globalvars.difficulty]
            enemy.center_x = 48
            enemy.worth = globalvars.dv_worth_hyperskeleton[globalvars.difficulty]
            enemy.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
            enemy.ng_x = self.node_graph_x
            enemy.ng_y = self.node_graph_y
            enemy.node_tracker = 1
            enemy.ticks_until_tile = 0
            enemy.node_direction = self.node_direction
            enemy.cur_floater = None
            enemy.death_floaters = self.death_floaters
            enemy.floater_randpos_x = random.randint(-16, 16)
            enemy.floater_randpos_y = random.randint(-16, 16)
            enemy.ignite = 0
            enemy.ignite_timer = 0
            enemy.fire_weakness = 1
            enemy.poisoned = None
            for item in self.skeletons_hyper:
                enemy.append_texture(item)
            globalvars.enemy_list.append(enemy)
        elif enemy_name == "raptor":
            enemy = gamedata.Raptor("images/TD/entities/skeletons/raptor.png")
            enemy.name = enemy_name
            enemy.curtime = 0
            enemy.speed = .5
            enemy.set_speed = .5
            enemy.health = globalvars.dv_health_raptor[globalvars.difficulty]
            enemy.center_x = 48
            enemy.worth = globalvars.dv_worth_raptor[globalvars.difficulty]
            enemy.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
            enemy.ng_x = self.node_graph_x
            enemy.ng_y = self.node_graph_y
            enemy.node_tracker = 1
            enemy.ticks_until_tile = 0
            enemy.node_direction = self.node_direction
            enemy.cur_floater = None
            enemy.death_floaters = self.death_floaters
            enemy.floater_randpos_x = random.randint(-16, 16)
            enemy.floater_randpos_y = random.randint(-16, 16)
            enemy.ignite = 0
            enemy.ignite_timer = 0
            enemy.fire_weakness = 1
            enemy.invincible = False
            enemy.poisoned = None
            globalvars.enemy_list.append(enemy)
        elif enemy_name == "lich":
            enemy = gamedata.Lich("images/TD/entities/skeletons/lich.png")
            enemy.name = enemy_name
            enemy.curtime = 0
            enemy.speed = 1
            enemy.set_speed = 1
            enemy.health = globalvars.dv_health_lich[globalvars.difficulty]
            enemy.shield = globalvars.dv_shield_lich[globalvars.difficulty]

            local_tiles = 0
            for unused in self.floor_list:
                local_tiles += 1

            enemy.shield_regen = 250
            enemy.health_track = 0
            enemy.should_regen = False
            enemy.health_switch = False

            enemy.center_x = 48
            enemy.worth = globalvars.dv_worth_lich[globalvars.difficulty]
            enemy.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
            enemy.ng_x = self.node_graph_x
            enemy.ng_y = self.node_graph_y
            enemy.node_tracker = 1
            enemy.ticks_until_tile = 0
            enemy.node_direction = self.node_direction
            enemy.cur_floater = None
            enemy.death_floaters = self.death_floaters
            enemy.floater_randpos_x = random.randint(-16, 16)
            enemy.floater_randpos_y = random.randint(-16, 16)
            enemy.ignite = 0
            enemy.ignite_timer = 0
            enemy.fire_weakness = 1
            enemy.invincible = False
            enemy.poisoned = None
            for item in self.skeletons_lich_shield:
                enemy.append_texture(item)
            globalvars.enemy_list.append(enemy)
        elif enemy_name == "skeletonlord":
            enemy = gamedata.Skeleton_Lord("images/TD/entities/skeletons/skeleton_lord.png")
            enemy.append_texture(arcade.load_texture("images/TD/entities/skeletons/skeleton_lord_gate.png"))
            enemy.name = enemy_name
            enemy.speed = 1 + random.random()
            enemy.set_speed = 1
            enemy.health = 100000
            enemy.center_x = 48
            enemy.worth = globalvars.dv_worth_skeletonlord[globalvars.difficulty]
            enemy.center_y = (self.doorpos * self.tilesize) - self.tilesize_half
            enemy.ng_x = self.node_graph_x
            enemy.ng_y = self.node_graph_y
            enemy.node_tracker = 1
            enemy.ticks_until_tile = 0
            enemy.node_direction = self.node_direction
            enemy.cur_floater = None
            enemy.death_floaters = self.death_floaters
            enemy.floater_randpos_x = random.randint(-16, 16)
            enemy.floater_randpos_y = random.randint(-16, 16)
            enemy.ignite = 0
            enemy.ignite_timer = 0
            enemy.fire_weakness = 1
            enemy.invincible = False
            enemy.health_gate = 100
            enemy.old_health = enemy.health
            enemy.curtime = 0
            enemy.anim_timer = 0
            enemy.poisoned = None
            globalvars.enemy_list.append(enemy)

    def update(self, delta_time):
        if self.game_started and not self.paused:
            if globalvars.population <= 0 and not self.lose_switch:
                globalvars.emit_sound("lose.ogg")
                self.lose_switch = True

            self.curtime_logic += 1

            globalvars.player = self.player

            # Set mana to full between waves
            if self.countdown != self.countdown_bound:
                self.player.mana = self.player.mana_cap

            if globalvars.population > 0 or self.win:
                globalvars.enemy_list.update()
                self.bullet_list.update()
                self.player.update()

                # Only have the towers be active during the wave.
                if self.countdown == self.countdown_bound and self.wave != 0:
                    self.tower_list.update()

                if self.curtime_logic > 2:
                    self.curtime += 1
                    self.curtime_logic = 0

                # If all the enemies are dead at the end of the wave have an intermission and set up next wave.
                if len(self.enemy_queue) <= 0:
                    local_count = 0
                    for enemies in globalvars.enemy_list:
                        local_count += 1
                    if local_count <= 0:
                        self.countdown_logic += 1
                        if self.countdown_logic > 50:
                            self.countdown -= 1
                            self.countdown_logic = 0
                        if self.countdown <= 0:
                            self.countdown = self.countdown_bound
                            self.wave += 1
                            globalvars.stats_waves += 1

                            if self.player.player_has_skill("Necromancy"):
                                add_pop = 1

                                if self.player.player_has_skill("Vitality"):
                                    add_pop = 2

                                if globalvars.population + add_pop > globalvars.max_population:
                                    add_pop = globalvars.max_population - globalvars.population

                                globalvars.population += add_pop



                            self.on_wave_change(self.wave)
                else:   # Else, spawn the enemies in the queue.
                    self.spawn_logic += 1
                    if self.spawn_logic > self.enemy_delay:
                        self.spawn_logic = 0
                        self.spawn_enemy(self.enemy_queue[0])
                        del self.enemy_queue[0]

            # Something I used for debugging
            if not self.main_menu_open and not self.game_started:
                self.curtime += 1
                if self.curtime > self.ghost_timer:
                    self.ghost_timer = self.curtime + 2
                    if self.ghost_x < len(self.node_graph_x):
                        self.debug_x = self.tilesize * self.node_graph_x[self.ghost_x]
                        self.debug_y = self.tilesize * self.node_graph_y[self.ghost_y]
                        self.ghost_x += 1
                        self.ghost_y += 1
                    else:
                        self.ghost_x = 0
                        self.ghost_y = 0

    # Tower stats
    def create_tower(self, selected_tower):
        tower = gamedata.Tower_Stone_Person_1("images/TD/entities/towers/stone/caveman_default.png")
        if self.age == "stone":
            if selected_tower == 0:
                tower = gamedata.Tower_Stone_Trap("images/TD/entities/towers/stone/deadfall_set.png")
            if selected_tower == 1:
                tower = gamedata.Tower_Stone_Person_1("images/TD/entities/towers/stone/clubman_default.png")
            if selected_tower == 2:
                tower = gamedata.Tower_Stone_Person_2("images/TD/entities/towers/stone/caveman_default.png")
            if selected_tower == 3:
                tower = gamedata.Tower_Stone_Person_3("images/TD/entities/towers/stone/caveman_blowgun.png")
            if selected_tower == 4:
                tower = gamedata.Tower_Stone_Boulder("images/TD/entities/towers/stone/boulder.png")
            if selected_tower == 5:
                tower = gamedata.Tower_Stone_Money("images/TD/entities/towers/stone/caveman_money_default.png")
            if selected_tower == 6:
                tower = gamedata.Tower_Stone_Super("images/TD/entities/towers/stone/atlatl_default.png")
        elif self.age == "medieval":
            if selected_tower == 0:
                tower = gamedata.Tower_Medieval_Trap("images/TD/entities/towers/medieval/spikes_default.png")
            if selected_tower == 1:
                tower = gamedata.Tower_Medieval_Person_1("images/TD/entities/towers/medieval/knight_default.png")
            if selected_tower == 2:
                tower = gamedata.Tower_Medieval_Person_2("images/TD/entities/towers/medieval/jav_default.png")
            if selected_tower == 3:
                tower = gamedata.Tower_Medieval_Person_3("images/TD/entities/towers/medieval/archer/archer_ready.png")
            if selected_tower == 4:
                tower = gamedata.Tower_Medieval_Special("images/TD/entities/towers/medieval/horse_1.png")
            if selected_tower == 5:
                tower = gamedata.Tower_Medieval_Money("images/TD/entities/towers/medieval/farm.png")
            if selected_tower == 6:
                tower = gamedata.Tower_Medieval_Super("images/TD/entities/towers/medieval/mage/mage_attack.png")
        elif self.age == "industrial":
            if selected_tower == 0:
                tower = gamedata.Tower_Industrial_Trap("images/TD/entities/towers/industrial/landmine_unlit.png")
            if selected_tower == 1:
                tower = gamedata.Tower_Industrial_Person_1("images/TD/entities/towers/industrial/shotgun/shotgun_idle.png")
                tower.shots = 6
                tower.reloading = False
                tower.reload_delay = 0
                tower.last_shot_delay = 0
            if selected_tower == 2:
                tower = gamedata.Tower_Industrial_Person_2("images/TD/entities/towers/industrial/ar2/idle.png")
                tower.shots = 30
                tower.reloading = False
                tower.reload_delay = 0
                tower.last_shot_delay = 0
            if selected_tower == 3:
                tower = gamedata.Tower_Industrial_Person_3("images/TD/entities/towers/industrial/sniper/idle.png")
                tower.shots = 1
                tower.reloading = False
                tower.reload_delay = 0
                tower.last_shot_delay = 0
            if selected_tower == 4:
                tower = gamedata.Tower_Industrial_Special("images/TD/entities/towers/industrial/plane.png")
            if selected_tower == 5:
                tower = gamedata.Tower_Industrial_Money("images/TD/entities/towers/industrial/oil_1.png")
            if selected_tower == 6:
                tower = gamedata.Tower_Industrial_Super_Base("images/TD/entities/towers/industrial/tank_base.png")
                tower.curtime = 0
                tower.enemy_list = globalvars.enemy_list
                tower.bullet_list = self.bullet_list
                tower.attack_radius = self.tower_data[selected_tower].attack_radius
                tower.damage = self.tower_data[selected_tower].damage
                tower.fire_rate = self.tower_data[selected_tower].fire_rate
                tower.can_shoot = True
                tower.delay_wait = 0
                tower.animation_wait = 0
                tower.center_x = self.current_mouse_x
                tower.center_y = self.current_mouse_y
                tower.detect_delay = 0
                self.bullet_list.append(tower)
                tower = gamedata.Tower_Industrial_Super("images/TD/entities/towers/industrial/tank_gun.png")

        tower.attack_radius = self.tower_data[selected_tower].attack_radius
        tower.damage = self.tower_data[selected_tower].damage
        tower.fire_rate = self.tower_data[selected_tower].fire_rate
        tower.price = self.tower_data[selected_tower].price
        tower.sellable = self.tower_data[selected_tower].sellable
        tower.can_shoot = True
        tower.delay_wait = 0
        tower.curtime = 0
        tower.animation_wait = 0
        tower.uses = 0
        tower.center_x = self.current_mouse_x
        tower.center_y = self.current_mouse_y
        tower.enemy_list = globalvars.enemy_list
        tower.bullet_list = self.bullet_list
        tower.x_origin = self.current_mouse_x
        tower.y_origin = self.current_mouse_y
        tower.ng_x = self.node_graph_x
        tower.ng_y = self.node_graph_y
        tower.detect_delay = 0
        for i in range (len(self.tower_data[selected_tower].anims)):
            tower.append_texture(self.tower_data[selected_tower].anims[i])

        self.all_sprites_list.append(tower)
        self.tower_list.append(tower)

    # Wave data
    def on_wave_change(self, wave):
        if globalvars.difficulty == 0:
            self.normal_wave_event(wave)
        elif globalvars.difficulty == 1:
            self.hard_wave_event(wave)
        elif globalvars.difficulty == 2:
            self.nightmare_wave_event(wave)
        else:
            print("What?")

    def normal_wave_event(self, wave):
        # Define what each wave should spawn.
        if wave == 1:
            self.enemy_delay = 150
            for unused in range(5):
                self.enemy_queue.append("skeleton")
        elif wave == 2:
            self.enemy_delay = 125
            for unused in range(10):
                self.enemy_queue.append("skeleton")
        elif wave == 3:
            self.enemy_delay = 100
            for unused in range(15):
                self.enemy_queue.append("skeleton")
        elif wave == 4:
            self.enemy_delay = 75
            for unused in range(20):
                self.enemy_queue.append("skeleton")
        elif wave == 5:
            self.enemy_delay = 50
            for unused in range(25):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("armored_skeleton")
        elif wave == 6:
            self.enemy_delay = 30
            for unused in range(5):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(30):
                self.enemy_queue.append("skeleton")
        elif wave == 7:
            for unused in range(5):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(15):
                self.enemy_queue.append("skeleton")
            for unused in range(5):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(15):
                self.enemy_queue.append("skeleton")
        elif wave == 8:
            for unused in range(25):
                self.enemy_queue.append("skeleton")
            for unused in range(25):
                self.enemy_queue.append("armored_skeleton")
        elif wave == 9:
            self.enemy_delay = 10
            self.enemy_queue.append("armored_skeleton")
            for unused in range(25):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("armored_skeleton")
        elif wave == 10:
            self.enemy_delay = 30
            for unused in range(25):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
            self.enemy_queue.append("hyperskeleton")
        elif wave == 11:
            self.enemy_delay = 25
            self.enemy_queue.append("skeleton")
            self.enemy_queue.append("hyperskeleton")
            for unused in range(15):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(3):
                self.enemy_queue.append("hyperskeleton")
            for unused in range(20):
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("hyperskeleton")
        elif wave == 12:
            for unused in range(60):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(5):
                self.enemy_queue.append("hyperskeleton")
        elif wave == 13:
            for unused in range(5):
                self.enemy_queue.append("hyperskeleton")
            for unused in range(30):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("hyperskeleton")
            for unused in range(10):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
        elif wave == 14:
            for unused in range(40):
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("armored_skeleton")
        elif wave == 15:
            self.enemy_delay = 5
            for unused in range(5):
                self.enemy_queue.append("hyperskeleton")
            self.enemy_queue.append("raptor")
        elif wave == 16:
            self.enemy_delay = 20
            for unused in range(3):
                self.enemy_queue.append("raptor")
            for unused in range(20):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
            for unused in range(20):
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("skeleton")
        elif wave == 17:
            for unused in range(15):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("raptor")
        elif wave == 18:
            for unused in range(30):
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("hyperskeleton")
        elif wave == 19:
            for unused in range(50):
                self.enemy_queue.append("raptor")
        elif wave == 20:
            self.enemy_delay = 20
            for unused in range(10):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(50):
                self.enemy_queue.append("raptor")
            for unused in range(10):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("lich")
        elif wave > 20:     # Past wave 20 it goes into automatic mode
            self.enemy_delay = 20 - ((wave - 20) * 2)  # Decrease by two each wave
            if self.enemy_delay < 2:
                self.enemy_delay = 2
            enemies_to_spawn = round(wave ** 1.25)
            # Each automatic wave spawns 12 "blocks" of enemies with gradually increasing size
            blocks = 12
            block_size = round((wave / 10) ** 1.5)
            local_enemies = ["skeleton", "armored_skeleton", "hyperskeleton", "raptor"]
            while enemies_to_spawn > len(self.enemy_queue):
                for block in range(blocks):
                    if random.randint(1, 4) == 2:
                        for unused in range(block_size):
                            self.enemy_queue.append(random.choice(local_enemies))
                    else:
                        local_chosen_enemy = "hyperskeleton"
                        math_temp = random.randint(1, wave - 18)
                        if math_temp == 1:
                            local_chosen_enemy = "armored_skeleton"
                        elif math_temp == 2:
                            local_chosen_enemy = "skeleton"

                        math_temp = 30 - wave
                        if math_temp < 1:
                            math_temp = 1
                        if random.randint(1, math_temp) == 1:
                            local_chosen_enemy = "raptor"

                        math_temp = round(1000 - (wave ** 1.85))
                        if math_temp < 1:
                            math_temp = 1
                        if random.randint(1, math_temp) == 1:
                            local_chosen_enemy = "lich"
                            block_size = 1

                        for unused in range(block_size):
                            self.enemy_queue.append(local_chosen_enemy)

    def hard_wave_event(self, wave):
        # Define what each wave should spawn.
        if wave == 1:
            self.enemy_delay = 150
            for unused in range(11):
                self.enemy_queue.append("skeleton")
        elif wave == 2:
            self.enemy_delay = 100
            for unused in range(15):
                self.enemy_queue.append("skeleton")
        elif wave == 3:
            self.enemy_delay = 50
            for unused in range(20):
                self.enemy_queue.append("skeleton")
        elif wave == 4:
            self.enemy_delay = 35
            for unused in range(25):
                self.enemy_queue.append("skeleton")
        elif wave == 5:
            self.enemy_delay = 30
            for unused in range(30):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("armored_skeleton")
        elif wave == 6:
            self.enemy_delay = 30
            for unused in range(10):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(25):
                self.enemy_queue.append("skeleton")
        elif wave == 7:
            for unused in range(10):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(15):
                self.enemy_queue.append("skeleton")
            for unused in range(10):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(15):
                self.enemy_queue.append("skeleton")
        elif wave == 8:
            for unused in range(50):
                self.enemy_queue.append("armored_skeleton")
        elif wave == 9:
            self.enemy_delay = 5
            self.enemy_queue.append("armored_skeleton")
            for unused in range(30):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("armored_skeleton")
        elif wave == 10:
            self.enemy_delay = 30
            for unused in range(30):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
            self.enemy_queue.append("hyperskeleton")
        elif wave == 11:
            self.enemy_delay = 25
            self.enemy_queue.append("skeleton")
            self.enemy_queue.append("hyperskeleton")
            for unused in range(15):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(5):
                self.enemy_queue.append("hyperskeleton")
            for unused in range(20):
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("hyperskeleton")
        elif wave == 12:
            for unused in range(65):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(5):
                self.enemy_queue.append("hyperskeleton")
        elif wave == 13:
            for unused in range(10):
                self.enemy_queue.append("hyperskeleton")
            for unused in range(30):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("hyperskeleton")
            for unused in range(15):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
        elif wave == 14:
            for unused in range(40):
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("armored_skeleton")
        elif wave == 15:
            self.enemy_delay = 5
            for unused in range(20):
                self.enemy_queue.append("hyperskeleton")
            self.enemy_queue.append("raptor")
        elif wave == 16:
            self.enemy_delay = 20
            for unused in range(5):
                self.enemy_queue.append("raptor")
            for unused in range(20):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
            for unused in range(20):
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("skeleton")
        elif wave == 17:
            for unused in range(20):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("raptor")
        elif wave == 18:
            for unused in range(40):
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("hyperskeleton")
        elif wave == 19:
            for unused in range(50):
                self.enemy_queue.append("raptor")
        elif wave == 20:
            self.enemy_delay = 20
            for unused in range(10):
                self.enemy_queue.append("armored_skeleton")
            for unused in range(50):
                self.enemy_queue.append("raptor")
            for unused in range(10):
                self.enemy_queue.append("skeleton")
            self.enemy_queue.append("lich")
        elif wave > 20:     # Past wave 20 it goes into automatic mode
            self.enemy_delay = 20 - ((wave - 20) * 2)  # Decrease by two each wave
            if self.enemy_delay < 1:
                self.enemy_delay = 1
            enemies_to_spawn = round(wave ** 1.5)
            # Each automatic wave spawns 12 "blocks" of enemies with gradually increasing size
            blocks = 12
            block_size = round((wave / 10) ** 2)
            local_enemies = ["skeleton", "armored_skeleton", "hyperskeleton", "raptor"]
            while enemies_to_spawn > len(self.enemy_queue):
                for block in range(blocks):
                    if random.randint(1, 4) == 2:
                        for unused in range(block_size):
                            self.enemy_queue.append(random.choice(local_enemies))
                    else:
                        local_chosen_enemy = "hyperskeleton"
                        math_temp = random.randint(1, wave - 18)
                        if math_temp == 1:
                            local_chosen_enemy = "armored_skeleton"
                        elif math_temp == 2:
                            local_chosen_enemy = "skeleton"

                        math_temp = 30 - wave
                        if math_temp < 1:
                            math_temp = 1
                        if random.randint(1, math_temp) == 1:
                            local_chosen_enemy = "raptor"

                        math_temp = round(1000 - (wave ** 1.85))
                        if math_temp < 1:
                            math_temp = 1
                        if random.randint(1, math_temp) == 1:
                            local_chosen_enemy = "lich"

                        for unused in range(block_size):
                            self.enemy_queue.append(local_chosen_enemy)

                    # Additional lich spawning
                    math_temp = 35 - wave
                    if math_temp < 1:
                        math_temp = 1
                    if random.randint(1, math_temp) == 1:
                        self.enemy_queue.append("lich")

            # Skeleton lord spawning
            if wave > 25:
                amount = 1
                if wave > 30:
                    amount = amount + (wave - 30)

                chance = (wave - 25) * (1 - (25 - wave))
                if chance >= 100:
                    chance = 100

                if random.randint(chance, 100) == 100:
                    for i in range(amount):
                        self.enemy_queue.append("skeletonlord")

    def nightmare_wave_event(self, wave):
        # Define what each wave should spawn.
        if wave == 1:
            self.enemy_delay = 150
            for unused in range(11):
                self.enemy_queue.append("skeleton")
        elif wave == 2:
            self.enemy_delay = 100

            self.enemy_queue.append("armored_skeleton")

            for unused in range(5):
                self.enemy_queue.append("skeleton")

            self.enemy_queue.append("armored_skeleton")

            for unused in range(5):
                self.enemy_queue.append("skeleton")

            self.enemy_queue.append("armored_skeleton")

            for unused in range(5):
                self.enemy_queue.append("skeleton")
        elif wave == 3:
            self.enemy_delay = 30

            for unused in range(5):
                self.enemy_queue.append("armored_skeleton")

            for unused in range(20):
                self.enemy_queue.append("skeleton")

            self.enemy_queue.append("hyperskeleton")
        elif wave == 4:
            for unused in range(3):
                self.enemy_queue.append("hyperskeleton")

            for unused in range(5):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")

            self.enemy_queue.append("hyperskeleton")
            for unused in range(5):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")

            self.enemy_queue.append("hyperskeleton")
            for unused in range(5):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")

            self.enemy_queue.append("hyperskeleton")
        elif wave == 5:
            self.enemy_delay = 15

            for unused in range(25):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("hyperskeleton")

            for unused in range(10):
                self.enemy_queue.append("armored_skeleton")

            self.enemy_queue.append("raptor")
        elif wave == 6:

            self.enemy_queue.append("raptor")

            for unused in range(10):
                self.enemy_queue.append("hyperskeleton")

            for unused in range(20):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")

            for unused in range(10):
                self.enemy_queue.append("hyperskeleton")

            self.enemy_queue.append("raptor")
        elif wave == 7:
            for unused in range(3):
                self.enemy_queue.append("raptor")

            for unused in range(15):
                self.enemy_queue.append("armored_skeleton")

            for unused in range(15):
                self.enemy_queue.append("skeleton")

            for unused in range(15):
                self.enemy_queue.append("hyperskeleton")

            for unused in range(15):
                self.enemy_queue.append("skeleton")

            for unused in range(15):
                self.enemy_queue.append("armored_skeleton")

            for unused in range(3):
                self.enemy_queue.append("raptor")
        elif wave == 8:
            for unused in range(50):
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("skeleton")

            for unused in range(10):
                self.enemy_queue.append("raptor")
        elif wave == 9:
            self.enemy_delay = 1

            for unused in range(100):
                self.enemy_queue.append("hyperskeleton")
        elif wave == 10:
            for unused in range(30):
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("hyperskeleton")

            self.enemy_queue.append("lich")
        elif wave == 11:
            self.enemy_delay = 5

            self.enemy_queue.append("lich")

            for unused in range(25):
                self.enemy_queue.append("hyperskeleton")

            for unused in range(15):
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("raptor")

            for unused in range(25):
                self.enemy_queue.append("hyperskeleton")

            for unused in range(20):
                self.enemy_queue.append("hyperskeleton")

            for unused in range(5):
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("skeleton")
                self.enemy_queue.append("raptor")

            for unused in range(25):
                self.enemy_queue.append("hyperskeleton")

            self.enemy_queue.append("lich")
        elif wave == 12:
            self.enemy_delay = 1

            self.enemy_queue.append("lich")
            for unused in range(200):
                self.enemy_queue.append("armored_skeleton")
            self.enemy_queue.append("lich")
        elif wave == 13:
            self.enemy_delay = 100

            for unused in range(5):
                self.enemy_queue.append("lich")
        elif wave == 14:
            self.enemy_delay = 5

            for unused in range(50):
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("hyperskeleton")

            for unused in range(5):
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("lich")
                self.enemy_queue.append("skeleton")
        elif wave == 15:
            self.enemy_delay = 1

            for unused in range(50):
                self.enemy_queue.append("raptor")
        elif wave == 16:
            self.enemy_delay = 20

            for unused in range(10):
                self.enemy_queue.append("lich")
        elif wave == 17:
            self.enemy_delay = 15

            for unused in range(15):
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("lich")
        elif wave == 18:
            self.enemy_delay = 10

            for unused in range(20):
                self.enemy_queue.append("hyperskeleton")
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("armored_skeleton")
                self.enemy_queue.append("lich")
        elif wave == 19:
            self.enemy_delay = 5

            for unused in range(200):
                self.enemy_queue.append("armored_skeleton")

            for unused in range(100):
                self.enemy_queue.append("raptor")

            for unused in range(25):
                self.enemy_queue.append("lich")
        elif wave == 20:
            self.enemy_delay = 1

            for unused in range(100):
                self.enemy_queue.append("raptor")
                self.enemy_queue.append("lich")
                self.enemy_queue.append("hyperskeleton")

            self.enemy_queue.append("skeletonlord")
        elif wave > 20:     # Past wave 20 it goes into automatic mode
            self.enemy_delay = 1

            enemies_to_spawn = round(wave ** 3)
            # Each automatic wave spawns 16 "blocks" of enemies with gradually increasing size
            blocks = 16
            block_size = round((wave / 10) ** 5)
            local_enemies = ["armored_skeleton", "hyperskeleton", "raptor", "lich"]
            while enemies_to_spawn > len(self.enemy_queue):
                for block in range(blocks):
                    for unused in range(block_size):
                        self.enemy_queue.append(random.choice(local_enemies))

                    # Additional lich spawning
                    math_temp = 30 - wave
                    if math_temp < 1:
                        math_temp = 1
                    if random.randint(1, math_temp) == 1:
                        self.enemy_queue.append("skeletonlord")

            # Skeleton lord spawning
            if wave > 25:
                amount = 1
                if wave > 30:
                    amount = amount + (wave - 30)

                chance = (wave - 25) * (1 - (25 - wave))
                if chance >= 100:
                    chance = 100

                if random.randint(chance, 100) == 100:
                    for i in range(amount):
                        self.enemy_queue.append("skeletonlord")


window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT)
window.setup()

arcade.run()
