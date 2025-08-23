software_version = 2.2
"""
-------------------------
Software version: 2.2
Release date: 2023/11/28
Release notes:
Add:    1. Return to menu after game over
        2. Press ESC at menu to kill program; Press ESC in game to return to menu
Remove: 1. Remove unnecessary code
-------------------------
Software version: 2.1.1
Release notes:
Fix:    1. Diagonal Selection Problem
-------------------------
Software version: 2.1
Release notes:
Fix:    1. User can select same element
Change: 1. Pointer A is moved directly without using site, additional site code will be removed in next version
Remove: 1. Additional testing notes
"""

import random
import pygame
import sys
import time
from pygame.locals import *

#window resize logic
screen = pygame.display.set_mode((400, 400), pygame.RESIZABLE)
pygame.display.set_caption('Resizable Window')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle window resize events
        if event.type == pygame.VIDEORESIZE:
            # Update the screen size
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    #GAME LOGIC HERE
pygame.quit()

def newBoard(size_x:int,size_y:int):
    """
    This function: Create an empty board
    Call with 2 values: Width of x-axis and width of y-axis
    Return 1 value: An empty board
    """
    board = []
    # Rows
    for i in range(size_x):
        board.append([])
        # Column
        for j in range(size_y):
            board[i].append(0)
    # Return created board
    return board



def insertElement(board:list,numb_elements:int):
    """
    This function: Insert random elements in pairs into the board
    Call with 2 values: Game board and number of different elements
    Return 1 value: Game board with each element evenly distributed
    """
    # Find how many spaces in total
    size_x = len(board)
    size_y = len(board[0])
    total_elements = size_x * size_y

    # Find how many spaces for each group of element
    max_elements = total_elements / numb_elements

    # Create a list, showing how many spaces remained for each element
    elements_remain = []
    for i in range(numb_elements):
        elements_remain.append(max_elements)

    # Nested loop to insert item
    for i in range(size_x):
        for j in range(size_y):
            # Randomly generate an element
            element = random.randint(1,numb_elements)

            # Check if current element has remaining
            while elements_remain[element - 1] == 0:
                element = random.randint(1,numb_elements)

            # Insert that element
            board[i][j] = element
            elements_remain[element - 1] -= 1

    return board



def removeElement(board:list,pointer_a:list):
    """
    This function: Removes elements with correct path
    Call with 2 values: Two elements to remove
    Return 1 value: Finished board
    """
    board[pointer_a[0]][pointer_a[1]] = 0
    return board



def checkAxis(space_1:list,space_2:list):
    """
    This function: Checks whether 2 space are on the same axis
    Call with 2 values: Two space for checking
    Return 1 value: Name of axis('x'/'y') if they are same, empty string('') if different
    """
    if space_1[0] == space_2[0]:
        return 'x'
    elif space_1[1] == space_2[1]:
        return 'y'
    return ''



def checkPath_1(board:list,space_1:list,space_2:list):
    """
    This function: Checks whether two space are next to each other
    Call with 3 values: Game board and two spaces for checking
    Return 1 value: Boolean True or False, depending on result
    """
    same_axis = checkAxis(space_1,space_2)
    if same_axis == '':
        return False ### Not on same axis

    # Same x-axis
    if same_axis == 'x':
        # Check if next to each other on x-axis
        if (space_1[1] == (space_2[1] + 1)) or (space_1[1] == (space_2[1] - 1)):
            return True

    # Same y-axis
    elif same_axis == 'y':
        # Check if next to each other on y-axis
        if (space_1[0] == (space_2[0] + 1)) or (space_1[0] == (space_2[0] - 1)):
            return True
    
    return False



def checkPath_2(board:list,space_1:list,space_2:list):
    """
    This function: Checks whether two space on same axis can be connected
    Call with 3 values: Game board and two spaces for checking
    Return 1 value: Boolean True or False
    """
    # Check whether they are on the same axis
    same_axis = checkAxis(space_1,space_2)
    if same_axis == '':
        return False

    # Same x-axis
    if same_axis == 'x':
        # Check which index is larger
        if space_1[1] > space_2[1]:
            temp_a = space_2[1]
            temp_b = space_1[1]
        else:
            temp_a = space_1[1]
            temp_b = space_2[1]
        # Check whether space in the middle is empty
        for i in range((temp_a + 1),temp_b): # Must be a+1 and b or otherwise it will check themself
            if board[space_1[0]][i] != 0:
                return False
    
    # Same y-axis
    elif same_axis == 'y':
        # Check which index is larger
        if space_1[0] > space_2[0]:
            temp_a = space_2[0]
            temp_b = space_1[0]
        else:
            temp_a = space_1[0]
            temp_b = space_2[0]
        # Check whether space in the middle is empty
        for i in range((temp_a + 1),temp_b): # Must be a+1 and b or otherwise it will check themself
            if board[i][space_1[1]] != 0:
                return False

    return True



