import arcade
import math
import globalvars
import random
import player

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 768


class Skeleton(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.health = 100
        self.speed = 1
        self.set_speed = 1
        self.ng_x = [0]
        self.ng_y = [0]
        self.cur_tile_x = 0
        self.cur_tile_y = 0
        self.node_tracker = 1
        self.ticks_until_tile = 0
        self.node_direction = None
        self.floater_timer = []
        self.worth = 0
        self.fire_weakness = 1
        self.invincible = False
        self.death_floaters = []

        self.health_gate = 0
        self.old_health = 0

        self.tiles = 0
        self.curtime = 0
        self.shield = 0
        self.ignite = 0
        self.ignite_timer = 0

        self.poisoned = None

    def spawn_floater(self, damage, death_floater):
        if self.cur_floater is not None:
            damage = self.cur_floater.damage + damage
        else:
            self.floater_randpos_x = random.randint(-16, 16)
            self.floater_randpos_y = random.randint(-16, 16)

        color = (0, 0, 0)

        if damage <= 0:
            color = (255, 255, 0)
        else:
            r = (damage / 1000) * 255
            if r > 255:
                r = 255
            if r < 0:
                r = 0

            b = (1000 / damage) * 10
            if b > 255:
                b = 255
            if b < 0:
                b = 0
            color = (int(r), 0, int(b))

        size = 9 + math.log1p(damage)
        if size < 10:
            size = 10

        floater = arcade.create_text(str(damage), color, size)
        floater.x_pos = self.center_x + self.floater_randpos_x
        floater.y_pos = self.center_y + self.floater_randpos_y
        floater.die_time = 3
        floater.damage = damage
        self.cur_floater = floater

        if death_floater:
            self.death_floaters.append(floater)

    def give_exp(self, damage, attacker_is_player):
        exp = damage / globalvars.dv_xpscale[globalvars.difficulty]

        if attacker_is_player:
            exp = exp * 2
        else:
            exp = exp / 2

        globalvars.player.give_exp(exp)

    def process_damage(self, damage, attacker_is_player):
        damage_taken = damage

        if damage_taken > self.health:
            damage_taken = self.health

        self.give_exp(damage_taken, attacker_is_player)

        self.spawn_floater(damage, self.health - damage <= 0)

        globalvars.stats_total_dmg += damage_taken
        if attacker_is_player:
            globalvars.stats_player_dmg += damage_taken

        self.health -= damage

        if self.health <= 0:
            globalvars.stats_kills += 1
            self.give_money()
            globalvars.emit_sound("skeleton_die.ogg")

            # globalvars.enemy_list.remove(self)

            # self.remove_from_sprite_lists()

            self.kill()

    def on_take_damage(self, damage, attacker_is_player):
        self.process_damage(damage, attacker_is_player)

    def give_money(self):
        amount = self.worth

        if globalvars.player.player_has_skill("Lucrative"):
            amount = int(self.worth * 1.25)

            if globalvars.player.player_has_skill("Vitality"):
                amount = int(self.worth * 1.25)

        globalvars.money += amount
        globalvars.stats_money += amount

    def ignite_logic(self):
        if self.ignite > 0:
            self.ignite_timer += 1
            if self.ignite_timer > 20:
                self.ignite_timer = 0
                self.ignite -= 1
                self.on_take_damage(5, True)

    def update(self):
        # Fire logic
        self.ignite_logic()

        # Enemy Movement and Path-Finding
        self.move()

        # Use features of update function without overriding it
        self.tick()

    def move(self):
        if self.ticks_until_tile == 0:
            self.ticks_until_tile = 48
            if len(self.ng_x) > self.node_tracker:
                self.center_x = (48 * (self.ng_x[self.node_tracker])) - 24
                self.center_y = (48 * (self.ng_y[self.node_tracker])) - 24
                self.node_tracker += 1
            else:
                globalvars.emit_sound("hurt.ogg")
                globalvars.population -= 1
                self.kill()

        self.ticks_until_tile -= self.speed
        if self.ticks_until_tile < 0:
            self.ticks_until_tile = 0

        if self.ticks_until_tile > 0:
            local_direction = "right"
            if len(self.ng_x) > self.node_tracker and self.node_tracker > 0:
                last_pos_x = self.ng_x[self.node_tracker - 1]
                last_pos_y = self.ng_y[self.node_tracker - 1]
                pos_x = self.ng_x[self.node_tracker]
                pos_y = self.ng_y[self.node_tracker]
                if last_pos_x < pos_x:
                    local_direction = "right"
                elif last_pos_x > pos_x:
                    local_direction = "left"
                elif last_pos_y < pos_y:
                    local_direction = "up"
                elif last_pos_y > pos_y:
                    local_direction = "down"

            if local_direction == "up":
                self.center_y += self.speed
            elif local_direction == "down":
                self.center_y -= self.speed

            if local_direction == "right":
                self.center_x += self.speed
            elif local_direction == "left":
                self.center_x -= self.speed

    def tick(self):
        return None


class Hyperskeleton(Skeleton):
    def on_take_damage(self, damage, attacker_is_player):
        if self.invincible:
            self.process_damage(0, attacker_is_player)
        else:
            self.process_damage(damage, attacker_is_player)

    def tick(self):
        if self.invincible:
            self.set_texture(random.randint(0, 5))
        else:
            self.set_texture(8)

        if self.node_tracker > self.tiles:
            self.invincible = False
            self.speed = 1
            self.set_speed = 1


class Raptor(Skeleton):
    def tick(self):
        self.curtime += 1
        if self.curtime > 60:
            self.curtime = 0
            self.speed += .2


class Lich(Skeleton):
    def on_take_damage(self, damage, attacker_is_player):
        damage_taken = damage

        if damage_taken > self.health:
            damage_taken = self.health

        self.give_exp(damage_taken, attacker_is_player)

        self.spawn_floater(damage, self.health - damage <= 0)

        if self.shield > 0:
            self.set_texture(6)
        else:
            self.set_texture(7)

        globalvars.stats_total_dmg += damage_taken
        if attacker_is_player:
            globalvars.stats_player_dmg += damage_taken

        self.health -= damage
        self.shield -= damage
        if self.shield > damage:
            self.health += damage
        elif self.shield > 0:
            self.health += self.shield
        if self.health <= 0:
            globalvars.stats_kills += 1
            self.give_money()
            self.kill()


    def tick(self):
        self.curtime += 1
        self.shield += 2

        if self.shield > 0:
            self.set_texture(random.randint(1, 5))
            self.speed = 1
        else:
            self.set_texture(0)
            self.speed = 3


class Skeleton_Lord(Skeleton):
    def on_take_damage(self, damage, attacker_is_player):
        if damage > self.health_gate:
            damage = self.health_gate

        self.process_damage(damage, attacker_is_player)


    def tick(self):
        self.curtime += 1

        if self.health < self.old_health - self.health_gate:
            self.health = self.old_health - self.health_gate
            self.set_texture(1)
            self.anim_timer = self.curtime + 5
        self.old_health = self.health

        if self.curtime > self.anim_timer:
            self.set_texture(0)



class Tower(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.attack_radius = 0
        self.bullet_list = None
        self.damage = 0
        self.fire_rate = 0

        self.can_shoot = True
        self.delay_wait = 0
        self.curtime = 0
        self.animation_wait = 0

        self.uses = 0
        self.shots = 0
        self.reloading = False
        self.reload_delay = 0
        self.last_shot_delay = 0
        self.x_origin = 0
        self.y_origin = 0
        self.ng_x = None
        self.ng_y = None

        self.price = 0

        self.detect_delay = 0 # You don't need to check for enemies every frame.
        # This new system needs to be applied to the wizard, the horse, and the rock.

    def update(self):
        self.curtime += 1

        self.tick()
        self.check_shoot()
        self.animation()

        self.detect_enemy()

    def tick(self):
        return None

    def check_shoot(self):
        if not self.can_shoot and float(self.curtime) > self.delay_wait:
            self.can_shoot = True

    def animation(self):
        if self.animation_wait > self.curtime:
            self.set_texture(1)
        else:
            self.set_texture(0)

    def random_variance(self, value, perc):
        scale = (perc / 100) * value
        variance = scale * random.random()

        if random.random() > 0.5:
            variance *= -1

        return value + variance

    def get_nearest_enemy(self, radius):
        for enemy in globalvars.enemy_list:
            hyper_check = enemy.name == "hyperskeleton" and enemy.invincible
            bound_check = (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= radius ** 2

            if enemy is not None and not hyper_check and bound_check:
                return enemy

        return None

    def detect_enemy(self):
        if float(self.curtime) > self.detect_delay:
            self.detect_delay = self.curtime + 0.25

            nearest_enemy = self.get_nearest_enemy(self.attack_radius)

            if self.can_shoot and nearest_enemy is not None:
                self.attack(nearest_enemy)

    def shoot_bullet(self, enemy, image, velocity, tower_angle, bullet_angle, radius, animation_timer):
        globalvars.emit_sound("stone_throw.ogg")
        bullet = Projectile(image)
        start_x = self.center_x
        start_y = self.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        bullet.curtime = 0
        bullet.check_delay = 0
        local_speed = velocity
        bullet.delay_speed = 8 / local_speed

        dest_x = enemy.center_x
        dest_y = enemy.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle) + tower_angle

        angle = self.random_variance(angle, 2)

        bullet.angle = math.degrees(angle) + bullet_angle

        bullet.change_x = math.cos(angle) * local_speed
        bullet.change_y = math.sin(angle) * local_speed

        bullet.animation_timer = animation_timer

        bullet.enemy_list = globalvars.enemy_list
        bullet.damage = self.damage
        bullet.attack_radius = radius
        self.bullet_list.append(bullet)

    def attack(self, enemy):
        self.animation_wait = self.curtime + 10
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
        self.shoot_bullet(enemy, "images/TD/entities/projectile/rock.png", 10, -90, 0, 25, 0)


class Tower_Stone_Trap(Tower):
    def animation(self):
        return None

    def check_shoot(self):
        if not self.can_shoot and self.curtime > self.delay_wait:
            self.kill()

    def attack(self, enemy):
        globalvars.emit_sound("rock_trap.ogg")
        self.set_texture(1)
        self.can_shoot = False
        self.delay_wait = self.curtime + 100
        enemy.on_take_damage(self.damage, False)


class Tower_Stone_Person_1(Tower):
    def animation(self):
        if self.curtime > self.animation_wait:
            self.set_texture(0)

        if self.animation_wait - 5 > self.curtime:
            self.set_texture(1)
        elif self.animation_wait > self.curtime:
            self.set_texture(2)

    def attack(self, enemy):
        self.animation_wait = self.curtime + 10
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
        x_diff = enemy.center_x - self.center_x
        y_diff = enemy.center_y - self.center_y
        angle = math.atan2(y_diff, x_diff)
        self.angle = math.degrees(angle) - 90
        enemy.on_take_damage(self.damage, False)
        globalvars.emit_sound("club_hit.ogg")


class Tower_Stone_Person_2(Tower):
    print("Loading...")


class Tower_Stone_Person_3(Tower):
    def animation(self):
        return None

    def attack(self, enemy):
        globalvars.emit_sound("blowgun.ogg")
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
        self.shoot_bullet(enemy, "images/TD/entities/projectile/blowdart.png", 20, -90, -90, 30, 0)


class Tower_Stone_Boulder(Tower):
    def animation(self):
        return None

    def attack(self, enemy):
        return None

    def check_shoot(self):
        return None

    def tick(self):
        if self.can_shoot:
            self.center_x += 2
            self.angle -= 3
        else:
            self.center_x -= 2
            self.angle += 3

        if self.center_x > (SCREEN_WIDTH + 64) and self.can_shoot:
            self.can_shoot = False
        if self.center_x < -64 and not self.can_shoot:
            self.can_shoot = True

        if self.center_x > (SCREEN_WIDTH + 64) or self.center_x < -64:
            self.delay_wait = self.curtime + 100

        if self.delay_wait > self.curtime:
            self.center_y = -1900
        elif self.delay_wait != 0:
            self.delay_wait = 0
            self.center_y = 48 * random.randint(2, 15)
            if self.can_shoot:
                self.center_x = -64
            else:
                self.center_x = SCREEN_WIDTH + 64

    def detect_enemy(self):
        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2:
                enemy.on_take_damage(self.damage, False)


class Tower_Stone_Money(Tower):
    def detect_enemy(self):
        return None

    def attack(self, enemy):
        return None

    def check_shoot(self):
        return None

    def animation(self):
        if self.curtime > 25:
            self.set_texture(1)
        else:
            self.set_texture(0)

    def tick(self):
        if self.curtime > 30:
            globalvars.emit_sound("mine.ogg")
            self.curtime = random.randint(0, 2)
            globalvars.money += self.damage
            globalvars.stats_money += self.damage


class Tower_Stone_Super(Tower):
    def animation(self):
        if self.animation_wait - 5 > self.curtime:
            self.set_texture(1)
        elif self.animation_wait > self.curtime:
            self.set_texture(2)
        else:
            self.set_texture(0)

    def attack(self, enemy):
        globalvars.emit_sound("atlatle.ogg")
        self.animation_wait = self.curtime + 10
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
        self.shoot_bullet(enemy, "images/TD/entities/projectile/atlatl_dart.png", 15, -90, -90, 25, 0)


# Medieval


class Tower_Medieval_Trap(Tower):
    def animation(self):
        if self.animation_wait - 8 > self.curtime:
            self.set_texture(1)
        elif self.animation_wait - 4 > self.curtime:
            self.set_texture(2)
        elif self.animation_wait > self.curtime:
            self.set_texture(3)
        elif self.animation_wait + 4 > self.curtime:
            self.set_texture(2)
        elif self.animation_wait + 8 > self.curtime:
            self.set_texture(1)
        elif self.animation_wait + 12 > self.curtime:
            self.set_texture(0)
        elif self.animation_wait + 16 > self.curtime:
            if self.uses >= 4:
                self.kill()

    def attack(self, enemy):
        globalvars.emit_sound("knife_hit.ogg")
        self.delay_wait = self.curtime + (self.fire_rate * 60)
        self.animation_wait = self.curtime + 12
        self.can_shoot = False
        enemy.on_take_damage(self.damage, False)
        self.uses += 1


class Tower_Medieval_Person_1(Tower):
    def animation(self):
        if self.curtime > self.animation_wait:
            self.set_texture(0)

        if self.animation_wait > self.curtime:
            self.set_texture(1)

    def attack(self, enemy):
        globalvars.emit_sound("knife_hit.ogg")
        self.animation_wait = self.curtime + 5
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.fire_rate * 60) + random.randint(1, 3)
        x_diff = enemy.center_x - self.center_x
        y_diff = enemy.center_y - self.center_y
        angle = math.atan2(y_diff, x_diff)
        self.angle = math.degrees(angle) - 90
        enemy.on_take_damage(self.damage, False)


class Tower_Medieval_Person_2(Tower):
    def animation(self):
        if self.animation_wait > self.curtime:
            self.set_texture(1)
        else:
            self.set_texture(0)

    def attack(self, enemy):
        globalvars.emit_sound("stone_throw.ogg")
        self.animation_wait = self.curtime + 15
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.fire_rate * 60) + random.randint(1, 3)
        self.shoot_bullet(enemy, "images/TD/entities/projectile/javelin.png", 10, -90, -90, 25, 0)


