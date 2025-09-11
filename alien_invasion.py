import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 控制帧率，定义一个时钟
        self.clock = pygame.time.Clock()
        # 游戏启动后处于非激活状态
        self.game_active = False
        self.play_buttom = Button(self, "Play")

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_bottom(mouse_pos)

    def _check_play_bottom(self, mouse_pos):
        """在玩家单机play的时候开始新游戏"""
        button_clicked = self.play_buttom.rect.collidepoint(mouse_pos)
        
        # rect的collidepoint()方法检查鼠标的单击位置是否在Play按钮的rect内
        if button_clicked and not self.game_active:

            # 重置游戏的统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True
            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建新舰队
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏光标
            pygame.mouse.set_visible(False)

                    

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

    def _create_fleet(self):
        """创建一个外星舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while(current_y < self.settings.screen_height - alien_height*3):
            while(current_x < self.settings.screen_width - alien_width*2):
                self._create_alien(current_x, current_y)
                current_x += alien_width*2
            current_x = alien_width
            current_y += alien_height*3


    def _create_alien(self, x_position, y_position):
        """创建一个外星人"""
        new_alien = Alien(self)
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """在有外星人到达边缘的时候采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        # 设置背景色
        # fill()方法用于处理surface，只接受一个表示颜色的实参。
        self.screen.fill(self.settings.bg_color)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        if not self.game_active:
            self.play_buttom.draw_button()
        # 让绘制的屏幕可见
        # 它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新的空屏幕可见
        pygame.display.flip()

    def _update_bullet(self):
        """更新子弹位置并消除已消失的子弹"""
        self.bullets.update()
        # 删除飞出屏幕的子弹
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        # 检查是否有子弹射中外星人，如果是则删除子弹和外星人
        self._check_bullet_alien_collisions()
            
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
        if not self.aliens:
            # 删除子弹创建外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘且更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.get_visible(True)

            

    def run_game(self):
        """开始游戏的主循环"""
        while(True):
            # 侦听键盘和鼠标事件
            self._check_events()
            if self.game_active:
                self.ship.update()   
                self._update_bullet()
                self._update_aliens()
            # 更新屏幕
            self._update_screen()
            # tick()方法接受一个参数：游戏的帧率
            self.clock.tick(60)


if __name__ == "__main__":

    ai = AlienInvasion()
    ai.run_game()
