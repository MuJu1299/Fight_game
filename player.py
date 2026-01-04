import pygame
from config import *

class Play(pygame.sprite.Sprite):
    # x,y用于初始玩家的坐标位置
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill((250,250,250))
        self.rect = self.image.get_rect(center=(x,y))
        # 碰撞箱
        self.hitbox = pygame.Rect(0,0,*PLAYER_HITBOX_SIZE)
        self.hitbox.center = self.rect.center
        # 玩家属性
        self.speed = PLAYER_SPEED
        self.attack_range = 60
        self.ATK = 40
        self.cooldown = 1000
        self.last_attack_time = 0
        self.attack_colldown = 0
        

    def update(self,key_pressed):
        '''更新玩家数据'''
        # # 冷却时间更新
        # current_time = pygame.time.get_ticks()
        # elapsed_time = current_time - self.last_attack_time
        # self.attack_colldown = max(0,self.cooldown - elapsed_time)
        # '''控制移动'''
        self.direction = pygame.Vector2(0,0)
        if key_pressed[pygame.K_w]:
            self.direction.y = -1
        if key_pressed[pygame.K_s]:
            self.direction.y = 1
        if key_pressed[pygame.K_d]:
            self.direction.x = 1
        if key_pressed[pygame.K_a]:
            self.direction.x = -1
        
        # 归一化对角线运动,将向量转化为方向
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # 更新移动
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.hitbox.center = self.rect.center

    def draw(self,screen,camera_offset):
        '''单独渲染玩家和其攻击范围'''
        # 创建半透明圆
        range_Surface = pygame.Surface((self.attack_range*2,self.attack_range*2)
                                       ,pygame.SRCALPHA)
        pygame.draw.circle(range_Surface,(230,0,0,120),(self.attack_range,self.attack_range),self.attack_range)

        screen.blit(range_Surface,(self.rect.x-camera_offset[0]-self.attack_range+self.rect.width/2
                                ,self.rect.y -camera_offset[1]-self.attack_range+self.rect.height/2))
        # 绘制玩家
        screen.blit(self.image,(self.rect.x-camera_offset[0]
                                ,self.rect.y -camera_offset[1]))
        
    def attack(self,enemier):
        '''敌人靠近到攻击范围则攻击'''
        # 控制冷却
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack_time
        remaining_cooldown = max(0,self.cooldown - elapsed_time)

        if remaining_cooldown > 0:
            return False
        
        attacked = False
        for enemy in enemier:
            distance = pygame.Vector2(enemy.rect.center).distance_to(self.rect.center)
            if distance < self.attack_range:
                enemy.take_damage(self.ATK)
                print("attack!")
                attacked = True
        if attacked:
            self.attack_colldown = self.cooldown
            self.last_attack_time = current_time
        return attacked
