# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 23:28:39 2022
Updated on Fri Jul 21 16:49:00 2023: re-organize flow

@author: nghia_sv
"""

import pygame
# from pygame.locals import *
from SPEC import _COLOR_WHITE, \
                 _FONT_PFT, _FONT_SIZE, _TR_DEF

_WINDOW_W = 640
_WINDOW_H = 400
_FRAME_RATE = 60

#screen layers
_SCREEN_L_BACKGR = 0
_SCREEN_L_OBJECT = 1
_SCREEN_L_FOREGR = 2
_SCREEN_L_UI     = 3
_SCREEN_LAYERS   = 4

class Game:
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._clock = None

        self._render_cache = {i : [] for i in range(_SCREEN_LAYERS)}
        
        self._text_renderer = {}

        self.window_w, self.window_h = _WINDOW_W, _WINDOW_H

    #initialization; run once when the game is executed
    def on_init(self):
        pygame.init()
        pygame.font.init()
        
        self._display_surf = pygame.display.set_mode((self.window_w, self.window_h), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._text_renderer[_TR_DEF] = pygame.font.Font(_FONT_PFT, _FONT_SIZE)
        self._running = True
        
        self._clock = pygame.time.Clock()
        return True
    
    #proceeds events like pressed keys, mouse motion etc.; maybe let each game obj handles the input on its own
    def on_event(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
        
        # self.player.handle_input(events, keys)
    
    #compute changes on game objects
    def on_update(self):
        # self.player.update()
        pass
    
    #append elements into layers and render layers onto screen
    def on_render(self):
        # self._render_cache[_SCREEN_L_FOREGR].append(self.player.render())

        #main: chaining display update
        # self._display_surf.fill(_COLOR_WHITE)
        
        # for layer in self._render_cache:
        #     for image, position in self._render_cache[layer]:
        #         self._display_surf.blit(image, position)
        
        # pygame.display.flip()
        
        #clear render cache
        # self._render_cache = {i : [] for i in range(_SCREEN_LAYERS)}
        
        pass
    
    #collects garbage on leaving the game
    def on_cleanup(self):
        pygame.quit()
    
    #framework logic
    def on_execute(self):
        #initialization
        if not self.on_init():
            self._running = False
        
        #game loop
        while self._running:
            #event check
            self.on_event()

            #state update
            self.on_update()

            #output render
            self.on_render()

            #next tick
            self._clock.tick(_FRAME_RATE)

        #finishing
        self.on_cleanup()
        
if __name__ == "__main__" :
    game = Game()
    game.on_execute()
