"Board class"
from collections import namedtuple

Color = namedtuple("Color", "name hex")

COLORS = [
    Color("red", "#FF0000"),
    Color("green", "#52FF00"),
    Color("blue", "#0043FF"),
    Color("yellow", "#F2FF00"),
    Color("pink", "#FF69B4"),
    Color("purple", "#800080"),
]


class PlayerExistsError(ValueError):
    "Raised if a player with pid already exists"


class PlayerNotFoundError(ValueError):
    "Raised if a player with pid doesn't exist"


class NotTurnError(ValueError):
    "Raised if it is not that player's turn"

class Board():
    """
    Class representing the snakes and ladders board. Parameters:
        - board: A dict which represents all snakes and ladders as a dict
            where the key is the place it start and value is the place it ends.
            e.g.
            {
                11: 99,
                98: 2
            } is a board where there is a ladder from 11 to 99 and a snake from
                98 to 2.
        - image: Path / an object with .read() which represents a 800x800 image
            with no padding and a grid of 10x10 where each square is 80x80
            representing the board in standard zig zag format as shown below

            |100|99|98|97|96|95|94|93|92|91|
            | 81|82|83|84|85|86|87|88|89|80|
            | 80|79|78|77|76|75|74|73|72|71|
            | 61|62|63|64|65|66|67|68|69|70|
            | 60|59|58|57|55|55|54|53|52|51|
            | 41|42|43|44|46|45|47|48|49|50|
            | 40|39|38|37|35|36|34|33|32|31|
            | 21|22|23|24|26|25|27|28|29|30|
            | 20|19|18|17|15|16|14|13|12|11|
            |  1| 2| 3| 4| 5| 5| 7| 8| 9|10|
    """
    def __init__(self, board, image=None, *, new_turn_on_six=False):
        self.board = dict(board)
        if image is None:
            self.image = None
        elif isinstance(image, str):
            with open(image, "rb") as img:
                self.image = img.read()
        else:
            self.image = image
        self.players = []
        self.turn_idx = 0
        self.new_turn_on_six = new_turn_on_six

    def add_player(self, pid, name):
        "Adds a player with the id and returns a colorname, colorid tuple"
        color = COLORS[len(self.players) % len(COLORS)]
        if pid in (player["pid"] for player in self.players):
            raise PlayerExistsError
        self.players.append({
            "pid": pid,
            "name": name,
            "color": color,
            "position": 0,
        })
        return color

    def move(self, pid, steps, *, check_turn=False):
        """
        Moves a player with pid as given pid steps. If check_turn is True, only
        moves if it is the turn of pid.  Returns a tuple of final position
        after snakes and ladders have been travelled (if any) and a number
        indicating if a ladder / snake has been travelled.
        1 - Ladder travelled
        0 - Nothing travelled
        -1 - Snake travelled
        """
        idx, player = self._get_player(pid)
        if check_turn and idx != self.turn_idx:
            raise NotTurnError
        movement = 0
        new_position = player["position"] + steps

        # Don't move unless you get exact number
        if new_position > 100:
            new_position = player["position"]
        # Check for snakes and ladders
        elif new_position in self.board:
            movement = self.board[new_position] - new_position
            movement = movement//abs(movement)  # Get's the signum of movement
            new_position = self.board[new_position]

        player["position"] = new_position
        if not steps == 6 and not self.new_turn_on_six:
            turn_idx = (turn_idx + 1) % len(self.players)
        return (new_position, movement)

    def remove_player(self, pid):
        "Removes the player with pid"

    def draw(self):
        "Returns the image with all players drawn on it"

    @property
    def turn(self):
        "Returns the player whose turn it is"
        if not self.players:
            return None
        return dict(self.players[self.turn_idx])

    def _get_player(self, pid):
        "Internal use only: Returns the idx, player"
        for idx, player in enumerate(self.players):
            if player["pid"] == pid:
                return (idx, player)
        raise PlayerNotFoundError
