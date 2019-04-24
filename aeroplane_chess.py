"""
Monte Carlo Simulation about Aeroplane Chess

by Yifan Bao, Mingyan Gong
last update on 04/23/2019
"""
import random


COLOR = ['red', 'yellow', 'blue', 'green']


class Plane:

    __all_pieces = []

    __entering_location = {'red': 39,
                           'yellow': 0,
                           'blue': 13,
                           'green': 26}

    def __init__(self, color, no, location='hangar'):
        self.color = color
        self.no = no
        self.location = location
        self.location_color = color
        self.distance_travelled = 0
        Plane.__all_pieces.append(self)

    @staticmethod
    def clear_board():
        while len(Plane.__all_pieces):
            piece = Plane.__all_pieces.pop(0)
            del piece

    def update_location(self):
        previous_location = self.location
        if self.location == 'hangar':
            self.location = 'standby'
        elif self.location == 'standby' or isinstance(self.location, int):
            if self.distance_travelled <= 50:  # still in the track
                entering_location = Plane.__entering_location[self.color]
                self.location = entering_location + self.distance_travelled
                if self.location > 52:
                    self.location -= 52
                self.location_color = COLOR[self.location % 4 - 1]
            elif self.distance_travelled <= 55:  # entering into home zone
                self.location = 'home zone'
                self.location_color = self.color
            else:  # arrived in the center
                self.location = 'settled'
        elif self.location == 'home zone':
            if self.distance_travelled >= 56:
                self.location = 'settled'
        elif self.location == 'settled':
            raise ValueError('Should not update the location of a settled plane!')

        # print('Plane {}: {} -> {} {}'.format(self.no, previous_location, self.location, self.location_color))

    def standby(self):
        """

        :return:
        >>> p = Plane('red')
        >>> print(p.color, p.location)
        red hangar
        >>> p.standby()
        Hangar -> Standby
        """
        # TODO: use update_location instead?
        if self.location != 'hangar':
            raise ValueError('Plane have entered in!')
        else:
            self.location = 'standby'
            # print('Plane {}: {} -> {}'.format(self.no, 'hangar', 'standby'))

    def move(self, distance: int, enable_jump=True):
        # Move the plane
        self.distance_travelled += distance
        self.update_location()

        if isinstance(self.location, int):
            # When landing on an opponent's piece, send back that piece to its hangar
            self.send_back_plane_against()

            # When landing on the entrance of the plane color's shortcut, jump to the exit
            if self.distance_travelled == 18:
                self.move(12, False)
            elif enable_jump:
                # When landing on a space of the plane's own color, jump to the next space of that color
                if self.color == self.location_color:
                    self.move(4, False)

    def send_back_plane_against(self):
        for plane in Plane.__all_pieces:
            if plane.location == self.location and plane.color != self.color:
                plane.send_back()

    def send_back(self):
        self.location = 'hangar'
        self.location_color = self.color
        self.distance_travelled = 0


class Player:

    players = []

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.moving_planes = []
        self.settled_planes = []
        Player.players.append(self)
        self.setup_planes()

    @staticmethod
    def clear_player():
        while len(Player.players):
            player = Player.players.pop(0)
            del player

    @staticmethod
    def setup_players(number=4):
        if not 2 <= number <= 4:
            raise ValueError('Only 2-4 players are allowed!')
        else:
            for n in range(number):
                Player(COLOR[n], COLOR[n].capitalize())

    def setup_planes(self):
        p1 = Plane(self.color, 'p1')
        p2 = Plane(self.color, 'p2')
        p3 = Plane(self.color, 'p3')
        p4 = Plane(self.color, 'p4')
        self.moving_planes = [p1, p2, p3, p4]

    def move_plane(self):
        # Roll the dice
        dice = random.randint(1, 6)
        # print('Player: {}  Dice: {}'.format(self.name, dice))

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
                if selected_plane.location == 'settled':
                    self.settle(selected_plane.no)
            # Get another roll after rolling a 6
            if not self.is_winner():
                self.move_plane()
        else:
            # A roll of 1-5, move a plane in the track
            for plane in self.moving_planes:
                if plane.location != 'hangar':
                    available_planes.append(plane)
            if len(available_planes):
                selected_plane = random.choice(available_planes)
                selected_plane.move(dice)
                if selected_plane.location == 'settled':
                    self.settle(selected_plane.no)

    def settle(self, p_no):
        for idx in range(len(self.moving_planes)):
            if self.moving_planes[idx].no == p_no:
                settled_plane = self.moving_planes.pop(idx)
                self.settled_planes.append(settled_plane)
                break

    def is_winner(self):
        if len(self.moving_planes):
            return None
        else:
            return self.name


if __name__ == '__main__':
    number_of_players = 4
    count_of_wins = {'Red': 0,
                     'Yellow': 0,
                     'Blue': 0,
                     'Green': 0}
    for i in range(100):
        Player.setup_players(number_of_players)
        winner = None
        while winner is None:
            for player_no in range(number_of_players):
                current_player = Player.players[player_no]
                current_player.move_plane()
                winner = current_player.is_winner()
                if winner is not None:
                    break
        print('The winner of this round is', winner)
        count_of_wins[winner] += 1
        Player.clear_player()

    print('\nRed:{}  Yellow:{}  Blue:{}  Green:{}'.format(count_of_wins['Red'], count_of_wins['Yellow'],
                                                        count_of_wins['Blue'], count_of_wins['Green']))

    print()
