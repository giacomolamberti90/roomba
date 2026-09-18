from roomba.direction import Direction
from roomba.robot import Roomba


def test_default_start_pose():
    roomba = Roomba()
    assert (roomba.x, roomba.y) == (0, 0)
    assert roomba.facing is Direction.NORTH


def test_turn_right_changes_facing_not_position():
    roomba = Roomba()
    roomba.turn_right()
    assert roomba.facing is Direction.EAST
    assert (roomba.x, roomba.y) == (0, 0)


def test_cell_ahead_does_not_mutate():
    roomba = Roomba(x=3, y=4, facing=Direction.EAST)
    assert roomba.cell_ahead() == (4, 4)
    assert (roomba.x, roomba.y, roomba.facing) == (3, 4, Direction.EAST)


def test_move_to():
    roomba = Roomba()
    roomba.move_to(2, 5)
    assert (roomba.x, roomba.y) == (2, 5)
    assert roomba.facing is Direction.NORTH
