from typing import Dict, Callable, Tuple, Optional, Iterator

import pygame
from pygame import Color, Surface

from engine import Camera, Pole, Stand, Disk

MIN_DISK_WIDTH: float = 2.
MAX_DISK_WIDTH: float = 5.
MIN_DISK_HEIGHT: float = 1.
MIN_POLE_WIDTH: float = 1.
MIN_STAND_HEIGHT: float = 1.
MIN_DISK_COUNT: int = 2


IsMoveValid = Callable[[Dict[str, Pole], str, str], bool]
IsGameOver = Callable[[Dict[str, Pole]], bool]
MoveGenerator = Callable[[int, Dict[str, Pole]], Iterator[Tuple[str, str]]]


class HanoiScene:
    _is_move_valid: IsMoveValid
    _is_game_over: IsGameOver
    _move_generator: MoveGenerator
    _disk_height: float
    _pole_width: float
    _stand_height: float
    _num_disk: int
    _camera: Camera
    _poles: Dict[str, 'Pole']
    _stand: 'Stand'

    def __init__(self, is_move_valid: IsMoveValid,
                 is_game_over: IsGameOver,
                 move_generator: MoveGenerator,
                 disk_height: float = MIN_DISK_HEIGHT, pole_width: float = MIN_POLE_WIDTH,
                 stand_height: float = MIN_STAND_HEIGHT, num_disks: int = MIN_DISK_COUNT):
        self._is_move_valid = is_move_valid
        self._is_game_over = is_game_over
        self._move_generator = move_generator
        self._disk_height = disk_height
        self._pole_width = pole_width
        self._stand_height = stand_height
        self._num_disk = num_disks
        self._camera = Camera(x=0., y=0., zoom=20.)
        self._create_objetcs(num_disks)
        self._set_camera_y()

    def _set_camera_y(self):
        y_center = (self._stand.height + next(iter(self._poles.values())).height) / 2
        self._camera.y = y_center

    def _create_objetcs(self, disk_count: int):
        assert disk_count >= MIN_DISK_COUNT
        stand_color = Color(235, 211, 115)
        self._stand = Stand(
            x_center=0,
            y_bottom=0,
            width=4 * MAX_DISK_WIDTH,
            height=self._stand_height,
            color=stand_color,
        )
        pole_names = ['A', 'B', 'C']
        self._poles = dict()
        for i in [-1, 0, 1]:
            self._poles[pole_names[i + 1]] = Pole(x_center=i * MAX_DISK_WIDTH,
                                                  y_bottom=self._stand_height,
                                                  width=self._pole_width,
                                                  height=(disk_count + 1) * self._disk_height,
                                                  color=stand_color,
                                                  )
        left_pole = self._poles[pole_names[0]]
        for i in range(disk_count):
            left_pole.add_disk(
                Disk(
                    x_center=0,
                    y_bottom=0,
                    width=MAX_DISK_WIDTH - (MAX_DISK_WIDTH - MIN_DISK_WIDTH) * (i / disk_count),
                    height=self._disk_height,
                )
            )

    def run(self):
        pygame.init()
        try:
            self._do_run()
        finally:
            pygame.quit()

    def _do_run(self):
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        moves_iterator = iter(self._move_generator(self._num_disk, self._poles))
        background_color = Color(230, 249, 255)
        state = 'playing'
        optimal_num_plays = 2 ** self._num_disk - 1
        num_plays = 0

        running = True
        while running:
            for event in pygame.event.get():
                running = event.type != pygame.QUIT

                if event.type == pygame.MOUSEWHEEL:
                    self._camera.zoom += event.y
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                match state:
                    case 'playing':
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                                or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                            src, dst = next(moves_iterator)
                            if self._is_move_valid(self._poles, src, dst):
                                self._poles[src].move_upper_disk(self._poles[dst])
                                num_plays += 1
                            else:
                                state = 'wrong move'
                                print(f"Impossible de déplacer un disque de {src} vers {dst}")
                        if self._is_game_over(self._poles):
                            state = 'win'
                            print(f'Nombre de coups joués : {num_plays}')
                            print(f'Nombre de coups optimal : {optimal_num_plays}')
                    case 'win':
                        background_color = Color(179, 255, 179)
                    case 'wrong move':
                        background_color = Color(255, 179, 179)

            screen.fill(background_color)
            self._render_on(screen)
            pygame.display.flip()

    def _render_on(self, surface: Surface):
        self._camera.render(surface, self._stand)
        for pole in self._poles.values():
            self._camera.render(surface, pole)
            for disk in pole._disks:
                self._camera.render(surface, disk)
