import arcade
import math
import globalvars
import random
import gamedata
import os
import spell_data

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 768

class Player(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.speed = 0
        self.anim_delay = 0
        self.anim_count = 0
        self.cast_delay = 0
        self.slash_delay = 0
        self.anim_rate = 0
        self.curtime = 0
        self.debug = 0
        self.walk_delay = 0
        self.melee_damage = 0
        self.exp_cur = 0
        self.exp_cap = 20
        self.level = 0
        self.skillpoints = 0
        self.mana = 0
        self.mana_cap = 0
        self.mana_regen_delay = 0
        self.sword_poisoned = 0

        self.window_ref = None
        self.spell_list = None
        self.spell_icon_list = None
        self.current_spell_icon = None
        self.bullet_list = None
        self.skill_list = []
        self.inferno_list = []
        self.orb_list = []

        self.rendering_animation = False
        self.attacking = False
        self.surged = False
        self.step_switch = False

        self.selected_spell = ""
        self.old_direction = "right"
        self.direction = "down"

        self.animation_list = []

    def getNearbyEnemies(self, source, range):
        result = []

        for enemy in globalvars.enemy_list:
            if (((source.center_x - enemy.center_x) ** 2) + ((source.center_y - enemy.center_y) ** 2)) <= range ** 2:
                result.append(enemy)

        return result

    def give_exp(self, amount):
        if self.level < 10:
            self.exp_cur += amount
            self.check_levelup()
        elif self.level > 10:
            self.level = 10

    def check_levelup(self):
        if self.exp_cur >= self.exp_cap:
            globalvars.emit_sound("levelup.ogg")

            if (self.level == 9):
                globalvars.skills_ultimate = True
                globalvars.emit_sound("ult_select.ogg")

            self.level += 1
            self.skillpoints += 1
            self.exp_cur = self.exp_cur - self.exp_cap
            self.exp_cap *= 1.5

            if self.level == 1:
                self.mana_cap = 100
            else:
                self.mana_cap *= 1.25
            self.mana = self.mana_cap

            if self.level >= 10:
                globalvars.level_text = arcade.create_text("10", (158, 17, 120), 32)
            else:
                globalvars.level_text = arcade.create_text(str(self.level), (50, 64, 200), 24)

            if self.exp_cur >= self.exp_cap:
                self.check_levelup()

    def give_spell(self, spell_name):
        found_spell = []

        for item in spell_data.spells:
            if spell_name == item[1]:
                found_spell = item

        exists = False
        for item in self.spell_list:
            if item == found_spell:
                exists = True

        if not exists:
            self.spell_list.append(found_spell)

            if found_spell[0] != "passive":
                self.spell_icon_list.append(arcade.load_texture("images/UI/icons/" + spell_name + ".png"))

    def give_skill(self, skill):
        exists = False
        for item in self.skill_list:
            if item == skill:
                exists = True

        if not exists:
            self.skill_list.append(skill)

    def update(self):
        self.curtime += 1

        self.mana_regen_delay += 1
        if self.mana_regen_delay > 10 and self.mana < self.mana_cap:
            self.mana += 1

            if self.player_has_skill("Affinity"):
                vit = 5

                if self.player_has_skill("Vitality"):
                    vit = 7

                self.mana_regen_delay = vit
            else:
                self.mana_regen_delay = 0

        if not self.attacking:
            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.center_x > SCREEN_WIDTH and self.change_x > 0:
                self.center_x = SCREEN_WIDTH
            if self.center_x < 0 and self.change_x < 0:
                self.center_x = 0
            if self.center_y > SCREEN_HEIGHT and self.change_y > 0:
                self.center_y = SCREEN_HEIGHT
            if self.center_y < 0 and self.change_y < 0:
                self.center_y = 0

        # Change direction based on where you're going.
        if self.change_x > 0 and self.change_y == 0:
            self.direction = "right"
        elif self.change_x < 0 and self.change_y == 0:
            self.direction = "left"
        elif self.change_y > 0 and self.change_x == 0:
            self.direction = "up"
        elif self.change_y < 0 and self.change_x == 0:
            self.direction = "down"

        # Plays the animations
        if self.rendering_animation and self.curtime > self.anim_delay:
            self.anim_delay = self.curtime + self.anim_rate
            if len(self.animation_list) > 0:
                for i in range(len(self.textures)):
                    if self.textures[i] == self.animation_list[self.anim_count]:
                        self.set_texture(i)
            self.anim_count += 1
            if self.anim_count >= len(self.animation_list):
                self.rendering_animation = False
                self.attacking = False

        # If you change directions, stop the previous walk animations.
        if self.direction != self.old_direction and not self.attacking:
            self.animation_list = []

        self.old_direction = self.direction

        # If you're not doing anything, play the idle animation.
        if self.change_x == 0 and self.change_y == 0 and not self.attacking:
            if self.direction == "down":
                self.set_texture(0)
            if self.direction == "left":
                self.set_texture(1)
            if self.direction == "right":
                self.set_texture(2)
            if self.direction == "up":
                self.set_texture(3)
        elif not self.rendering_animation:
            walk_anim = "walk/" + self.direction
            self.play_animation(walk_anim, 1.5)

    def play_animation(self, animation, rate):
        # Footstep sounds
        if len(animation) > 6:
            if animation[:4] == "walk":
                if self.step_switch:
                    globalvars.emit_sound("footstep_left.ogg")
                else:
                    globalvars.emit_sound("footstep_right.ogg")
                self.step_switch = not self.step_switch

        # Load images for animation
        self.animation_list = []
        try:
            folder = "images/char/" + animation
            temp = os.listdir(folder)
            for i in range(len(temp)):
                self.animation_list.append(arcade.load_texture(folder + "/" + temp[i]))
            self.anim_count = 0
            self.anim_rate = rate
            self.rendering_animation = True
        except:
            print("Error loading animation")

    # Check if the key you press corresponds to what your supposed to based on the config for custom key binds.
    def check_key(self, index, button):
        result = False
        for item in globalvars.keys[index]:
            if str(item) == str(button):
                result = True
        return result

    def key_press(self, key, modifier):
        # Quick Select a spell with 1-2-3
        quickspell = -1

        if self.check_key(6, key):
            quickspell = 0

        if self.check_key(7, key):
            quickspell = 1

        if self.check_key(8, key):
            quickspell = 2

        adj_list = self.spell_list.copy()
        local_done = False

        while not local_done:
            local_finished = True

            for item in adj_list:
                if item[0] == "passive":
                    adj_list.remove(item)
                    local_finished = False
                    break

            local_done = local_finished

        if quickspell >= 0 and quickspell < len(adj_list):
            new_spell = adj_list[quickspell]

            if new_spell != self.selected_spell:
                globalvars.emit_sound("click.ogg")
                self.selected_spell = adj_list[quickspell]
                self.current_spell_icon = self.spell_icon_list[quickspell]


        # Sword
        if self.check_key(4, key) and not self.attacking:
            if self.curtime > self.slash_delay:
                delay = 40

                if self.player_has_skill("Frenzy"):
                    delay = 30

                    if self.player_has_skill("Vitality"):
                        delay = 20

                self.slash_delay = self.curtime + delay
                self.attacking = True
                temp = "slash/" + self.direction
                self.play_animation(temp, 2)
                globalvars.emit_sound("knife_swing.ogg")

                # Find the range where the slash will hit.
                forward_range = 42
                side_range = 32
                box_left = 0
                box_right = 0
                box_up = 0
                box_down = 0
                if self.direction == "up":
                    box_left = self.center_x - side_range
                    box_right = self.center_x + side_range
                    box_up = self.center_y + forward_range
                    box_down = self.center_y
                if self.direction == "down":
                    box_left = self.center_x - side_range
                    box_right = self.center_x + side_range
                    box_up = self.center_y
                    box_down = self.center_y - forward_range
                if self.direction == "left":
                    box_left = self.center_x - forward_range
                    box_right = self.center_x
                    box_up = self.center_y + side_range
                    box_down = self.center_y - side_range
                if self.direction == "right":
                    box_left = self.center_x
                    box_right = self.center_x + forward_range
                    box_up = self.center_y + side_range
                    box_down = self.center_y - side_range

                # If any enemies are in this range damage them.
                for enemy in globalvars.enemy_list:
                    if box_left < enemy.center_x < box_right and box_down < enemy.center_y < box_up:
                        globalvars.emit_sound("knife_hit.ogg")

                        damage = self.melee_damage

                        if self.player_has_skill("Beserk"):
                            damage = self.melee_damage + 35

                            if self.player_has_skill("Vitality"):
                                damage = damage + 35

                        enemy.on_take_damage(damage, True)

                        if self.player_has_skill("Siphon"):
                            amount = 5

                            if self.player_has_skill("Vitality"):
                                amount = 10

                            if (self.mana_cap - self.mana) < amount:
                                amount = self.mana_cap - self.mana

                            self.mana += amount

                        if self.sword_poisoned > 0:
                            if not self.player_has_skill("Eternal"):
                                self.sword_poisoned -= 1

                            duration = 200
                            damage = 3
                            if self.player_has_skill("Lasting"):
                                duration = 400

                            if self.player_has_skill("Frailty"):
                                damage += round(enemy.health / 50)

                            if self.surged:
                                damage = round(damage * 1.5)

                            poison = Blade_Poison("images/status.png")
                            poison.enemy = enemy
                            poison.duration = duration
                            poison.damage = damage
                            poison.damage_delay = 0
                            poison.curtime = 0
                            poison.center_x = -1000
                            poison.center_y = -1000
                            poison.player = self
                            poison.orig_speed = enemy.speed

                            for i in range(1, 6):
                                poison.append_texture(arcade.load_texture("images/effects/poison/" + str(i) + ".png"))

                            self.bullet_list.append(poison)
                            self.surged = False

                        if not self.player_has_skill("Fury"):
                            break   # Prevents multiple enemies being hit.
            else:
                if not self.player_has_skill("Frenzy"):
                    self.slash_delay += 5   # Spamming the button increases the delay

        # Spell
        if self.check_key(5, key) and not self.attacking:
            if self.curtime > self.cast_delay:
                if len(self.selected_spell) > 0:
                    local_spell_name = self.selected_spell[1]

                    delay = 40
                    if local_spell_name == "Lightning":
                        delay = 30
                        if self.player_has_skill("Rapid"):
                            delay = 20

                    if local_spell_name == "Magic Missile":
                        if self.player_has_skill("Barrage"):
                            delay = 25

                    if self.player_has_skill("Spellcaster"):
                        delay = int(math.ceil(delay / 2))

                        if self.player_has_skill("Vitality"):
                            delay = int(math.ceil(delay / 2))

                    should_cast = True

                    if local_spell_name == "Venomblade":
                        if self.player_has_skill("Eternal") and self.sword_poisoned == 1:
                            should_cast = False

                        if not self.player_has_skill("Eternal") and self.sword_poisoned == 1:
                            should_cast = False

                    if should_cast:
                        self.cast_delay = self.curtime + delay
                        self.attacking = True
                        temp = "spellcast/" + self.direction
                        self.play_animation(temp, 2)
                        self.cast_spell(local_spell_name)
            else:
                prevent_spam = True

                if self.player_has_skill("Frenzy"):
                    prevent_spam = False

                if self.selected_spell[1] == "Lightning" and self.player_has_skill("Rapid"):
                    prevent_spam = False

                if self.selected_spell[1] == "Magic Missile" and self.player_has_skill("Barrage"):
                    prevent_spam = False

                if prevent_spam:
                    self.cast_delay += 5    # Spamming the button increases the delay

        # Movement
        if not self.attacking:
            if self.check_key(0, key):
                self.change_y = self.speed

            if self.check_key(1, key):
                self.change_y = -self.speed

            if self.check_key(3, key):
                self.change_x = self.speed

            if self.check_key(2, key):
                self.change_x = -self.speed

    def key_release(self, key, modifier):
        if self.check_key(0, key):
            if self.change_y > 0:
                self.change_y = 0

        if self.check_key(3, key):
            if self.change_x > 0:
                self.change_x = 0

        if self.check_key(2, key):
            if self.change_x < 0:
                self.change_x = 0

        if self.check_key(1, key):
            if self.change_y < 0:
                self.change_y = 0

    def check_mana(self, cost):
        can_cast = False

        if self.player_has_skill("Mastery"):
            cost = math.ceil(cost / 1.5)

            if self.player_has_skill("Vitality"):
                cost = math.ceil(cost / 1.5)

        if self.mana > cost:
            self.mana -= cost
            can_cast = True
        else:
            self.window_ref.display_errorbox("Not enough mana!")

        return can_cast

    def player_has_skill(self, skill):
        result = False
        for item in self.skill_list:
            if item == skill:
                result = True
        return result

    def ignite(self, enemy, duration):
        if enemy.ignite <= 0:
            effect = Flame("images/effects/flame/1.png")
            for i in range(1, 12):
                effect.append_texture(arcade.load_texture("images/effects/flame/" + str(i) + ".png"))
            effect.center_x = enemy.center_x
            effect.center_y = enemy.center_y
            effect.enemy = enemy
            effect.enemy_list = globalvars.enemy_list
            effect.player = self
            effect.bullet_list = self.bullet_list
            effect.lifetime = duration
            effect.anim_timer = 0
            effect.anim_track = 0
            self.bullet_list.append(effect)

            enemy.ignite = duration

    # I probably could have automated this way more using sub-classes but the spells varied so much I didn't think it would help much.

    def cast_spell(self, spell_data):
        spell = spell_data

        globalvars.emit_sound("spell_cast_" + str(random.randint(1, 5)) + ".ogg")

        x_change = 0
        y_change = 0
        if self.direction == "right":
            x_change = 1
            y_change = 0
        elif self.direction == "left":
            x_change = -1
            y_change = 0
        elif self.direction == "down":
            x_change = 0
            y_change = -1
        elif self.direction == "up":
            x_change = 0
            y_change = 1

        if spell == "Fireball" and self.check_mana(20):
            globalvars.emit_sound("fireball.ogg")
            speed = 2
            if self.player_has_skill("Velocity"):
                speed = 4

            damage = 30
            if self.player_has_skill("Potent"):
                damage = 50

            if self.surged:
                damage = round(damage * 1.5)

            fireball = Fireball("images/effects/fireball.png", 2)
            fireball.center_x = self.center_x
            fireball.center_y = self.center_y
            fireball.speed = speed
            fireball.contact_damage = damage
            fireball.explosion_damage = round(fireball.contact_damage / 2.5)
            fireball.attack_radius = 16
            fireball.explosion_radius = 64
            fireball.enemy_list = globalvars.enemy_list
            fireball.bullet_list = self.bullet_list
            fireball.player = self

            fireball.change_x = x_change * fireball.speed
            fireball.change_y = y_change * fireball.speed

            self.bullet_list.append(fireball)
            self.surged = False

        if spell == "Beam" and self.check_mana(25):
            damage = 15
            speed = 10
            if self.player_has_skill("Hyper"):
                damage = 25
                speed = 15

            if self.surged:
                damage = round(damage * 1.5)

            globalvars.emit_sound("beam_shoot.ogg")
            beam = Beam("images/TD/entities/projectile/beam.png")
            beam.center_x = self.center_x
            beam.center_y = self.center_y
            beam.speed = speed
            beam.change_x = x_change * beam.speed
            beam.change_y = y_change * beam.speed
            beam.enemy_list = globalvars.enemy_list
            beam.damage = damage
            beam.penetrate = 5
            beam.hit_list = []
            beam.player = self

            if self.direction == "right":
                beam.center_x += 16
            elif self.direction == "left":
                beam.center_x -= 16
            elif self.direction == "up":
                beam.center_y += 16
                beam.angle = 90
            elif self.direction == "down":
                beam.center_y -= 16
                beam.angle = 90

            self.bullet_list.append(beam)
            self.surged = False

        if spell == "Inferno" and self.check_mana(50):
            for item in self.inferno_list:
                item.kill()

            length = 3

            if self.player_has_skill("Wildfire"):
                length = 9

            duration = 200

            if self.player_has_skill("Fueled"):
                duration = 300

            if self.player_has_skill("Wildfire"):
                duration *= 2

            for i in range(length):
                inferno = Inferno("images/effects/inferno/1.png")
                inferno.center_x = self.center_x + (x_change * (i + 1) * 32)
                inferno.center_y = self.center_y + (y_change * (i + 1) * 32)
                inferno.duration = duration
                inferno.curtime = 0
                inferno.enemy_list = globalvars.enemy_list
                inferno.anim_track = 0
                inferno.hit_delay = 0

                damage = 2
                if self.surged:
                    damage = round(damage * 1.5)

                inferno.damage = damage
                inferno.player = self
                for i in range(1, 5):
                    inferno.append_texture(arcade.load_texture("images/effects/inferno/" + str(i) + ".png"))

                self.bullet_list.append(inferno)
                self.inferno_list.append(inferno)
            self.surged = False

        if spell == "Dart" and self.check_mana(75):
            dart = Dart("images/TD/entities/projectile/dart.png")
            dart.center_x = self.center_x
            dart.center_y = self.center_y
            dart.speed = 10
            dart.change_x = x_change * dart.speed
            dart.change_y = y_change * dart.speed
            dart.player = self

            damage = 50
            if self.surged:
                damage = round(damage * 1.5)

            dart.damage = damage
            dart.enemy_list = globalvars.enemy_list
            dart.hit_list = []

            if self.direction == "right":
                dart.center_x += 16
                dart.angle = 180
            elif self.direction == "left":
                dart.center_x -= 16
                dart.angle = 0
            elif self.direction == "up":
                dart.center_y += 16
                dart.angle = 90
            elif self.direction == "down":
                dart.center_y -= 16
                dart.angle = 270

            self.bullet_list.append(dart)
            self.surged = False

        if spell == "Venomblade" and self.check_mana(25):
            self.sword_poisoned = 1

        if spell == "Cloud" and self.check_mana(35):
            if self.pcloud is not None:
                self.pcloud.kill()

            cloud = Cloud("images/status.png")
            cloud.center_x = self.center_x + (x_change * 32)
            cloud.center_y = self.center_y + (y_change * 32)

            size = 32
            if self.player_has_skill("Expansive"):
                size = 48

            duration = 300
            cloud.duration = duration
            cloud.curtime = 0
            cloud.range = size
            cloud.hit_list = []
            cloud.player = self
            cloud.enemy_list = globalvars.enemy_list
            cloud.bullet_list = self.bullet_list
            cloud.damage_delay = 0

            for i in range(1, 6):
                cloud.append_texture(arcade.load_texture("images/effects/poison_cloud/" + str(i) + ".png"))

            self.bullet_list.append(cloud)
            self.pcloud = cloud
            self.surged = False

        if spell == "Lightning" and self.check_mana(10):
            damage = 25
            if self.player_has_skill("Voltage"):
                damage = 35

            globalvars.emit_sound("lightning_cast.ogg")

            speed = 5
            if self.player_has_skill("Amplitude"):
                speed = 9
                damage = round(damage * 1.5)

            if self.surged:
                damage = round(damage * 1.5)

            shock = Lightning("images/status.png")
            shock.center_x = self.center_x
            shock.center_y = self.center_y
            shock.speed = speed
            shock.change_x = x_change * shock.speed
            shock.change_y = y_change * shock.speed
            shock.player = self
            shock.damage = damage
            shock.enemy_list = globalvars.enemy_list
            shock.hit_list = []

            if self.direction == "right":
                shock.center_x += 16
                shock.angle = 180
            elif self.direction == "left":
                shock.center_x -= 16
                shock.angle = 0
            elif self.direction == "up":
                shock.center_y += 16
                shock.angle = 90
            elif self.direction == "down":
                shock.center_y -= 16
                shock.angle = 270

            for i in range(1, 5):
                shock.append_texture(arcade.load_texture("images/TD/entities/towers/medieval/shock/shock_" + str(i) + ".png"))

            self.bullet_list.append(shock)
            self.surged = False

        if spell == "Thunderstrike" and self.check_mana(75):
            thunder = Thunder("images/status.png")
            thunder.center_x = self.center_x + (x_change * 64)
            thunder.center_y = self.center_y + (y_change * 64) + 42

            radius = 48
            if self.player_has_skill("Powerful"):
                radius = 64

            damage = 100
            if self.player_has_skill("Smiting"):
                damage = 150

            if self.surged:
                damage = round(damage * 1.5)

            thunder.anim_timer = 0
            thunder.curtime = 0
            thunder.damage = damage
            thunder.radius = radius
            thunder.anim_track = 0
            thunder.enemy_list = globalvars.enemy_list
            thunder.bullet_list = self.bullet_list
            thunder.player = self

            for i in range(1, 10):
                thunder.append_texture(arcade.load_texture("images/effects/thunder/" + str(i) + ".png"))

            self.bullet_list.append(thunder)
            self.surged = False

        if spell == "Orb" and self.check_mana(50):
            if self.player_has_skill("Scorn"):
                for i in range(0, len(self.orb_list) - 1):
                    self.orb_list[i].kill()
            else:
                for item in self.orb_list:
                    item.kill()

            dmg = 5
            if self.player_has_skill("Static"):
                dmg = 10

            if self.surged:
                dmg = round(dmg * 1.5)

            orb = Orb("images/status.png")
            orb.center_x = self.center_x + (x_change * 32)
            orb.center_y = self.center_y + (y_change * 32)
            orb.curtime = 0
            orb.starting_speed = 1
            orb.starting_change_x = x_change * orb.starting_speed
            orb.starting_change_y = y_change * orb.starting_speed
            orb.change_x = orb.starting_change_x
            orb.change_y = orb.starting_change_y
            orb.player = self
            orb.damage = dmg
            orb.path_counter = 0
            orb.anim_counter = 0

            for i in range(1, 21):
                orb.append_texture(arcade.load_texture("images/effects/orb/" + str(i) + ".png"))

            self.bullet_list.append(orb)
            self.orb_list.append(orb)
            self.surged = False

        if spell == "Burden" and self.check_mana(30):
            burden = Burden("images/effects/burden.png")
            burden.center_x = self.center_x + (x_change * 32)
            burden.center_y = self.center_y + (y_change * 32)
            burden.speed = 3
            burden.change_x = x_change * burden.speed
            burden.change_y = y_change * burden.speed
            burden.player = self

            radius = 32
            if self.player_has_skill("Broaden"):
                radius = 64
            burden.explosion_radius = radius

            self.bullet_list.append(burden)

        if spell == "Magic Missile" and self.check_mana(15):
            if self.active_mm is not None and not self.player_has_skill("Devour"):
                self.active_mm.kill()

            mm = MagicMissile("images/status.png")
            mm.center_x = self.center_x + (x_change * 32)
            mm.center_y = self.center_y + (y_change * 32)

            size = 32

            if self.player_has_skill("Devour"):
                size = 50

            drag = size

            if self.player_has_skill("Concentrate"):
                drag = size / 2

            if self.player_has_skill("Overcharged"):
                size = size + (size * (self.mana / self.mana_cap))

            img_scale = size / 256

            base_damage = 50
            if self.player_has_skill("Devastating"):
                base_damage = 75

            local_damage = int(base_damage + (math.pow(32, math.sqrt(size) / 10)))

            if self.player_has_skill("Devour") and self.active_mm is not None:
                current_volume = math.pow((self.active_mm.size / 2), 3) * math.pi * (4 / 3)
                new_volume = math.pow((size / 2), 3) * math.pi * (4 / 3)
                adj_volume = current_volume + new_volume
                adj_radius = math.pow(adj_volume / (math.pi * (4 / 3)), (1 / 3))

                size = (adj_radius * 2) + 3

                drag = size

                if self.player_has_skill("Concentrate"):
                    drag = size / 2

                img_scale = size / 256
                local_damage = int(base_damage + (math.pow(32, math.sqrt(size) / 10)))

                mm.center_x = self.active_mm.center_x
                mm.center_y = self.active_mm.center_y

                self.active_mm.kill()

            mm.curtime = 0
            mm.range = size / 2
            mm.hit_list = []
            mm.player = self
            mm.enemy_list = globalvars.enemy_list
            mm.bullet_list = self.bullet_list
            mm.damage_delay = 0
            mm.damage = local_damage
            mm.drag = drag
            mm.img_scale = img_scale
            mm.size = size

            for i in range(1, 6):
                mm.append_texture(arcade.load_texture("images/effects/magic_missile/" + str(i) + ".png", scale=img_scale))

            self.bullet_list.append(mm)
            self.active_mm = mm

        if spell == "Starblast" and self.check_mana(16):
            sb = Starblast("images/status.png")
            sb.center_x = self.center_x + (x_change * 32)
            sb.center_y = self.center_y + (y_change * 32)

            size = self.mana

            if self.player_has_skill("Dark Energy"):
                self.mana -= int(math.ceil(self.mana / 4))
            else:
                self.mana = 0

            if self.player_has_skill("Protostar") and size < 64:
                size = 64

            img_scale = size / 128

            local_damage = int(math.ceil((math.pow(5, math.pow(size, (1/4))))))

            local_range = size / 4

            if self.player_has_skill("Red Giant"):
                local_range = size / 2

            local_range += 16

            sb.curtime = 0
            sb.range = local_range
            sb.hit_list = []
            sb.player = self
            sb.enemy_list = globalvars.enemy_list
            sb.bullet_list = self.bullet_list
            sb.damage_delay = 0
            sb.damage = local_damage
            sb.img_scale = img_scale
            sb.size = size
            sb.anim_pattern = [1, 1, 65, 2, 2, 2, 1]
            sb.anim_track = 0

            if size > 320:
                globalvars.emit_sound("starblast_superheavy.ogg")
            if size >= 192:
                globalvars.emit_sound("starblast_heavy.ogg")
            elif size > 64:
                globalvars.emit_sound("starblast_normal.ogg")
            else:
                globalvars.emit_sound("starblast_light.ogg")

            for i in range(1, 8):
                sb.append_texture(arcade.load_texture("images/effects/starblast/" + str(i) + ".png", scale=img_scale))

            self.bullet_list.append(sb)


# One-time effect that displays all the textures found in the sprite on a delay and deletes itself afterwards
class Effect(arcade.Sprite):
    def _init_(self):
        self.anim_track = 0
        self.delay = 0
        self.curtime = 0
        self.delay_logic = 0

    def update(self):
        self.curtime += 1
        if self.curtime > self.delay_logic:
            self.delay_logic = self.curtime + self.delay
            if self.anim_track < len(self.textures):
                self.set_texture(self.anim_track)
            else:
                self.kill()
            self.anim_track += 1

# Looping fire effect that lasts a specific amount of time
class Flame(arcade.Sprite):
    def _init_(self):
        self.enemy = None
        self.player = None
        self.bullet_list = None
        self.lifetime = 0
        self.anim_timer = 0
        self.anim_track = 0

    def update(self):
        self.center_x = self.enemy.center_x
        self.center_y = self.enemy.center_y + 10

        if self.enemy.health <= 0:
            if self.player.player_has_skill("Melting"):
                globalvars.emit_sound("fireball_explode.ogg")
                effect = Effect("images/TD/effects/explosion/explosion_1.png")
                for i in range(1, 6):
                    effect.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_" + str(i) + ".png"))
                effect.anim_track = 0
                effect.curtime = 0
                effect.delay_logic = 0
                effect.center_x = self.center_x
                effect.center_y = self.center_y
                effect.delay = 1
                self.bullet_list.append(effect)

                for enemy in globalvars.enemy_list:
                    if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 64 ** 2:
                        enemy.on_take_damage(50, True)
                        if enemy.ignite <= 0:
                            self.player.ignite(enemy, 15)

            self.kill()

        if self.anim_track < len(self.textures):
            self.set_texture(self.anim_track)
            self.anim_track += 1
        else:
            self.anim_track = 0

        self.anim_timer += 1
        if self.anim_timer > 20:
            self.anim_timer = 0
            self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()


class Fireball(arcade.Sprite):
    def _init_(self):
        self.contact_damage = 0
        self.explosion_damage = 0
        self.attack_radius = 0
        self.explosion_radius = 0
        self.bullet_list = []
        self.player = None

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 20

        if self.center_x > SCREEN_WIDTH + 32 or self.center_x < -32 or self.center_y > SCREEN_HEIGHT + 32 or self.center_y < -32:
            self.kill()

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2:
                # Contact Damage
                globalvars.emit_sound("fireball_hit.ogg")
                enemy.on_take_damage(self.contact_damage, True)
                i_time = 6
                if self.player.player_has_skill("Volcanic"):
                    i_time = 12
                enemy.ignite = i_time

                effect = Flame("images/effects/flame/1.png")
                for i in range(1, 12):
                    effect.append_texture(arcade.load_texture("images/effects/flame/" + str(i) + ".png"))
                effect.center_x = enemy.center_x
                effect.center_y = enemy.center_y
                effect.enemy = enemy
                effect.enemy_list = globalvars.enemy_list
                effect.player = self.player
                effect.bullet_list = self.bullet_list
                effect.lifetime = i_time
                effect.anim_timer = 0
                effect.anim_track = 0
                self.bullet_list.append(effect)

                # Explosion Effect
                if self.player.player_has_skill("Fire Blast"):
                    globalvars.emit_sound("fireball_explode.ogg")
                    effect = Effect("images/TD/effects/explosion/explosion_1.png")
                    for i in range(1, 6):
                        effect.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_" + str(i) + ".png"))
                    effect.anim_track = 0
                    effect.curtime = 0
                    effect.delay_logic = 0
                    effect.center_x = self.center_x
                    effect.center_y = self.center_y
                    effect.delay = 1
                    self.bullet_list.append(effect)

                    # Explosion Damage
                    for enemy in globalvars.enemy_list:
                        if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.explosion_radius ** 2:
                            enemy.on_take_damage(self.explosion_damage, True)
                            if enemy.ignite <= 0:
                                self.player.ignite(enemy, i_time)

                # Delete afterwards
                self.kill()
                break

class Beam(arcade.Sprite):
    def _init_(self):
        self.penetrate = 0
        self.damage = 0
        self.hit_list = []
        self.player = None
        self.speed = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x > SCREEN_WIDTH + 32 or self.center_x < -32 or self.center_y > SCREEN_HEIGHT + 32 or self.center_y < -32:
            self.kill()

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 15 ** 2:
                if self.penetrate > 0:
                    in_list = False
                    for item in self.hit_list:
                        if item == enemy:
                            in_list = True

                    if not in_list:
                        globalvars.emit_sound("beam_hit.ogg")

                        if not self.player.player_has_skill("Plasma"):
                            self.penetrate -= 1

                        self.hit_list.append(enemy)

                        damage = self.damage
                        if enemy.ignite > 0 and self.player.player_has_skill("Searing"):
                            damage = round(damage * 1.7)
                        enemy.on_take_damage(damage, True)

                        if self.player.player_has_skill("Blistering"):
                            self.player.ignite(enemy, 6)
                else:
                    if self.player.player_has_skill("Reflective") and random.randint(1, 4) == 3:
                        self.penetrate = 5
                        self.change_x *= -1
                        self.change_y *= -1
                    else:
                        self.kill()


class Inferno(arcade.Sprite):
    def _init_(self):
        self.duration = 0
        self.curtime = 0
        self.anim_track = 0
        self.hit_delay = 0
        self.damage = 0
        self.player = None

    def update(self):
        if self.curtime > self.duration:
            self.kill()

        self.curtime += 1
        self.anim_track += 1
        if self.anim_track >= len(self.textures):
            self.anim_track = 0
        self.set_texture(self.anim_track)

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 15 ** 2 and self.curtime > self.hit_delay:
                self.hit_delay = self.curtime + 2

                damage = round(self.damage * enemy.fire_weakness)

                if self.player.player_has_skill("Ash"):
                    damage = round(damage * 1.5)

                enemy.on_take_damage(damage, True)

                if self.player.player_has_skill("Decay"):
                    enemy.fire_weakness += .1

                if self.player.player_has_skill("Consuming"):
                    if enemy.health <= 0:
                        self.duration += 100

class Dart(arcade.Sprite):
    def _init_(self):
        self.player = None
        self.damage = 0
        self.hit_list = []

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x > SCREEN_WIDTH + 32 or self.center_x < -32 or self.center_y > SCREEN_HEIGHT + 32 or self.center_y < -32:
            self.kill()

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 15 ** 2:
                already_hit = False
                for item in self.hit_list:
                    if item == enemy:
                        already_hit = True

                if not already_hit:
                    enemy.on_take_damage(self.damage, True)
                    self.hit_list.append(enemy)

                    if self.player.player_has_skill("Lethal"):
                        if random.randint(1, 4) == 3:
                            if enemy.name != "skeletonlord":
                                enemy.health = 0
                                enemy.kill()
                            else:
                                enemy.on_take_damage(enemy.health_gate, True)

                    # I'm using an empty sprite to calculate the poison.
                    duration = 125
                    damage = 10

                    if self.player.player_has_skill("Venom"):
                        duration = 250

                    if self.player.player_has_skill("Debilitating"):
                        damage = 15

                    poison = Poison("images/status.png")
                    poison.enemy = enemy
                    poison.duration = duration
                    poison.damage = damage
                    poison.damage_delay = 0
                    poison.curtime = 0
                    poison.center_x = -1000
                    poison.center_y = -1000
                    poison.player = self.player
                    poison.orig_speed = enemy.speed
                    poison.paralyzed = False

                    for i in range(1, 6):
                        poison.append_texture(arcade.load_texture("images/effects/poison/" + str(i) + ".png"))

                    if self.player.player_has_skill("Paralyzing"):
                        if random.randint(1, 4) == 3 and not enemy.invincible:
                            poison.paralyzed = True

                    self.player.bullet_list.append(poison)

                    if self.player.player_has_skill("Penetrating"):
                        if random.randint(1, 2) == 2:
                            self.kill()
                    else:
                        self.kill()

class Poison(arcade.Sprite):
    def _init_(self):
        self.enemy = None
        self.duration = 0
        self.damage = 0
        self.damage_delay = 0
        self.curtime = 0
        self.player = None
        self.paralyze = False
        self.orig_speed = 0
        self.paralyzed = False

    def update(self):
        self.curtime += 1

        self.center_x = self.enemy.center_x
        self.center_y = self.enemy.center_y
        self.set_texture(random.randint(1, 5))

        if self.paralyzed:
            self.enemy.speed = 0

        if self.curtime > self.duration or self.enemy.health <= 0:
            if self.player.player_has_skill("Paralyzing") and self.paralyzed:
                self.enemy.speed = self.orig_speed
            self.kill()

        if self.curtime > self.damage_delay:
            self.damage_delay = self.curtime + 15
            self.enemy.on_take_damage(self.damage, True)

class Blade_Poison(arcade.Sprite):
    def _init_(self):
        self.enemy = None
        self.duration = 0
        self.damage = 0
        self.damage_delay = 0
        self.curtime = 0
        self.player = None
        self.paralyze = False
        self.orig_speed = 0

    def update(self):
        self.curtime += 1

        self.center_x = self.enemy.center_x
        self.center_y = self.enemy.center_y
        self.set_texture(random.randint(1, 5))

        if self.player.player_has_skill("Hebenon") and self.enemy.speed > 0:
            self.enemy.speed = self.orig_speed / 2

        if self.curtime > self.duration or self.enemy.health <= 0:
            if self.player.player_has_skill("Hebenon"):
                self.enemy.speed = self.orig_speed

            if self.player.player_has_skill("Necrotic Siphon") and self.enemy.health <= 0:
                amount = 25
                diff = self.player.mana_cap - self.player.mana
                if diff <= 25:
                    amount = 25 - (25 - diff)   # Prevents overflow
                self.player.mana += amount

            self.kill()

        if self.curtime > self.damage_delay:
            self.damage_delay = self.curtime + 25
            self.enemy.on_take_damage(self.damage, True)

class Cloud_Poison(arcade.Sprite):
    def _init_(self):
        self.enemy = None
        self.duration = 0
        self.damage = 0
        self.damage_delay = 0
        self.curtime = 0
        self.player = None
        self.bullet_list = []

    def update(self):
        self.curtime += 1

        self.center_x = self.enemy.center_x
        self.center_y = self.enemy.center_y
        self.set_texture(random.randint(1, 5))

        if self.enemy.health <= 0:
            if self.player.player_has_skill("Plague"):
                cloud = Cloud("images/status.png")
                cloud.center_x = self.enemy.center_x
                cloud.center_y = self.enemy.center_y

                size = 32

                if self.player.player_has_skill("Expansive"):
                    size = 48

                duration = 150
                cloud.duration = duration
                cloud.curtime = 0
                cloud.range = size
                cloud.hit_list = []
                cloud.player = self.player
                cloud.enemy_list = globalvars.enemy_list
                cloud.bullet_list = self.bullet_list
                cloud.damage_delay = 0

                for i in range(1, 6):
                    cloud.append_texture(arcade.load_texture("images/effects/poison_cloud/" + str(i) + ".png"))

                self.bullet_list.append(cloud)

        if self.curtime > self.duration or self.enemy.health <= 0:
            self.enemy.poisoned = None
            self.kill()

        if self.curtime > self.damage_delay:
            self.damage_delay = self.curtime + 20
            self.enemy.on_take_damage(self.damage, True)

class Cloud(arcade.Sprite):
    def _init_(self):
        self.duration = 0
        self.curtime = 0
        self.hit_list = []
        self.player = None
        self.range = 0
        self.bullet_list = []
        self.damage_delay = 0

    def update(self):
        self.curtime += 1

        self.set_texture(random.randint(1, 5))

        if self.curtime > self.duration:
            self.kill()

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.range ** 2:
                if self.curtime > self.damage_delay:
                    self.damage_delay = self.curtime + 10

                    damage = 3

                    if self.player.player_has_skill("Noxious"):
                        damage = 5

                    local_pre_x = enemy.center_x
                    local_pre_y = enemy.center_y
                    enemy.on_take_damage(damage, True)

                already_hit = False
                for item in self.hit_list:
                    if item == enemy:
                        already_hit = True

                if not already_hit:
                    duration = 200
                    if self.player.player_has_skill("Venomous"):
                        duration = 300

                    if enemy.poisoned is not None:
                        enemy.poisoned.duration = duration
                    else:
                        if self.player.player_has_skill("Caustic"):
                            self.player.ignite(enemy, 12)

                        poison = Cloud_Poison("images/status.png")
                        poison.enemy = enemy

                        duration = 200
                        if self.player.player_has_skill("Venomous"):
                            duration = 300

                        poison.duration = duration
                        poison.damage = 2
                        poison.damage_delay = 0
                        poison.curtime = 0
                        poison.center_x = -1000
                        poison.center_y = -1000
                        poison.player = self.player
                        poison.enemy_list = globalvars.enemy_list
                        poison.bullet_list = self.bullet_list

                        for i in range(1, 6):
                            poison.append_texture(arcade.load_texture("images/effects/poison/" + str(i) + ".png"))

                        self.bullet_list.append(poison)
                        self.hit_list.append(enemy)

                        enemy.poisoned = poison

class Lightning(arcade.Sprite):
    def _init_(self):
        self.player = None
        self.damage = 0
        self.hit_list = []

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.set_texture(random.randint(1, 4))

        if self.center_x > SCREEN_WIDTH + 32 or self.center_x < -32 or self.center_y > SCREEN_HEIGHT + 32 or self.center_y < -32:
            self.kill()

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 15 ** 2:
                enemy.on_take_damage(self.damage, True)
                globalvars.emit_sound("lightning_hit.ogg")
                self.hit_list.append(enemy)
                if self.player.mana < (self.player.mana_cap - 3) and self.player.player_has_skill("Energized"):
                    self.player.mana += 3

                if self.player.player_has_skill("Chain"):
                    if random.randint(1, 10) > 2 and len(globalvars.enemy_list) > 1:
                        local_enemy = "Error"
                        for i in range(len(globalvars.enemy_list)):
                            already_hit = False
                            for item in self.hit_list:
                                if globalvars.enemy_list[i] == item:
                                    already_hit = True

                            if not already_hit:
                                local_enemy = globalvars.enemy_list[i]
                                break

                        if local_enemy == "Error":
                            self.kill()
                        else:
                            self.center_x = local_enemy.center_x
                            self.center_y = local_enemy.center_y
                    else:
                        self.kill()
                else:
                    self.kill()


class Thunder(arcade.Sprite):
    def _init_(self):
        self.anim_timer = 0
        self.curtime = 0
        self.damage = 100
        self.radius = 48
        self.anim_track = 0
        self.bullet_list = []
        self.player = None

    def update(self):
        if self.curtime == 0:
            globalvars.emit_sound("thunderstrike.ogg")

        self.curtime += 1

        pattern = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 2, 1]

        if self.anim_track == 8 and self.anim_timer == self.curtime + 2:
            chance = random.randint(1, 20)
            for enemy in globalvars.enemy_list:
                y_pos = self.center_y - 42
                if (((self.center_x - enemy.center_x) ** 2) + ((y_pos - enemy.center_y) ** 2)) <= self.radius ** 2:
                    if self.player.player_has_skill("Fiery"):
                        self.player.ignite(enemy, 20)

                    damage = self.damage
                    if self.player.player_has_skill("Disintegrate") and chance == 7:
                        damage *= 5

                    enemy.on_take_damage(damage, True)

            effect = Effect("images/TD/effects/explosion/explosion_1.png")
            for i in range(1, 6):
                effect.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_" + str(i) + ".png"))

            if chance == 7 and self.player.player_has_skill("Disintegrate"):
                globalvars.emit_sound("disintegrate.ogg")
                effect = Effect("images/TD/effects/big_explosion/explosion_1.png")
                for i in range(1, 6):
                    effect.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_" + str(i) + ".png"))

            effect.anim_track = 0
            effect.curtime = 0
            effect.delay_logic = 0
            effect.center_x = self.center_x
            effect.center_y = self.center_y - 42
            effect.delay = 1
            self.bullet_list.append(effect)

        if self.anim_track == 11:
            if self.player.player_has_skill("Supercell") and random.randint(1, 5) == random.randint(1, 10):
                self.anim_track = 4

        if self.anim_track > len(pattern) - 1:
            self.kill()

        if self.curtime > self.anim_timer:
            self.anim_timer = self.curtime + 3
            self.set_texture(pattern[self.anim_track])
            self.anim_track += 1

