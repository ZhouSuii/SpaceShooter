import pgzrun
import random 
import pygame
WIDTH = 512 
HEIGHT = 768   
TITLE = 'Battle Plane'

pygame.init()

# import background
background1 = Actor('background1') 
background2 = Actor('background1')
background1.x = WIDTH / 2      
background1.y = HEIGHT / 2     
background2.x = WIDTH / 2       
background2.y = -HEIGHT / 2     

# import hero
hero = Actor('ship_fullhealth')  # 导入玩家飞机图片
hero.x = WIDTH/2      # 设置玩家飞机的x坐标
hero.y = HEIGHT*2/3   # 设置玩家飞机的y坐标
HP = 100
invincible = False
invincible_time = 1000
invincible_start = 0
last_shoot_time = 0

# import bullet
bullet = Actor('bullet1')  # 导入子弹图片
bullets = []              # 创建子弹列表
bullet.x = hero.x         # 设置子弹的x坐标
bullet.y = -HEIGHT        # 设置子弹的y坐标

# import emeny
enemy = Actor('enemy')    # 导入敌机图片
enemy.x = WIDTH/2         # 设置敌机的x坐标
enemy.y = 0               # 设置敌机的y坐标

# import enemy bullet
enemy_bullet = Actor('bullet')        # 导入敌机子弹图片
enemy_bullets = []                    # 创建敌机子弹列表
enemy_bullet.x = enemy.x              # 设置敌机子弹的x坐标
enemy_bullet.y = enemy.y              # 设置敌机子弹的y坐标

# import Boss
boss_bullets = []
boss = Actor('bossman2')  # 导入boss图片
boss.x = WIDTH / 2         # 设置boss的x坐标
boss.y = -150              # 设置boss的y坐标，开始在屏幕外面
boss.health = 10           # 设置boss的生命值
boss.active = False        # 设置boss是否激活，默认为不激活# Boss属性
boss_speed = 2             # boss的速度
boss_direction = 1         # boss的移动方向，1为向右，-1为向左
boss_score = 10             # 出现boss时的得分
boss_bullet_interval = 1000  # boss子弹发射间隔
number = 5                 # boss子弹数量

# import final boss
final_boss = Actor('final_boss')  # 导入boss图片

# import shield
shield = Actor('shield')  # 导入shield图片
shield.x = -WIDTH
shield.y = 0
shield_interval = 30000
last_shield_time = 0
has_shield = False
shield_duration = 5000
shield_start = 0

# score
score = 0
isLoose = False # 游戏是否失败，初始不失败
# sounds. game_music.play(-1)  # 循环播放背景音乐

# 定义一个函数来创建新的boss子弹
def create_boss_bullet():
    global last_shoot_time, number
    current_time = pygame.time.get_ticks()  # 获取当前时间
    if current_time - last_shoot_time >= boss_bullet_interval / 3:
        number = number - 1
        if number == 0:
            number = 5
            last_shoot_time = current_time
        
        new_bullet = Actor('bullet')  # 使用boss子弹的图片
        new_bullet.x = boss.x
        new_bullet.y = boss.y
        boss_bullets.append(new_bullet)
        

def draw():
    global invincible_start, invincible, invincible_time, isLoose, has_shield, shield_sprite
    background1.draw()      # draw background1
    background2.draw()      #a draw background2
    shield.draw()           # draw shield

    if invincible:
        current_time = pygame.time.get_ticks()
        if current_time - invincible_start >= invincible_time:
            if current_time - invincible_start >= invincible_time:
                if (current_time - invincible_start) % 100 < 50:
                    hero.draw()
    else:
        hero.draw()         # draw hero
    for bullet in bullets:
        bullet.draw()       # draw bullet
    enemy.draw()            # draw enemy
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw() # draw enemy bullet
    for b_bullet in boss_bullets:  # boss子弹
        b_bullet.draw()

    screen.draw.text("得分: "+str(score), (200, HEIGHT-50), fontsize=30,
                     fontname='s', color='black')

    # 绘制玩家的生命值条
    player_health_bar_length = 100  # 生命值条的总长度
    player_health_bar_height = 10  # 生命值条的高度
    player_health_bar_x = 10  # 生命值条的x坐标，左上角
    player_health_bar_y = 10  # 生命值条的y坐标，左上角

    # 绘制生命值条背景
    screen.draw.filled_rect(Rect((player_health_bar_x, player_health_bar_y), (player_health_bar_length, player_health_bar_height)), "red")

    # 根据玩家的当前生命值绘制生命值条前景
    player_health_bar_current_length = (HP / 10) * player_health_bar_length
    screen.draw.filled_rect(Rect((player_health_bar_x, player_health_bar_y), (player_health_bar_current_length, player_health_bar_height)), "green")

    # 只有boss处于激活状态时才绘制boss
    if boss.active:
        boss.draw()  # 绘制boss
        # 显示boss的生命值
        # screen.draw.text("Boss Health: " + str(boss.health), (10, 10), color="white")

        # 绘制生命值条
        health_bar_length = 100  # 生命值条的总长度
        health_bar_height = 10  # 生命值条的高度
        health_bar_x = boss.x - health_bar_length / 2  # 生命值条的x坐标
        health_bar_y = boss.y + boss.height / 2 + 10  # 生命值条的y坐标

        # 绘制生命值条背景
        screen.draw.filled_rect(Rect((health_bar_x, health_bar_y), (health_bar_length, health_bar_height)), "red")

        # 根据boss的当前生命值绘制生命值条前景
        health_bar_current_length = (boss.health / 10) * health_bar_length
        screen.draw.filled_rect(Rect((health_bar_x, health_bar_y), (health_bar_current_length, health_bar_height)), "green")

    if isLoose:  # 游戏失败后输出信息
        screen.draw.text("游戏失败！", (50, HEIGHT/2), fontsize=90,fontname='s', color='red')


