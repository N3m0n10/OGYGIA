import pygame
from ball import ball
from math import atan2, pi , sqrt
from random import randint, random

###PYGAME SETUP
pygame.init()
WIDTH, HEIGHT = 720,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
win_font = pygame.font.SysFont('Times New Roman', 70)
s_p_font = pygame.font.SysFont('Times New Roman', 30)
select_player_text = s_p_font.render("Press 0 for 1p or 1 for 2p", True, (90, 100, 240))

###VARS SETUP
touch_token = 0
ball_min_speed = 3
ball_max_speed = 13
ball_radius = 20  #y_side
ball_start_color = "white"
ball1 = ball(screen,ball_start_color,ball_radius,ball_max_speed,ball_min_speed)
circle_radius = 300
recta = pygame.Rect(60, 60, circle_radius*2, circle_radius*2)
colide = None
player1_color = "blue"
opponent_color = ["red","orange"]
max_points = 3
points = [0 , 0]
wait = True
win = False
winner = ''
time_restart = 0
next_ball_vel = [0,0]

class arc_player():
    def __init__(self,screen, color, rectangle, player_num,format = "arc"):
        self.format = format
        self.screen = screen
        self.color = color
        self.player_num = player_num
        self.movement_keys = [[None],\
                              [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d], \
                              [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]]
        self.rect = rectangle
        if self.player_num == 0 or self.player_num == 2:
            self.last_ang = pi
        else:
            self.last_ang = 0

    ###REMAKING THE MOVE SINCE THE INCOMPATIBILITY --- UNNEDED FOR UNRESTRICTED MOVESET
    def arc_move(self, movement_keys ,  keys, clock, ball_pos_y , ball_pos_x):
        ##BOT config --- TO BE DONE
         
    #CHANGE TO ELSE:
        if self.player_num != 0:
            if keys[movement_keys[0]]:  
                self.last_ang -= 0.1
            if keys[movement_keys[1]]:
                self.last_ang += 0.1
        if self.last_ang > 2*pi:
            self.last_ang -= 2*pi
        elif self.last_ang < 0:
            self.last_ang += 2*pi

    def arc_atualize(self,dt ,ball_pos_y , ball_pos_x ): 
        keys = pygame.key.get_pressed()
        self.arc_move( self.movement_keys[self.player_num], keys, dt, ball_pos_y, ball_pos_x)
        pygame.draw.arc(self.screen,self.color , self.rect,self.last_ang,self.last_ang+pi/4,10) #change second angle in the future #make bonus itens, etc
        
        return self.last_ang, self.last_ang+pi/4
    
def placar(screen, pontos_1 , pontos_2, pos_1 = (380,100), pos_2 = (900,100)): #make arg
    text_placar_font = pygame.font.SysFont('tahoma', 100) 
    text_placar1 = text_placar_font.render(f'{pontos_1}', True, ('White'))
    text_placar2 = text_placar_font.render(f'{pontos_2}', True, ('White'))
    screen.blit(text_placar1,pos_1)
    screen.blit(text_placar2,pos_2)
    p1_points_rect = text_placar1.get_rect(topleft = pos_1)
    op_points_rect = text_placar1.get_rect(topleft = pos_2)
    return p1_points_rect , op_points_rect
    
    
def is_ball_in_arc(ball_angle, start_ang, end_ang):
    if start_ang < end_ang:
        return start_ang <= ball_angle <= end_ang
    else:
        #return ball_angle >= start_ang or ball_angle <= end_ang
        return  start_ang >=  ball_angle >= end_ang

def score(points_,colide_,max_points_,cld_brder):  #fix vars
    global colide
    if cld_brder == True:
        return_to_start_pos()
        ball1.clean_colison()
        if colide_ != None:
            points_[colide_] += 1
            colide = None
            end_game(max_points_,points_)

def handle_collision(player_hit, ball1, dx, dy, ball_max_speed, player_color, opponent_color, players):
    # 1. Reflect the velocity
    velocity_vec = pygame.Vector2(ball1.ball_vel_x, ball1.ball_vel_y)
    normal_vec = pygame.Vector2(dx, dy).normalize()
    reflected_vel = velocity_vec.reflect(normal_vec)

    # 2. Increase speed a bit, but clamp to max
    if reflected_vel.length() < ball_max_speed:
        reflected_vel.scale_to_length(min(ball_max_speed, reflected_vel.length() + 0.3))

    # 3. Randomize X/Y split of the speed vector (without changing direction)
    angle_noise = (random() - 0.5) * 0.3  # small angle change: +/- 15 degrees
    reflected_vel = reflected_vel.rotate(angle_noise * 180)

    # 4. Assign new velocity
    ball1.ball_vel_x = reflected_vel.x
    ball1.ball_vel_y = reflected_vel.y

    # 5. Choose color
    if player_hit == 0:
        ball1.chose_color(player_color)
    else:
        ball1.chose_color(opponent_color[players])

