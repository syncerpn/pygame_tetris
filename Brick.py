# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:53:11 2023

@author: NghiaServer
"""

import numpy as np
import pygame
from SPEC import _COLOR_GREEN

_O = "O"
_I = "I"
_L = "L"
_J = "J"
_S = "S"
_Z = "Z"

class Brick:
    _size = 10
    _color = _COLOR_GREEN
    def __init__(self, shape=None):
        self.block = None
        if shape is None:
            shape_list = [_O, _I, _L, _J, _S, _Z]
            shape = np.random.choice(shape_list, 1)[0]
        
        if shape == _O:
            self.block = np.array([[1,1],[1,1]], dtype=np.uint8)
        elif shape == _I:
            self.block = np.array([[1],[1],[1],[1]], dtype=np.uint8)
        elif shape == _L:
            self.block = np.array([[1,0],[1,0],[1,1]], dtype=np.uint8)
        elif shape == _J:
            self.block = np.array([[0,1],[0,1],[1,1]], dtype=np.uint8)
        elif shape == _S:
            self.block = np.array([[0,1,1],[1,1,0]], dtype=np.uint8)
        elif shape == _Z:
            self.block = np.array([[1,1,0],[0,1,1]], dtype=np.uint8)
    
    def get_rotate_shape(self):
        h, w = self.block.shape
        new_block = np.zeros((w, h), dtype=np.uint8)
        for ih in range(h):
            for iw in range(w):
                new_block[iw, h-1-ih] = self.block[ih, iw]
        
        return new_block
    
    def render_on(self, main_surf, pos):
        x, y = pos
        h, w = self.block.shape
        for ih in range(h):
            for iw in range(w):
                if self.block[ih, iw]:
                    pygame.draw.rect(main_surf, Brick._color, pygame.Rect((x + iw) * Brick._size, (y + ih) * Brick._size, Brick._size, Brick._size))