class Tower_Medieval_Person_3(Tower):
    def animation(self):
        if self.curtime > self.animation_wait - 30:
            self.set_texture(2)
        if self.curtime > self.animation_wait - 20:
            self.set_texture(3)
        if self.curtime > self.animation_wait - 10:
            self.set_texture(4)
        if self.curtime > self.animation_wait:
            self.set_texture(0)

    def attack(self, enemy):
        globalvars.emit_sound("bow_shoot.ogg")
        self.animation_wait = self.curtime + 40
        self.set_texture(1)
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.fire_rate * 60) + random.randint(1, 3)
        self.shoot_bullet(enemy, "images/TD/entities/projectile/arrow.png", 20, -90, -90, 25, 0)


class Tower_Medieval_Special(Tower):
    def tick(self):
        self.curtime += 1
        self.animation_wait += 1

        if self.center_x > SCREEN_WIDTH or self.center_x < 0:
            self.can_shoot = not self.can_shoot

        if self.can_shoot:
            self.center_x += 2
            if self.animation_wait > 40:
                self.animation_wait = 0
                self.set_texture(0)
            elif self.animation_wait > 30:
                self.set_texture(3)
            elif self.animation_wait > 20:
                self.set_texture(2)
            elif self.animation_wait > 10:
                self.set_texture(1)
        else:
            self.center_x -= 2
            if self.animation_wait > 40:
                self.animation_wait = 0
                self.set_texture(4)
            elif self.animation_wait > 30:
                self.set_texture(7)
            elif self.animation_wait > 20:
                self.set_texture(6)
            elif self.animation_wait > 10:
                self.set_texture(5)

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2:
                enemy.on_take_damage(self.damage, False)

    def detect_enemy(self):
        return None

    def attack(self, enemy):
        return None

    def animation(self):
        return None

    def check_shoot(self):
        return None


