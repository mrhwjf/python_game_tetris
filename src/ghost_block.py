# ghost_block.py
from block import Block
from position import Position

# No import of Grid here to avoid the circular mess

def get_ghost_block_position(block: Block, grid) -> list[Position]:
    ghost_block = Block(block.id)
    ghost_block.cells = block.cells
    ghost_block.rotation_state = block.rotation_state
    ghost_block.row_offset = block.row_offset
    ghost_block.column_offset = block.column_offset

    while True:
        ghost_block.move(1, 0)
        if not block_inside(ghost_block, grid) or not block_fits(ghost_block, grid):
            ghost_block.move(-1, 0)
            break

    return ghost_block.get_cell_positions()

def block_inside(block: Block, grid) -> bool:
    for tile in block.get_cell_positions():
        if not grid.is_inside(tile.row, tile.column):
            return False
    return True

def block_fits(block: Block, grid) -> bool:
    for tile in block.get_cell_positions():
        if not grid.is_empty(tile.row, tile.column):
            return False
    return True
