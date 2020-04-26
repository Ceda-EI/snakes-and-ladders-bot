"Board class"

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
    def __init__(self, board, image=None):
        pass

    def add_player(self, pid, name):
        "Adds a player with the id and returns a colorname, colorid tuple"

    def move(self, pid, steps, *, check_turn=False):
        """
        Moves a player with pid as given pid steps. Returns final position
        after snakes and ladders have been travelled (if any). If check_turn
        is True, only moves if it is the turn of pid.
        """

    def remove_player(self, pid):
        "Removes the player with pid"

    def draw(self):
        "Returns the image with all players drawn on it"

    @property
    def turn(self):
        "Returns the player whose turn it is"
