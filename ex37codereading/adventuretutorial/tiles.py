"""Describes the tiles in the world space."""
__author__ = 'Phillip Johnson'

import items, enemies, actions, world


class MapTile(object): #Creates the MapTile
    """The base class for a tile within the world space"""
    def __init__(self, x, y): #defines the class creation, and takes two parameters
    #seems that when you enter the class as a parameter in any of the functions below, it initiates the
    #object as a room with the two arguments
    #each room has its own special changes to the base class
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y #puts the arguments into a variable object within the class

    def intro_text(self): #not used
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def modify_player(self, the_player): #not used
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self): #will be the class instance roomname.adjacent_moves()
        """Returns all move actions for adjacent tiles."""
        moves = [] # list to store moved
        if world.tile_exists(self.x + 1, self.y): #if exists, returns that particular dictionary key value
        # which will be a room object
            moves.append(actions.MoveEast()) #appends the MoveEast() action from the action module and appends to moves
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves # returns the possible adjacent move options from the actions module

    def available_actions(self): #room available actions
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves() #available actions from adjacent moves
        moves.append(actions.ViewInventory()) #add viewinventory from actions module to the moves list

        return moves #return moves list with adjacent moves and the newly added viewinventory


class StartingRoom(MapTile): #an instance of the maptile class
    def intro_text(self): #StartingRoom.intro_text() will return some text
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """

    def modify_player(self, the_player): #startingroom.modifyplayer(player) will do nothing
        #Room has no action on player
        pass


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""
    def __init__(self, x, y, item): #needs some kind of item passed as an argument. A new type of maptile.
    #the init statement will use the init from the parent class using super(). the item is
    #specific for this type of room using the self.item line
        self.item = item
        super(LootRoom, self).__init__(x, y)

    def add_loot(self, the_player): #adds the item this room has to the specified player
        the_player.inventory.append(self.item) #uses the inventory.append method from an object added as argument

    def modify_player(self, the_player):
        self.add_loot(the_player) #calls the add loot function using the lootroominstance.add_loot(player)
        #no idea why add_loot is kept seperate. perhaps to keep consistent with modify_player(player)


class FindDaggerRoom(LootRoom): #part of the lootroom subclass
    def __init__(self, x, y):
        super(FindDaggerRoom, self).__init__(x, y, items.Dagger()) #specifies the item to be a dagger from items module

    def intro_text(self):
        return """
        You notice something shiny in the corner.
        It's a dagger! You pick it up.
        """


class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super(Find5GoldRoom, self).__init__(x, y, items.Gold(5))

    def intro_text(self):
        return """
        Someone dropped a 5 gold piece. You pick it up.
        """


class EnemyRoom(MapTile): #new type of room subclass
    def __init__(self, x, y, enemy): #adds an enemy
        self.enemy = enemy #object for enemy in the room
        super(EnemyRoom, self).__init__(x, y) #inherits these arguments from super()

    def modify_player(self, the_player):
        if self.enemy.is_alive(): #checks if enemy is alive from some other module
            the_player.hp = the_player.hp - self.enemy.damage #decreases a player hp value from another class
            # by the enemy.damage value from an enemy class
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))
            # new string.format seems to add the values in the {} fields

    def available_actions(self): # must overwrite the same method from parent class. returns the
    # adjacent_moves() object so I'm assuming we can't use inventory
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)] #two from the actions module
        else:
            return self.adjacent_moves()


class GiantSpiderRoom(EnemyRoom): #enemy room instance for giant spider. has it's own intro text.
# seems enemy hp and other properties must be in the object for the enemy
    def __init__(self, x, y):
        super(GiantSpiderRoom, self).__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super(OgreRoom, self).__init__(x, y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is blocking your path!
            """
        else:
            return """
            A dead ogre reminds you of your triumph.
            """


class SnakePitRoom(MapTile): #a particular room that uses maptile. 
    def intro_text(self):
        return """
        You have fallen into a pit of deadly snakes!

        You have died!
        """

    def modify_player(self, player): # modifies the player attribute hp
        player.hp = 0


class LeaveCaveRoom(MapTile): # another instance of MapTile
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """

    def modify_player(self, player): # this instance alters the player.victory object
        player.victory = True
