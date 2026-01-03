import pygame
import sys
from config import *
from player import Play
from enemy import Enemy
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
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
        self.camera_offset = (0, 0)
         # 创建敌人实例
        self.spawn_enemies(5)

    def run_game(self):
        '''开始游戏主循环'''
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)

    def _render(self):
        '''渲染画面'''
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            if hasattr(sprite,'draw'):
                sprite.draw(self.screen,self.camera_offset)
            else:
                self.screen.blit(sprite.image,sprite.rect
                                 )
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
    
    def _update(self):
        '''更新游戏逻辑'''
        self.enemies.update(self.player)
        pass

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