class Tower_Medieval_Money(Tower):
    def tick(self):
        if self.curtime > 30:
            self.curtime = 0
            globalvars.money += self.damage
            globalvars.stats_money += self.damage

    def animation(self):
        return None

    def detect_enemy(self):
        return None


class Tower_Medieval_Super(Tower):
    def animation(self):
        return None

    def attack(self, enemy):
        globalvars.emit_sound("lightning_cast.ogg")
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
        bullet = Projectile("images/TD/entities/towers/medieval/shock/shock_1.png")
        bullet.append_texture(
            arcade.load_texture("images/TD/entities/towers/medieval/shock/shock_2.png"))
        bullet.append_texture(
            arcade.load_texture("images/TD/entities/towers/medieval/shock/shock_3.png"))
        bullet.append_texture(
            arcade.load_texture("images/TD/entities/towers/medieval/shock/shock_4.png"))
        start_x = self.center_x
        start_y = self.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        bullet.curtime = 0
        bullet.check_delay = 0
        local_speed = 10
        bullet.delay_speed = 8 / local_speed

        dest_x = enemy.center_x
        dest_y = enemy.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle) - 90

        bullet.angle = math.degrees(angle)

        bullet.animation_timer = 0

        bullet.change_x = math.cos(angle) * local_speed
        bullet.change_y = math.sin(angle) * local_speed

        bullet.enemy_list = globalvars.enemy_list
        bullet.damage = self.damage
        bullet.attack_radius = 25
        self.bullet_list.append(bullet)


    def detect_enemy(self):
        for enemy in globalvars.enemy_list:

            hyper_check = False
            if enemy.name == "hyperskeleton":
                if enemy.invincible == True:
                    hyper_check = True

            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2 and not hyper_check:
                self.set_texture(0)
                self.animation_wait = self.curtime + 25
                if self.can_shoot:
                    self.attack(enemy)
            else:
                if self.curtime > self.animation_wait:
                    self.set_texture(random.randint(2, 11))


