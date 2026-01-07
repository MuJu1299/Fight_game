import pygame
from config import *

class Collision:
    '''管理碰撞系统'''
    def __init__(self,game):
        self.game = game
        self.push = 0
    def update(self):
        '''放在while里逐帧检测碰撞'''
        self.check_enemy_player_collision()
        pass

    def check_enemy_player_collision(self):
        '''检测敌人及player的碰撞'''
        for enemy in self.game.enemies:
            if self.game.player.hitbox.colliderect(enemy.hitbox):
                self.push_apart(self.game.player, enemy)

    def push_apart(self,entity1,entity2,max_iterations = 5):
        '''推开敌人'''
        iterations = 0
        # 计算移动方向的影响
        entity1_moving_towards = self.is_moving_towards(entity1, entity2)
        entity2_moving_towards = self.is_moving_towards(entity2, entity1)
        
        while (entity1.hitbox.colliderect(entity2.hitbox)) and (iterations < max_iterations):
            dx = entity1.rect.centerx - entity2.rect.centerx
            dy = entity1.rect.centery - entity2.rect.centery
            # 防止length为零
            if dx == 0 and dy == 0:
                dx = 1  

            length = max(0.1,(dx**2 + dy**2)**0.5)
            dx /= length
            dy /= length

            # 推开距离
            push_distance = 5 + iterations

            # 推开实体1
            if entity1_moving_towards:
                push_distance1 = push_distance + 3  # 额外推开距离
                push_distance2 = push_distance
            # 如果实体2向实体1移动，实体2应该被推开更多
            elif entity2_moving_towards:
                push_distance1 = push_distance
                push_distance2 = push_distance + 3
            else:
                push_distance1 = push_distance
                push_distance2 = push_distance

            # 推开实体
            entity1.rect.centerx += push_distance1 * dx
            entity1.rect.centery += push_distance1 * dy
            
            entity2.rect.centerx -= push_distance2 * dx
            entity2.rect.centery -= push_distance2 * dy
        
            # 更新碰撞箱位置
            if hasattr(entity1, 'update_hitbox'):
                entity1.update_hitbox()
            else:
                entity1.hitbox.center = entity1.rect.center
                
            if hasattr(entity2, 'update_hitbox'):
                entity2.update_hitbox()
            else:
                entity2.hitbox.center = entity2.rect.center
                self.push += 1
                iterations += 1
                # print(self.push)

                

    def is_moving_towards(self, entity, target):
        '''判断实体是否向目标移动'''
        if not hasattr(entity, 'direction'):
            return False
        
        # 计算从实体到目标的方向向量
        dx = target.rect.centerx - entity.rect.centerx
        dy = target.rect.centery - entity.rect.centery
        
        # 归一化
        length = max(0.1, (dx**2 + dy**2)**0.5)
        dx /= length
        dy /= length
        
        # 如果实体的移动方向与到目标的方向夹角小于90度，说明在向目标移动
        dot_product = entity.direction.x * dx + entity.direction.y * dy
        return dot_product > 0.5  # 阈值可以调整