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
        """ this function initialize the Plane instance

        :param color: the color of plane
        :param no: the number of plane
        :param location: the location of plane
        """
        self.color = color
        self.no = no
        self.location = location
        self.location_color = color
        self.distance_travelled = 0
        Plane.__all_pieces.append(self)

    @staticmethod
    def clear_board():
        """ this function will delete all the planes

        :return: nothing
        >>> p1 = Plane('red', 'p1')
        >>> p2 = Plane('yellow', 'p2')
        >>> Plane.clear_board()
        """
        while len(Plane.__all_pieces):
            piece = Plane.__all_pieces.pop(0)
            del piece

    def update_location(self):
        """ this function will update the location of plane when it moves

        :return: nothing
        >>> p1 = Plane('red', 'p1')
        >>> p1.update_location()
        >>> print(p1.location, p1.location_color)
        standby red
        >>> p2 = Plane('yellow', 'p2', 45)
        >>> p2.distance_travelled = 49
        >>> p2.update_location()
        >>> print(p2.location, p2.location_color)
        49 red
        >>> p3 = Plane('blue', 'p3', 'standby')
        >>> p3.distance_travelled = 5
        >>> p3.update_location()
        >>> print(p3.location, p3.location_color)
        18 yellow
        >>> p4 = Plane('green', 'p4', 50)
        >>> p4.distance_travelled = 54
        >>> p4.update_location()
        >>> print(p4.location, p4.location_color)
        home zone green
        >>> p5 = Plane('red', 'p5', 52)
        >>> p5.distance_travelled = 56
        >>> p5.update_location()
        >>> print(p5.location, p5.location_color)
        settled red
        >>> p6 = Plane('blue','p6', 'settled')
        >>> p6.distance_travelled = 3
        >>> p6.update_location()
        Traceback (most recent call last):
        ValueError: Should not update the location of a settled plane!
        >>> Plane.clear_board()
        """
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
        """ get the plane from hangar to standby

        :return: nothing
        >>> p = Plane('red', 'p')
        >>> print(p.color, p.location)
        red hangar
        >>> p.standby()
        >>> Plane.clear_board()
        """
        # TODO: use update_location instead?
        if self.location != 'hangar':
            raise ValueError('Plane have entered in!')
        else:
            self.location = 'standby'
            # print('Plane {}: {} -> {}'.format(self.no, 'hangar', 'standby'))

    def move(self, distance: int, enable_jump=True):
        """ this function move the planes

        :param distance: the distance that the plane is going to move
        :param enable_jump: whether the plane can move with shortcuts
        :return: nothing
        >>> p1 = Plane('yellow', 'p1', 'standby')
        >>> p2 = Plane('red', 'p2', 4)
        >>> p1.move(4, True)
        >>> print(p1.location, p2.location)
        4 hangar
        >>> p3 = Plane('red', 'p3', 1)
        >>> p3.distance_travelled = 14
        >>> p3.move(4, True)
        >>> print(p3.location)
        17
        >>> p4 = Plane('yellow', 'p4', 12)
        >>> p4.distance_travelled = 12
        >>> p4.move(2, True)
        >>> print(p4.location)
        30
        >>> Plane.clear_board()
        """
        # Check if there are planes stacked
        stacked_planes = self.get_planes_stacked()

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

        # Move planes in the same stack
        if len(stacked_planes):
            for plane in stacked_planes:
                plane.distance_travelled = self.distance_travelled
                plane.location = self.location
                plane.location_color = self.location_color

    def send_back_plane_against(self):
        """ send the opponents' planes back to their hangars

        :return: nothing
        >>> p1 = Plane('red', 'p1', 14)
        >>> p2 = Plane('yellow', 'p2', 14)
        >>> p1.send_back_plane_against()
        >>> print(p2.location)
        hangar
        >>> Plane.clear_board()
        """
        for plane in Plane.__all_pieces:
            if plane.location == self.location and plane.color != self.color:
                plane.send_back()

    def send_back(self):
        """ to send the plane to its hangar

        :return: nothing
        >>> p1 = Plane('red', 'p1', 14)
        >>> p1.send_back()
        >>> print(p1.location)
        hangar
        >>> Plane.clear_board()
        """
        self.location = 'hangar'
        self.location_color = self.color
        self.distance_travelled = 0

    def can_stack_after(self, distance):
        """ find out whether this plane can stack with other planes after moving

        :param distance: the distance that the plane will move
        :return: whether this plane can stack with other planes after moving
        >>> p1 = Plane('red', 'p1', 14)
        >>> p2 = Plane('yellow', 'p2', 18)
        >>> p1.can_stack_after(4)
        False
        >>> p3 = Plane('blue', 'p3', 14)
        >>> p4 = Plane('blue', 'p4', 18)
        >>> p3.can_stack_after(4)
        True
        >>> Plane.clear_board()
        """
        if isinstance(self.location, int):  # TODO: and standby
            for plane in Plane.__all_pieces:
                if isinstance(plane.location, int):
                    if self.location + distance == plane.location and self.color == plane.color:
                        return True
        return False

    def get_planes_stacked(self):
        """ get the planes that stuck with this plane

        :return:
        >>> p1 = Plane('red', 'p1', 18)
        >>> p1.distance_travelled = 4
        >>> p2 = Plane('red', 'p2', 18)
        >>> p2.distance_travelled = 4
        >>> p3 = Plane('red', 'p3', 18)
        >>> p3.distance_travelled = 4
        >>> stack = p1.get_planes_stacked()
        >>> print(len(stack))
        3
        >>> Plane.clear_board()
        """
        stack = []
        if self.distance_travelled > 0:
            for plane in Plane.__all_pieces:
                if self.distance_travelled == plane.distance_travelled and self.color == plane.color:
                    stack.append(plane)
        return stack