# Industrial


class Tower_Industrial_Trap(Tower):
    def animation(self):
        return None

    def detect_enemy(self):
        return None

    def check_shoot(self):
        return None

    def update(self):
        self.curtime += 1
        self.animation_wait += 1
        if not self.can_shoot:
            if self.curtime > 12:
                self.kill()

        if self.animation_wait > 10 and self.can_shoot:
            self.animation_wait = 0

        if self.animation_wait > 5 and self.can_shoot:
            self.set_texture(1)
        elif self.can_shoot and self.uses == 0:
            self.set_texture(0)

        if self.curtime > self.uses and self.uses != 0:
            self.delay_wait = 1

        for detect in globalvars.enemy_list:
            if (((self.center_x - detect.center_x) ** 2) + ((self.center_y - detect.center_y) ** 2)) <= self.attack_radius ** 2 and self.uses == 0:
                self.uses = self.curtime + 20
                self.set_texture(1)

        if self.delay_wait == 1:
            for enemy in globalvars.enemy_list:
                if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2:
                    enemy.on_take_damage(self.damage, False)
                    if self.can_shoot:
                        self.can_shoot = False
                        self.curtime = 0
                        globalvars.emit_sound("small_explosion.ogg")
                        explosion = MineExplosion("images/TD/effects/explosion/explosion_1.png")
                        explosion.curtime = 0
                        explosion.center_x = self.center_x
                        explosion.center_y = self.center_y
                        explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_1.png"))
                        explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_2.png"))
                        explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_3.png"))
                        explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_4.png"))
                        explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_5.png"))
                        explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_6.png"))
                        self.bullet_list.append(explosion)


