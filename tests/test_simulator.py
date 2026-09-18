from roomba.direction import Direction
from roomba.robot import Roomba
from roomba.simulator import GRID_SIZE, Grid, Simulator


def test_open_space_forward():
    sim = Simulator()
    sim.forward()
    assert (sim.roomba.x, sim.roomba.y) == (0, 1)
    assert sim.roomba.facing is Direction.NORTH


def test_wall_turns_right_instead_of_moving():
    sim = Simulator(Roomba(x=0, y=0, facing=Direction.WEST))
    sim.forward()
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)
    assert sim.roomba.facing is Direction.NORTH


def test_corner_turns_once_and_stays():
    sim = Simulator(Roomba(x=0, y=0, facing=Direction.SOUTH))
    sim.forward()
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)
    assert sim.roomba.facing is Direction.WEST


def test_opposite_edge_north():
    sim = Simulator(Roomba(x=9, y=9, facing=Direction.NORTH))
    sim.forward()
    assert (sim.roomba.x, sim.roomba.y) == (9, 9)
    assert sim.roomba.facing is Direction.EAST


def test_opposite_edge_east():
    sim = Simulator(Roomba(x=9, y=9, facing=Direction.EAST))
    sim.forward()
    assert (sim.roomba.x, sim.roomba.y) == (9, 9)
    assert sim.roomba.facing is Direction.SOUTH


def test_explicit_turn_right_does_not_move():
    sim = Simulator()
    sim.turn_right()
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)
    assert sim.roomba.facing is Direction.EAST


def test_can_enter_false_outside_bounds():
    sim = Simulator()
    assert sim.can_enter(0, 0)
    assert sim.can_enter(9, 9)
    assert not sim.can_enter(-1, 0)
    assert not sim.can_enter(0, -1)
    assert not sim.can_enter(10, 0)
    assert not sim.can_enter(0, 10)


def test_render_is_10x10_with_facing_glyph():
    sim = Simulator()
    lines = sim.render().splitlines()
    assert len(lines) == GRID_SIZE
    assert all(len(line.split()) == GRID_SIZE for line in lines)
    assert lines[-1].split()[0] == "^"
    assert lines[0].split()[0] == "."


def test_grid_in_bounds():
    grid = Grid()
    assert grid.in_bounds(0, 0)
    assert grid.in_bounds(9, 9)
    assert not grid.in_bounds(-1, 5)
    assert not grid.in_bounds(5, 10)