def return_to_start_pos():
    ball1.chose_color(ball_start_color)
    ball1.atualize(clock, (WIDTH, HEIGHT), True,[360,360])
    global wait
    global time_restart
    time_restart = pygame.time.get_ticks() #start timer-
    wait = True

def end_game(max_points,points):
    global win
    global winner
    if points[0] == max_points:
        winner = "PLAYER 1"
        win = True
    elif points[1] == max_points:
        win = True
        if players == 1:
            winner = "PLAYER 2"
        else:
            winner = "BOT"

def winning_screen(t_winner):
    finish_text = win_font.render("PRESS ANY KEY", True, (90, 100, 240))
    finish_text_ln_2 = win_font.render("TO EXIT", True, (90, 100, 240))
    winning_text = win_font.render(f"{t_winner} WON", True, (90, 100, 240))
    screen.blit(winning_text, (120,120))
    screen.blit(finish_text, (20,500))
    screen.blit(finish_text_ln_2, (20,600))
    

###PLAYERS SETUP --- CHECK IF MULTIPLAYER OR VS BOT
player1 = arc_player(screen, player1_color , recta,1)
 

###LOOP
runing = True
game = False
select_player = True
while runing:
    while select_player:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and win:
                runing = False
                select_player = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    players = 0
                    opponent = arc_player(screen, opponent_color[0] , recta,0)
                    select_player = False
                    game = True
                elif event.key == pygame.K_1:
                    players = 1
                    opponent = arc_player(screen, opponent_color[1] , recta,2)
                    select_player = False
                    game = True

        screen.fill("black")
        screen.blit(select_player_text, (190,240))
        pygame.display.flip()
        clock.tick(10)
        

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and win:
                runing = False
                game = False
            
        
        screen.fill("black")
        placar(screen,points[0],points[1],(200,200),(520,200))

        if win == False:
            p1_ang = player1.arc_atualize(clock , ball1.player_pos.y , ball1.player_pos.x)
            p2_ang = opponent.arc_atualize(clock, ball1.player_pos.y , ball1.player_pos.x) 
            

            ###Pause from ball exit
            if wait == True:
                match next_ball_vel:
                    case [0,0]:
                        next_ball_vel = [randint(-ball_max_speed,ball_max_speed),randint(-ball_max_speed,ball_max_speed)]
                ball1.atualize(clock, (WIDTH, HEIGHT), True,[360,360])
                actual_ticks = pygame.time.get_ticks()
                text = win_font.render("PREPARE", True, "white")
                pygame.draw.line(screen, "RED", (360, 360), (360 + 2*next_ball_vel[0], 360 + 2*next_ball_vel[1]), 5)
                screen.blit(text, [230, 650])
                if actual_ticks - time_restart >= 3000:
                    wait = False
            else:
                ball1.atualize(clock, (WIDTH, HEIGHT),ball_should_not_stop=[True,next_ball_vel[0],next_ball_vel[1]])
                next_ball_vel = [0,0] 

            ##collision
            ###1. the posiion of ball pos will be checked, if its on the circle the next stage comes
            ###2. The angle of the ball will be checked, if its on the arc collision occours
                dx = ball1.player_pos.x - 360 
                dy = ball1.player_pos.y - 360
                distance = sqrt(dx**2 + dy**2)
                if 330 >= (distance + ball_radius) >= circle_radius:
                    if touch_token == 0: #makes sure the collision only happens once
                        ball_angle = atan2(-dy, dx) #ball angle -> make variable
                        if ball_angle < 0:
                            ball_angle += 2 * pi  # Ensure the angle is in [0, 2*pi]
                        match is_ball_in_arc(ball_angle, p1_ang[0], p1_ang[1]):
                            case True:
                                if touch_token == 0:
                                    colide = 0
                                    touch_token = 15
                                    handle_collision(0, ball1, dx, dy, ball_max_speed, player1_color, opponent_color, players)

                        match is_ball_in_arc(ball_angle, p2_ang[0], p2_ang[1]):
                            case True:
                                if touch_token == 0:
                                    colide = 1
                                    touch_token = 15
                                    handle_collision(1, ball1, dx, dy, ball_max_speed, player1_color, opponent_color, players)

                                    #ball1.ball_vel_x = ball1.ball_vel_x - 2 * dot_product * normal[0] + random_vel_factor  # [old_ver]
                                    #ball1.ball_vel_y = ball1.ball_vel_y - 2 * dot_product * normal[1] + random_vel_factor

            #if sqrt(ball1.player_pos.y**2 + ball1.player_pos.x**2) is in  p1_pos_list:
                
                score(points,colide,max_points,ball1.collide_border)

                if touch_token > 0:
                    touch_token -= 1


            pygame.draw.arc(screen, "red", recta, 0, 2*pi)


        else:
            winning_screen(winner)


        pygame.display.flip()
        clock.tick(60)

pygame.quit()