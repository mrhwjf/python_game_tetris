from game.block import Block
from game.position import Position

BLOCK_CELLS = {
    1: {
        0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
        1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
        2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
        3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
    },
    2: {
        0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
        1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
        2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
        3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
    },
    3: {
        0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
        1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
        2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
        3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
    },
    4: {
        0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
    },
    5: {
        0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
        1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
        2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
        3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
    },
    6: {
        0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
        1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
        2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
        3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
    },
    7: {
        0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
        1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
        2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
        3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
    }
}

class LBlock(Block):
    def __init__(self):
        super().__init__(id=1)
        self.cells = BLOCK_CELLS[1]
        self.move(0, 3)

class JBlock(Block):
    def __init__(self):
        super().__init__(id=2)
        self.cells = BLOCK_CELLS[2]
        self.move(0, 3)

class IBlock(Block):
    def __init__(self):
        super().__init__(id=3)
        self.cells = BLOCK_CELLS[3]
        self.move(-1, 3)

class OBlock(Block):
    def __init__(self):
        super().__init__(id=4)
        self.cells = BLOCK_CELLS[4]
        self.move(0, 4)

class SBlock(Block):
    def __init__(self):
        super().__init__(id=5)
        self.cells = BLOCK_CELLS[5]
        self.move(0, 3)

class TBlock(Block):
    def __init__(self):
        super().__init__(id=6)
        self.cells = BLOCK_CELLS[6]
        self.move(0, 3)

class ZBlock(Block):
    def __init__(self):
        super().__init__(id=7)
        self.cells = BLOCK_CELLS[7]
        self.move(0, 3)