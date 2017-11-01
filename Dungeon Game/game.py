"""
# Images
Artwork from https://opengameart.org/content/denzis-public-domain-art
https://opengameart.org/content/topdown-knight
https://opengameart.org/content/top-down-demon-animations
https://opengameart.org/content/modified-32x32-treasure-chest
https://opengameart.org/content/potion-bottles

# Sounds
https://freesound.org/people/Davidsraba/sounds/347174/
https://freesound.org/people/Q.K./sounds/56271/
https://freesound.org/people/LiamG_SFX/sounds/334234/
https://freesound.org/people/missozzy/sounds/169985/
https://freesound.org/people/Pyrocamancer/sounds/137036/
https://freesound.org/people/pagancow/sounds/15419/
https://freesound.org/people/rdaly95/sounds/387134/
https://freesound.org/people/jawbutch/sounds/344403/
https://freesound.org/people/RandomationPictures/sounds/138480/
https://freesound.org/people/Artmasterrich/sounds/345456/
https://freesound.org/people/Christopherderp/sounds/342229/
https://freesound.org/people/Christopherderp/sounds/342230/
https://freesound.org/people/Christopherderp/sounds/342231/
https://freesound.org/people/isteak/sounds/387232/
"""

import random
import arcade
import math
import sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

SCROLL_WIDTH = 512
SCROLL_HEIGHT = 384

BR_X = 64
BR_Y = 48

VIEWPORT_MARGIN = 200

MOVEMENT_SPEED = 3


