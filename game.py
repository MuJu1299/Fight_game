import pygame
import sys
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Fight_Game")
        self.clock = pygame.time.Clock()
        self.running = True
        # 切换状态
        self.states = {}
        self.current_states = None

    def run_game(self):
        '''开始游戏主循环'''
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)

    def _render(self):
        '''渲染画面'''
        self.screen.fill(bg_color)
        pass
        pygame.display.flip()
    
    def _update(self):
        '''更新游戏逻辑'''
        pass

    def _handle_events(self):
        '''监听按键操作'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

    def quit_game(self):
        '''退出游戏'''
        self.running = False
        sys.exit()
        

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    fg = Game()
    try:
        fg.run_game()
    finally:
        fg.quit_game()