class Orb(arcade.Sprite):
    def _init_(self):
        self.curtime = 0
        self.starting_speed = 0
        self.starting_change_x = 0
        self.starting_change_y = 0
        self.player = None
        self.damage = 0
        self.path_counter = 0
        self.anim_counter = 0

    def update(self):
        self.curtime += 1

        delay = 4
        if self.player.player_has_skill("Energetic"):
            delay = 2
        if self.curtime > delay:
            self.curtime = 0

        self.angle += random.randint(1, 10)

        self.anim_counter += 1
        if self.anim_counter > 20:
            self.anim_counter = 1
        self.set_texture(self.anim_counter)



        self.path_counter += 1
        if self.player.player_has_skill("Stabilized"):
            if self.path_counter > 100:
                self.path_counter = 0
                self.change_x += (random.random() / 2) * random.randint(-1, 1)
                self.change_y += (random.random() / 2) * random.randint(-1, 1)
        else:
            if self.path_counter > 50:
                self.path_counter = 0
                self.change_x += random.random() * random.randint(-1, 1)
                self.change_y += random.random() * random.randint(-1, 1)

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x > SCREEN_WIDTH + 32 or self.center_x < -32 or self.center_y > SCREEN_HEIGHT + 32 or self.center_y < -32:
            self.kill()

        if self.curtime == 0:
            for enemy in self.player.enemy_list:
                if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 48 ** 2:
                    globalvars.emit_sound("orb_hit_" + str(random.randint(1, 5)) + ".ogg")
                    enemy.on_take_damage(self.damage, True)

                    if self.player.player_has_skill("Quantum"):
                        if random.randint(1, 100) == 10:
                            globalvars.emit_sound("orb_warp.ogg")
                            enemy.node_tracker = 0

                        if random.randint(1, 7) == 3:
                            if len(self.player.enemy_list) > 1:
                                globalvars.emit_sound("orb_teleport_" + str(random.randint(1, 2)) + ".ogg")
                                random_enemy = random.choice(self.player.enemy_list)
                                if not random_enemy.invincible:
                                    self.center_x = random_enemy.center_x
                                    self.center_y = random_enemy.center_y

