import pygame
import sys
import random


# pygame初始化
pygame.init()
size = width, height = 900, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
# 游戏参数设置
# 声音
fly_sound = pygame.mixer.Sound('fly.wav')
gg_sound = pygame.mixer.Sound('gg.wav')
play_sound = True
# 颜色
red = 255, 0, 0
black = 0, 0, 0
white = 255, 255, 255
green = 0, 128, 0
# 字体
font = pygame.font.SysFont('Arial', 40)
# 分数
score = 0
score_surf = font.render(str(score), True, black)
score_rect = pygame.Rect(0, 0, 100, 50)
# GG文字
fail_text = font.render('GAME OVER!', True, red)
text_width, text_height = 200, 100
fail_rect = pygame.Rect((width - text_width) / 2,
                        (height - text_height) / 2,
                        text_width, text_height)
# 小鸟
bird = pygame.image.load('bird.png').convert()
bird_left = 200
bird_top = 100
bird_rect = bird.get_rect(left=bird_left, top=bird_top)
bird_speed = 1
# 管道
pipeline_list = []
pipeline_width = 30
pipeline_speed = 2
old_time = 0
game_over = False

while True:
    # 事件响应
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -6
                # 重开游戏
                if game_over:
                    game_over = False
                    play_sound = True
                    bird_speed = 1
                    pipeline_speed = 2
                    bird_rect = bird.get_rect(left=bird_left, top=bird_top)
                    score_surf = font.render(str(score), True, black)
                    pipeline_list = []
                else:
                    fly_sound.play()
    # 碰撞检测
    for pipeline in pipeline_list:
        if bird_rect.colliderect(pipeline):
            game_over = True
    # 出界检测
    if bird_rect[1] < 0 or bird_rect[1] > height:
        game_over = True
    # 游戏结束
    if game_over:
        bird_speed = pipeline_speed = score = 0
        old_time = pygame.time.get_ticks() - 1500
        if play_sound:
            gg_sound.play()
            play_sound = False
    # 鸟的运动
    bird_speed += 0.2
    bird_rect = bird_rect.move(0, int(bird_speed))
    # 2秒节点
    new_time = pygame.time.get_ticks()
    if new_time - old_time > 2000:
        # 生成管道
        old_time = new_time
        pass_height = random.randint(100, 230)
        pass_begin = random.randint(20, 230)
        pipeline_list.append(pygame.Rect(width, 0, pipeline_width, pass_begin))
        pipeline_list.append(pygame.Rect(
            width, pass_begin + pass_height, pipeline_width, height - pass_begin - pass_height)
        )
        # 计算分数
        for pipeline in pipeline_list:
            if pipeline[0] < bird_left - pipeline_width:
                score += 1
                score_surf = font.render(str(score), True, black)
                break
    # 管道移动
    for pipeline in pipeline_list:
        pipeline[0] -= pipeline_speed
        if pipeline[0] < 0:
            pipeline_list.remove(pipeline)
    # 屏幕绘制
    screen.fill(white)
    screen.fill(red, (0, 0, width, 2))
    screen.fill(red, (0, height - 2, width, 2))
    for pipeline in pipeline_list:
        screen.fill(green, pipeline)
    screen.blit(score_surf, score_rect)
    screen.blit(bird, bird_rect)
    if game_over:
        screen.blit(fail_text, fail_rect)
    # 设置帧率
    clock.tick_busy_loop(60)
    pygame.display.flip()
