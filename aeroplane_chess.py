"""
Monte Carlo Simulation about Aeroplane Chess

by Yifan Bao, Mingyan Gong
last update on 04/23/2019
"""
import random


COLOR = ['red', 'yellow', 'blue', 'green']


class Plane:

    __all_pieces = {'red': [],
                    'yellow': [],
                    'blue': [],
                    'green': []}

    __entering_location = {'red': 39,
                           'yellow': 0,
                           'blue': 13,
                           'green': 26}

    def __init__(self, color, location='hangar'):
        self.color = color
        self.location = location
        self.location_color = color
        self.distance_travelled = 0
        Plane.__all_pieces[color].append(self)

    @staticmethod
    def clear_board():
        for color in COLOR:
            while len(Plane.__all_pieces[color]):
                piece = Plane.__all_pieces[color].pop(0)
                del piece

    def update_location_color(self):
        if isinstance(self.location, int):
            self.location_color = COLOR[self.location % 4 - 1]
        else:
            raise ValueError('Cannot update location color!')

    def standby(self):
        if self.location != 'hangar':
            raise ValueError('Plane have entered in!')
        else:
            self.location = 'standby'

    def move(self, distance: int, enable_jump=True):
        # Move the plane
        self.distance_travelled += distance
        # TODO: update location, consider standby
        # TODO: enter into home zone
        self.update_location_color()

        # When landing on an opponent's piece, send back that piece to its hangar
        # TODO: get_plane_at(self.location), send_back()

        # When landing on the entrance of the plane color's shortcut, jump to the exit
        if self.distance_travelled == 18:
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
        self.setup_planes()

    @staticmethod
    def setup_players(number=4):
        for player_no in range(number):
            Player(COLOR[player_no])
        # TODO: check the number of players (should be 2-4)

    def setup_planes(self):
        p1 = Plane(self.color)
        p2 = Plane(self.color)
        p3 = Plane(self.color)
        p4 = Plane(self.color)
        self.moving_planes = [p1, p2, p3, p4]

    def move_plane(self):
        # Roll the dice
        dice = random.randint(1, 6)

        # Get a list of all planes that are available to move or standby,
        # and select one from them to move
        available_planes = []
        if dice == 6:
            # If there are planes in the hangar, get one of them standby
            for plane in self.moving_planes:
                if plane.location == 'hangar':
                    available_planes.append(plane)
            if len(available_planes):
                selected_plane = random.choice(available_planes)
                selected_plane.standby()
            # If not, move one of the planes in the track
            else:
                available_planes = self.moving_planes
                selected_plane = random.choice(available_planes)
                selected_plane.move(6)
            # Get another roll after rolling a 6
            self.move_plane()
        else:
            # A roll of 1-5, move a plane in the track
            for plane in self.moving_planes:
                if plane.location != 'hangar':
                    available_planes.append(plane)
            if len(available_planes):
                selected_plane = random.choice(available_planes)
                selected_plane.move(dice)