class Tower_Industrial_Person_1(Tower):
    def animation(self):
        if self.curtime > self.last_shot_delay and self.last_shot_delay != 0 and self.shots < 6:
            self.last_shot_delay = 0
            self.reloading = True
            self.can_shoot = False

        if self.shots <= 0:
            self.can_shoot = False
            self.reloading = True

        if self.reloading:
            self.reload_delay += 1
            if self.reload_delay > 10:
                self.set_texture(4)
            else:
                self.set_texture(3)
            if self.reload_delay > 20:
                self.reload_delay = 0
                self.shots += 1
                globalvars.emit_sound("shotgun_shell.ogg")

        if self.reloading and self.shots == 6:
            self.reloading = False
            self.can_shoot = False
            self.set_texture(0)
            self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)

        if self.curtime == self.animation_wait and not self.reloading:
            self.set_texture(2)
            # globalvars.emit_sound("shotgun_pump.ogg")
        elif self.curtime == self.animation_wait + 10 and not self.reloading:
            self.set_texture(0)

    def attack(self, enemy):
        if not self.reloading:
            self.set_texture(1)
            self.animation_wait = self.curtime + 20
            self.can_shoot = False
            self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
            self.last_shot_delay = self.curtime + random.randint(90, 110)

            self.shots -= 1

            start_x = self.center_x
            start_y = self.center_y

            dest_x = enemy.center_x
            dest_y = enemy.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.angle = math.degrees(angle)

            globalvars.emit_sound("shotgun_fire.ogg")

            local_speed = 15
            for unused in range(12):
                adj_angle = angle + (random.randint(-10, 10) / 100)

                bullet = Projectile("images/TD/entities/projectile/bullet.png")
                bullet.center_x = start_x
                bullet.center_y = start_y
                bullet.angle = math.degrees(adj_angle)
                bullet.change_x = math.cos(adj_angle) * local_speed
                bullet.change_y = math.sin(adj_angle) * local_speed
                bullet.animation_timer = 0
                bullet.enemy_list = globalvars.enemy_list
                bullet.damage = self.damage
                bullet.attack_radius = 25
                bullet.curtime = 0
                bullet.check_delay = 0
                bullet.delay_speed = 8 / local_speed
                self.bullet_list.append(bullet)