def create_enemy_bullet():
    global enemy_bullet
    global last_shoot_time
    current_time = pygame.time.get_ticks()  # 获取当前时间
    if current_time - last_shoot_time >= 500:
        new_enemy_bullet = Actor('bullet')  # create a new enemy bullet
        new_enemy_bullet.x = enemy.x        # set the x coordinate of enemy bullet
        new_enemy_bullet.y = enemy.y        # set the y coordinate of enemy bullet
        enemy_bullets.append(new_enemy_bullet)  # add enemy bullet to the list
        last_shoot_time = current_time

def on_mouse_move(pos, rel, buttons):
    if isLoose:
        return
    hero.x = pos[0]             # set the x coordinate of hero
    hero.y = pos[1]             # set the y coordinate of hero

def on_mouse_down(pos, button):
    if isLoose:
        return
    new_bullet = Actor('bullet1')# create a new bullet
    new_bullet.x = hero.x           # set the x coordinate of bullet
    new_bullet.y = hero.y - 50      # set the y coordinate of bullet
    bullets.append(new_bullet)      # add bullet to the list
    sounds.gun.play()           # play the sound of gun

def update():
    global score, isLoose, HP, invincible, invincible_time, invincible_start, boss_direction, boss, boss_score  # 声明全局变量
    global shield, shield_start, shield_interval, shield_duration, has_shield, last_shield_time, shield1, shield_sprite
    if isLoose:
        return

    # 背景图片循环滚动
    background1.y += 1        # move background1 down
    background2.y += 1

    if background1.y > HEIGHT / 2 + HEIGHT:     # if background1 is out of the screen
        background1.y = -HEIGHT / 2            # move background1 to the top of background2
    if background2.y > HEIGHT / 2 + HEIGHT:
        background2.y = -HEIGHT / 2

    create_enemy_bullet()  # create enemy bullet

    # bullet move up
    for bullet in bullets:
        bullet.y -= 10  
    
    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += 10
    
    # delete bullet out of the screen
    for bullet in bullets:
        if bullet.y < -HEIGHT:
            bullets.remove(bullet)
    
    for enemy_bullet in enemy_bullets:
        if enemy_bullet.y > HEIGHT:
            enemy_bullets.remove(enemy_bullet)

    # enemy move down
    enemy.y += 5
    # reset enemy position when it moves out of the screen
    if enemy.y > HEIGHT:
        enemy.x = random.randint(50, WIDTH-50)  # 重新设置敌机的x坐标
        enemy.y = 0                       # 重新设置敌机的y坐标
    
    # Boss行为
    if score % 15 == 0 and score != 0 and not boss.active:  # 达到一定得分并且boss未激活时激活boss
        boss.active = True
        boss.y = random.randint(20, WIDTH - 50)  # boss出现在屏幕中
        boss.health = 10

    if boss.active:
        # Boss移动代码（直线往返移动）
        boss.x += boss_speed * boss_direction
        if boss.x <= 0 or boss.x >= WIDTH:
            boss_direction *= -1  # 当boss到达屏幕边缘时改变方向
        boss.y += boss_speed * boss_direction
        if boss.y <= 0 or boss.y >= HEIGHT:
            boss_direction *= -1  # 当boss到达屏幕边缘时改变方向

        # Boss攻击代码
        # 示例：随机发射子弹
        if random.randint(0, 2) == 0:
            # 创建boss子弹，设置位置等
            create_boss_bullet()

        # 更新boss子弹的位置
        for b_bullet in boss_bullets:
            b_bullet.y += 3  # 子弹向下移动
            if b_bullet.colliderect(hero):
                HP -= 5  # 玩家生命值减1
                boss_bullets.remove(b_bullet)  # 移除击中的子弹
                break  # 玩家已经被击中，不需要检查其他子弹
            if b_bullet.y > HEIGHT:  # 子弹移出屏幕
                boss_bullets.remove(b_bullet)  # 移除子弹

        # boss和玩家碰撞
        if hero.colliderect(boss) and invincible_time <= 0:  # 玩家飞机和敌机发生碰撞
            invincible = True  # 设置玩家为无敌状态
            HP -= 5
            if HP <= 0:
                isLoose = True  # 标记游戏失败
                hero.image = 'hero_blowup'
        else:
            invincible_time = 1000      # 重置无敌时间
            invincible_start = pygame.time.get_ticks()  # 重置无敌开始时间
            invincible = False  # 玩家不再无敌

        # 检查boss是否被子弹击中
        for bullet in bullets:
            if bullet.colliderect(boss) :
                sounds.got_enemy.play()  # 播放击中boss音效，如果有这个音效就取消注释
                boss.health -= 1  # boss生命值减少
                bullets.remove(bullet)  # 移除击中的子弹
                if boss.health <= 0:
                    boss.active = False  # boss被击败，设置为不激活
                    score += 10  # 增加得分
                    boss.y = -150  # boss消失在屏幕外
                    boss_bullets.clear()  # 清空屏幕上的boss子弹

    # shield
    current_time = pygame.time.get_ticks()
    if current_time - last_shield_time > shield_interval:
        shield.x = random.randint(50, WIDTH - 50)
        shield.y = 0
        last_shield_time = current_time
    
    if shield.x > 0:
        shield.y += 5
        if shield.y > HEIGHT:
            shield.x = -WIDTH

    # 无敌时间
    if invincible_time > 0:
        current_time = pygame.time.get_ticks()
        if current_time - invincible_start > invincible_time:
            invincible_time = 0
            hero.image = 'ship_slightdmg'

    # check collision between enemy and hero
    if hero.colliderect(enemy) and invincible_time <= 0:
        if not has_shield:
            # handle collision between hero and enemy
            invincible = True  # 设置玩家为无敌状态
            HP -= 1  # 减少玩家生命值
            if HP <= 0:
                isLoose = True  # 标记游戏失败
                hero.image = 'hero_blowup'
            else:
                invincible_time = 1000      # 重置无敌时间
                invincible_start = pygame.time.get_ticks()  # 重置无敌开始时间
                invincible = False  # 玩家不再无敌

    # check collision between enemy and bullets
    for bullet in bullets:
        if bullet.colliderect(enemy):
            # handle collision between bullet and enemy
            bullets.remove(bullet)  # remove the bullet
            enemy.y = 0              # reset enemy position
            enemy.x = random.randint(0, WIDTH)  # reset enemy position
            score += 1  # increase score

    # check collision between hero and enemy bullets
    for enemy_bullet in enemy_bullets:
        if enemy_bullet.colliderect(hero) and invincible_time <= 0:
            if not has_shield:
                invincible = True  # 设置玩家为无敌状态
                # handle collision between hero and enemy bullet
                HP -= 1  # 减少玩家生命值
                enemy_bullets.remove(enemy_bullet)  # remove the enemy bullet
                if HP <= 0:
                    isLoose = True  # 标记游戏失败
                    hero.image = 'hero_blowup'
                else:
                    invincible_time = 1000
                    invincible_start = pygame.time.get_ticks()  # 重置无敌开始时间
                    invincible = False  # 玩家不再无敌

    # check collision between hero and boss bullets
    for boss_bullet in boss_bullets:
        if boss_bullet.colliderect(hero) and invincible_time <= 0:
            if not has_shield:
                invincible = True  # 设置玩家为无敌状态
                # handle collision between hero and boss bullet
                HP -= 5  # 减少玩家生命值
                boss_bullets.remove(boss_bullet)  # remove the boss bullet
                if HP <= 0:
                    isLoose = True
                    hero.image = 'hero_blowup'
                else:
                    invincible_time = 1000
                    invincible_start = pygame.time.get_ticks()
                    invincible = False
    
    # check collision between hero and shield
    if hero.colliderect(shield):
        has_shield = True
        shield.start = pygame.time.get_ticks()
        shield.x = -WIDTH

    if has_shield:
        current_time = pygame.time.get_ticks()
        hero.image = 'hero'
        if current_time - shield_start > shield_duration:
            has_shield = False
pgzrun.go()  # 开始执行游戏