def checkPath_3(board:list,space_1:list,space_2:list):
    """
    This function: Checks whether two space can be connected with one turn
    Call with 3 values: Game board and two spaces for checking
    Return 2 values: Boolean True or False, with successful turn space or two fail spaces
    """
    fail_path = [] # May be removed in later versions
    # First attempt
    temp_space = [space_2[0],space_1[1]] # Seprate one turn to two single line
    check_status = checkPath_2(board,space_1,temp_space) and board[space_2[0]][space_1[1]] == 0 # Check first line
    if check_status:
        check_status = checkPath_2(board,temp_space,space_2) # Check second line
        if check_status:
            return True,temp_space # Return successful turn location
    fail_path.append(temp_space)

    # Second attempt
    temp_space = [space_1[0],space_2[1]]
    check_status = checkPath_2(board,space_1,temp_space) and board[space_1[0]][space_2[1]] == 0 # Check first line
    if check_status:
        check_status = checkPath_2(board,temp_space,space_2) # Check second line
        if check_status:
            return True,temp_space # Return successful turn location
    fail_path.append(temp_space)

    return False,fail_path



def checkPath_4(board:list,space_1:list,space_2:list):
    """
    This function: Checks whether two space can be connected with two turn
    Call with 3 values: Game board and two spaces for checking
    Return 2 values: Boolean True or False, with successful path or empty list when fail
    """
    # Loop A
    for i in range(len(board)):
        if board[i][space_1[1]] == 0: # Check if temp space is empty
            if checkPath_2(board,space_1,[i,space_1[1]]): # Check connection with origin and temp
                status,path = checkPath_3(board,[i,space_1[1]],space_2) # Check connection with temp and final
                if status:
                    return True,[[i,space_1[1]],path] # Return True with correct path
    
    # Loop B
    for i in range(len(board[0])):
        if board[space_1[0]][i] == 0: # Check if space is empty
            if checkPath_2(board,space_1,[space_1[0],i]): # Check connection with origin and temp
                status,path = checkPath_3(board,[space_1[0],i],space_2) # Check connection with temp and final
                if status:
                    return True,[[space_1[0],i],path] # Return True with correct path
    
    return False,[] # Return False with empty path



def blockCheck(board:list,space_1:list,space_2:list):
    """
    This function: Checks whether two space are same and not zero
    Call with 3 values: Game board and two spaces for checking
    Return 1 value: Boolean True or False
    """
    # Check if zero
    if board[space_1[0]][space_1[1]] == 0:
        return False
    # Check if same
    if board[space_1[0]][space_1[1]] == board[space_2[0]][space_2[1]]:
        return True
    return False



def gameOver(board:list):
    """
    This function: Checks whether the game is ended or not
    Call with 1 value: Game board
    Return 1 value: Boolean True or False
    """
    # Check if it is empty
    flag = True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                flag = False
    if(flag):
        return True,"clear"

    # Check whether the remaining spaces can still be linked.
    for i in range(len(board)):
        for j in range(len(board[0])):
            for k in range(len(board)):
                for l in range(len(board[0])):
                    if board[i][j] == board[k][l]:
                        space1 = [0,0]
                        space2 = [0,0]
                        space1[0] = i
                        space1[1] = j
                        space2[0] = k
                        space2[1] = l
                        checkResult_3,temp = checkPath_3(board,space1,space2)
                        checkResult_4,temp = checkPath_4(board,space1,space2)
                        if(checkPath_1(board,space1,space2) or checkPath_2(board,space1,space2) or checkResult_3 or checkResult_4):
                            return False,"continue"
    
    return True,"unsolve"



