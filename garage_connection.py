from aladdin_connect import AladdinConnectClient
from enum import StrEnum

class DoorStatus(StrEnum):
    open = 'open'
    closed = 'closed'
    opening = 'opening'
    closing = 'closing'
    unknown = 'unknown'

class Door:
    def __init__(self, obj):
        self.id = obj['device_id']
        self.number = obj['door_number']

class GarageConnection:
    def __init__(self, user, password):
        # assert valid == "validation_hack", "Please don't call this constructor directly. Use create instead."
        self.client = AladdinConnectClient(user, password)
        self.client.login()

        self._doors = self.client.get_doors()
        self.door = Door(self._doors[0])

    def open_door(self):
        self.client.open_door(self.door.id, self.door.number)

    def close_door(self):
        self.client.close_door(self.door.id, self.door.number)
    
    def get_status(self):
        key = self.client.get_door_status(self.door.id, self.door.number)
        return DoorStatus[key]

    def is_open(self):
        return self.get_status() == DoorStatus.open

    def can_open(self):
        return self.get_status() == DoorStatus.closed

    def can_close(self):
        return self.is_open()