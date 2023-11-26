# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 23:28:39 2022
Updated on Fri Jul 21 16:49:00 2023: re-organize flow

@author: nghia_sv
"""

import pygame
# from pygame.locals import *
from SPEC import _COLOR_WHITE, _COLOR_BLACK, \
                 _FONT_PFT, _FONT_SIZE, _TR_DEF

from Board import Board

_WINDOW_W = 640
_WINDOW_H = 400
_FRAME_RATE = 60

#screen layers
_SCREEN_L_BACKGR = 0
_SCREEN_L_OBJECT = 1
_SCREEN_L_FOREGR = 2
_SCREEN_L_UI     = 3
_SCREEN_LAYERS   = 4

_STATE_BEGIN = 0
_STATE_RUNNING = 1
_STATE_OVER = 2

class Game:
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._clock = None

        self._render_cache = {i : [] for i in range(_SCREEN_LAYERS)}
        
        self._text_renderer = {}

        self.window_w, self.window_h = _WINDOW_W, _WINDOW_H
        self.board = Board(8, 15)
        self.board_update_period = 0
        self.score = 0
        self._state = None

    #initialization; run once when the game is executed
    def on_init(self):
        pygame.init()
        pygame.font.init()
        
        self._display_surf = pygame.display.set_mode((self.window_w, self.window_h), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._text_renderer[_TR_DEF] = pygame.font.Font(_FONT_PFT, _FONT_SIZE)
        self._running = True
        self._state = _STATE_BEGIN
        
        self._clock = pygame.time.Clock()
        return True
    
    #proceeds events like pressed keys, mouse motion etc.; maybe let each game obj handles the input on its own
    def on_event(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_LEFT:
                    self.board.try_move_brick(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.board.try_move_brick(1, 0)
                elif event.key == pygame.K_UP:
                    self.board.try_rotate_brick()
                elif event.key == pygame.K_DOWN:
                    self.board.try_move_brick(0, 1)
                elif event.key == pygame.K_SPACE:
                    if self._state == _STATE_BEGIN:
                        self._state = _STATE_RUNNING
                        self.board.reset()
                        self.score = 0
                    elif self._state == _STATE_OVER:
                        self._state = _STATE_BEGIN
        
        # self.player.handle_input(events, keys)
    
    #compute changes on game objects
    def on_update(self):
        # self.player.update()
        if self._state == _STATE_RUNNING:
            self.board_update_period = (self.board_update_period + 1) % (_FRAME_RATE // 4)
            if self.board_update_period == 0:
                score = self.board.progress()
                if score == -1:
                    self._state = _STATE_OVER
                else:
                    self.score += score
    
    #append elements into layers and render layers onto screen
    def on_render(self):
        if self._state == _STATE_BEGIN:
            self._render_cache[_SCREEN_L_UI] += [(self._text_renderer[_TR_DEF].render("Press Space to start", False, _COLOR_BLACK), (10, 20))]
        elif self._state == _STATE_RUNNING:
            self._render_cache[_SCREEN_L_OBJECT] += self.board.render()
            self._render_cache[_SCREEN_L_UI] += [(self._text_renderer[_TR_DEF].render(f"Score: {self.score}", False, _COLOR_BLACK), (10, self.board.h * self.board.entity_size))]
        elif self._state == _STATE_OVER:
            self._render_cache[_SCREEN_L_UI] += [(self._text_renderer[_TR_DEF].render(f"Final score: {self.score}", False, _COLOR_BLACK), (10, 20))]
        #main: chaining display update
        self._display_surf.fill(_COLOR_WHITE)
        
        for layer in self._render_cache:
            for image, position in self._render_cache[layer]:
                if layer == _SCREEN_L_OBJECT:
                    self._display_surf.blit(image, position)
                elif layer == _SCREEN_L_UI:
                    self._display_surf.blit(image, position)
                
        pygame.display.flip()
        
        #clear render cache
        self._render_cache = {i : [] for i in range(_SCREEN_LAYERS)}
            
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
