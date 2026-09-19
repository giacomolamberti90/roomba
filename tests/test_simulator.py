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


def test_starts_with_one_selected_roomba():
    sim = Simulator()
    listed = sim.list_roombas()
    assert [rid for rid, _ in listed] == [1]
    assert sim.selected_id == 1


def test_create_adds_without_changing_selection():
    sim = Simulator()
    sim.forward()
    new_id = sim.create()
    assert new_id == 2
    assert sim.selected_id == 1
    assert (sim.roomba.x, sim.roomba.y) == (0, 1)
    other = dict(sim.list_roombas())[2]
    assert (other.x, other.y) == (0, 0)


def test_create_skips_occupied_origin():
    sim = Simulator()
    new_id = sim.create()
    assert new_id == 2
    other = dict(sim.list_roombas())[2]
    assert (other.x, other.y) == (1, 0)


def test_create_fails_when_grid_full():
    sim = Simulator(grid=Grid(size=1))
    assert sim.create() is None
    assert [rid for rid, _ in sim.list_roombas()] == [1]


def test_select_then_forward_moves_only_that_id():
    sim = Simulator()
    sim.create()
    assert sim.select(2) == "ok"
    sim.forward()
    poses = {rid: (r.x, r.y) for rid, r in sim.list_roombas()}
    assert poses[1] == (0, 0)
    assert poses[2] == (1, 1)
    assert sim.selected_id == 2


def test_delete_non_selected_keeps_selection():
    sim = Simulator()
    sim.create()
    assert sim.delete(2) == "ok"
    assert sim.selected_id == 1
    assert [rid for rid, _ in sim.list_roombas()] == [1]


def test_delete_selected_picks_lowest_remaining():
    sim = Simulator()
    sim.create()
    sim.create()
    sim.select(2)
    assert sim.delete(2) == "ok"
    assert sim.selected_id == 1
    assert [rid for rid, _ in sim.list_roombas()] == [1, 3]


def test_delete_last_then_forward_is_no_selection():
    sim = Simulator()
    assert sim.delete(1) == "ok"
    assert sim.selected_id is None
    assert sim.forward() == "no_selection"
    assert sim.turn_right() == "no_selection"


def test_create_after_empty_auto_selects():
    sim = Simulator()
    sim.delete(1)
    new_id = sim.create()
    assert new_id == 2
    assert sim.selected_id == 2
    assert sim.forward() == "ok"
    assert (sim.roomba.x, sim.roomba.y) == (0, 1)


def test_select_and_delete_unknown_id():
    sim = Simulator()
    assert sim.select(99) == "not_found"
    assert sim.delete(99) == "not_found"
    assert sim.selected_id == 1


def test_forward_blocked_by_another_roomba():
    sim = Simulator()
    sim.create()
    sim.turn_right()
    assert sim.forward() == "blocked"
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)
    assert sim.roomba.facing is Direction.EAST
    other = dict(sim.list_roombas())[2]
    assert (other.x, other.y) == (1, 0)


def test_render_two_roombas_on_separate_cells():
    sim = Simulator()
    sim.create()
    sim.select(2)
    sim.turn_right()
    lines = sim.render().splitlines()
    assert lines[-1].split()[0] == "^"
    assert lines[-1].split()[1] == ">"


def test_grid_in_bounds():
    grid = Grid()
    assert grid.in_bounds(0, 0)
    assert grid.in_bounds(9, 9)
    assert not grid.in_bounds(-1, 5)
    assert not grid.in_bounds(5, 10)
