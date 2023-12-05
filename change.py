class Hero(TankSprite):

    def __init__(self, image_name, screen):
        
        self.is_dash = False

    def update(self):
        if not self.is_hit_wall:
            super().update()   
            if self.is_dash :
                for i in range(10):
                    super().update()
                self.is_dash = False
            self.__turn()


# def __check_keyup(self, event):

#         elif event.key == pygame.K_BACKSPACE:
#             self.hero.is_moving = False
        



# def __check_keydown(self, event):

#     elif event.key == pygame.K_BACKSPACE:
#         self.hero.is_moving = True
#         self.hero.is_hit_wall = False
#         self.hero.is_dash = True