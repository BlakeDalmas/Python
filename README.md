# Python
School projects in Python that use the arcade library (http://arcade.academy/)

Installation:

1) Install python https://www.python.org/downloads/
2) Install the Arcade Library, I used a library made by Dr. Craven that can be found here https://pypi.python.org/pypi/arcade
3) Install an IDE, I used PyCharm but feel free to use whatever works for you. https://www.jetbrains.com/pycharm/

After doing all of that, you should be able to get the files for the game from this github, put it into the IDE and run it.
For The Great Skeleton War, you have to run lab_12.py to launch the actual game.

The Great Skeleton War:
=======================

This is a tower defence game that has three seperate ages. The Stone Age, the Medieval Age, and the Modern Age. In each age you get new
towers that you can buy. There's a horde of skeletons coming to destroy your village and as the game progresses stronger skeletons spawn
in higher quantities. You also play as a wizard that can cast spells. You can unlock new spells or upgrade your spells by killing enemies and leveling up. The game includes various other features such as randomized maps, multiple difficulties, a console with cheat codes, and more.

Here's a video demonstration of version 1.0:

https://www.youtube.com/watch?v=4yRxBYXP_Eo


Version 2.0 : Changelog
-----------------------

<b>Bug Fixes</b>

Fixed a bug where the game would crash if config.txt was missing a keybinding.

Fixed a bug where using Burden on an de-activated hyperskeleton causes them to move at hyper speed
instead of slowing down.

Fixed a bug where the Ultimate Orb could teleport to activated hyperskeletons.

Fixed a bug where you could cast venomblade while your sword was already poisoned.

Fixed a bug where you could get extra experience by doing more damage than what would kill the enemy.

Fixed a bug where towers and spells wouldn't target the right enemies.

<b>Reducing Lag</b>

Modified the damage number system:
    Instead of having thousands of hard-to-read and laggy damage numbers everywhere, each enemy can only have one damage number at a
    time. If you attack an enemy rapidly, the damage number will simply go up instead of creating another one.

Made projectiles more efficient:
    Instead of checking every enemy on the map every frame, it only checks every few frames determined by a formula according to the
    speed of the projectile. The slower the projectile the less often it has to check for nearby enemies.

Made tower detection more efficient:
    Towers only check for nearby enemies every .1 seconds or so instead of every frame. Also they check through the list backwards
    because the enemy they are going to target will most likely be at the front of the list, rather than the back.

<b>New Features and Changes</b>

Spells and Skills:
   Instead of having a ~20% chance to get an ultimate randomly, after you reach level 10, you get an Ultimate Skillpoint.
   If you have any spells that have all of their skills purchased, you can click on the icon of that spell to spend the
   Ultimate Skillpoint and make that spell go ultimate. Otherwise, it acts as a normal skillpoint.

   Reaching level 10, and other things associated with Ultimates have cooler graphics and sounds now.

   The way spells and skills are added have been re-programmed so that it's far easier to simply add a new spell without
   worrying about changing little variables everywhere.

   Lightning shoots faster and costs less mana.

   New Spell: Magic Missile

   New Spell: Starblast

   Passive Spells no longer show up in the spell selection menu at all.

   Every game, you can choose from 2 random spells and the passive spell. Rather than 3 spells of a certain type.

   Made a new spell type called Sorcery. Magic Missile, Burden, and Starblast go into this.

   Made a new spell type called Passive, essentially, this is just battlemage and mysticism combined.

   The inferno ultimate also extends the duration of the fire.

   Dart ultimate instant kill chance: 10% -> 25%

   Cloud ultimate changed, instead of allowing you to place 3 at once, any enemy that dies from the cloud places
   another cloud.

   Venomblade ultimate makes the poison last forever, instead of 3 swings.


General:
   You can now press 1-3 on the keyboard to quickly switch to another spell. You can rebind these in the options.

   Made it easier to program new buttons into the options menu.

   The spell you currently have selected is shown next to the spell hand icon.

   You can now pause the game at any time (deafult is P, key bind can be changed in options).

   Hyperskeletons have been buffed, they remain invincible until about 3/4 through the map instead of 1/2.

   Towers have more variability on their delays so they won't all attack at the same exact time every time.

   Towers have slight inaccuracy, especially in the case of the tank, it makes it look more like bullets and less like a laser.

   The game now has 3 separate difficulties:
    
   Normal: A good difficulty for new players. Lich chains and skeleon lords are removed, you start with more money, gain more money on
   kill, and you need less money to win.
    
   Hard: Essentially what the game was like originally. Better for players that have played the game before.
    
   Nightmare: Ridiculously difficult, don't expect to even get close to winning unless you know how to exploit the finest details
   of the game. Hyperskeletons appear mere feet away from your village, you start with no money, raptors start spawning by wave 5, 
   and it only gets worse from there.

<b>Misc Changes</b>

Added 1 more skeleton to the first wave so that if you kill all the skeletons with no towers on wave 1 you get to level up
before the wave ends, rather than after.