class Arrow(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 20


class Enemy(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.player = None
        self.curtime = 0
        self.delay = 0
        self.growl = False
        self.fireball_list = None
        self.sound_list = None
        self.coin_list = None
        self.health = 100
        self.death_animation = 0

    def shoot(self):
        if self.player.alive:
            arcade.play_sound(self.sound_list[4])

            fireball = Fireball("images/fireball.png")
            fireball.center_x = self.center_x
            fireball.center_y = self.center_y
            fireball.reflected = False

            local_speed = 4
            x_diff = self.player.center_x - self.center_x
            y_diff = self.player.center_y - self.center_y
            angle = math.atan2(y_diff, x_diff)
            fireball.angle = math.degrees(angle)
            fireball.change_x = math.cos(angle) * local_speed
            fireball.change_y = math.sin(angle) * local_speed

            self.fireball_list.append(fireball)

    def update(self):
        self.curtime += 1

        # If enemy dies play death animation
        if self.health <= 0 and self.death_animation == 0:
            self.death_animation = self.curtime + 30
        if self.death_animation - 20 > self.curtime:
            self.set_texture(1)
        elif self.death_animation - 10 > self.curtime:
            self.set_texture(2)
        elif self.death_animation > self.curtime:
            # Spawn a coin on death
            coin = arcade.Sprite("images/coin.png", 0.1)
            coin.center_x = self.center_x
            coin.center_y = self.center_y
            coin.force = 0
            self.coin_list.append(coin)
            self.kill()


        # If player is nearby shoot at him every 100-200 frames
        d = math.sqrt(((self.center_x - self.player.center_x) ** 2) + ((self.center_y - self.player.center_y) ** 2))
        if d < 150 and self.health > 0:
            if not self.growl:
                self.growl = True
                arcade.play_sound(self.sound_list[5])

            x_diff = self.player.center_x - self.center_x
            y_diff = self.player.center_y - self.center_y
            self.angle = math.degrees(math.atan2(y_diff, x_diff)) - 90

            if self.curtime > self.delay:
                self.delay = self.curtime + random.randint(100, 200)
                self.shoot()
        else:
            # Prevent detection noise from playing every frame
            self.growl = False


class MyApplication(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "The Dungeon")

        self.set_mouse_visible(False)

        # High Scores
        self.highscore_sound = False
        self.highscore = 0
        file = open("scores.txt")
        for items in file:
            self.highscore = int(items.strip())

        # Game Variables
        self.game_started = False
        self.curtime = 0
        self.score = 0
        self.room = 0

        # Sprite lists
        self.all_sprites_list = None
        self.coin_list = None
        self.ammo_list = None
        self.arrow_list = None
        self.enemy_list = None
        self.fireball_list = None
        self.chest_list = None
        self.potion_list = None
        self.effect_list = None

        # Set up the player
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.health = 100
        self.ammo = 5
        self.knife_delay = 0
        self.knife_rate = 0

        # Map Generation Variables
        self.blocks = [[True for useless in range(BR_Y)] for useless in range(BR_X)]
        self.doorpos = 0

        # Textures
        self.chest_texture = arcade.load_texture("images/chest_opened.png")
        self.controls = arcade.load_texture("images/controls.png")

        # Sounds
        self.sound_list = []
        self.sound_list.append(arcade.load_sound("sounds/default.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/bow_shoot.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/pickup_coin.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/gulp.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/fireball.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/demon_growl.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/demon_die.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/char_pain_1.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/char_pain_2.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/char_pain_3.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/char_die.ogg"))    # 10
        self.sound_list.append(arcade.load_sound("sounds/arrow_hit.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/chest_open.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/knife_swing.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/knife_hit.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/highscore.ogg"))
        self.sound_list.append(arcade.load_sound("sounds/coin_pickup.ogg"))

    def setup(self):
        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        self.chest_list = arcade.SpriteList()
        self.potion_list = arcade.SpriteList()
        self.effect_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("images/archer/right.png", 1)
        self.player_sprite.append_texture(arcade.load_texture("images/archer/left.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/archer/up.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/archer/down.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/dead.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/archer/stab_up.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/archer/stab_right.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/archer/stab_left.png"))
        self.player_sprite.append_texture(arcade.load_texture("images/archer/stab_down.png"))
        self.player_sprite.center_x = 1 * 32
        self.player_sprite.center_y = 5 * 32
        self.player_sprite.eye_pos = "right"
        self.player_sprite.alive = True
        self.player_sprite.death_sound = False
        self.all_sprites_list.append(self.player_sprite)
        self.view_left = 0
        self.view_bottom = 0

        # Enemy Textures
        self.demon_die_1 = arcade.load_texture("images/demon_die_1.png")
        self.demon_die_2 = arcade.load_texture("images/demon_die_2.png")
        self.demon_slash = arcade.load_texture("images/demon_slash.png")

        # Text
        self.ammo_text = None
        self.highscore_text = None
        self.score_text = None

        # Map Generation
        self.blocks = [[True for useless in range(BR_Y)] for useless in range(BR_X)]
        self.direction = "right"
        self.ng_x = 0
        self.ng_y = 0

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcade.set_background_color(arcade.color.BLACK)
        self.generate_map()
        arcade.play_sound(self.sound_list[0])

    def generate_map(self):
        self.blocks[1][5] = False

        self.ng_x = 1
        self.ng_y = 5
        self.direction = "right"
        anti_crash = 0

        # The map is generated by having a "snake" go around the map in random directions until it hits the right wall.
        while anti_crash < 2000:
            anti_crash += 1

            # If the generation gets stuck somehow force it to finish
            if anti_crash > 1999:
                for x in range(BR_X - 1):
                    self.blocks[x][16] = False
                self.blocks[0][16] = True
                self.doorpos = 16
                wall = arcade.Sprite("images/castle_door_open.png", 1)
                wall.center_x = (BR_X - 1) * 32
                wall.center_y = 16 * 32
                self.all_sprites_list.append(wall)
                self.wall_list.append(wall)

            # Keep trying different directions until it's a valid direction.
            valid_movement = False
            while not valid_movement:
                old_ngx = self.ng_x
                old_ngy = self.ng_y
                if self.direction == "right":
                    self.ng_x += 1
                if self.direction == "left":
                    self.ng_x -= 1
                if self.direction == "up":
                    self.ng_y += 1
                if self.direction == "down":
                    self.ng_y -= 1

                if 0 < self.ng_x < BR_X and 0 < self.ng_y < BR_Y - 1:
                    valid_movement = True

                if not valid_movement:
                    self.ng_x = old_ngx
                    self.ng_y = old_ngy
                    self.change_direction()

            # If it's a valid movement set it to a floor block.
            if valid_movement:
                self.blocks[self.ng_x][self.ng_y] = False
                if random.randint(0, 3) == 2:
                    # Every once and while randomly change direction to prevent straight lines from forming.
                    self.change_direction()

            # Create spawn door
            if self.ng_x >= BR_X - 1:
                self.doorpos = self.ng_y
                wall = arcade.Sprite("images/castle_door_open.png", 1)
                wall.center_x = self.ng_x * 32
                wall.center_y = self.ng_y * 32
                self.all_sprites_list.append(wall)
                self.wall_list.append(wall)
                break

        # Create a randomly chosen wall sprite where all the wall blocks should  be.
        wall_textures = []
        wall_textures.append("images/tile_1.png")
        wall_textures.append("images/tile_2.png")
        wall_textures.append("images/tile_3.png")
        wall_textures.append("images/tile_4.png")
        for x in range(BR_X):
            for y in range(BR_Y):
                if self.blocks[x][y]:
                    wall = arcade.Sprite(random.choice(wall_textures), 1)
                    wall.center_x = x * 32
                    wall.center_y = y * 32
                    self.all_sprites_list.append(wall)
                    self.wall_list.append(wall)

        # Create the items and enemies randomly around the map.
        for x in range(BR_X):
            for y in range(BR_Y):
                if not self.blocks[x][y]:
                    # Each time you enter a new room increase the chance for enemies to spawn
                    difficulty = 17 - self.room
                    if difficulty <= 0:
                        difficulty = 0

                    # Randomly place chests
                    if random.randint(1, 50) == 5:
                        chest = arcade.Sprite("images/chest_closed.png", .75)
                        chest.center_x = x * 32
                        chest.center_y = y * 32
                        chest.append_texture(self.chest_texture)
                        self.all_sprites_list.append(chest)
                        self.chest_list.append(chest)
                    elif random.randint(1, 3 + difficulty) == 2:
                        # Randomly place enemies away from spawn
                        if x > 7:
                            enemy = Enemy("images/demon.png", .75)
                            enemy.center_x = x * 32
                            enemy.center_y = y * 32
                            enemy.player = self.player_sprite
                            enemy.fireball_list = self.fireball_list
                            enemy.sound_list = self.sound_list
                            enemy.coin_list = self.coin_list
                            enemy.curtime = 0
                            enemy.delay = 0
                            enemy.growl = False
                            enemy.health = 100
                            enemy.death_animation = 0
                            enemy.append_texture(self.demon_die_1)
                            enemy.append_texture(self.demon_die_2)
                            enemy.append_texture(self.demon_slash)
                            self.all_sprites_list.append(enemy)
                            self.enemy_list.append(enemy)

        # Just a random easter egg
        if anti_crash == 777:
            arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

        # Create end door
        wall = arcade.Sprite("images/castle_door_closed.png", 1)
        wall.center_x = 0
        wall.center_y = 5 * 32
        self.all_sprites_list.append(wall)
        self.wall_list.append(wall)

    def change_direction(self):
        # Randomly change to an adjacent direction.
        new_direction = self.direction

        if self.direction == "right" or self.direction == "left":
            if random.randint(0, 1) == 1:
                new_direction = "up"
            else:
                new_direction = "down"
        if self.direction == "up" or self.direction == "down":
            if random.randint(0, 1) == 1:
                new_direction = "left"
            else:
                new_direction = "right"

        self.direction = new_direction

    def on_draw(self):
        arcade.start_render()

        # Draw all the sprites.
        self.effect_list.draw()
        self.chest_list.draw()
        self.arrow_list.draw()
        self.fireball_list.draw()
        self.wall_list.draw()
        self.player_sprite.draw()
        self.enemy_list.draw()
        self.potion_list.draw()
        self.coin_list.draw()
        self.ammo_list.draw()

        # If you get a high score change the text
        if self.highscore_sound:
            # Render the high-score text
            output = "High Score: " + str(self.highscore)
            if not self.highscore_text or self.highscore_text != output:
                self.highscore_text = arcade.create_text(output, arcade.color.YELLOW, 14)

            arcade.render_text(self.highscore_text, self.view_left + 8, self.view_bottom + 365)
        else:
            # Render the score text
            output = "Score: " + str(self.score) + " (" + str(self.highscore) + ")"
            if not self.score_text or self.score_text != output:
                self.score_text = arcade.create_text(output, arcade.color.GREEN, 10)

            arcade.render_text(self.score_text, self.view_left + 8, self.view_bottom + 365)

        if self.player_sprite.alive:
            # Render the arrow count text
            output = "Arrows: " + str(self.ammo)
            if not self.ammo_text or self.ammo_text != output:
                self.ammo_text = arcade.create_text(output, arcade.color.WHITE, 12)

            arcade.render_text(self.ammo_text, self.view_left + 8, self.view_bottom + 8)

            # Draw Health bar
            x = self.player_sprite.center_x
            y = self.player_sprite.center_y
            arcade.draw_rectangle_filled(x, y - 16, 24, 4, (255, 0, 0))
            arcade.draw_rectangle_filled(x - math.ceil((24 - (self.health / 4.16)) / 2), y - 16, math.ceil(self.health / 4.16), 4, (0, 255, 0))

        # Death screen
        if not self.player_sprite.alive:
            arcade.draw_text("You died!", self.player_sprite.center_x - 125, self.player_sprite.center_y, (200, 20, 20), 48)
            arcade.draw_text("Press R To Restart", self.player_sprite.center_x - 125, self.player_sprite.center_y - 125, (200, 20, 20), 24)

        # Instructions
        if not self.game_started:
            arcade.draw_texture_rectangle(self.player_sprite.center_x, self.player_sprite.center_y, 150, 200, self.controls)

    def stab(self):
        if self.player_sprite.alive:
            # Makes it so if you spam the stab button the delay takes longer
            if self.curtime < self.knife_rate:
                self.knife_rate += 5

            if self.curtime > self.knife_rate:
                # Makes it so if you time it right you can stab quickly
                self.knife_delay = self.curtime + 20
                self.knife_rate = self.curtime + 20
                arcade.play_sound(self.sound_list[13])

                # Determine if something is in front of you
                box_l = 0
                box_r = 0
                box_t = 0
                box_b = 0
                range = 36
                if self.player_sprite.eye_pos == "right":
                    box_l = self.player_sprite.center_x
                    box_r = self.player_sprite.center_x + range
                    box_t = self.player_sprite.center_y + 16
                    box_b = self.player_sprite.center_y - 16
                if self.player_sprite.eye_pos == "left":
                    box_l = self.player_sprite.center_x - range
                    box_r = self.player_sprite.center_x
                    box_t = self.player_sprite.center_y + 16
                    box_b = self.player_sprite.center_y - 16
                if self.player_sprite.eye_pos == "up":
                    box_l = self.player_sprite.center_x - 16
                    box_r = self.player_sprite.center_x + 16
                    box_t = self.player_sprite.center_y + range
                    box_b = self.player_sprite.center_y
                if self.player_sprite.eye_pos == "down":
                    box_l = self.player_sprite.center_x - 16
                    box_r = self.player_sprite.center_x + 16
                    box_t = self.player_sprite.center_y
                    box_b = self.player_sprite.center_y - range

                # If it's an enemy kill it
                for enemy in self.enemy_list:
                    if box_l < enemy.center_x < box_r and box_b < enemy.center_y < box_t:
                        enemy.health = 0
                        arcade.play_sound(self.sound_list[14])
                        arcade.play_sound(self.sound_list[6])

                # If it's a fireball reflect it
                for fireball in self.fireball_list:
                    if box_l < fireball.center_x < box_r and box_b < fireball.center_y < box_t:
                        fireball.reflected = True
                        fireball.change_x *= -1
                        fireball.change_y *= -1
                        arcade.play_sound(self.sound_list[14])

    def shoot(self):
        # If you don't have any ammo stab instead.
        if self.ammo <= 0 and self.player_sprite.alive:
            self.stab()

        # If you do have ammo shoot an arrow and remove one ammo.
        elif self.ammo > 0 and self.player_sprite.alive:
            arcade.play_sound(self.sound_list[1])
            self.ammo -= 1
            arrow = Arrow("images/arrow.png", .5)
            arrow.center_x = self.player_sprite.center_x
            arrow.center_y = self.player_sprite.center_y
            arrow.speed = 6
            if self.player_sprite.eye_pos == "right":
                arrow.change_x = arrow.speed
                arrow.change_y = 0
                arrow.angle = -90
            elif self.player_sprite.eye_pos == "left":
                arrow.change_x = -arrow.speed
                arrow.change_y = 0
                arrow.angle = 90
            elif self.player_sprite.eye_pos == "up":
                arrow.change_x = 0
                arrow.change_y = arrow.speed
                arrow.angle = 0
            elif self.player_sprite.eye_pos == "down":
                arrow.change_x = 0
                arrow.change_y = -arrow.speed
                arrow.angle = 180
            self.arrow_list.append(arrow)

    def on_mouse_press(self, x, y, button, modifier):
        # Shoot arrow, start the game if not already started.
        if self.game_started:
            self.shoot()
        else:
            self.game_started = True

    def on_key_press(self, key, modifiers):
        # If you press R restart the game.
        if key == arcade.key.R:
            self.highscore_sound = False
            self.score = 0
            self.curtime = 0
            self.room = 0
            self.health = 100
            self.ammo = 5
            self.knife_delay = 0
            self.knife_rate = 0
            self.setup()

        # If you press a button while the game isn't started, start the game.
        self.game_started = True
        if self.player_sprite.alive:
            # Shoot an arrow
            if key == arcade.key.SPACE:
                self.shoot()

            # Stab
            if key == arcade.key.LSHIFT or key == arcade.key.LALT:
                self.stab()

            # Move
            if key == arcade.key.UP or key == arcade.key.W:
                self.player_sprite.change_y = MOVEMENT_SPEED
                self.player_sprite.set_texture(2)
                self.player_sprite.eye_pos = "up"
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player_sprite.change_y = -MOVEMENT_SPEED
                self.player_sprite.set_texture(3)
                self.player_sprite.eye_pos = "down"
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -MOVEMENT_SPEED
                self.player_sprite.set_texture(1)
                self.player_sprite.eye_pos = "left"
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = MOVEMENT_SPEED
                self.player_sprite.set_texture(0)
                self.player_sprite.eye_pos = "right"

    def on_key_release(self, key, modifiers):
        # Helps prevent the player from getting stuck
        if key == arcade.key.UP or key == arcade.key.W:
            if self.player_sprite.change_y > 0:
                self.player_sprite.change_y = 0

        if key == arcade.key.DOWN or key == arcade.key.S:
            if self.player_sprite.change_y < 0:
                self.player_sprite.change_y = 0

        if key == arcade.key.RIGHT or key == arcade.key.D:
            if self.player_sprite.change_x > 0:
                self.player_sprite.change_x = 0

        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.player_sprite.change_x < 0:
                self.player_sprite.change_x = 0

    def open_chest(self, chest):
        # If chest isn't already opened, open it and spawn random item.
        if chest.get_texture() == 0:
            arcade.play_sound(self.sound_list[12])
            chest.set_texture(1)
            chance = random.randint(1, 2)
            if chance == 1:
                ammo = arcade.Sprite("images/arrow_pack.png", 0.75)
                ammo.center_x = chest.center_x
                ammo.center_y = chest.center_y
                ammo.force = self.curtime + 10  # I'm using force to store time
                self.all_sprites_list.append(ammo)
                self.ammo_list.append(ammo)
            else:
                potion = arcade.Sprite("images/pt1.png")
                potion.center_x = chest.center_x
                potion.center_y = chest.center_y
                potion.force = self.curtime + 10
                self.all_sprites_list.append(potion)
                self.potion_list.append(potion)


    def update(self, delta_time):
        self.curtime += 1

        if self.game_started:
            self.arrow_list.update()
            self.enemy_list.update()
            self.fireball_list.update()
            self.physics_engine.update()

        # If you get a high score write it to scores.txt
        if self.score > self.highscore:
            self.highscore = self.score
            open("scores.txt").close()  # Delete old score
            file = open("scores.txt", 'w')
            file.write(str(self.score))  # Write new score

            # Play a sound when you get a new high score.
            if not self.highscore_sound:
                self.highscore_sound = True
                arcade.play_sound(self.sound_list[15])

        # Stab animation
        if self.knife_delay != 0:
            if self.knife_delay - 10 > self.curtime:
                if self.player_sprite.eye_pos == "up":
                    self.player_sprite.set_texture(5)
                if self.player_sprite.eye_pos == "right":
                    self.player_sprite.set_texture(6)
                if self.player_sprite.eye_pos == "left":
                    self.player_sprite.set_texture(7)
                if self.player_sprite.eye_pos == "down":
                    self.player_sprite.set_texture(8)
            else:
                if self.player_sprite.eye_pos == "up":
                    self.player_sprite.set_texture(2)
                if self.player_sprite.eye_pos == "right":
                    self.player_sprite.set_texture(0)
                if self.player_sprite.eye_pos == "left":
                    self.player_sprite.set_texture(1)
                if self.player_sprite.eye_pos == "down":
                    self.player_sprite.set_texture(3)

        # Makes player slide on death
        if self.health <= 0:
            self.player_sprite.set_texture(4)
            self.player_sprite.alive = False
            if self.player_sprite.change_x > 0:
                self.player_sprite.change_x -= .1
            if self.player_sprite.change_x < 0:
                self.player_sprite.change_x += .1
            if -.2 < float(self.player_sprite.change_x) < .2:
                self.player_sprite.change_x = 0
            if self.player_sprite.change_y > 0:
                self.player_sprite.change_y -= .1
            if self.player_sprite.change_y < 0:
                self.player_sprite.change_y += .1
            if -.2 < float(self.player_sprite.change_y) < .2:
                self.player_sprite.change_y = 0

        # Play sound on death
        if not self.player_sprite.alive and not self.player_sprite.death_sound:
            arcade.play_sound(self.sound_list[10])
            self.player_sprite.death_sound = True

        # When fireball collides with stuff
        for fireball in self.fireball_list:
            # If it hits a wall make it disappear.
            wall_check = arcade.check_for_collision_with_list(fireball, self.wall_list)
            for wall in wall_check:
                fireball.kill()

            # If it hits a chest open the chest and destroy the projectile
            chest_check = arcade.check_for_collision_with_list(fireball, self.chest_list)
            for chest in chest_check:
                if chest.get_texture() == 0:
                    fireball.kill()
                    self.open_chest(chest)

            # If it hits the player hurt them
            if not fireball.reflected:
                if arcade.check_for_collision(fireball, self.player_sprite):
                    self.health -= 25
                    arcade.play_sound(self.sound_list[random.randint(7, 9)])
                    fireball.kill()

            # If the player reflects the fireball have it hurt other enemies
            if fireball.reflected:
                enemy_check = arcade.check_for_collision_with_list(fireball, self.enemy_list)
                for enemy in enemy_check:
                    if enemy.health > 0:
                        fireball.kill()
                        enemy.health = 0
                        arcade.play_sound(self.sound_list[6])

        # When arrow collides with stuff
        for arrow in self.arrow_list:
            # Make arrow stick in wall when it hits it
            wall_check = arcade.check_for_collision_with_list(arrow, self.wall_list)
            for wall in wall_check:
                ghost_arrow = arcade.Sprite("images/arrow.png", .5)
                ghost_arrow.center_x = arrow.center_x
                ghost_arrow.center_y = arrow.center_y
                ghost_arrow.angle = arrow.angle
                self.effect_list.append(ghost_arrow)
                arrow.kill()
                arcade.play_sound(self.sound_list[11])

            # When arrow hits enemy kill them and remove projectile
            enemy_check = arcade.check_for_collision_with_list(arrow, self.enemy_list)
            for enemy in enemy_check:
                if enemy.health > 0:
                    arrow.kill()
                    enemy.health = 0
                    arcade.play_sound(self.sound_list[6])

            # When arrow hits chest open it and remove projectile
            chest_check = arcade.check_for_collision_with_list(arrow, self.chest_list)
            for chest in chest_check:
                if chest.get_texture() == 0:
                    self.open_chest(chest)
                    arrow.kill()

        # If the player runs into an enemy kill the player
        for enemy in self.enemy_list:
            enemy_check = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
            for enemy in enemy_check:
                if enemy.health > 0:
                    self.health = 0
                    enemy.set_texture(3)

        # If player runs into a chest open the chest
        chest_list = arcade.check_for_collision_with_list(self.player_sprite, self.chest_list)
        for item in chest_list:
            self.open_chest(item)

        # If player runs into the ammo pickup give arrows and remove it
        ammo_list = arcade.check_for_collision_with_list(self.player_sprite, self.ammo_list)
        for item in ammo_list:
            if self.curtime > item.force:
                arcade.play_sound(self.sound_list[2])
                item.kill()
                self.ammo += 3

        # If player runs into the coin pick it up
        coin_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for item in coin_list:
            if self.curtime > item.force:
                arcade.play_sound(self.sound_list[16])
                item.kill()
                self.score += 1

        # If player runs into the potion pickup heal player and remove it
        potion_list = arcade.check_for_collision_with_list(self.player_sprite, self.potion_list)
        for item in potion_list:
            if self.curtime > item.force:
                arcade.play_sound(self.sound_list[3])
                item.kill()
                if self.health <= 90:
                    self.health += 10
                else:
                    self.health += (100 - self.health)

        # If you walk into the end door go into a new dungeon
        y = self.doorpos * 32
        if (y - 16) < self.player_sprite.center_y < (y + 16) and self.player_sprite.center_x > ((BR_X - 2) * 32):
            self.room += 1
            self.score = int(self.score * (1 + (self.room / 10)))  # Give a bonus for beating a dungeon.
            self.setup()

        # Track if we need to change the viewport
        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCROLL_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCROLL_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left, SCROLL_WIDTH + self.view_left, self.view_bottom, SCROLL_HEIGHT + self.view_bottom)


def main():
    window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
