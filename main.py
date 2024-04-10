import pygame
import random
import asyncio

pygame.init()
pygame.font.init()
# pygame.mixer.init()

# Game setup
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Vayun Jumps")
timer = pygame.time.Clock()
font = pygame.font.Font("DoodleJump_v2.ttf", 16)
super_jump_font = pygame.font.Font("DoodleJump_v2.ttf", 20)
go_font = pygame.font.Font("DoodleJump_v2.ttf", 24)
# jump_sound = pygame.mixer.Sound("boing.mp3")
# go_sound = pygame.mixer.Sound("game_over.mp3")

white = (255, 255, 255)
black = (0, 0, 0)
background = white
player = pygame.transform.scale(pygame.image.load("doodle.png"), (150, 160))
fps = 60
score = 0
high_score = 0
game_over = False
score_last = 0
super_jump = 2
jump_last = 0
count_sound = 1

# Game variables
player_x = 130
player_y = 330
platforms = [[168, 480, 75, 10], [85, 370, 75, 10], [265, 330, 75, 10], [175, 260, 75, 10], [85, 200, 75, 10], [60, 100, 75, 10], [265, 100, 75, 10]]
jump = False
y_change = 0
x_change = 0
player_speed = 5

# Update player position (y)
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = 0.4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

# Check collisions
def check_collisions(block_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(block_list)):
        platform = block_list[i]
        if jump == False and platform.colliderect([player_x, player_y+125, 77, 4]) and y_change > 0:
            if player_x + 78 > platform.right:
                j = False
            else:
                j = True
                # pygame.mixer.Sound.play(pygame.mixer.Sound("boing.mp3"))
    return j    

# Handle new platforms appearing as game progresses
def update_platforms(platforms_list, y_pos, change):
    global score
    if player_y < 100 and y_change < 0:
        for i in range(len(platforms_list)):
            platforms_list[i][1] -= change
    else:
        pass
    for item in range(len(platforms_list)):
        if platforms_list[item][1] > 500:
            platforms_list[item] = [random.randint(30, 320), random.randint(-50, -10), 75, 10]
            score += 1

    return platforms_list

async def main():
    running = True
    global fps
    global background
    global player
    global player_x
    global player_y
    global score
    global black
    global high_score
    global super_jump
    global platforms
    global count_sound
    global game_over
    global score_last
    global jump_last
    global y_change
    global x_change
    global player_speed
    global jump
    while running:
        timer.tick(fps)
        screen.fill(background)
        screen.blit(player, (player_x, player_y))
        blocks = []
        score_text = font.render('Score: ' + str(score), True, black, background)
        screen.blit(score_text, (340, 35))
        high_score_text = font.render('High Score: ' + str(high_score), True, black, background)
        screen.blit(high_score_text, (313, 15))
        super_jump_text = super_jump_font.render('Press e to super jump', True, black, background)
        screen.blit(super_jump_text, (100, 15))
        super_jump_avai = super_jump_font.render('Super Jumps remaining: ' + str(super_jump), True, black, background)
        screen.blit(super_jump_avai, (97, 35))

        for i in range(len(platforms)):
            block = pygame.draw.rect(screen, black, platforms[i], 0, 4)
            blocks.append(block)

        if game_over:
            if count_sound > 0:
                # pygame.mixer.Sound.play(pygame.mixer.Sound("game_over.mp3"))
                count_sound -= 1
            screen.fill(background)
            game_over_text = go_font.render("Game Over, press spacebar to restart ", True, black, background)
            screen.blit(game_over_text, (45, 200))
            game_over_score_text = go_font.render("Score: " + str(score), True, black, background)
            screen.blit(game_over_score_text, (155, 230))
            game_over_high_score_text = go_font.render("High Score: " + str(high_score), True, black, background)
            screen.blit(game_over_high_score_text, (140, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    score = 0
                    player_x = 130
                    player_y = 330
                    background = white
                    score_last = 0
                    super_jump = 2
                    jump_last = 0
                    count_sound = 1
                    platforms = [[168, 480, 75, 10], [85, 370, 75, 10], [265, 330, 75, 10], [175, 260, 75, 10], [85, 200, 75, 10], [60, 100, 75, 10], [265, 100, 75, 10]]
                if event.key == pygame.K_e and not game_over and super_jump > 0:
                    super_jump -= 1
                    y_change = -15
                if event.key == pygame.K_a:
                    x_change = -player_speed
                if event.key == pygame.K_d:
                    x_change = player_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    x_change = 0
                if event.key == pygame.K_d:
                    x_change = 0

        jump = check_collisions(blocks, jump)
        player_x += x_change
        if player_x < -20:
            player_x = -20
        elif player_x > 310:
            player_x = 310
        if player_y < 440:
            player_y = update_player(player_y)
        else:
            game_over = True
            y_change = 0
            x_change = 0
            
        platforms = update_platforms(platforms, player_y, y_change)

        if score > high_score:
            high_score = score
        
        if score - score_last > 30:
            score_last = score
            background = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))

        if score - jump_last > 50:
            jump_last = score
            super_jump += 1

        pygame.display.flip()

        await asyncio.sleep(0)
    # if not running:
    #     pygame.quit()
    #     return

asyncio.run(main())