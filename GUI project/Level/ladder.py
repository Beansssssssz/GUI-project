from cmath import rect
import pygame


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos :tuple , image :pygame.Surface):
        """
        the build function in python
        :param: the pos of the tile
                the image
        :type: tupel and pygame.Surface
        :return: it isnt supposed to return something
        return type: None
        """ 
        super().__init__()
        #player image
        self.image = image
        self.image.set_colorkey('black') # removes all the black pixels
        self.rect = self.image.get_rect(topleft = pos) #the rect of the player
        self.mask = pygame.mask.from_surface(self.image) #create a mask


    def climb_up(self, player :pygame.sprite.Sprite):
        if player.climbing:
            if (player.rect.x + player.rect.width <= self.rect.x + self.rect.width
                and player.rect.x >= self.rect.x):
                player.rect.y += -10
            
        if player.falling:
            player.direction.y = 0       

    def collision(self, player :pygame.sprite.Sprite):
        """
        a function to check collision
        :param: player object
        :type: pygame.sprite.Sprite
        :return: it isnt supposed to return something
        return type: None
        """ 
        if self.rect.colliderect(player.rect) and not player.collision_types['top']:
            player.standing = True
            self.climb_up(player)                

    def update_pos(self,world_shift_x):
        """
        shift the ladder the amount they are supposed to be shifted
        :param: the amount that the worlds is
                supposed to shift
        :type: int 
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.rect.x += world_shift_x

    def update(self, player :pygame.sprite.Sprite, world_shift_x):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: the amount that the worlds is
                supposed to shift
        the player object
        :type: int
               pygame.sprite.Sprite
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.collision(player)
        self.update_pos(world_shift_x)
        counter = 0