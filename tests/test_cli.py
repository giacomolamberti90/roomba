from unittest.mock import patch

from roomba.cli import apply_command, format_list, main
from roomba.direction import Direction
from roomba.simulator import Simulator


def test_forward_command():
    sim = Simulator()
    assert apply_command(sim, "f") == "ok"
    assert (sim.roomba.x, sim.roomba.y) == (0, 1)


def test_right_command():
    sim = Simulator()
    assert apply_command(sim, "r") == "ok"
    assert sim.roomba.facing is Direction.EAST
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)


def test_quit_and_unknown():
    sim = Simulator()
    assert apply_command(sim, "q") == "quit"
    assert apply_command(sim, "nope") == "unknown"
    assert apply_command(sim, "   ") == "unknown"
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)


def test_new_select_delete_list():
    sim = Simulator()
    assert apply_command(sim, "n") == "ok"
    assert apply_command(sim, "s 2") == "ok"
    assert sim.selected_id == 2
    assert apply_command(sim, "d 1") == "ok"
    assert [rid for rid, _ in sim.list_roombas()] == [2]
    assert apply_command(sim, "l") == "list"
    listed = format_list(sim)
    assert "* 2 (0, 0) NORTH" in listed
    assert " 1 " not in listed
    sim.delete(2)
    assert format_list(sim) == "(no roombas)"


def test_select_unknown_id():
    sim = Simulator()
    assert apply_command(sim, "s 99") == "not_found"
    assert apply_command(sim, "d 99") == "not_found"
    assert apply_command(sim, "s") == "unknown"
    assert apply_command(sim, "d xyz") == "unknown"


def test_forward_empty_fleet():
    sim = Simulator()
    assert apply_command(sim, "d 1") == "ok"
    assert apply_command(sim, "f") == "no_selection"
    assert apply_command(sim, "n") == "ok"
    assert apply_command(sim, "f") == "ok"
    assert (sim.roomba.x, sim.roomba.y) == (0, 1)


def test_main_loop():
    inputs = iter(["nope", "f", "r", "q"])
    with patch("builtins.input", side_effect=lambda _prompt: next(inputs)):
        with patch("builtins.print") as printed:
            main()
    texts = [str(call.args[0]) if call.args else "" for call in printed.call_args_list]
    assert any("Unknown command" in text for text in texts)
    assert any("^" in text for text in texts)


def test_main_loop_fleet_and_errors():
    inputs = iter(["n", "l", "s 99", "d 1", "d 2", "f", "q"])
    with patch("builtins.input", side_effect=lambda _prompt: next(inputs)):
        with patch("builtins.print") as printed:
            main()
    texts = [str(call.args[0]) if call.args else "" for call in printed.call_args_list]
    assert any("No Roomba with that id" in text for text in texts)
    assert any("No Roomba selected" in text for text in texts)
    assert any("* 1 (0, 0) NORTH" in text for text in texts)
