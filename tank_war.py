import pygame
import tkinter as tk
from tkinter import filedialog

from sprites import *


class TankWar:
    def __init__(self):
        self.level = 1
    def run_game(self):
        if self.level == 1:
            lv1 = Level1()
            lv1.run_game()
        elif self.level == 2:
            lv2 = Level2()
            lv2.run_game()
    # def __generate_map(self):


class Level1:
    def __init__(self):
        self.pause = False
        self.map = Settings.MAP_ONE
        self.screen = pygame.display.set_mode(Settings.SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.game_still = True
        self.heros = None
        self.hero = None
        self.enemies = None
        self.walls = None

        self.pickaxes = None
        self.pickaxe = None
        self.pickaxe_posx = None
        self.pickaxe_posy = None
        self.updatePickaxe = True

        self.stars = None
        self.star = None
        self.star_posx = None
        self.star_posy = None
        self.updateStars = True

        self.healths= None
        self.health = None
        self.updateHealth = True

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
        self.heros = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.pickaxes = pygame.sprite.Group()
        self.healths = pygame.sprite.Group()
        

        # generate hero
        self.hero = Hero(Settings.HERO_IMAGE_NAME, self.screen)
        self.heros.add(self.hero)
        # generate enemies
        for i in range(Settings.ENEMY_COUNT):
            direction = random.randint(0, 3)
            enemy = Enemy(Settings.ENEMY_IMAGES[direction], self.screen)
            y = random.randint(0, len(self.map)-1)
            x = random.randint(0, len(self.map[y])-1)
            if self.map[y][x] == 0:
                enemy.rect.x = x*Settings.BOX_SIZE
                enemy.rect.y = y*Settings.BOX_SIZE
            enemy.direction = direction
            self.enemies.add(enemy)

    def __draw_walls(self):
        self.walls = pygame.sprite.Group()
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 5:
                    self.basex = x
                    self.basey = y
                if self.map[y][x] == 0:
                    continue
                # print("y:", y, "x:", x)
                # print("corresponding map value", self.map[y][x])
                # print(Settings.WALLS[self.map[y][x]])
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
                wall.x = x
                wall.y = y


    def endow_shield(self):
        print("shield acquired")
        print("star_posx ", self.star_posx, "star_posy ", self.star_posy)
        self.map[self.star_posy][self.star_posx] = 0
        self.map[self.pickaxe_posy][self.pickaxe_posx] = 0
        self.hero.unbeatable = True
        time.sleep(10)
        self.hero.unbeatable = False
        print("shield expired")

    def endow_pickaxe(self):
        print("pickaxe acquired")
        print("pickaxe_posx ", self.pickaxe_posx, "pickaxe_posy ", self.pickaxe_posy)
        self.map[self.star_posy][self.star_posx] = 0
        self.map[self.pickaxe_posy][self.pickaxe_posx] = 0
        self.hero.getpickaxe = True
        self.protect_base()
        self.__draw_walls()
        time.sleep(10)
        self.protect_base()
        self.__draw_walls()
        self.hero.getpickaxe = False
        print("pickaxe expired")

    def decide_wall_exits(self,x,y):
        # if out of bounds return false and swap the walls 
        if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
            return False
        return True
    def swap_wall(self,x, y, num):
        temp = self.steelwall[num]
        self.steelwall[num] = self.map[y][x] 
        self.map[y][x] = temp

    def protect_base(self):
        if self.decide_wall_exits(self.basex -1, self.basey -1):
            self.swap_wall(self.basex -1, self.basey -1, 0)
        if self.decide_wall_exits(self.basex -1, self.basey +1):
            self.swap_wall(self.basex -1, self.basey +1, 1)
        if self.decide_wall_exits(self.basex -1, self.basey ):
            self.swap_wall(self.basex -1, self.basey, 2)
        if self.decide_wall_exits(self.basex, self.basey -1):
            self.swap_wall(self.basex, self.basey -1, 3)
        if self.decide_wall_exits(self.basex, self.basey +1):
            self.swap_wall(self.basex, self.basey +1, 4)
        if self.decide_wall_exits(self.basex +1, self.basey -1):
            self.swap_wall(self.basex +1, self.basey -1, 5)
        if self.decide_wall_exits(self.basex +1, self.basey +1):
            self.swap_wall(self.basex +1, self.basey +1, 6)
        if self.decide_wall_exits(self.basex +1, self.basey ):
            self.swap_wall(self.basex +1, self.basey, 7)

        
    def __draw_pickaxe(self):
        """
        draw pickaxe only on the blank path
        """
        if self.updatePickaxe:
            while True:
                y = random.randint(0, len(self.map)-1)
                x = random.randint(0, len(self.map[y])-1)
                if self.map[y][x] == 0:
                    pickaxe = Pickaxe(Settings.PICKAXE_IMG, self.screen)
                    pickaxe.rect.x = x*Settings.BOX_SIZE
                    pickaxe.rect.y = y*Settings.BOX_SIZE
                    self.map[y][x] = Settings.PICKAXE
                    self.pickaxe_posx = x
                    self.pickaxe_posy = y
                    print(self.map[y][x])
                    print( "pickaxe: pos " + str(y) + " and pos " + str(x))
                    self.pickaxe = pickaxe
                    self.pickaxes.add(pickaxe)

                    self.pickaxe_posx = x
                    self.pickaxe_posy = y
                    self.updatePickaxe = False
                    return
                
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
                    self.star_posx = x
                    self.star_posy = y
                    # print(self.map[y][x])
                    # print( "star: pos " + str(x) + " and pos " + str(y))
                    self.star = star
                    self.stars.add(star)
                    self.updateStars = False
                    return

    def __draw_health(self):
        """
        draw health at top left corner of window
        """
        if self.updateHealth:
            while True:
                x=1
                y=0
                for i in range(self.hero.life):
                    health = Health(Settings.HEALTH_IMG, self.screen)
                    health.rect.x = i*Settings.BOX_SIZE
                    health.rect.y = y*Settings.BOX_SIZE
                    self.map[y][i]= Settings.HEALTH
                    self.health = health
                    self.healths.add(health)
                
                    # print(self.healths)

                self.updateHealth = False
                return
            
    def __show_score(self):

        """
        draw score at top right corner
        """

        if self.updateScore:
            while True:
                x=18
                y=1
                my_font = pygame.font.Font(None, 30)
                rect_width=100
                rect_height = 80
                text_surface = my_font.render(self.scoreprint,True,(255,255,255))
                rect = text_surface.get_rect(center=(x*Settings.BOX_SIZE,0.5*Settings.BOX_SIZE))
                rect.width = rect_width
                rect.height = rect_height
                self.screen.blit(text_surface,rect)
                self.updateScore=False
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
        elif event.key == pygame.K_BACKSPACE:
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
            self.hero.is_dash = True


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
        elif event.key == pygame.K_BACKSPACE:
            self.hero.is_moving = False
            self.hero.is_dash = False
    


    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否是退出游戏
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == pygame.KEYDOWN:
                self.__check_keydown(event)
            elif event.type == pygame.KEYUP:
                self.__check_keyup(event)

    def __check_collide(self):
        # tanks don't move out of the screen
        self.hero.hit_wall()
        for enemy in self.enemies:
            enemy.hit_wall_turn()

        # wall is collided with bullets
        for wall in self.walls:
            # hero bullets hit wall
            for bullet in self.hero.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        if wall.life == 1:
                            self.map[wall.y][wall.x] = 0
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.BOSS_WALL:
                        self.game_still = False
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            # enemy bullets hit wall
            for enemy in self.enemies:
                for bullet in enemy.bullets:
                    if pygame.sprite.collide_rect(wall, bullet):
                        if wall.type == Settings.RED_WALL:

                            self.map[wall.y][wall.x] = 0
                            wall.kill()
                            bullet.kill()
                        elif wall.type == Settings.BOSS_WALL:
                            self.game_still = False
                        elif wall.type == Settings.IRON_WALL:
                            bullet.kill()

            # Tanks colliding with walls, not going through the walls
            # hero hit wall
            if pygame.sprite.collide_rect(self.hero, wall):
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                    self.hero.is_hit_wall = True
                    self.hero.move_out_wall(wall)
            
            # enemies hit wall
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(wall, enemy):
                    if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                        enemy.move_out_wall(wall)
                        enemy.random_turn()
                for health in self.healths:
                    if pygame.sprite.collide_rect(health, enemy):
                        enemy.move_out_health(health)
                        enemy.random_turn()

            for health in self.healths:
                if pygame.sprite.collide_rect(self.hero, health):
                    self.hero.is_hit_wall = True
                    self.hero.move_out_health(health)
            
            


        # hero bullets collide with enemies
        score_track= pygame.sprite.groupcollide(self.hero.bullets, self.enemies, True, True)
        self.score+= len(score_track)*5
        # enemies bullets collide with hero
        for enemy in self.enemies:
            if not self.hero.unbeatable:
                collision = pygame.sprite.groupcollide(enemy.bullets, self.heros, True, False)
                if collision != {} and self.hero.life > 0:
                    self.hero.life -= 1
                    self.hero.rect.centerx = Settings.SCREEN_RECT.centerx - Settings.BOX_RECT.width * 2
                    self.hero.rect.bottom = Settings.SCREEN_RECT.bottom
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
            self.map
            self.updateStars = True

        if pygame.sprite.collide_rect(self.hero, self.pickaxe):
            self.pickaxe.kill()
            t = Thread(target=self.endow_pickaxe)
            t.start()
            self.updatePickaxe = True

    def __update_sprites(self):
        # update the static thing 
        self.walls.update()
        self.stars.update()
        self.pickaxes.update()
        self.healths.update()
        self.__enemyrespawn()

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
        self.pickaxes.draw(self.screen)
        self.healths.draw(self.screen)
        self.__show_score()

    def __update_health(self):
        if self.hero.life< len(self.healths):
            self.healths.remove(self.healths.sprites()[-1])

    def __updatescore(self):
        self.updateScore=True
        self.scoreprint = "Score" +  " " + str(self.score)
        self.__show_score()

    def __enemyrespawn(self):
        for i in range(Settings.ENEMY_COUNT-len(self.enemies)):
            direction = random.randint(0, 3)
            enemy = Enemy(Settings.ENEMY_IMAGES[direction], self.screen)
            enemy.direction = direction
            self.enemies.add(enemy)

    def __save_to_file(self):
        def save():
            if folder_path:
                    try:
                        with open(folder_path+'/'+file_path, 'a') as file:
                            player_name=  text_widget.get("1.0", "end-1c")
                            text_content =  str(self.score)
                            file.write(player_name + "  " + text_content)
                        status_label.config(text=f"File saved: {file_path}")
                    except Exception as e:
                        status_label.config(text=f"Error saving file: {str(e)}")
            else :
                    with open(folder_path+'/'+file_path, "x") as file:
                        text_content= "I created a new file first"
                        file.write(text_content)
                        status_label.config(text=f"File saved")
                
        root = tk.Tk()
        root.title("Text Editor")

        text_widget = tk.Text(root, wrap=tk.WORD)
        text_widget.pack(padx=20, pady=20, fill="both", expand=True)

        save_button = tk.Button(root, text="Save to File", command=save)
        save_button.pack(pady=10)

        status_label = tk.Label(root, text="", padx=20, pady=10)
        status_label.pack()

        tk.Button(root, text="Quit", command=root.destroy).pack()
        file_path = "scores.txt"
        folder_path = filedialog.askdirectory()
        root.mainloop()   

    def run_game(self):
        self.__init_game()
        self.__create_sprite()
        self.__draw_walls()
        while True and self.hero.is_alive and self.game_still:
            if not self.pause:
                self.screen.fill(Settings.SCREEN_COLOR)
                # 1、设置刷新帧率
                self.clock.tick(Settings.FPS)
                self.__draw_star()
                self.__draw_pickaxe()
                self.__draw_health()
                print (self.updateScore)
                # 2、事件监听
                self.__event_handler()
                # 3、碰撞监测
                self.__check_collide()
                self.__updatescore()
                self.__update_health()
                # 4、更新/绘制精灵/经理组
                self.__update_sprites()
                # 5、更新显示
                pygame.display.update()
                #print(len(self.healths))
        self.__save_to_file()
        self.__game_over()

    @staticmethod
    def __game_over():
        pygame.quit()
        exit()



class Level2:
    def __init__(self):
        self.pause = False
        self.map = Settings.MAP_ONE
        self.screen = pygame.display.set_mode(Settings.SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.game_still = True
        self.heros = None
        self.hero = None
        self.enemies = None
        self.walls = None

        self.pickaxes = None
        self.pickaxe = None
        self.pickaxe_posx = None
        self.pickaxe_posy = None
        self.updatePickaxe = True

        self.stars = None
        self.star = None
        self.star_posx = None
        self.star_posy = None
        self.updateStars = True

        self.healths= None
        self.health = None
        self.updateHealth = True

        self.basex = None
        self.basey = None

        self.steelwall = [Settings.IRON_WALL] * 8

        self.updateScore= True
        self.score = 0
        self.scoreprint = "Score" +  " " + str(self.score)

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
        self.heros = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.pickaxes = pygame.sprite.Group()
        self.healths = pygame.sprite.Group()
        

        # generate hero
        self.hero = Hero(Settings.HERO_IMAGE_NAME, self.screen)
        self.heros.add(self.hero)
        # generate enemies
        for i in range(Settings.ENEMY_COUNT):
            direction = random.randint(0, 3)
            enemy = Enemy(Settings.ENEMY_IMAGES[direction], self.screen)
            y = random.randint(0, len(self.map)-1)
            x = random.randint(0, len(self.map[y])-1)
            if self.map[y][x] == 0:
                enemy.rect.x = x*Settings.BOX_SIZE
                enemy.rect.y = y*Settings.BOX_SIZE
            enemy.direction = direction
            self.enemies.add(enemy)

    def __draw_walls(self):
        self.walls = pygame.sprite.Group()
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 5:
                    self.basex = x
                    self.basey = y
                if self.map[y][x] == 0:
                    continue
                # print("y:", y, "x:", x)
                # print("corresponding map value", self.map[y][x])
                # print(Settings.WALLS[self.map[y][x]])
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
                wall.x = x
                wall.y = y


    def endow_shield(self):
        print("shield acquired")
        print("star_posx ", self.star_posx, "star_posy ", self.star_posy)
        self.map[self.star_posy][self.star_posx] = 0
        self.map[self.pickaxe_posy][self.pickaxe_posx] = 0
        self.hero.unbeatable = True
        time.sleep(10)
        self.hero.unbeatable = False
        print("shield expired")

    def endow_pickaxe(self):
        print("pickaxe acquired")
        print("pickaxe_posx ", self.pickaxe_posx, "pickaxe_posy ", self.pickaxe_posy)
        self.map[self.star_posy][self.star_posx] = 0
        self.map[self.pickaxe_posy][self.pickaxe_posx] = 0
        self.hero.getpickaxe = True
        self.protect_base()
        self.__draw_walls()
        time.sleep(10)
        self.protect_base()
        self.__draw_walls()
        self.hero.getpickaxe = False
        print("pickaxe expired")

    def decide_wall_exits(self,x,y):
        # if out of bounds return false and swap the walls 
        if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
            return False
        return True
    def swap_wall(self,x, y, num):
        temp = self.steelwall[num]
        self.steelwall[num] = self.map[y][x] 
        self.map[y][x] = temp

    def protect_base(self):
        if self.decide_wall_exits(self.basex -1, self.basey -1):
            self.swap_wall(self.basex -1, self.basey -1, 0)
        if self.decide_wall_exits(self.basex -1, self.basey +1):
            self.swap_wall(self.basex -1, self.basey +1, 1)
        if self.decide_wall_exits(self.basex -1, self.basey ):
            self.swap_wall(self.basex -1, self.basey, 2)
        if self.decide_wall_exits(self.basex, self.basey -1):
            self.swap_wall(self.basex, self.basey -1, 3)
        if self.decide_wall_exits(self.basex, self.basey +1):
            self.swap_wall(self.basex, self.basey +1, 4)
        if self.decide_wall_exits(self.basex +1, self.basey -1):
            self.swap_wall(self.basex +1, self.basey -1, 5)
        if self.decide_wall_exits(self.basex +1, self.basey +1):
            self.swap_wall(self.basex +1, self.basey +1, 6)
        if self.decide_wall_exits(self.basex +1, self.basey ):
            self.swap_wall(self.basex +1, self.basey, 7)

        
    def __draw_pickaxe(self):
        """
        draw pickaxe only on the blank path
        """
        if self.updatePickaxe:
            while True:
                y = random.randint(0, len(self.map)-1)
                x = random.randint(0, len(self.map[y])-1)
                if self.map[y][x] == 0:
                    pickaxe = Pickaxe(Settings.PICKAXE_IMG, self.screen)
                    pickaxe.rect.x = x*Settings.BOX_SIZE
                    pickaxe.rect.y = y*Settings.BOX_SIZE
                    self.map[y][x] = Settings.PICKAXE
                    self.pickaxe_posx = x
                    self.pickaxe_posy = y
                    print(self.map[y][x])
                    print( "pickaxe: pos " + str(y) + " and pos " + str(x))
                    self.pickaxe = pickaxe
                    self.pickaxes.add(pickaxe)

                    self.pickaxe_posx = x
                    self.pickaxe_posy = y
                    self.updatePickaxe = False
                    return
                
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
                    self.star_posx = x
                    self.star_posy = y
                    # print(self.map[y][x])
                    # print( "star: pos " + str(x) + " and pos " + str(y))
                    self.star = star
                    self.stars.add(star)
                    self.updateStars = False
                    return

    def __draw_health(self):
        """
        draw health at top left corner of window
        """
        if self.updateHealth:
            while True:
                x=1
                y=0
                for i in range(self.hero.life):
                    health = Health(Settings.HEALTH_IMG, self.screen)
                    health.rect.x = i*Settings.BOX_SIZE
                    health.rect.y = y*Settings.BOX_SIZE
                    self.map[y][i]= Settings.HEALTH
                    self.health = health
                    self.healths.add(health)
                
                    # print(self.healths)

                self.updateHealth = False
                return
            
    def __show_score(self):

        """
        draw score at top right corner
        """

        if self.updateScore:
            while True:
                x=18
                y=1
                my_font = pygame.font.Font(None, 30)
                rect_width=100
                rect_height = 80
                text_surface = my_font.render(self.scoreprint,True,(255,255,255))
                rect = text_surface.get_rect(center=(x*Settings.BOX_SIZE,0.5*Settings.BOX_SIZE))
                rect.width = rect_width
                rect.height = rect_height
                self.screen.blit(text_surface,rect)
                self.updateScore=False
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
        elif event.key == pygame.K_BACKSPACE:
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
            self.hero.is_dash = True


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
        elif event.key == pygame.K_BACKSPACE:
            self.hero.is_moving = False
            self.hero.is_dash = False
    


    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否是退出游戏
            if event.type == pygame.QUIT:
                TankWar.__game_over()
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
            # hero bullets hit wall
            for bullet in self.hero.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        if wall.life == 1:
                            self.map[wall.y][wall.x] = 0
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.BOSS_WALL:
                        self.game_still = False
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            # enemy bullets hit wall
            for enemy in self.enemies:
                for bullet in enemy.bullets:
                    if pygame.sprite.collide_rect(wall, bullet):
                        if wall.type == Settings.RED_WALL:

                            self.map[wall.y][wall.x] = 0
                            wall.kill()
                            bullet.kill()
                        elif wall.type == Settings.BOSS_WALL:
                            self.game_still = False
                        elif wall.type == Settings.IRON_WALL:
                            bullet.kill()

            # Tanks colliding with walls, not going through the walls
            # hero hit wall
            if pygame.sprite.collide_rect(self.hero, wall):
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                    self.hero.is_hit_wall = True
                    self.hero.move_out_wall(wall)
            

            for health in self.healths:
                if pygame.sprite.collide_rect(self.hero, health):
                    self.hero.is_hit_wall = True
                    self.hero.move_out_health(health)

            

            # enemies
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(wall, enemy):
                    if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                        enemy.move_out_wall(wall)
                        enemy.random_turn()
                for health in self.healths:
                    if pygame.sprite.collide_rect(health, enemy):
                        enemy.move_out_health(health)
                        enemy.random_turn()

            for health in self.healths:
                if pygame.sprite.collide_rect(self.hero, health):
                    self.hero.is_hit_wall = True
                    self.hero.move_out_health(health)
            
            


        # hero bullets collide with enemies
        score_track= pygame.sprite.groupcollide(self.hero.bullets, self.enemies, True, True)
        self.score+= len(score_track)*5
        print(self.score)
        # enemies bullets collide with hero
        for enemy in self.enemies:
            if not self.hero.unbeatable:
                collision = pygame.sprite.groupcollide(enemy.bullets, self.heros, True, False)
                if collision != {} and self.hero.life > 0:
                    self.hero.life -= 1
                    print("life remaining :  ", self.hero.life)
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
            self.map
            self.updateStars = True

        if pygame.sprite.collide_rect(self.hero, self.pickaxe):
            self.pickaxe.kill()
            t = Thread(target=self.endow_pickaxe)
            t.start()
            self.updatePickaxe = True

    def __update_sprites(self):
        # update the static thing 
        self.walls.update()
        self.stars.update()
        self.pickaxes.update()
        self.healths.update()
        self.__enemyrespawn()

        



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
        self.pickaxes.draw(self.screen)
        self.healths.draw(self.screen)
        self.__show_score()


    def __update_health(self):
        if self.hero.life< len(self.healths):
            self.healths.remove(self.healths.sprites()[-1])

    def __updatescore(self):
        self.updateScore=True
        self.scoreprint = "Score" +  " " + str(self.score)
        self.__show_score()


    def __enemyrespawn(self):
        for i in range(Settings.ENEMY_COUNT-len(self.enemies)):
            direction = random.randint(0, 3)
            enemy = Enemy(Settings.ENEMY_IMAGES[direction], self.screen)
            enemy.direction = direction
            self.enemies.add(enemy)

    def __save_to_file(self):


        def save():
            if folder_path:
                    try:
                        with open(folder_path+'/'+file_path, 'a') as file:
                            player_name=  text_widget.get("1.0", "end-1c")
                            text_content =  str(self.score)
                            file.write(player_name + "  " + text_content)
                        status_label.config(text=f"File saved: {file_path}")
                    except Exception as e:
                        status_label.config(text=f"Error saving file: {str(e)}")
            else :
                    with open(folder_path+'/'+file_path, "x") as file:
                        text_content= "I created a new file first"
                        file.write(text_content)
                        status_label.config(text=f"File saved")
                


        root = tk.Tk()
        root.title("Text Editor")

        text_widget = tk.Text(root, wrap=tk.WORD)
        text_widget.pack(padx=20, pady=20, fill="both", expand=True)

        save_button = tk.Button(root, text="Save to File", command=save)
        save_button.pack(pady=10)

        status_label = tk.Label(root, text="", padx=20, pady=10)
        status_label.pack()

        tk.Button(root, text="Quit", command=root.destroy).pack()
        file_path = "scores.txt"
        folder_path = filedialog.askdirectory()
       

        root.mainloop()


        
       


    



    




    def run_game(self):
        self.__init_game()
        self.__create_sprite()
        self.__draw_walls()
        while True and self.hero.is_alive and self.game_still:
            self.screen.fill(Settings.SCREEN_COLOR)
            # 1、设置刷新帧率
            self.clock.tick(Settings.FPS)
            self.__draw_star()
            self.__draw_health()
            print (self.updateScore)
          
            # 2、事件监听
            self.__event_handler()
            # 3、碰撞监测
            self.__check_collide()
            self.__updatescore()
            self.__update_health()
           
            # 4、更新/绘制精灵/经理组
            self.__update_sprites()
            # 5、更新显示
            pygame.display.update()
            #print(len(self.healths))



        

        
        self.__save_to_file()
        self.__game_over()

    @staticmethod
    def __game_over():
        pygame.quit()
        exit()
