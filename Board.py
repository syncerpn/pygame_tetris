# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:45:12 2023

@author: NghiaServer
"""
import pygame
import numpy as np
from Brick import Brick
from SPEC import _COLOR_BLACK, _COLOR_RED

class Board:
    def __init__(self, w, h, entity_size=20):
        self.entity_size = entity_size
        self.w = w
        self.h = h
        
        self.board = np.zeros((self.h, self.w), dtype=np.uint8)
        self.brick = None
        self.brick_pos = None
        
        Brick._size = entity_size
        
    
    def progress(self):
        score = 0
        if self.brick is not None:
            if not self.try_move_brick(0, 1):
                self._carve_brick()
                score = self._remove_lines()
                self.brick = None
        else:
            self.brick = Brick()
            self.brick_pos = (self.w // 2, 0)
            if not self._is_brick_fit_board(self.brick.block, self.brick_pos):
                return -1
        
        return score
    
    def reset(self):
        self.brick = None
        self.brick_pos = None
        self.board = np.zeros((self.h, self.w), dtype=np.uint8)
    
    def _carve_brick(self):
        h, w = self.brick.block.shape
        x, y = self.brick_pos
        self.board[y:y+h, x:x+w] = self.board[y:y+h, x:x+w] | self.brick.block
    
    def _remove_lines(self):
        line_to_remove = []
        for hi in range(self.h-1,-1,-1):
            if (np.uint32(self.board[hi, :] > 0)).sum() == self.w:
                line_to_remove += [hi]
        
        new_board = np.zeros_like(self.board)
        hin = self.h - 1
        for hi in range(self.h-1,-1,-1):
            if hi in line_to_remove:
                continue
            
            new_board[hin, :] = self.board[hi, :]
            hin -= 1
        
        self.board = new_board
        return len(line_to_remove)
    
    def _is_brick_fit_board(self, brick_block, pos):
        x, y = pos
        h, w = brick_block.shape
        brick_board_next_occupied = self.board[y:y+h, x:x+w]
        h_new, w_new = brick_board_next_occupied.shape
        if h_new != h or w_new != w:
            return False
        else:
            for hi in range(h):
                for wi in range(w):
                    if brick_board_next_occupied[hi, wi] == 1 and brick_block[hi, wi] == 1:
                        return False
        return True
        
    def try_rotate_brick(self):
        if self.brick is not None:
            new_shape = self.brick.get_rotate_shape()
            if self._is_brick_fit_board(new_shape, self.brick_pos):
                self.brick.block = new_shape
                return True
            
        return False
    
    def try_move_brick(self, dx, dy):
        if self.brick is not None:
            x, y = self.brick_pos
            if self._is_brick_fit_board(self.brick.block, (x+dx, y+dy)):
                self.brick_pos = (x+dx, y+dy)
                return True
        
        return False
            
    
    def render(self):
        render_buffer = []
        rimg_main = pygame.Surface((self.w * self.entity_size, self.h * self.entity_size))
        rimg_main.fill(_COLOR_BLACK)
        
        hs, ws = np.where(self.board)
        for hi, wi in zip(hs, ws):
            pygame.draw.rect(rimg_main, _COLOR_RED, pygame.Rect(wi * self.entity_size, hi * self.entity_size, self.entity_size, self.entity_size))
        
        if self.brick is not None:
            self.brick.render_on(rimg_main, self.brick_pos)
        
        render_buffer += [(rimg_main, (0, 0))]
        return render_buffer