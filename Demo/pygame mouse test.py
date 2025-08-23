import pygame
 
pygame.init()
surface = pygame.display.set_mode((600, 400))

#buttons = pygame.mouse.get_pressed()

 
while True:
    for event in pygame.event.get():
        buttons = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEMOTION:
            print(pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            exit()
        if buttons[0]:  # Check if left button is pressed
            print("Left button is pressed")
 
    pygame.display.update()