class Tower_Industrial_Person_2(Tower):
    def animation(self):
        if self.curtime > self.last_shot_delay and self.last_shot_delay != 0 and self.shots < 30:
            self.last_shot_delay = 0
            self.reloading = True
            self.can_shoot = False

        if self.shots <= 0:
            self.can_shoot = False
            self.reloading = True

        if self.reloading:
            self.reload_delay += 1
            if self.reload_delay == 1:
                globalvars.emit_sound("ar_reload.ogg")
            elif self.reload_delay > 40:
                self.set_texture(0)
                self.reloading = False
                self.reload_delay = 0
                self.shots = 30
                self.delay_wait = self.curtime + self.random_variance(30, 5)
            elif self.reload_delay > 30:
                self.set_texture(2)
            elif self.reload_delay > 20:
                self.set_texture(3)
            elif self.reload_delay > 10:
                self.set_texture(2)

        if not self.reloading and self.curtime > self.animation_wait:
            self.set_texture(0)

    def attack(self, enemy):
        if not self.reloading:
            self.set_texture(1)
            self.animation_wait = self.curtime + 5
            self.can_shoot = False
            self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
            self.last_shot_delay = self.curtime + random.randint(90, 110)

            self.shots -= 1
            start_x = self.center_x + (math.sin(self.angle) * 10)
            start_y = self.center_y - (math.cos(self.angle) * 10)

            dest_x = enemy.center_x
            dest_y = enemy.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.angle = math.degrees(angle)

            local_speed = 15
            adj_angle = angle + (random.randint(-5, 5) / 100)

            globalvars.emit_sound("ar_fire.ogg")

            bullet = Projectile("images/TD/entities/projectile/bullet.png")
            bullet.center_x = start_x
            bullet.center_y = start_y
            bullet.angle = math.degrees(adj_angle)
            bullet.change_x = math.cos(adj_angle) * local_speed
            bullet.change_y = math.sin(adj_angle) * local_speed
            bullet.animation_timer = 0
            bullet.enemy_list = globalvars.enemy_list
            bullet.damage = self.damage
            bullet.attack_radius = 25
            bullet.curtime = 0
            bullet.check_delay = 0
            bullet.delay_speed = 8 / local_speed
            self.bullet_list.append(bullet)


class Tower_Industrial_Person_3(Tower):
    def animation(self):
        if self.curtime > self.last_shot_delay and self.last_shot_delay != 0 and self.shots < 1:
            self.last_shot_delay = 0
            self.reloading = True
            self.can_shoot = False

        if self.shots <= 0:
            self.can_shoot = False
            self.reloading = True

        if self.reloading:
            self.reload_delay += 1
            if self.reload_delay > 70:
                self.set_texture(0)
                self.reloading = False
                self.reload_delay = 0
                self.shots = 1
                self.delay_wait = self.curtime + self.random_variance(300, 5)
            elif self.reload_delay > 60:
                self.set_texture(2)
            elif self.reload_delay > 50:
                self.set_texture(3)
            elif self.reload_delay > 10:
                self.set_texture(2)

        if not self.reloading and self.curtime > self.animation_wait:
            self.set_texture(0)

    def detect_enemy(self):
        # Shoot the highest health enemy on the map
        highest_health = 0
        target = None
        for enemy in globalvars.enemy_list:
            hyper_check = False
            if enemy.name == "hyperskeleton":
                if enemy.invincible:
                    hyper_check = True

            if enemy.health > highest_health and not hyper_check:
                highest_health = enemy.health
                target = enemy

        if target is not None and self.can_shoot:
            self.attack(target)


    def attack(self, enemy):
        if not self.reloading:
            self.set_texture(1)
            self.animation_wait = self.curtime + 5
            self.can_shoot = False
            self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)
            self.last_shot_delay = self.curtime + random.randint(350, 400)

            self.shots -= 1
            start_x = self.center_x + (math.sin(self.angle) * 10)
            start_y = self.center_y - (math.cos(self.angle) * 10)

            dest_x = enemy.center_x
            dest_y = enemy.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.angle = math.degrees(angle)

            local_speed = 75
            adj_angle = angle

            globalvars.emit_sound("sniper_shot.ogg")

            bullet = Projectile("images/TD/entities/projectile/bullet.png")
            bullet.center_x = start_x
            bullet.center_y = start_y
            bullet.angle = math.degrees(adj_angle)
            bullet.change_x = math.cos(adj_angle) * local_speed
            bullet.change_y = math.sin(adj_angle) * local_speed
            bullet.animation_timer = 0
            bullet.enemy_list = globalvars.enemy_list
            bullet.damage = self.damage
            bullet.attack_radius = 42
            bullet.curtime = 0
            bullet.check_delay = 0
            bullet.delay_speed = 8 / local_speed
            self.bullet_list.append(bullet)


