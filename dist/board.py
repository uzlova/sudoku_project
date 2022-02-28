class Board:
    def __init__(self, wight, height):
        self.width = wight
        self.height = height
        self.board = [[0] * wight for _ in range(height)]
        self.left = 65
        self.top = 65
        self.cell_size = 15
        self.set_view(self.left, self.top, self.cell_size)

    def on_click(self, cell):
        pass

    def set_view(self, left, top, cell_self):
        self.left = left
        self.top = top
        self.cell_size = cell_self

    def get_cell(self, mouse_pos):
        x1 = (mouse_pos[0] - self.left) // self.cell_size
        y1 = (mouse_pos[1] - self.top) // self.cell_size
        if x1 < 0 or x1 >= self.width or y1 < 0 or y1 >= self.height:
            return None
        return x1, y1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, "white", ((j * self.cell_size,
                                                    i * self.cell_size), (self.cell_size,
                                                                          self.cell_size)), 1)  # поля
