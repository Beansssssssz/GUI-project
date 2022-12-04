import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos :tuple, size:int):
        """
        the build function in python
        :param: the pos of the tile
                the size of the tile
        :type: tupel and int
        :return: it isnt supposed to return something
        return type: None
        """ 
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, X_shift):
        """
        shift the tiles the amount they are supposed to be shifted
        :param: the amount that the worlds is
                supposed to shift
        :type: int 
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.rect.x += X_shift
