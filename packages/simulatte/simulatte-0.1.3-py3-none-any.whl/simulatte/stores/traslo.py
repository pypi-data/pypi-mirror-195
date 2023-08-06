from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

import matplotlib.pyplot as plt
import simpy

import simulatte

if TYPE_CHECKING:
    from simulatte.stores import WarehouseLocation, WarehouseStore

T = TypeVar("T", bound=simulatte.unitload.CaseContainer)


class Traslo(simpy.PriorityResource, Generic[T]):
    def __init__(
        self, *, store: WarehouseStore, x: int, y: int, speed_x: float, speed_y: float, load_time: float
    ) -> None:
        self.env = simulatte.Environment()
        super().__init__(self.env, capacity=1)

        self.store = store
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.load_time = load_time

        self._handling_time = 0
        self._saturation_history: simulatte.typings.History[float] = [(0, 0)]
        self._unit_load: T | None = None

    @property
    def handling_time(self) -> float:
        return self._handling_time

    @handling_time.setter
    def handling_time(self, handling_time: float) -> None:
        self._handling_time = handling_time
        self._saturation_history.append((self.env.now, self.saturation))

    @property
    def saturation(self) -> float:
        return self._handling_time / self.env.now

    @property
    def unit_load(self) -> T | None:
        return self._unit_load

    @unit_load.setter
    def unit_load(self, unit_load: T | None) -> None:
        if self._unit_load is not None and unit_load is not None:
            raise RuntimeError("The traslo is already loaded.")

        if self._unit_load is None and unit_load is None:
            raise RuntimeError("The traslo is not loaded.")

        self._unit_load = unit_load

    @simulatte.as_process
    def move(self, *, location: WarehouseLocation) -> None:
        time_x = abs(self.x - location.x) * location.width / self.speed_x
        time_y = abs(self.y - location.y) * location.height / self.speed_y
        t = max(time_x, time_y)
        yield self.env.timeout(max(time_x, time_y))
        self.handling_time += t
        self.x, self.y = location.x, location.y

    @simulatte.as_process
    def load(self, *, unit_load: T) -> None:
        self.unit_load = unit_load
        yield self.env.timeout(self.load_time)
        self.handling_time += self.load_time

    @simulatte.as_process
    def unload(self) -> None:
        self.unit_load = None
        yield self.env.timeout(self.load_time)
        self.handling_time += self.load_time

    def plot(self) -> None:
        x = [t / 3600 for t, _ in self._saturation_history]
        y = [s * 100 for _, s in self._saturation_history]
        plt.plot(x, y)
        plt.xlabel("Time [h]")
        plt.ylabel(f"Saturation [%]")
        plt.title(f"{self.store.name} {self.__class__.__name__} Productivity")
        plt.ylim([0, 100])
        plt.show()