def algotithm(board:list,pointer_a:list,pointer_b:list):
    """
    This function: Pass values to all Checks one by one to find path
    Call with 3 values: Game board and two spaces for checking
    Return 1 value: Boolean True or False
    """
    
    # Reject different block
    if not blockCheck(board,pointer_a,pointer_b):
        return False
    # Check all 4 check
    if checkPath_1(board,pointer_a,pointer_b):
        print("Check 1 Pass")
        return True
    if checkPath_2(board,pointer_a,pointer_b):
        print("Check 2 Pass")
        return True
    checkResult_3,temp = checkPath_3(board,pointer_a,pointer_b)
    if checkResult_3:
        print("Check 3 Pass")
        return True
    checkResult_4,temp = checkPath_4(board,pointer_a,pointer_b)
    if checkResult_4:
        print("Check 4 Pass")
        return True
    
    return False



def gameInitialize(level:int):
    """
    This parameter: Pass the correct parameters to start game by providing level
    Call with 1 values: Game level
    """
    print("Game level:",level)
    if level == 0:
        print("Size: 10*10\nElements: 5")
        gameboardGUI(10,10,5)
    elif level == 1:
        print("Size: 10*10\nElements: 10")
        gameboardGUI(10,10,10)
    elif level == 2:
        print("Size: 20*20\nElements: 50")
        gameboardGUI(20,20,50)



def getDifficulty(size_x:int,size_y:int,numb_elements:int):
    if size_x == 10 and numb_elements == 5:
        return 'Easy'
    elif size_x == 10 and numb_elements == 10:
        return 'Medium'
    elif size_x == 20 and numb_elements == 50:
        return 'Hard'



def menuGUI():
    pygame.init() # Initialize Pygame

    # Initialize menu board
    size = 800,800 # Width,height
    background = (200,191,231)

    # Load img resources
    img_level = []
    for i in range(3):
        img_level.append(pygame.image.load("./src/img/level-{i}.png".format(i=i)))
    img_menu_text = []
    for i in range(2):
        img_menu_text.append(pygame.image.load("./src/img/menu_text-{i}.png".format(i=i)))
    img_pointer = pygame.image.load("./src/img/pointer.png")
    msg_loading = pygame.image.load("./src/img/message-4.png")

    # Get image position
    position = img_pointer.get_rect()
    # Create screen
    screen = pygame.display.set_mode(size)
    # Title
    pygame.display.set_caption("Link Link Game")
    
   
    level_pointer = 0
    start = True # Check if initialized
    # Main loop
    flag = True
    status_menu = False

    while flag:
        # Initialize number of pixels to move
        time.sleep(0.05)
        site = [0,0]
        if start:
            site = [240,400]
            start = False

        level_pointer_new = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Move by key in
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_UP:
                    print("KEYDOWN: UP")
                    level_pointer_new -= 1
                if event.key == pygame.K_DOWN:
                    print("KEYDOWN: DOWN")
                    level_pointer_new += 1
                if event.key == pygame.K_SPACE:
                    print("KEYDOWN: SPACE")
                    status_menu = True
        
        # Find new space
        if level_pointer_new == -1: # Move UP
            if level_pointer == 0: # If at top
                site = [0,200]
                level_pointer = 2
            else: # If at middle or bottom
                site = [0,-100]
                level_pointer -= 1
        if level_pointer_new == 1: # Move down
            if level_pointer == 2: # If at bottom
                site = [0,-200]
                level_pointer = 0
            else: # If at top or middle
                site = [0,100]
                level_pointer += 1

        # Move selection box
        position = position.move(site)

        # Fill background
        screen.fill(background)
        # Display resources
        for i in range(3): # Display level image
            screen.blit(img_level[i],(240,(100*i+400)))
        for i in range(2): # Display menu text
            screen.blit(img_menu_text[i],(80,(100*i+100)))
        screen.blit(img_pointer,position)
        # Update display
        pygame.display.flip()

        if status_menu:
            screen.fill(background)
            screen.blit(msg_loading,(160,160))
            flag = False
            pygame.display.flip()

        if not flag:
            gameInitialize(level_pointer)
            pygame.quit()



