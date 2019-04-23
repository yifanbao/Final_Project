"""
Monte Carlo Simulation about Aeroplane Chess

by Yifan Bao, Mingyan Gong
last update on 04/23/2019
"""


COLOR = ['red', 'yellow', 'blue', 'green']


class Plane:

    __all_pieces = []

    def __init__(self, color, location='hangar'):
        self.color = color
        self.location = location
        self.location_color = color
        self.distance_travelled = 0
        Plane.__all_pieces.append(self)

    @staticmethod
    def clear_board():
        while len(Plane.__all_pieces):
            piece = Plane.__all_pieces.pop(0)
            del piece

    @staticmethod
    def setup_planes():
        # TODO: set up initial planes
        # TODO: May need to move this function outward
        r1 = Plane('red')
        r2 = Plane('red')
        r3 = Plane('red')
        r4 = Plane('red')

    def update_location_color(self):
        if isinstance(self.location, int):
            self.location_color = COLOR[self.location % 4]

    def move(self, distance: int, enable_jump=True):
        # Move the plane
        self.distance_travelled += distance
        # TODO: update location
        # TODO: enter into home zone
        self.update_location_color()

        # When landing on an opponent's piece, send back that piece to its hangar
        # TODO: get_plane_at(self.location), send_back()

        # When landing on the entrance of the plane color's shortcut, jump to the exit
        if self.distance_travelled == 17:
            self.move(12, False)
        elif enable_jump:
            # When landing on a space of the plane's own color, jump to the next space of that color
            if self.color == self.location_color:
                self.move(4, False)

    def send_back(self):
        self.location = 'hangar'
        self.location_color = self.color
        self.distance_travelled = 0


class Player:

    def __init__(self, color):
        self.color = color
        self.moving_planes = []
        self.settled_planes = []



