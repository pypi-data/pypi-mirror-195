import os

# Disabling welcome message when importing pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

try:
    from NepalStockTracker.Assets import Assets

except ImportError:
    from Assets import Assets


def Play():
    '''
    Play error audio
    '''

    AudioFile = Assets().ErrorAudio

    pygame.mixer.init()
    pygame.mixer.music.load(AudioFile)

    pygame.mixer.music.play()
