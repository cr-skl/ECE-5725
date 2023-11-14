import pygame
import time
import random
from sprites import *
from threading import Thread


class TankWar:

    def __init__(self):
        self.map = Settings.MAP_ONE
        self.screen = pygame.display.set_mode(Settings.SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.game_still = True
        self.heros = None
        self.hero = None
        self.enemies = None
        self.walls = None
        self.stars = None
        self.star = None
        self.updateStars = True

    @staticmethod
    def __init_game():
        """
        初始化游戏的一些设置
        :return:
        """
        pygame.init()   # 初始化pygame模块
        pygame.display.set_caption(Settings.GAME_NAME)  # 设置窗口标题
        pygame.mixer.init()    # 初始化音频模块

    def __create_sprite(self):
        # generate groups 
        self.heros = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # generate hero
        self.hero = Hero(Settings.HERO_IMAGE_NAME, self.screen)
        self.heros.add(self.hero)
        # generate enemies
        for i in range(Settings.ENEMY_COUNT):
            direction = random.randint(0, 3)
            enemy = Enemy(Settings.ENEMY_IMAGES[direction], self.screen)
            enemy.direction = direction
            self.enemies.add(enemy)
        self.__draw_map()

    def __draw_map(self):
        """
        绘制地图
        :return:
        """
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 0:
                    continue
                wall = Wall(Settings.WALLS[self.map[y][x]], self.screen)
                wall.rect.x = x*Settings.BOX_SIZE
                wall.rect.y = y*Settings.BOX_SIZE
                if self.map[y][x] == Settings.RED_WALL:
                    wall.type = Settings.RED_WALL
                elif self.map[y][x] == Settings.IRON_WALL:
                    wall.type = Settings.IRON_WALL
                elif self.map[y][x] == Settings.WEED_WALL:
                    wall.type = Settings.WEED_WALL
                elif self.map[y][x] == Settings.BOSS_WALL:
                    wall.type = Settings.BOSS_WALL
                    wall.life = 1
                self.walls.add(wall)

    def endow_shield(self):
        print("shield acquired")
        self.hero.unbeatable = True
        time.sleep(10)
        self.hero.unbeatable = False
        print("shield expired")

    def __draw_star(self):
        """
        draw star only on the blank path, not on the walls
        """
        if self.updateStars:
            while True:
                y = random.randint(0, len(self.map)-1)
                x = random.randint(0, len(self.map[y])-1)
                if self.map[y][x] == 0:
                    star = Star(Settings.STAR_IMG, self.screen)
                    star.rect.x = x*Settings.BOX_SIZE
                    star.rect.y = y*Settings.BOX_SIZE
                    self.map[y][x] = Settings.STAR
                    self.star = star
                    self.stars.add(star)
                    self.updateStars = False
                    return
        



    def __check_keydown(self, event):
        """检查按下按钮的事件"""
        if event.key == pygame.K_LEFT:
            # 按下左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_RIGHT:
            # 按下右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_UP:
            # 按下上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_DOWN:
            # 按下下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_SPACE:
            # 坦克发子弹
            self.hero.shot()
        elif event.key == pygame.K_d:
            # Tank dash
            self.hero.dash()

    def __check_keyup(self, event):
        """检查松开按钮的事件"""
        if event.key == pygame.K_LEFT:
            # 松开左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = False
        elif event.key == pygame.K_RIGHT:
            # 松开右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = False
        elif event.key == pygame.K_UP:
            # 松开上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = False
        elif event.key == pygame.K_DOWN:
            # 松开下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = False

    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否是退出游戏
            if event.type == pygame.QUIT:
                TankWar.__game_over()
            # 判断按键按下
            elif event.type == pygame.KEYDOWN:
                TankWar.__check_keydown(self, event)
            elif event.type == pygame.KEYUP:
                TankWar.__check_keyup(self, event)

    def __check_collide(self):
        # tanks don't move out of the screen
        self.hero.hit_wall()
        for enemy in self.enemies:
            enemy.hit_wall_turn()

        # wall is collided with bullets
        for wall in self.walls:
            # hero bullets
            for bullet in self.hero.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.BOSS_WALL:
                        self.game_still = False
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            # enemy bullets
            for enemy in self.enemies:
                for bullet in enemy.bullets:
                    if pygame.sprite.collide_rect(wall, bullet):
                        if wall.type == Settings.RED_WALL:
                            wall.kill()
                            bullet.kill()
                        elif wall.type == Settings.BOSS_WALL:
                            self.game_still = False
                        elif wall.type == Settings.IRON_WALL:
                            bullet.kill()

            # Tanks colliding with walls, not going through the walls
            # hero 
            if pygame.sprite.collide_rect(self.hero, wall):
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                    self.hero.is_hit_wall = True
                    # 移出墙内
                    self.hero.move_out_wall(wall)

            # enemies
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(wall, enemy):
                    if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                        enemy.move_out_wall(wall)
                        enemy.random_turn()

        # hero bullets collide with enemies
        pygame.sprite.groupcollide(self.hero.bullets, self.enemies, True, True)
        # enemies bullets collide with hero
        for enemy in self.enemies:
            if not self.hero.unbeatable:
                collision = pygame.sprite.groupcollide(enemy.bullets, self.heros, True, False)
                if collision != {} and self.hero.life > 0:
                    self.hero.life -= 1
                    print("life remainging :  ", self.hero.life)
                if self.hero.life == 0:
                    self.hero.kill()
                    self.heros.remove(self.hero)
            else:
                pygame.sprite.groupcollide(enemy.bullets, self.heros, True, False)

        # 英雄得到了星星
        if pygame.sprite.collide_rect(self.hero, self.star):
            self.star.kill()
            t = Thread(target=self.endow_shield)
            t.start()
            self.updateStars = True



    def __update_sprites(self):
        # update the static thing 
        self.walls.update()
        self.stars.update()


        # update and show enemy tanks and each bullets
        self.enemies.update()
        self.enemies.draw(self.screen)
        for enemy in self.enemies:
            enemy.bullets.update()
            enemy.bullets.draw(self.screen)

        # update and show heros tanks and its bullets
        if self.hero.is_moving:
            self.hero.update()
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        self.heros.draw(self.screen)
        #self.screen.blit(self.hero.image, self.hero.rect)


        self.walls.draw(self.screen)
        self.stars.draw(self.screen)

    def run_game(self):
        
        self.__init_game()
        self.__create_sprite()
        current_time = time.time()

        while True and self.hero.is_alive and self.game_still:
            self.screen.fill(Settings.SCREEN_COLOR)
            # 1、设置刷新帧率
            self.clock.tick(Settings.FPS)
            self.__draw_star()
            # 2、事件监听
            self.__event_handler()
            # 3、碰撞监测
            self.__check_collide()
            # 4、更新/绘制精灵/经理组
            self.__update_sprites()
            # 5、更新显示
            pygame.display.update()
        self.__game_over()

    @staticmethod
    def __game_over():
        pygame.quit()
        exit()
