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
            self.hitbox = pygame.Rect(0,0,*BASIC_ENEMY_COLLISION)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 2
            self.damage = 2
            self.health = 100
            self.cooldown = 2000
        # 快速敌人
        elif self.type == "fast":
            # 创建敌人图形
            self.image = pygame.Surface((22,22))
            self.image.fill(FAST_ENEMY_COLOR)
            self.rect = self.image.get_rect(center=(x,y))
            # 碰撞箱
            self.hitbox = pygame.Rect(0,0,*FAST_ENEMY_COLLISION)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 3
            self.health = 40
            self.damage = 1
            self.cooldown = 1500
        # 慢速敌人
        elif self.type == "slow":
            # 创建敌人图形
            self.image = pygame.Surface((42,42))
            self.image.fill(SLOW_ENEMY_COLOR)
            self.rect = self.image.get_rect(center=(x,y))
            # 碰撞箱
            self.hitbox = pygame.Rect(0,0,*SLOW_ENEMY_COLLISION)
            self.hitbox.center = self.rect.center
            # 设置敌人基本数值
            self.speed = 1
            self.health = 150
            self.damage = 4
            self.cooldown = 3000
        # 共用状态
        self.attack_cooldown = self.cooldown
        self.attack_warning = 0
        self.attack_range = 60
        # 初始化加速度与力
        self.velocity = pygame.Vector2(0,0)
        self.repulsion_strength = 1000

    
    def update(self,player,enemies,dt):
        '''朝玩家移动的AI'''
        # 重置加速度
        acceleration = pygame.Vector2(0, 0)
        # 朝玩家移动的力
        distance_to_player = pygame.Vector2(player.hitbox.center) - pygame.Vector2(self.rect.center)
        if distance_to_player.length() > 100:
            acceleration += distance_to_player.normalize() * self.speed

        # 敌人与敌人之间的碰撞
        for enemy in enemies:
            if enemy != self:
                enemies_direction = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center)
                enemies_distance = enemies_direction.length()
                
                if enemies_distance < self.hitbox.width and enemies_distance > 0:
                    force = self.repulsion_strength/(enemies_distance * enemies_distance)
                    acceleration += enemies_direction.normalize() * force
                    

        self.velocity += acceleration 
        self.velocity *= 0.1
        

        if self.velocity.length() > 10:
            self.velocity = self.velocity.normalize() * 10
            
        if self.attack_warning <= 0 :
            self.rect.x += self.velocity.x * dt
            self.rect.y += self.velocity.y * dt
            self.hitbox.center = self.rect.center
            

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        else:
            self.attack_warning += dt
            if self.attack_warning >= 1000:
                self.attack(player)
                self.attack_cooldown =self.cooldown
                self.attack_warning = 0

            


    def attack(self,player):
        '''敌人攻击'''
        if self.attack_cooldown > 0:
            return False
        distance = pygame.Vector2(self.rect.center).distance_to(player.rect.center)
        if distance <= self.attack_range:
            player.damage(self.damage)
            print("enemy_attack!")
        if self.attack_warning >= 1000:
            self.attack_cooldown = self.cooldown
            self.attack_warning = 0
        
    def take_damage(self,damage):
        '''接受损伤值在health小于零敌人死亡'''
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def draw(self,screen,camera_offset=(0,0)):
        '''绘制敌人'''
        screen.blit(self.image,(self.rect.x - camera_offset[0],
                                self.rect.y - camera_offset[1]))
    
        # 绘制示警范围
        if self.attack_warning > 0:
            pos = (self.rect.centerx - camera_offset[0], 
                   self.rect.centery - camera_offset[1])
            warning_percent = min(1.0,self.attack_warning/1000)
            warning_color = (255,int(255*(1 - warning_percent)),0,int(100*warning_percent))

            range_Surface = pygame.Surface((self.attack_range*2,self.attack_range*2)
                                        ,pygame.SRCALPHA)
            pygame.draw.circle(range_Surface,warning_color,(self.attack_range,self.attack_range)
                            ,self.attack_range)
            screen.blit(range_Surface,(pos[0]-self.attack_range, 
                                       pos[1]-self.attack_range))
    

    