class Burden(arcade.Sprite):
    def _init_(self):
        self.player = None
        self.speed = 0
        self.explosion_radius = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.angle = random.randint(1, 360)

        if self.center_x > SCREEN_WIDTH + 32 or self.center_x < -32 or self.center_y > SCREEN_HEIGHT + 32 or self.center_y < -32:
            self.kill()

        for enemy in self.player.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= 32 ** 2:
                status = Burden_Status("images/status.png")
                status.center_x = -1000
                status.center_y = -1000
                status.curtime = 0

                duration = 250
                if self.player.player_has_skill("Enduring"):
                    duration = 500
                status.lifetime = duration

                slow = 0.5
                if self.player.player_has_skill("Slug"):
                    slow = 0.25

                if self.player.player_has_skill("Diminishing"):
                    slow = slow - (.05 * enemy.speed)
                    if slow < .05:
                        slow = .05

                if self.player.player_has_skill("Freezing"):
                    slow = 0

                status.slow = slow
                status.player = self.player
                status.enemy = enemy

                self.player.bullet_list.append(status)
                for enemyx in self.player.enemy_list:
                    if (((self.center_x - enemyx.center_x) ** 2) + ((self.center_y - enemyx.center_y) ** 2)) <= self.explosion_radius ** 2 and enemy != enemyx:
                        status = Burden_Status("images/status.png")
                        status.center_x = -1000
                        status.center_y = -1000
                        status.curtime = 0

                        duration = 250
                        if self.player.player_has_skill("Enduring"):
                            duration = 500
                        status.lifetime = duration

                        slow = 0.5
                        if self.player.player_has_skill("Slug"):
                            slow = 0.25

                        if self.player.player_has_skill("Diminishing"):
                            slow = slow - (.05 * enemyx.speed)
                            if slow < .05:
                                slow = .05

                        status.slow = slow
                        status.player = self.player
                        status.enemy = enemyx

                        self.player.bullet_list.append(status)
                self.kill()

