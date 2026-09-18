from unittest.mock import patch

from roomba.cli import apply_command, main
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
    assert (sim.roomba.x, sim.roomba.y) == (0, 0)


def test_main_loop():
    inputs = iter(["nope", "f", "r", "q"])
    with patch("builtins.input", side_effect=lambda _prompt: next(inputs)):
        with patch("builtins.print") as printed:
            main()
    texts = [str(call.args[0]) if call.args else "" for call in printed.call_args_list]
    assert any("Unknown command" in text for text in texts)
    assert any("^" in text for text in texts)