class Tower_Industrial_Money(Tower):
    def check_shoot(self):
        return None

    def detect_enemy(self):
        return None

    def update(self):
        self.curtime += 1

        self.delay_wait += 1
        if self.delay_wait > 10:
            self.delay_wait = 0
            if self.animation_wait > 1:
                self.can_shoot = False
            if self.animation_wait < 1:
                self.can_shoot = True
            if self.can_shoot:
                self.animation_wait += 1
            else:
                self.animation_wait -= 1

        self.set_texture(self.animation_wait)

        if self.curtime > 30:
            self.curtime = 0
            globalvars.money += self.damage
            globalvars.stats_money += self.damage


class Tower_Industrial_Special(Tower):
    def check_shoot(self):
        return None

    def detect_enemy(self):
        return None

    def update(self):
        self.curtime += 1

        time = self.curtime / 100
        scale = 2 / (3 - math.cos(2 * time))
        self.center_x = ((scale * math.cos(time)) * 300) + self.x_origin
        self.center_y = (((scale * math.sin(time * 2)) / 2) * 300) + self.y_origin

        self.angle = (math.sin(time) * 135)

        local_current_tile_x = int((self.center_x + 48) / 48)
        local_current_tile_y = int((self.center_y + 48) / 48)

        if self.animation_wait > 0:
            self.animation_wait -= 1

        for check in range(len(self.ng_x)):
            if local_current_tile_x == self.ng_x[check] and local_current_tile_y == self.ng_y[check]:
                if self.animation_wait == 0:
                    self.animation_wait = 10
                    globalvars.emit_sound("mine_explosion.ogg")
                    explosion = BombExplosion("images/TD/effects/explosion/explosion_1.png")
                    explosion.curtime = 0
                    explosion.center_x = self.center_x
                    explosion.center_y = self.center_y
                    explosion.damage = self.damage
                    explosion.radius = self.attack_radius
                    explosion.exploded = False
                    explosion.enemy_list = globalvars.enemy_list
                    explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_1.png"))
                    explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_2.png"))
                    explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_3.png"))
                    explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_4.png"))
                    explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_5.png"))
                    explosion.append_texture(arcade.load_texture("images/TD/effects/explosion/explosion_6.png"))
                    self.bullet_list.append(explosion)


class Tower_Industrial_Super_Base(Tower):
    def animation(self):
        return None

    def attack(self, enemy):
        self.animation_wait = self.curtime + 10
        self.can_shoot = False
        self.delay_wait = self.curtime + self.random_variance(3, 5)

        globalvars.emit_sound("tank_gun.ogg")

        bullet = Projectile("images/TD/entities/projectile/bullet.png")
        start_x = self.center_x
        start_y = self.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        local_speed = 25
        bullet.delay_speed = 8 / local_speed

        dest_x = enemy.center_x
        dest_y = enemy.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        angle = self.random_variance(angle, 2)

        bullet.angle = math.degrees(angle)

        bullet.animation_timer = 0

        bullet.change_x = math.cos(angle) * local_speed
        bullet.change_y = math.sin(angle) * local_speed
        bullet.curtime = 0
        bullet.check_delay = 0

        bullet.enemy_list = globalvars.enemy_list
        bullet.damage = 25
        bullet.attack_radius = 25
        self.bullet_list.append(bullet)


