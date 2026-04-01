from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def get_info(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time

    def get_pets(self) -> List[Pet]:
        pass

    def schedule_appointment(self, pet: Pet, service: 'Service', time: str) -> 'Appointment':
        pass


class Appointment:
    def __init__(self, date: str, time: str, duration: int, pet: Pet, service: 'Service'):
        self.date = date
        self.time = time
        self.duration = duration
        self.pet = pet
        self.service = service

    def schedule(self) -> None:
        pass

    def cancel(self) -> None:
        pass


@dataclass
class Service:
    name: str
    description: str
    default_duration: int

    def get_details(self) -> str:
        pass