class Burden_Status(arcade.Sprite):
    def _init_(self):
        self.curtime = 0
        self.lifetime = 0
        self.slow = 0
        self.player = None
        self.enemy = None

    def update(self):
        self.curtime += 1

        if self.curtime > self.lifetime:
            self.enemy.speed = self.enemy.set_speed
            self.kill()
        else:
            self.enemy.speed = self.enemy.set_speed * self.slow


class MagicMissile(arcade.Sprite):
    def _init_(self):
        self.curtime = 0
        self.hit_list = []
        self.player = None
        self.range = 0
        self.bullet_list = []
        self.damage = 0
        self.drag = 10
        self.img_scale = 0
        self.size = 0

    def update(self):
        self.curtime += 1

        self.center_x += ((self.player.current_mouse_x - self.center_x) / self.drag)
        self.center_y += ((self.player.current_mouse_y - self.center_y) / self.drag)

        self.set_texture(random.randint(1, 5))

        local_exploded = False
        dir_hit_enemy = None

        nearby_enemies = self.player.getNearbyEnemies(self, self.range)

        for enemy in nearby_enemies:
            if not local_exploded:
                local_exploded = True
                dir_hit_enemy = enemy

                enemy.on_take_damage(self.damage, True)

                if self.player.player_has_skill("Incendiary"):
                    enemy.ignite = 2
                    ignite = Flame("images/effects/flame/1.png")
                    for i in range(1, 12):
                        ignite.append_texture(arcade.load_texture("images/effects/flame/" + str(i) + ".png"))
                    ignite.center_x = enemy.center_x
                    ignite.center_y = enemy.center_y
                    ignite.enemy = enemy
                    ignite.enemy_list = globalvars.enemy_list
                    ignite.player = self.player
                    ignite.bullet_list = self.bullet_list
                    ignite.lifetime = self.size / 16
                    ignite.anim_timer = 0
                    ignite.anim_track = 0
                    self.bullet_list.append(ignite)

                self.player.active_mm = None
                globalvars.emit_sound("mm_hit.ogg")

                local_scale = self.img_scale

                effect = MagicMissileEffect("images/status.png")
                effect.append_texture(arcade.load_texture("images/effects/mm_explode/1.png", scale=local_scale))
                effect.append_texture(arcade.load_texture("images/effects/mm_explode/" + str(random.randint(2, 5)) + ".png", scale=local_scale))
                effect.img_track = 1
                effect.pos_x = self.center_x
                effect.pos_y = self.center_y
                effect.curtime = 0
                effect.delay = 2
                effect.delay_track = 0
                self.bullet_list.append(effect)

        if local_exploded:
            if self.player.player_has_skill("Blast"):
                nearby_enemies = self.player.getNearbyEnemies(self, self.range * 3)

                for enemy in nearby_enemies:
                    if enemy != dir_hit_enemy:
                        enemy.on_take_damage(int(self.damage / 2), True)

            self.kill()

