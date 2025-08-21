import tcod

KEY_MAPPING = {
    "UP": tcod.event.KeySym.UP,
    "DOWN": tcod.event.KeySym.DOWN,
    "LEFT": tcod.event.KeySym.LEFT,
    "RIGHT": tcod.event.KeySym.RIGHT,
    "WAIT": tcod.event.KeySym.w,
    "HISTORY": tcod.event.KeySym.h,
    "PICKUP": tcod.event.KeySym.g,
    "USE": tcod.event.KeySym.g,
    "DROP": tcod.event.KeySym.g,
    "LOOK": tcod.event.KeySym.g,
    "STAIRS": tcod.event.KeySym.g,
    "LEAVE": tcod.event.KeySym.g,
}

MODIFIER_KEYS = {  # Ignore modifier keys.
    tcod.event.KeySym.LSHIFT,
    tcod.event.KeySym.RSHIFT,
    tcod.event.KeySym.LCTRL,
    tcod.event.KeySym.RCTRL,
    tcod.event.KeySym.LALT,
    tcod.event.KeySym.RALT,
}

MOVE_DIRECTIONS = {
    # Arrow keys.
    KEY_MAPPING["UP"]: (0, -1),
    KEY_MAPPING["DOWN"]: (0, 1),
    KEY_MAPPING["LEFT"]: (-1, 0),
    KEY_MAPPING["RIGHT"]: (1, 0),
}
