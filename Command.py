from __future__ import annotations
from abc import ABC, abstractmethod
import snake
import os
import global_variables as gv
import pygame


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class StartTheGameCommand(Command):
    def execute(self) -> None:
        game = snake.Snake()
        gv.load_bg_music('game_bg_music.mp3')
        if not gv.music_volume:
            pygame.mixer.music.pause()
        game.run()


class HelpCommand(Command):
    def execute(self) -> None:
        os.system("hh.exe help.chm")


class ChangeVolumeCommand(Command):
    def __init__(self):
        self.value = True

    def execute(self) -> None:
        gv.volume = self.value


class ChangeMusicVolumeCommand(Command):
    def __init__(self):
        self.value = True

    def execute(self) -> None:
        gv.music_volume = self.value
        if not self.value:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()


class Invoker:
    def __init__(self, start_the_game, help, change_volume, change_music_value):
        self._start_the_game = start_the_game
        self._help = help
        self._change_volume = change_volume
        self._change_music_value = change_music_value

    def start_the_game(self):
        self._start_the_game.execute()

    def help(self):
        self._help.execute()

    def change_volume(self, string, value):
        self._change_volume.value = value
        self._change_volume.execute()

    def change_music_volume(self, string, value):
        self._change_music_value.value = value
        self._change_music_value.execute()

    def change_resolution(self, string, value):
        self._change_resolution.value = value
        self._change_resolution.execute()


invoker = Invoker(StartTheGameCommand(), HelpCommand(), ChangeVolumeCommand(), ChangeMusicVolumeCommand())