class MagicMissileEffect(arcade.Sprite):
    def _init_(self):
        self.img_track = 0
        self.pos_x = 0
        self.pos_y = 0
        self.curtime = 0
        self.delay = 0
        self.delay_track = 0

    def update(self):
        self.center_x = self.pos_x
        self.center_y = self.pos_y
        self.curtime += 1

        if self.curtime > self.delay_track:
            self.delay_track += self.delay

            if self.img_track == 3:
                self.kill()
            else:
                self.set_texture(self.img_track)
                self.img_track += 1

class Starblast(arcade.Sprite):
    def _init_(self):
        self.curtime = 0
        self.hit_list = []
        self.player = None
        self.range = 0
        self.bullet_list = []
        self.damage = 0
        self.img_scale = 0
        self.size = 0
        self.anim_pattern = 0
        self.anim_track = 0

    def update(self):
        if self.anim_track >= len(self.anim_pattern):
            self.kill()
        else:
            self.set_texture(self.anim_track + 1)

            if self.curtime > self.anim_pattern[self.anim_track]:
                if self.anim_track == 5:
                    self.explode()

                self.curtime = 0
                self.anim_track += 1
            else:
                self.curtime += 1

    def explode(self):
        if self.player.player_has_skill("Gamma Rays"):

            ray_range = math.floor(math.pow(self.damage, (1/4))) - 2

            if ray_range < 0:
                ray_range = 0

            if random.random() > .5:
                ray_range += 1

            for i in range(ray_range):
                damage = 15
                speed = 10
                if self.player.player_has_skill("Hyper"):
                    damage = 25
                    speed = 15

                if self.player.surged:
                    damage = round(damage * 1.5)

                random_xdir = random.random()
                random_ydir = random.random()

                if random.random() > .5:
                    random_xdir *= -1

                if random.random() > .5:
                    random_ydir *= -1

                beam = Beam("images/TD/entities/projectile/starblast_beam.png")
                beam.center_x = self.center_x
                beam.center_y = self.center_y
                beam.speed = speed * 2
                beam.change_x = random_xdir * beam.speed
                beam.change_y = random_ydir * beam.speed
                beam.enemy_list = globalvars.enemy_list
                beam.damage = damage * 2
                beam.penetrate = 5
                beam.hit_list = []
                beam.player = self.player

                beam.angle = math.degrees(math.atan2(random_ydir, random_xdir))

                self.bullet_list.append(beam)

        nearby_enemies = self.player.getNearbyEnemies(self, self.range)

        for enemy in nearby_enemies:
            enemy.on_take_damage(self.damage, True)

            if self.player.player_has_skill("Radioactive"):
                poison = Cloud_Poison("images/status.png")
                poison.enemy = enemy

                duration = 150 + int(math.sqrt(self.damage))

                poison.duration = duration
                poison.damage = int(math.ceil(math.pow(self.damage, (1/4))))
                poison.damage_delay = 0
                poison.curtime = 0
                poison.center_x = -1000
                poison.center_y = -1000
                poison.player = self.player

                for i in range(1, 6):
                    poison.append_texture(arcade.load_texture("images/effects/poison/" + str(i) + ".png"))

                self.bullet_list.append(poison)
                self.hit_list.append(enemy)

        if self.player.player_has_skill("Singularity"):
            nearby_enemies = self.player.getNearbyEnemies(self, int(self.range / 4))

            for enemy in nearby_enemies:
                enemy.on_take_damage(int(self.damage * 1.1), True)