import pygame
from settings import Settings

class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = Settings()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(r"images/ship.bmp")
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 移动标志，飞船一开始不移动
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.setting.ship_speed

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
