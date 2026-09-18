from roomba.direction import Direction


def test_turn_right_cycles_clockwise():
    assert Direction.NORTH.turn_right() is Direction.EAST
    assert Direction.EAST.turn_right() is Direction.SOUTH
    assert Direction.SOUTH.turn_right() is Direction.WEST
    assert Direction.WEST.turn_right() is Direction.NORTH


def test_deltas():
    assert Direction.NORTH.delta == (0, 1)
    assert Direction.EAST.delta == (1, 0)
    assert Direction.SOUTH.delta == (0, -1)
    assert Direction.WEST.delta == (-1, 0)


def test_symbols():
    assert Direction.NORTH.symbol == "^"
    assert Direction.EAST.symbol == ">"
    assert Direction.SOUTH.symbol == "v"
    assert Direction.WEST.symbol == "<"
