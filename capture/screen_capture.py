# capture/screen_capture.py
import numpy as np
import pygame.surfarray
from collections import deque
import cv2

class FrameProcessor:
    def __init__(self, stack_size=4, width=84, height=84):
        self.stack = deque(maxlen=stack_size)
        self.target_size = (width, height)

    def process(self, screen):
        # Capture
        frame = pygame.surfarray.array3d(screen)
        frame = np.transpose(frame, (1, 0, 2))[:, :, ::-1]  # RGB

        # Grayscale + resize
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.resize(gray, self.target_size, interpolation=cv2.INTER_AREA)
        gray = gray.astype(np.float32) / 255.0

        self.stack.append(gray)

        # Pad si pas assez de frames
        while len(self.stack) < self.stack.maxlen:
            self.stack.append(gray)

        return np.stack(self.stack, axis=0)  # (4, 84, 84)