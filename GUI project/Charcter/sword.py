import pygame
from Charcter.player import Player

class Sword(pygame.sprite.Sprite):
    def __init__(self, image :pygame.Surface, player : Player):
        """
        the build function in python
        :param: the player object
                the image
        :type: pygame.Surface and Player
        :return: it isnt supposed to return something
        return type: None
        """ 
        super().__init__()
        self.player = player
        self.image = image
        self.old_image = image
        self.image.set_colorkey('black') # removes all the black pixels
        self.rect = player.rect.copy()
         
        self.active = False
        self.timer = 3 #the timer that counts how long to keep the sword stabing
        self.hit_something = False

    def Updateloc(self, world_shift_X):
        """
        shift the sword the amount they are supposed to be shifted
        :param: the amount that the worlds is
                supposed to shift
        :type: int 
        :return: it isnt supposed to return something
        return type: None
        """ 
        if not self.player.facing_right:
            self.rect.x += world_shift_X
        if not self.active:
            self.rect = self.player.rect.copy()
            if self.player.facing_right:
                self.image = self.old_image
                self.rect.x += 10 #makes it look better(trust me bro)
            else:     
                self.image = pygame.transform.flip(self.old_image, True, False) #flips the old_image of the player
                self.rect.x -= self.player.rect.width
                
    def Stab(self):
        """
        checks if the player is gonna 
        stab someone
        :param: doesnt get any cause lonely
        :type: doesnt get any cause lonely 
        :return: it isnt supposed to return something
        return type: None
        """ 
        if pygame.mouse.get_pressed()[0]:
            self.active = True

    def InMoition(self):
        """
        checks if the sword is in motion and if yes then moves it
        :param: doesnt get any cause lonely
        :type: doesnt get any cause lonely 
        :return: it isnt supposed to return something
        return type: None
        """ 
        if self.active:
            self.timer -= 0.1
            if self.player.facing_right:
                self.rect.x += 10
            else:     
                self.rect.x -= 10
        
    def reset(self):
        """
        resets the timer... the sword timer
        :param: doesnt get any cause lonely
        :type: doesnt get any cause lonely 
        :return: it isnt supposed to return something
        return type: None
        """ 
        if self.timer < -3:
            self.hit_something = True
        if self.timer < -10:
            self.active = False
            self.hit_something = False
            self.timer = 3
        if self.hit_something:
            self.rect.y += 1000             

    def update(self, world_shift_X):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: the amount that the worlds is
                supposed to shift
        :type: int
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.Updateloc(world_shift_X)
        self.Stab()
        self.InMoition()
        self.reset()