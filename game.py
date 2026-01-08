import pygame
import sys
from config import *
from player import Play
from enemy import Enemy
from collision import Collision
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Fight_Game")
        self.clock = pygame.time.Clock()
        self.running = True
        # 切换状态
        self.states = {}
        self.current_states = None
        # 创建玩家游戏实例
        self.player = Play(self.screen_rect.centerx,self.screen_rect.centery)
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.player.add(self.players)
        self.player.add(self.all_sprites)
        # 相机偏移
        self.camera_offset = [0,0]
         # 创建敌人实例
        self.spawn_enemies(5)
        # 创建碰撞实例
        self.collision = Collision(self)

    def run_game(self):
        '''开始游戏主循环'''
        while self.running:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._update(dt)
            self._render()
            

    def _render(self):
        '''渲染画面'''
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            if hasattr(sprite,'draw'):
                sprite.draw(self.screen,self.camera_offset)
            else:
                # sprite.rect.x是世界坐标，如果删除self.camera_offset，敌人会跟随世界坐标移动，但player的坐标会被self.camera_offset抵消为0，造成屏幕中player不变，而敌人跟着增大的世界坐标变化
                self.screen.blit(sprite.image,(sprite.rect.x - self.camera_offset[0],
                                 sprite.rect.y - self.camera_offset[1]))
        pygame.display.flip()

    def spawn_enemies(self,count):
        '''生成count数量的敌人'''
        enemy_types = ["basic","fast","slow"]
        for _ in range(count):
            enemy_type = random.choice(enemy_types)
            x = random.randint(50,SCREEN_WIDTH-50)
            y = random.randint(50,SCREEN_HEIGHT-50)
            new_enemy = Enemy(x,y,enemy_type)
            self.all_sprites.add(new_enemy)
            self.enemies.add(new_enemy)
    
    def _update(self,dt):
        '''更新游戏逻辑'''
        self.enemies.update(self.player,self.enemies,dt)
        self.collision.update()
        self.player.attack(self.enemies)
        self._update_camera()
        pass

    def _update_camera(self):
        '''更新相机位置，跟随玩家'''
        # 简单的相机跟随：让玩家始终在屏幕中央
        self.camera_offset[0] = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_offset[1] = self.player.rect.centery - SCREEN_HEIGHT // 2

    def _handle_events(self):
        '''处理输入事件'''
        self._handle_player_input()
        self._handle_quit_events()

    def _handle_quit_events(self):
        '''处理退出事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
    
    def _handle_player_input(self):
        '''处理外加输出'''
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def quit_game(self):
        '''退出游戏'''
        self.running = False
        pygame.quit()
        sys.exit()
        

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    fg = Game()
    try:
        fg.run_game()
    finally:
        fg.quit_game()