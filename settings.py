class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        # 灰色
        self.bg_color = (230, 230, 230)
        # 天蓝
        # self.bg_color = (173, 216, 230)

        # 飞船信息
        self.ship_speed = 2
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed = 4.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)    

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 50
        # 1是向右，-1是向左
        self.fleet_direction = 1

        #游戏速度
        self.speedup_scale = 2
        # 外星人分数的提高速度
        self.score_scale = 2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
            """初始化随游戏进行而变化的设置"""
            self.ship_speed = 2
            self.bullet_speed = 4
            self.alien_speed = 1 

            self.fleet_direction = 1
            # 计分设置
            self.alien_points = 50
        
    def increase_speed(self):
            """提高速度设置的值"""
            self.ship_speed *= self.speedup_scale
            self.bullet_speed *= self.speedup_scale
            self.alien_speed *= self.speedup_scale
            self.alien_points = int(self.alien_points * self.score_scale)
            print(self.alien_points)