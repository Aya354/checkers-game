import pygame
#                                           constants

WIDTH, HEIGHT = 600, 600  #dimensions of the window
ROWS, COLUMNS = 8, 8    #number of squares in each row and column
SQUARE_SIZE = WIDTH//COLUMNS  #size of each square

# colors in RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('E:\\year 3\\AI_Project\\CROWN.png'), (44, 25))
###########################################################################################################
#                                              piece



########################################################################################################################
#                                              board



###################################################################################################################
#                                              game



######################################################################################################################
#                                             algorithms



###########################################################################################################################
#                                             main
# Frames per Second
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
global difficulty_level 
difficulty_level = 1

def draw_winner(winner): 
        run = True
        pygame.display.set_caption('GAME OVER')
        while run:
            WIN.fill(GREY)
            pygame.font.init()
            font = pygame.font.SysFont('arial', 60)
            font2 = pygame.font.SysFont('arial',40)
            WIN.blit(font.render("GAME OVER", True, YELLOW), (150,150))
            if winner == WHITE:
                line2 = font2.render("WHITE (AGENT) WON", True, YELLOW)
            else:
                line2 = font2.render("RED (RANDOM) WON", True, YELLOW)       
            text_rect = line2.get_rect()
            text_rect.center = (WIDTH/2, HEIGHT/2-20)
            WIN.blit(line2,text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
        pygame.quit()
import pygame_gui
def selections():
    pygame.init()

    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((600, 600))

    algorithm_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 75), (100, 50)),
                                             text='Algorithm',
                                             manager=manager)

    algorithm_options = ['Alpha-beta', 'Minimax']
    algorithm_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((250, 125), (100, 75)),
                                                       item_list=algorithm_options,
                                                       manager=manager)

    difficulty_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 225), (100, 50)),
                                               text='Difficulty',
                                               manager=manager)

    difficulty_options = ['Easy', 'Hard']
    difficulty_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((250, 275), (100, 75)),
                                                        item_list=difficulty_options,
                                                        manager=manager)

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 375), (100, 50)),
                                            text='Start',
                                            manager=manager)

    run = True
    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        algorithm = algorithm_select.get_single_selection()
                        difficulty = difficulty_select.get_single_selection()
                        return algorithm, difficulty
                        # Pass the selected algorithm and difficulty to your main function here

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill((255, 255, 255))
        manager.draw_ui(screen)
        pygame.display.update()