class Player:

    players = []

    def __init__(self, color, name, strategy=None, max_planes_on_track=4):
        """ initialize players

        :param color: the color of player
        :param name: the name of player
        :param strategy: which strategy the player will take
        :param max_planes_on_track: how many planes on the track we will control
        """
        self.color = color
        self.name = name
        self.moving_planes = []
        self.settled_planes = []
        self.strategy = strategy
        self.max_planes_on_track = max_planes_on_track
        Player.players.append(self)
        self.setup_planes()

    @staticmethod
    def clear_player():
        """ delete all the players

        :return: nothing
        >>> player1 = Player('red', 'Red')
        >>> player2 = Player('yellow', 'Yellow')
        >>> Player.clear_player()
        >>> print(len(Player.players))
        0
        """
        while len(Player.players):
            player = Player.players.pop(0)
            del player

    @staticmethod
    def setup_players(number=4):
        """ initialize all the player with some specific attributes

        :param number: the number of the players
        :return: nothing
        >>> Player.setup_players(4)
        >>> Plane.clear_board()
        >>> Player.clear_player()
        """
        if not 2 <= number <= 4:
            raise ValueError('Only 2-4 players are allowed!')
        else:
            for n in range(number - 1):
                Player(COLOR[n], COLOR[n].capitalize())
            Player('green', 'Green', '')
            # Player('green', 'Green', 'stack_planes_first')
            # Player('green', 'Green', 'control_planes_on_track')

    def setup_planes(self):
        """ set up all the planes for the player

        :return: nothing
        >>> player1 = Player('red', 'Red')
        >>> player1.setup_planes()
        >>> print(len(player1.moving_planes))
        4
        >>> player2 = Player('yellow', 'Yellow')
        >>> player2.setup_planes()
        >>> print(len(player2.moving_planes))
        4
        >>> player3 = Player('blue', 'Blue')
        >>> player3.setup_planes()
        >>> print(len(player3.moving_planes))
        4
        >>> player4 = Player('green', 'Green')
        >>> player4.setup_planes()
        >>> print(len(player4.moving_planes))
        4
        """
        p1 = Plane(self.color, 'p1')
        p2 = Plane(self.color, 'p2')
        p3 = Plane(self.color, 'p3')
        p4 = Plane(self.color, 'p4')
        self.moving_planes = [p1, p2, p3, p4]

    def move_plane(self):
        """ every actions that the player will take in one round

        :return: nothing
        >>> player1 = Player('red', 'Red')
        >>> player1.setup_planes()
        >>> player1.move_plane()
        """
        # Roll the dice
        dice = random.randint(1, 6)
        # print('Player: {}  Dice: {}'.format(self.name, dice))

        # Get a list of all planes that are available to move or standby,
        # and select one from them to move
        awaiting_planes = []
        available_planes = []
        if dice == 6:
            # If there are planes waiting in the hangar, get one of them standby
            for plane in self.moving_planes:
                if plane.location == 'hangar':
                    awaiting_planes.append(plane)
            if len(awaiting_planes):
                selected_plane = random.choice(awaiting_planes)
                selected_plane.standby()
            # If not, move one of the planes in the track
            else:
                available_planes = self.moving_planes
                selected_plane = self.select_plane_by_strategy(dice, available_planes)

                selected_plane.move(6)
                if selected_plane.location == 'settled':
                    stacked_planes = selected_plane.get_planes_stacked()
                    self.settle(selected_plane.no)
                    if len(stacked_planes):
                        for plane in stacked_planes:
                            self.settle(plane.no)
            # Get another roll after rolling a 6
            if not self.is_winner():
                self.move_plane()
        else:
            # A roll of 1-5, move a plane in the track
            for plane in self.moving_planes:
                if plane.location != 'hangar':
                    available_planes.append(plane)
            if len(available_planes):
                selected_plane = self.select_plane_by_strategy(dice, available_planes)
                selected_plane.move(dice)
                if selected_plane.location == 'settled':
                    stacked_planes = selected_plane.get_planes_stacked()
                    self.settle(selected_plane.no)
                    if len(stacked_planes):
                        for plane in stacked_planes:
                            self.settle(plane.no)

    def select_plane_by_strategy(self, dice, available_planes):
        """ decide which plane the player is going to move based on strategy

        :param dice: the result of rolling the dice
        :param available_planes: the planes that player can move
        :return: the selected plane that the player will move
        >>> player1 = Player('red', 'Red')
        >>> player1.strategy = 'control_planes_on_track'
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player1.move_plane()
        >>> player2 = Player('red', 'Red')
        >>> player2.strategy = 'stack_planes_first'
        >>> player2.setup_planes()
        >>> player2.move_plane()
        """
        if self.strategy == 'control_planes_on_track':
            on_track_planes = []
            standby_planes = []
            for plane in available_planes:
                if isinstance(plane.location, int):
                    on_track_planes.append(plane)
                elif plane.location == 'standby':
                    standby_planes.append(plane)
            if len(on_track_planes) < self.max_planes_on_track and len(standby_planes):
                return random.choice(standby_planes)
            else:
                return random.choice(available_planes)

        elif self.strategy == 'stack_planes_first':
            stackable_planes = []
            for plane in available_planes:
                if plane.can_stack_after(dice):
                    stackable_planes.append(plane)
            if len(stackable_planes):
                return random.choice(stackable_planes)
            else:
                return random.choice(available_planes)

        else:
            return random.choice(available_planes)

    def settle(self, p_no):
        """ when the plane reach the end, it will be added to settled planes

        :param p_no: the number of the settled plane
        :return: nothing
        >>> player1 = Player('red', 'Red')
        >>> player1.setup_planes()
        >>> player1.moving_planes[1].location = 'settled'
        >>> player1.settle(player1.moving_planes[1].no)
        >>> print(len(player1.settled_planes))
        1
        """
        for idx in range(len(self.moving_planes)):
            if self.moving_planes[idx].no == p_no:
                settled_plane = self.moving_planes.pop(idx)
                self.settled_planes.append(settled_plane)
                settled_plane.distance_travelled = -1
                break

    def is_winner(self):
        """

        :return:
        >>> player1 = Player('red', 'Red')
        >>> player1.setup_planes()
        >>> player1.moving_planes[0].location = 'settled'
        >>> player1.settle(player1.moving_planes[0].no)
        >>> player1.moving_planes[0].location = 'settled'
        >>> player1.settle(player1.moving_planes[0].no)
        >>> player1.moving_planes[0].location = 'settled'
        >>> player1.settle(player1.moving_planes[0].no)
        >>> player1.moving_planes[0].location = 'settled'
        >>> player1.settle(player1.moving_planes[0].no)
        >>> print(player1.is_winner())
        Red
        """
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
    for i in range(2):
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
