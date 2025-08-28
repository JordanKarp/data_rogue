import tcod

KEY_MAPPING = {
    "UP": tcod.event.KeySym.UP,
    "DOWN": tcod.event.KeySym.DOWN,
    "LEFT": tcod.event.KeySym.LEFT,
    "RIGHT": tcod.event.KeySym.RIGHT,
    # "UP": tcod.event.KeySym.w,
    # "DOWN": tcod.event.KeySym.s,
    # "LEFT": tcod.event.KeySym.a,
    # "RIGHT": tcod.event.KeySym.d,
    "WAIT": tcod.event.KeySym.w,
    "HISTORY": tcod.event.KeySym.h,
    "PICKUP": tcod.event.KeySym.g,
    "USE": tcod.event.KeySym.i,
    "DROP": tcod.event.KeySym.d,
    "DISPLAY": tcod.event.KeySym.z,
    "LOOK": tcod.event.KeySym.SLASH,
    "STAIRS": tcod.event.KeySym.p,
    "LEAVE": tcod.event.KeySym.o,
    "NOTES": tcod.event.KeySym.c,
    "CYCLE_HUD": tcod.event.KeySym.q,
    "SCAN_UP": tcod.event.KeySym.PAGEUP,
    "SCAN_DOWN": tcod.event.KeySym.PAGEDOWN,
    "HOME": tcod.event.KeySym.HOME,
    "END": tcod.event.KeySym.END,
}

MENU_MAPPING = {
    "NEW": tcod.event.KeySym.n,
    "CONTINUE": tcod.event.KeySym.c,
    "OPTIONS": tcod.event.KeySym.o,
    "QUIT": tcod.event.KeySym.q,
}

MODIFIER_KEYS = {
    tcod.event.KeySym.LSHIFT,
    tcod.event.KeySym.RSHIFT,
    tcod.event.KeySym.LCTRL,
    tcod.event.KeySym.RCTRL,
    tcod.event.KeySym.LALT,
    tcod.event.KeySym.RALT,
}

CONFIRM_KEYS = {
    tcod.event.KeySym.RETURN,
    tcod.event.KeySym.KP_ENTER,
}

MOVE_DIRECTIONS = {
    # Arrow keys.
    KEY_MAPPING["UP"]: (0, -1),
    KEY_MAPPING["DOWN"]: (0, 1),
    KEY_MAPPING["LEFT"]: (-1, 0),
    KEY_MAPPING["RIGHT"]: (1, 0),
}
UP_DOWN_DIRECTIONS = {
    # Arrow keys.
    KEY_MAPPING["UP"]: (0, -1),
    KEY_MAPPING["DOWN"]: (0, 1),
}

CURSOR_Y_KEYS = {
    KEY_MAPPING["UP"]: -1,
    KEY_MAPPING["DOWN"]: 1,
    KEY_MAPPING["SCAN_UP"]: -10,
    KEY_MAPPING["SCAN_DOWN"]: 10,
}
