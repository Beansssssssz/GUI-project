import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos :tuple, image :pygame.Surface, tiles :pygame.sprite.Group):
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
        self.image.set_colorkey('white') # removes all the black pixels
        self.image.set_colorkey('cyan') # removes all the black pixels
        self.rect = self.image.get_rect(topleft = pos) #the rect of the player

        self.old_image = self.image #saves the original image in a var to flip at a later time

        #player movment and collision
        self.direction = pygame.math.Vector2(0,0) #create a vector2
        self.speed = 8 #the speed of the player
        self.collision_types = {'top' :False, 'bottom' :False, 'left' :False, 'right' :False} 
        self.air_timer = 3 #the timer for the player jump 
        self.Gforce = 10 #the gravity of the player
        self.jump_speed = self.Gforce * -2 #the jump speed of the player
        self.tiles = tiles
        self.standing = False

        #player animation
        self.facing_right = True

        #player battle stats
        self.attack = 1.5
        self.hp = 3

    def Update_state(self):
        """
        update the state of the player's picture(facing left/right)
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

    def __Get_Input(self, Sword):
        """
        checks for input 
        :param: the sword
        :type: Sword class
        :return: it isnt supposed to return something
        return type: None
        """ 
        keys = pygame.key.get_pressed() # gives a array of all the keys in bool (True if pressed)

        if not Sword.active or Sword.hit_something:
            if keys[pygame.K_d] and not self.collision_types['right']:#chekcs if the d key has been pressed and 
                #if the player is colliding with a wall to his right
                self.facing_right = True 
                self.direction.x = 1 #moving right is done by increasing the x in a positive way

            elif keys[pygame.K_a] and not self.collision_types['left']:
                self.facing_right = False
                self.direction.x = -1 #moving left is done by increasing the x in a negetive way

            else:
                self.direction.x = 0 #if d or a key was pressed the the player will not move
        else:
            self.direction.x = 0 #if d or a key was pressed the the player will not move

        if keys[pygame.K_w]:
            self.climbing = True
            self.falling = False

        elif keys[pygame.K_s]:
            self.falling = True
            self.climbing = False
            
        else:
            self.climbing = False
            self.falling = False
        
        if keys[pygame.K_SPACE] and self.air_timer > 0 and not self.collision_types['top']:#chekcs for spacebar input 
            #collision with a ceiling and if the player has enough time to jump
            self.direction.y = self.jump_speed # moving up is by increasing the y in a negetive way
            
        else:
            self.direction.y = 0 #if not moving the dont move the player Y pos
            self.air_timer = 0 #if not currently jumping then resete time to jump
    

    def Gravity(self):
        """
        the gravity.
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        if not self.standing or self.falling:
            if not self.collision_types['bottom']: #if the player isnt colliding with the floor dec the air_timer
                #and add to the player Y pos the gravity
                self.direction.y += self.Gforce 
                self.air_timer -= 0.1
        self.rect.y += self.direction.y #updates the player Y position
        self.standing = False


    def touch_Grass(self):
        """
        resete the air_timer
        (is called ny the level.py file only when there is collision)
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.air_timer = 3

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

        for tile in hit_list:#cycle thru everytime there is a collision
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
        self.rect.y += self.direction.y 

        for tile in hit_list: #cycle thru everytime there is a collision
            if self.direction.y > 0: #if player is moving down
                self.rect.bottom = tile.top #changes the position of the player to fix collision
                self.collision_types['bottom'] = True
                self.direction.y = 0 #resets the y velocity
                self.touch_Grass()
            elif self.direction.y < 0: #if player is moving up
                self.collision_types['top'] = True
                self.rect.top = tile.bottom #changes the position of the player to fix collision
                self.direction.y = 0 #resets the y velocity
        self.rect.y -= self.direction.y

    def Collision_Tiles(self):
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: doest get any
        :type: doest get any
        :return: it isnt supposed to return something
        return type: None
        """ 
        self.Y_collision()#checks collision  in the Y axis
        self.X_collision()#checks collision  in the X axis

    def update(self, Sword): #calls all the methods in this class
        """
        instead of calling all the fucntion seperately
        u call them from here
        :param: the sword
        :type: Sword class
        :return: it isnt supposed to return something
        :return type: None
        """ 
        self.__Get_Input(Sword)
        self.Update_state()
        self.Gravity()
        self.Collision_Tiles()
