import pygame
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,enemy_type = "basic"):
        super().__init__()
        self.type = enemy_type
        # 基础enemy
        if self.type == "basic":
            # 创建敌人图形
            self.image = pygame.Surface((32,32))
            self.image.fill(BASIC_ENEMY_COLOR)
            self.rect = self.image.get_rect(center=(x,y))
            # 碰撞箱
            self.hitbox = pygame.Rect(0,0,20,20)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 2
            self.health = 100
        # 快速敌人
        elif self.type == "fast":
            # 创建敌人图形
            self.image = pygame.Surface((22,22))
            self.image.fill(FAST_ENEMY_COLOR)
            self.rect = self.image.get_rect(center=(x,y))
            # 碰撞箱
            self.hitbox = pygame.Rect(0,0,15,15)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 3
            self.health = 40
        # 慢速敌人
        elif self.type == "slow":
            # 创建敌人图形
            self.image = pygame.Surface((42,42))
            self.image.fill(SLOW_ENEMY_COLOR)
            self.rect = self.image.get_rect(center=(x,y))
            # 碰撞箱
            self.hitbox = pygame.Rect(0,0,30,30)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 1
            self.health = 150
    
    def update(self,player):
        '''朝玩家移动的AI'''
        player_pos = pygame.Vector2(player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        # 两点间的向量及两点间的距离
        direction =player_pos - enemy_pos
        distance = direction.length()
        if distance > 0:
            if distance > 40:
                direction = direction.normalize()
                self.rect.x += direction.x * self.speed
                self.rect.y += direction.y * self.speed
                self.hitbox.center = self.rect.center
        

    
    def take_damage(self,damage):
        '''接受损伤值在health小于零敌人死亡'''
        self.health -= damage
        if self.health <= 0:
            self.kill()

        