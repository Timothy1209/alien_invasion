import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建资源"""
        pygame.init()
        self.settings = Settings()
        # 创建一个显示窗口
        # display.set_mode()返回的surface表示整个游戏窗口，激活游戏的动画循环后，每经过一次循环都将自动重绘这个surface，将用户输入触发的所有变化都反映出来。
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 全屏游戏
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # 控制帧率，定义一个时钟
        self.clock = pygame.time.Clock()

    def _check_events(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
                # 当玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT事件，进而调用sys.exit()来退出游戏
                if event.type == pygame.QUIT:
                    sys.exit()
                # 监听键盘
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                    

    def _check_keydown_events(self, event):
        """按下按键"""
        # 右键移动
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 左键移动
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # 按Q退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """松开按键"""
        # 不按按键停止移动
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)


    def _uodate_screen(self):
        # 设置背景色
        # fill()方法用于处理surface，只接受一个表示颜色的实参。
        self.screen.fill(self.settings.bg_color)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        # 让绘制的屏幕可见
        # 它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新的空屏幕可见
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while(True):
            # 侦听键盘和鼠标事件
            self._check_events()
            self.ship.update()
            self.bullets.update()
            # 更新屏幕
            self._uodate_screen()
            # tick()方法接受一个参数：游戏的帧率
            self.clock.tick(60)


if __name__ == "__main__":

    ai = AlienInvasion()
    ai.run_game()
