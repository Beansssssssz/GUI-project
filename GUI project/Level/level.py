from random import randint
from sys import exit as sys_exit

import pygame
from time import sleep

from Charcter.enemy import Enemy
from Charcter.player import Player
from Charcter.sword import Sword
from Level.ladder import Ladder
from Level.shelf import Shelf
from Level.Tile import Tile
from Main.settings import *


class Level:
    def __init__(self, Level_data :list[str], dis:pygame.Surface):
        """
        the build function in python
        :param: the level map created in setting
                the screen pygame displays
        :type: list[str]
                pygame.Surface
        :return: it isnt supposed to return something
        return type: None
        """ 
        super().__init__()

        self.dis = dis
        self.Level_Creation(Level_data)
        self.world_shift_X = 0 #shift so the other tiles are seen

        font = pygame.font.Font(None, 50)
        self.end_screen = font.render("you have died, the game will close now... bye", True, "red")
        self.win_screen = font.render("you have won yay, the game will close now... bye", True, "pink")

    
    def Level_Creation(self, level_map :list[str]):
        """
        creates all the elements of the level
        :param: the level map created in setting
        :type: list[str]
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.shelfs = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.sword = pygame.sprite.GroupSingle()

        
        for row_index,row in enumerate(level_map):
            for col_index,col in enumerate(row):
                x = col_index * Tile_size
                y = row_index * Tile_size

                if col == 'X':
                    tile = Tile((x,y),Tile_size)
                    self.tiles.add(tile)
                
                if col == 'P':
                    image = pygame.image.load('art/player_art/player.png').convert_alpha()
                    player_sprite = Player((x,y), image, self.tiles)
                    self.player.add(player_sprite)

                    image = pygame.image.load('art/player_art/sword.png').convert_alpha()
                    sword_sprite = Sword(image, self.player.sprite)
                    self.sword.add(sword_sprite)

                if col == 'E':
                    image = pygame.image.load('art/player_art/enemy.png').convert_alpha()
                    enemy_sprite = Enemy((x,y), image, self.tiles)
                    self.enemies.add(enemy_sprite)
                
                if col == 'L':
                    image = pygame.image.load('art/level_art/ladder.png').convert_alpha()
                    ladder = Ladder((x,y), image)
                    self.ladders.add(ladder)
                
                if col == '/': #the start of the shelf
                    image = pygame.image.load('art/level_art/start_shelf.png').convert_alpha()
                    shelf = Shelf((x,y), image)
                    self.shelfs.add(shelf)

                if col == 'S': #the middle of teh shelf
                    image =  pygame.image.load('art/level_art/middle_shelf.png').convert_alpha()
                    shelf = Shelf((x,y), image)
                    self.shelfs.add(shelf)
                    
                if col == '\\': #the end of the shelf
                    image = pygame.image.load('art/level_art/end_shelf.png').convert_alpha()
                    shelf = Shelf((x,y), image)
                    self.shelfs.add(shelf)
            
    def scrolling_X(self): 
        """
        instead of calling all the fucntion seperately, u call them from here
        moves all the elements the amount teh world is moving
        :param: None
        :type: None
        :return: it isnt supposed to return something
        :return type: None
        """ 
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift_X = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift_X = -8
            player.speed = 0
        else:
            self.world_shift_X = 0
            player.speed = 8

    def end_level(self):
        """
        instead of calling all the fucntion seperately, u call them from here
        ends the game
        :param: None
        :type: None
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.dis.fill('black')
        self.dis.blit(self.end_screen, (0, 0))
        pygame.display.update()
        sleep(2)
        pygame.quit()
        sys_exit()

    def update_world(self):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: None
        :type: None
        :return: it isnt supposed to return something
        :return type: None
        """ 
        #level moving
        self.scrolling_X() #to see the player when moving too much in a direction

        player = self.player.sprite #a pointer to the player

        #level changes
        self.tiles.update(self.world_shift_X) #changes the camera pos based on the amount in the var
        self.tiles.draw(self.dis) #draws the tiles sprites
  
        self.ladders.update(player, self.world_shift_X)
        self.ladders.draw(self.dis)

        self.shelfs.update(player, self.world_shift_X)
        self.shelfs.draw(self.dis)
    
    def Did_Win(self):
        if self.enemies.__len__() <= 0:
            self.dis.fill('black')
            self.dis.blit(self.win_screen, (0, 0))
            pygame.display.update()
            sleep(2)
            pygame.quit()
            sys_exit()

    def run(self):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: None
        :type: None
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.update_world()
        self.mouse_pos =  pygame.mouse.get_pos() #gets the pos of the mouse
        player = self.player.sprite #a pointer to the player
        sword = self.sword.sprite #a pointer to the sword

        self.enemies.draw(self.dis) #draws the enemies
        self.enemies.update(self.world_shift_X) #upates all the enemies

        for enemy in self.enemies.sprites():#cycle thru enemies and player collision
            if Sprite_Collision(sword, enemy): 
                if sword.active and not sword.hit_something:
                    sword.hit_something = True
                    Check_Direction(enemy)
                    self.enemies.remove(enemy)          
            if Sprite_Collision(player, enemy): 
                self.end_level()

        self.player.draw(self.dis) #draws the player sprite
        self.player.update(sword) # calls the update method in the player

        if not sword.hit_something:
            self.sword.draw(self.dis) #draws the sword sprite
        self.sword.update(self.world_shift_X)

        self.Did_Win()

def Sprite_Collision(sprite1 :pygame.sprite.Sprite, sprite :pygame.sprite.Sprite):
    """
    a function to check collision
    :param: a sprite
    :type: pygame.sprite.Sprite
    :return: it isnt supposed to return something
    return type: None
    """ 
    if sprite1.rect.colliderect(sprite.rect):
        return True
    return False

def Check_Direction(sprite :pygame.sprite.Sprite):
    """
    a function to check Direction
    :param: player object
    :type: Player class
    :return: it isnt supposed to return something
    return type: None
    """ 
    if sprite.direction.x > 0: #if player is moving left
        sprite.collision_types['right'] = True
        return 'right'
    elif sprite.direction.x < 0: #if player is moving left
        sprite.collision_types['left'] = True
        return 'left'