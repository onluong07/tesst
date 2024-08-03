import random, sys, pygame
from pygame import mixer
def move_floor():
    screen.blit(floor,(floor_x,490))
    screen.blit(floor,(floor_x+432,490))
def create_pipe():
    random_pipe = random.choice(heigh_pipe)
    bottom_pipe = pipesuf.get_rect(midtop = (500,random_pipe))
    top_pipe = pipesuf.get_rect(midtop = (500,random_pipe-690))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipesuf,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipesuf,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <=-75 or bird_rect.bottom >=490:
        hit_sound.play()
        return False
    return True
def rotote_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*2,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird,new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (200,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (200,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High_Score:{int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (200,550))
        screen.blit(high_score_surface,high_score_rect)
def cul_score(pipes):
    global score
    collision = False
    for pipe in pipes:
        if pipe.centerx < bird_rect.centerx and pipe.centerx == 45:
            collision = True
    if collision:
        return True
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.init()
gravity = 0.25
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400,600))
pygame.display.set_caption('Flappy Bird')
game_active = True
game_font = pygame.font.Font('04B_19.ttf',40)
#score
score = 0
high_score = 0
Score = True
# background
bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png')).convert()
#floor
floor = pygame.transform.scale2x(pygame.image.load('assets/floor.png')).convert()
floor_x = 0
#bird
birddown = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png')).convert_alpha()
birdmid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png')).convert_alpha()
birdup = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png')).convert_alpha()
bird_movement = 0
bird_list = [birddown,birdmid,birdup]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (50,200))
# timer bird
flap_bird = pygame.USEREVENT + 1
pygame.time.set_timer(flap_bird,200)
#pipe
pipesuf = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png')).convert()
pipe_list=[]
heigh_pipe =[250,260,270,280,290,300,310,320,330,340,350]
spawm_pipe = pygame.USEREVENT
pygame.time.set_timer(spawm_pipe,1000)
# music
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
#ending
game_over = pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect = game_over.get_rect(center = (200,300))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                bird_movement =-8
                flap_sound.play()
        if event.type == pygame.KEYDOWN and game_active == False:
            game_active = True
            bird_movement = 0
            bird_rect.center = (50,200)
            pipe_list.clear()
        if event.type == spawm_pipe:
            pipe_list.extend(create_pipe())
        if event.type == flap_bird:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    screen.blit(bg,(0,0))
    if game_active:
        #bird
        bird_movement += gravity
        bird_rect.centery += bird_movement 
        rototed_bird = rotote_bird(bird)
        screen.blit(rototed_bird,bird_rect)
        game_active = check_collision(pipe_list)
        #pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        #score
        if cul_score(pipe_list):
            score += 1
            score_sound.play()
        #floor
        floor_x -= 1
        if floor_x <= -432:
            floor_x = 0
        move_floor()
        score_display('main game')
    else:
        high_score = update_score(score,high_score)
        screen.blit(game_over,game_over_rect)   
        score_display('game over')
        score = 0
    pygame.display.update()
    clock.tick(100)