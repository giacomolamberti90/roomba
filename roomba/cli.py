from .simulator import Simulator


def apply_command(sim: Simulator, cmd: str) -> str:
    """Apply one CLI command. Returns 'ok', 'quit', or 'unknown'."""
    cmd = cmd.strip().lower()
    if cmd in ("q", "quit"):
        return "quit"
    if cmd in ("f", "forward"):
        sim.forward()
        return "ok"
    if cmd in ("r", "right"):
        sim.turn_right()
        return "ok"
    return "unknown"


def main() -> None:
    sim = Simulator()
    print(sim.render())
    while True:
        result = apply_command(sim, input("f=forward r=right q=quit> "))
        if result == "quit":
            break
        if result == "unknown":
            print("Unknown command. Use f, r, or q.")
            continue
        print(sim.render())


if __name__ == "__main__":
    main()
