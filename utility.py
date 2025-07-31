def slices_to_xys(sx: slice, sy: slice):
    rx = range(sx.start or 0, sx.stop, sx.step or 1)
    ry = range(sy.start or 0, sy.stop, sy.step or 1)
    return [(x, y) for x in rx for y in ry]
