# Python
School projects in Python that use the arcade library (http://arcade.academy/)

Installation:
I didn't really plan on this being something you could just easily download and play, so you will have to install Python and get an IDE
and all that stuff. I will try to provide steps on how to do this:
1) Install python https://www.python.org/downloads/
2) Install the Arcade Library, I used a library made by Dr. Craven that can be found here https://pypi.python.org/pypi/arcade
3) Install an IDE, I used PyCharm but feel free to use whatever works for you. https://www.jetbrains.com/pycharm/

After doing all of that, you should be able to get the files for the game from this github, put it into the IDE and run it.
I will try putting a download link on the github so you don't have to deal with git commands.

The Game:
This is a school project I made for an intro to programming class themed around video games. The game is called, "The Great Skeleton War"
and it's a tower defence game that has three seperate ages. The Stone Age, the Medieval Age, and the Modern Age. In each age you get new
towers that you can buy. There's a horde of skeletons coming to destroy your village and as the game progresses stronger skeletons spawn
in higher quantities. Oh, also you're a wizard that can cast spells. You can unlock new spells or upgrade your spells by killing enemies and
leveling up.

Just as a fair warning, the game gets very laggy around wave 20+ because of the large amount of enemies. It will still work, just expect
a large FPS drop.

I've also included a console feature where you can press ~ to type in the following commands:
quit - Exits the game
win - Makes you win the game
lose - Instantly destroys your village
restart - Restarts the game
restoremana - Restores your mana to the maximum value
nextage - Sets you to the next age
killall - Kills all enemies on the screen
endwave - Ends the wave and clears the enemy spawning queue
spawndata - Tells you how many enemies are left in the spawning queue
tgm - Sets your level to 10, gives you thousands of mana, speed, population, and money.
player.levelup - Levels up the player (ex: player.levelup for one level or player.levelup 3 for 3 levels)
player.givespell - Gives the player the specified spell (ex: player.giveskill Inferno)
player.giveskill - Gives the player the specified skill (ex: player.giveskill Blistering)
player.setmana - Sets current mana (not max mana) (ex: player.setmana 50)
player.setmaxmana - Sets max mana (ex: player.setmaxmana 100)
player.givexp - Gives experience (ex: player.givexp 10)
player.setspeed - Sets movement speed of player (ex: player.setspeed 10)
game.setpopulation - Sets population of your village (ex: game.setpopulation 100)
game.setwave - Sets current wave (ex: game.setwave 10)
game.givemoney - Gives you money (ex: game.givemoney 100)
game.setage - Sets the age (ex: game.setage medieval)
game.spawnenemy - Spawns an enemy (ex: game.spawnenemy raptor)
where the wild things are - ???
