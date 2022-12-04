from random import randint

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos :tuple , image :pygame.Surface, tiles :pygame.sprite.Group):
        """
        the build function in python
        :param: the pos of the tile
                the image
                all the tiles
        :type: tupel and pygame.Surface and pygame.sprite.Group
        :return: it isnt supposed to return something
        return type: None
        """ 
        super().__init__()
        #player image
        self.image = image
        self.image.set_colorkey('black') # removes all the black pixels
        self.rect = self.image.get_rect(topleft = pos) #the rect of the player
        self.mask = pygame.mask.from_surface(self.image) #create a mask

        self.old_image = self.image #saves the original image in a var to flip at a later time

        #player movment and collision
        self.direction = pygame.math.Vector2(0,0) #create a vector2
        self.speed = randint(2,10) #the speed of the enemy
        self.collision_types = {'top' :False, 'bottom' :False, 'left' :False, 'right' :False} 
        self.air_timer = 3 #the timer for the player jump 
        self.Gforce = 10 #the gravity of the player
        self.jump_speed = self.Gforce * -2 #the jump speed of the player
        self.tiles = tiles #the map tiles

        self.facing_right = True

    def Update_state(self):
        """
        update the state of the enemys's picture(facing left/right)
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        for name in self.collision_types: #reset the collision_types
            self.collision_types[name] = False

        if self.facing_right:
           self.image = self.old_image #resets the player imgae to the old one
        
        else:
            self.image = pygame.transform.flip(self.old_image, True, False) #flips the old_image of the player

    def Enemy_Move_Right(self):
        """
        moves the right left
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.facing_right = True 
        self.direction.x = 1 #moving right is done by increasing the x in a positive way

    def Enemy_Move_Left(self):
        """
        moves the enemy left
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.facing_right = False
        self.direction.x = -1 #moving left is done by increasing the x in a negetive way

    def Gravity(self):
        """
        the gravity.
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        if not self.collision_types['bottom']: #if the player isnt colliding with the floor dec the air_timer
            #and add to the player Y pos the gravity
            self.direction.y += self.Gforce 
            self.air_timer -= 0.1

    def update_pos(self,X_shift):
        """
        shift the enemy the amount they are supposed to be shifted
        :param: the amount that the worlds is
                supposed to shift
        :type: int 
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.rect.x += self.direction.x + X_shift
        self.rect.y += self.direction.y

    def collision_test(self):
        """
        returns all active collision 
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        hit_list = [] 
        for sprite in self.tiles.sprites(): #cycle thru all the sprites
            if self.rect.colliderect(sprite.rect): #finds all the times there was a collision with the tiles
                hit_list.append(sprite.rect) 

        return hit_list

    def X_collision(self):
        """
        checks all the collision in th x axis
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.rect.x += self.direction.x * self.speed #updates teh player position to a couple blocks ahead
        #because sometimes the player can move too fast for the collision

        hit_list = self.collision_test() #gets all the times there were collision

        for tile in hit_list: #cycles thru everytime there is a collision
            if self.direction.x > 0: #if player is moving left
                self.rect.right = tile.left #changes the position of the player to fix collision
                self.collision_types['right'] = True
            elif self.direction.x < 0: #if player is moving left
                self.rect.left = tile.right #changes the position of the player to fix collision
                self.collision_types['left'] = True 

    def Y_collision(self):
        """
        checks all the collision in th y axis
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        hit_list = self.collision_test()#gets all the times there were collision

        for tile in hit_list: #cycle thru everytime there is a collision
            if self.direction.y > 0: #if player is moving down
                self.rect.bottom = tile.top #changes the position of the player to fix collision
                self.collision_types['bottom'] = True
                self.direction.y = 0 #resets the y velocity
            elif self.direction.y < 0: #if player is moving up
                self.collision_types['top'] = True
                self.rect.top = tile.bottom #changes the position of the player to fix collision
                self.direction.y = 0 #resets the y velocity

    def Collision_Tiles(self):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: None
        :type: int
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.Y_collision()#checks collision  in the Y axis
        self.X_collision()#checks collision  in the X axis

    def randome_movments(self):
        """
        decides the movment of the bot
        cause u cant know what ill do if i dont know
        :param: None
        :type: int
        :return: it isnt supposed to return something
        :return type: None
        """ 
        rand = randint(0, 100)
        if rand > 99 :
            self.facing_right = not self.facing_right
        if self.direction.x > 0:
            if self.collision_types['right']:
                self.facing_right = False
        elif self.direction.x < 0: #if player is moving left
            if self.collision_types['left']:
                self.facing_right = True
  
    def move_him(self):      
        """
        moves the bot. yeah
        :param: None
        :type: int
        :return: it isnt supposed to return something
        :return type: None
        """ 
        if self.facing_right:
            self.Enemy_Move_Right()
        else:
            self.Enemy_Move_Left()

    def update(self, X_shift):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: the amount that the worlds is
                supposed to shift
        :type: int
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.update_pos(X_shift)
        self.Collision_Tiles() #calls the collision methods
        self.Gravity()
        self.randome_movments()
        self.Update_state() #update the state of the enemy
        self.move_him()
        
