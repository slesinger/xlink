
class Cursor():
    x: int
    y: int
    color: int
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def move_left(self, distance: int) -> None:
        self.x -= distance

    def move_right(self, distance: int) -> None:
        self.x += distance

    def move_up(self, distance: int) -> None:
        self.y -= distance

    def move_down(self, distance: int) -> None:
        self.y += distance

    def move_to(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def move_to_x(self, x: int) -> None:
        self.x = x

    def move_to_y(self, y: int) -> None:
        self.y = y

    def move_left(self) -> None:
        self.x -= 1

    def move_right(self) -> None:
        self.x += 1

    def move_up(self) -> None:
        self.y -= 1

    def move_down(self) -> None:
        self.y += 1

    def move_to_top(self) -> None:
        self.y = 0

    def move_to_bottom(self) -> None:
        self.y = 24

    def move_to_left(self) -> None:
        self.x = 0

    def move_to_right(self) -> None:
        self.x = 79

    def move_to_home(self) -> None:
        self.x = 0
        self.y = 0

    def move_to_end(self) -> None:
        self.x = 79
        self.y = 24

    def move_to_next_line(self) -> None:
        self.x = 0
        self.y += 1

    def move_to_previous_line(self) -> None:
        self.x = 0
        self.y -= 1

    def move_to_next_line(self, lines: int) -> None:
        self.x = 0
        self.y += lines

    def move_to_previous_line(self, lines: int) -> None:
        self.x = 0
        self.y -= lines

    def move_to_next_line(self, lines: int) -> None:
        self.x = 0
        self.y += lines