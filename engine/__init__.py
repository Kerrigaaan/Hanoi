from dataclasses import dataclass, field
from typing import Tuple, List, Optional

import pygame
from pygame import Color, Surface

from util import random_color


@dataclass
class Camera:
    x: float
    y: float
    zoom: float

    def world_to_pixel(self, target: Surface, x: float, y: float) -> Tuple[int, int]:
        relative_x = x - self.x
        relative_y = y - self.y
        pixel_x = int(relative_x * self.zoom) + target.get_width() // 2
        pixel_y = int(-relative_y * self.zoom) + target.get_height() // 2
        return pixel_x, pixel_y

    def render(self, target: Surface, obj: 'SceneObject'):
        pixel_x, pixel_y = self.world_to_pixel(
            target=target,
            x=obj.x_center - obj.width / 2,
            y=obj.y_bottom + obj.height
        )
        rect = (
            pixel_x,
            pixel_y,
            obj.width * self.zoom,
            obj.height * self.zoom,
        )
        pygame.draw.rect(target, obj.color, rect)


@dataclass
class SceneObject:
    x_center: float = 0
    y_bottom: float = 0
    width: float = 1.
    height: float = 1.
    color: Color = field(default_factory=random_color)

    def move_to(self, x_center: float, y_bottom: float):
        self.x_center = x_center
        self.y_bottom = y_bottom

    def render_on(self, target: Surface, camera: Camera):
        camera.render(target, self)


class IllegalMoveError(RuntimeError):
    pass


class Disk(SceneObject):
    pass


@dataclass
class Pole(SceneObject):
    _disks: List[Disk] = field(default_factory=list)

    def add_disk(self, disk: Disk):
        if len(self._disks) != 0 and self._disks[-1].width <= disk.width:
            raise IllegalMoveError()
        disk.move_to(self.x_center,
                     self.y_bottom + sum([e.height for e in self._disks]))
        self._disks.append(disk)

    def move_upper_disk(self, target: 'Pole'):
        if len(self._disks) == 0:
            raise IllegalMoveError()

        upper_disk = self._disks[-1]
        self._disks = self._disks[:-1]
        target.add_disk(upper_disk)

    def render_on(self, target: Surface, camera: Camera):
        super().render_on(target, camera)
        for disk in self._disks:
            disk.render_on(target, camera)

    @property
    def upper_disk(self) -> Optional[Disk]:
        if len(self._disks) == 0:
            return None
        return self._disks[-1]

    @property
    def num_disks(self) -> int:
        return len(self._disks)


@dataclass
class Stand(SceneObject):
    _poles: List[Pole] = field(default_factory=list)

    def add_pole(self, pole: Pole):
        self._poles.append(pole)
        x_left = self.x_center - self.width / 2.
        pole_count = len(self._poles)
        for i in range(pole_count):
            pole = self._poles[i]
            pole.x_center = x_left + self.width * (i + 1) / (pole_count + 1)

    def render_on(self, target: Surface, camera: Camera):
        super().render_on(target, camera)