def gameboardGUI(size_x:int,size_y:int,numb_elements:int):
    # Initialize game board
    board = newBoard(size_y,size_x)
    board = insertElement(board,numb_elements)

    pygame.init() # Initialize Pygame

    # Initialize menu board
    size = (size_x*50),(size_y*50)
    background = (200,191,231)

    # Load img resources
    img_numb = []
    for i in range(51):
        img_numb.append(pygame.image.load("./src/img/numb-{i}.png".format(i=i)))
    img_pointer_a = pygame.image.load("./src/img/pointer-2.png")
    img_pointer_b = pygame.image.load("./src/img/pointer-3.png")
    msg_congratulation = pygame.image.load("./src/img/message-1.png")
    msg_game_over = pygame.image.load("./src/img/message-2.png")
    msg_return_menu = pygame.image.load("./src/img/message-3.png")

    # Create screen
    screen = pygame.display.set_mode(size)
    # Title
    pygame.display.set_caption("Link Link Game - {difficulty}".format(difficulty = getDifficulty(size_x,size_y,numb_elements)))
    
    pointer_fixed = [0,0]
    pointer_move = [0,0]
    counter_used_pointers = 0
    # Main loop
    flag = True
    status_menu = False

    while flag:
        # Initialize number of pixels to move
        #site = [0,0]
        pointer_temp = [0,0]
        time.sleep(0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Key in
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    status_menu = True
                if event.key == pygame.K_UP:
                    print('KEYDOWN: UP')
                    pointer_temp[0] -= 1
                if event.key == pygame.K_DOWN:
                    print('KEYDOWN: DOWN')
                    pointer_temp[0] += 1
                if event.key == pygame.K_LEFT:
                    print('KEYDOWN: LEFT')
                    pointer_temp[1] -= 1
                if event.key == pygame.K_RIGHT:
                    print('KEYDOWN: RIGHT')
                    pointer_temp[1] += 1
                # Store movement
                pointer_move[0] += pointer_temp[0]
                pointer_move[1] += pointer_temp[1]
                # Check overflow
                for i in range(2):
                    if pointer_move[i] >= len(board):
                        pointer_move[i] -= len(board)
                        pointer_temp[i] -= len(board)
                    elif pointer_move[i] < 0:
                        pointer_move[i] += len(board)
                        pointer_temp[i] += len(board)

                if event.key == pygame.K_SPACE:
                    print('KEYDOWN: SPACE')
                    if (board[pointer_move[0]][pointer_move[1]] != 0) and (pointer_move != pointer_fixed): # If empty, do not store ### Check if same (bug 3)
                        counter_used_pointers += 1
                        if counter_used_pointers == 1: # Store move pointer to fixed pointer
                            pointer_fixed[0] = pointer_move[0]
                            pointer_fixed[1] = pointer_move[1]
                            #pointer_move = [0,0] ### Do not reset move pointers!!
        
        

        # Check when two elements ready
        if counter_used_pointers == 2:
            if algotithm(board,pointer_fixed,pointer_move):
                print("True")
                # Remove two elements
                board = removeElement(board,pointer_fixed)
                board = removeElement(board,pointer_move)
            else:
                print("False")
            # Reset pointers
            pointer_fixed = [0,0]
            #pointer_move = [0,0] ### Do not reset move pointers!!
            counter_used_pointers = 0

        # DEBUG
        if pointer_temp != [0,0]:
            print("Movement:",pointer_temp)
            print("Pointer A position:",pointer_move)

        # Check game over
        status_over,type_over = gameOver(board)

        # Output
        # Fill background
        screen.fill(background)

        # Print board
        for i in range(len(board)):
            for j in range(len(board[0])):
                screen.blit(img_numb[board[i][j]],((j*50),(i*50))) ### Reverse x-axis and y-axis!!!!!

        # Set pointer A
        screen.blit(img_pointer_a,((pointer_move[1] * 50),(pointer_move[0] * 50)))

        if counter_used_pointers == 1: # Hide fixed pointer if first one does not exist
            screen.blit(img_pointer_b,((pointer_fixed[1] * 50),(pointer_fixed[0] * 50))) ### Must pass in turple like"(y,x)"
        else:
            screen.blit(img_pointer_b,(-50,-50)) ### Must pass in turple like"(y,x)"

        # Get message centre position
        position_y_msg = ((size_x * 50 / 2) - 240)
        position_x_msg = (size_x * 50 / 4)

        # Display message
        if status_over: # If game over
            if type_over == "clear":
                screen.blit(msg_congratulation,((position_y_msg),(position_x_msg)))
            elif type_over == "unsolve":
                screen.blit(msg_game_over,((position_y_msg),(position_x_msg)))
        
        # Update display
        pygame.display.flip()

        if status_over:
            print(pygame.time.wait(3000)) # Wait 3000ms
            status_over = False
            status_menu = True
        
        if status_menu:
            screen.fill(background)
            screen.blit(msg_return_menu,((position_y_msg),(position_x_msg)))
            flag = False
            pygame.display.flip()

        if not flag:# Return to menu
            menuGUI()
            pygame.quit()



menuGUI()
