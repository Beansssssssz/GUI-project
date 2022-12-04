import pygame

from Main.settings import *
from Charcter.player import *
from Level.level import *

def main():
    """
    in order to start the game u 
    need to call this function
    :param: it does get any parameters
    :type: it does get any parameters
    :return: it isnt supposed to return something
    return type: None
    """ 
    pygame.init() 
    dis = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('roguelike') #sets the title of the window 

    clock = pygame.time.Clock() #creates a clock that controls the frames

    level = Level(level_map, dis)


    font = pygame.font.Font(None, 40)
    start_screen1 = font.render("dont touch any of the cyan rectanglas that move, they will kill u", True, "red")
    start_screen2 = font.render("press left click to shoot/enter the game", True, "red")
    start_screen3 = font.render("oh btw u cant move while the sword is out... gd", True, "red")
    running = True
    dis.blit(start_screen1, (0,0))
    dis.blit(start_screen2, (0,40))
    dis.blit(start_screen3, (0,80))
    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #checks if the window was attapted to be cloesed     
                pygame.quit()
                sys_exit()
        if pygame.mouse.get_pressed()[0]:
            running = False

    sleep(0.1) #trust me bro just trust me...

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #checks if the window was attapted to be cloesed     
                running = False
            
        dis.fill('blue')#fills the screen with blue color

        level.run() #runs all the methods
        #TODO sword health bar, bosses(also boss ai) 

        pygame.display.update()#updates the display
        clock.tick(60)#set the max amount of frames to 60

    pygame.quit()