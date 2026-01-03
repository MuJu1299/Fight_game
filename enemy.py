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
            self.image.fill(ENEMY_COLOR)
            self.rect = self.image.get_rect(center=(x,y))
            # 碰撞箱
            self.hitbox = pygame.Rect(0,0,20,20)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 5
    
    def update(self,player):
        '''朝玩家移动的AI'''
        player_pos = pygame.Vector2(player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        # 两点间的向量及两点间的距离
        direction =player_pos - enemy_pos
        distance = direction.length()

        if distance > 0:
            direction = direction.normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed
            self.hitbox.center = self.rect.center

        