from .simulator import Simulator


def format_list(sim: Simulator) -> str:
    lines = []
    for rid, roomba in sim.list_roombas():
        mark = "*" if rid == sim.selected_id else " "
        lines.append(f"{mark} {rid} ({roomba.x}, {roomba.y}) {roomba.facing.name}")
    return "\n".join(lines) if lines else "(no roombas)"


def _parse_id(parts):
    if len(parts) < 2:
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


def apply_command(sim: Simulator, cmd: str) -> str:
    """Apply one CLI command.

    Returns ok, list, quit, unknown, no_selection, or not_found.
    """
    parts = cmd.strip().split()
    if not parts:
        return "unknown"
    op = parts[0].lower()
    if op in ("q", "quit"):
        return "quit"
    if op in ("f", "forward"):
        return sim.forward()
    if op in ("r", "right"):
        return sim.turn_right()
    if op in ("n", "new"):
        sim.create()
        return "ok"
    if op in ("l", "list"):
        return "list"
    if op in ("s", "select"):
        rid = _parse_id(parts)
        if rid is None:
            return "unknown"
        return sim.select(rid)
    if op in ("d", "delete"):
        rid = _parse_id(parts)
        if rid is None:
            return "unknown"
        return sim.delete(rid)
    return "unknown"


def main() -> None:
    sim = Simulator()
    print(sim.render())
    while True:
        result = apply_command(
            sim, input("f=forward r=right n=new l=list s=select d=delete q=quit> ")
        )
        if result == "quit":
            break
        if result == "unknown":
            print("Unknown command. Use f, r, n, l, s <id>, d <id>, or q.")
            continue
        if result == "no_selection":
            print("No Roomba selected. Create one with n.")
            continue
        if result == "not_found":
            print("No Roomba with that id.")
            continue
        if result == "list":
            print(format_list(sim))
            continue
        print(sim.render())


if __name__ == "__main__":
    main()