class Tower_Industrial_Super(Tower):
    def animation(self):
        return None

    def attack(self, enemy):
        self.animation_wait = self.curtime + 10
        self.can_shoot = False
        self.delay_wait = self.curtime + (self.random_variance(self.fire_rate, 5) * 60)

        globalvars.emit_sound("tank_cannon_shoot.ogg")

        rocket = Missile("images/TD/entities/projectile/spr_missile.png")
        start_x = self.center_x
        start_y = self.center_y
        rocket.center_x = start_x
        rocket.center_y = start_y
        local_speed = 15

        dest_x = enemy.center_x
        dest_y = enemy.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle)

        rocket.angle = math.degrees(angle)

        rocket.bullet_list = self.bullet_list

        rocket.animation_timer = 0

        rocket.change_x = math.cos(angle) * local_speed
        rocket.change_y = math.sin(angle) * local_speed

        rocket.enemy_list = globalvars.enemy_list
        rocket.damage = self.damage
        rocket.attack_radius = 25
        self.bullet_list.append(rocket)


# Effects


class MineExplosion(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.curtime = 0

    def update(self):
        self.curtime += 1
        if self.curtime < 2:
            self.set_texture(0)
        elif self.curtime < 4:
            self.set_texture(1)
        elif self.curtime < 6:
            self.set_texture(2)
        elif self.curtime < 8:
            self.set_texture(3)
        elif self.curtime < 10:
            self.set_texture(4)
        elif self.curtime < 12:
            self.set_texture(5)
        else:
            self.kill()


class BombExplosion(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.curtime = 0
        self.damage = 0
        self.radius = 0
        self.exploded = False

    def update(self):
        if not self.exploded:
            for enemy in globalvars.enemy_list:
                if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.radius ** 2:
                    enemy.on_take_damage(self.damage, False)
                    self.exploded = True

        self.curtime += 1
        if self.curtime == 1:
            globalvars.emit_sound("small_explosion.ogg")
        elif self.curtime < 2:
            self.set_texture(0)
        elif self.curtime < 4:
            self.set_texture(1)
        elif self.curtime < 6:
            self.set_texture(2)
        elif self.curtime < 8:
            self.set_texture(3)
        elif self.curtime < 10:
            self.set_texture(4)
        elif self.curtime < 12:
            self.set_texture(5)
        else:
            self.kill()


class Projectile(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.attack_radius = 10
        self.change_x = 0
        self.change_y = 0
        self.damage = 0
        self.animation_timer = 0
        self.curtime = 0
        self.check_delay = 0
        self.delay_speed = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if len(self.textures) > 1:
            self.animation_timer += 1
            if self.animation_timer >= len(self.textures):
                self.animation_timer = 0
            self.set_texture(self.animation_timer)

        if int(self.center_x) < 0 or int(self.center_x) > SCREEN_WIDTH or int(self.center_y) < 0 or int(self.center_y) > SCREEN_HEIGHT:
            self.kill()

        if self.curtime > self.check_delay:
            self.check_delay = self.curtime + self.delay_speed

            target_index = len(globalvars.enemy_list) - 1
            target_found = False

            while not target_found and target_index >= 0:
                enemy = globalvars.enemy_list[target_index]

                if (((self.center_x - enemy.center_x) ** 2) + (
                            (self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2:
                    target_found = True
                    enemy.on_take_damage(self.damage, False)
                    self.kill()

                target_index = target_index - 1

        self.curtime += 1


class Missile(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.attack_radius = 10
        self.change_x = 0
        self.change_y = 0
        self.damage = 0
        self.animation_timer = 0
        self.bullet_list = []

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if 0 > int(self.center_x) > SCREEN_WIDTH or 0 > int(self.center_y) > SCREEN_HEIGHT:
            self.kill()

        for enemy in globalvars.enemy_list:
            if (((self.center_x - enemy.center_x) ** 2) + ((self.center_y - enemy.center_y) ** 2)) <= self.attack_radius ** 2:
                globalvars.emit_sound("big_explosion.ogg")
                explosion = BombExplosion("images/TD/effects/big_explosion/explosion_1.png")
                explosion.curtime = 0
                explosion.center_x = self.center_x
                explosion.center_y = self.center_y
                explosion.damage = self.damage
                explosion.radius = 100
                explosion.exploded = False
                explosion.enemy_list = globalvars.enemy_list
                explosion.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_1.png"))
                explosion.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_2.png"))
                explosion.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_3.png"))
                explosion.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_4.png"))
                explosion.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_5.png"))
                explosion.append_texture(arcade.load_texture("images/TD/effects/big_explosion/explosion_6.png"))
                self.bullet_list.append(explosion)
                self.kill()
                break