class mxRibbon:
    UNKNOWN = "UNKNOWN"

    BASE_CAPTURE = "RIBBON_BASE_CAPTURE"
    BASE_CAPTURE_ASSIST = "RIBBON_BASE_CAPTURE_ASSIST"
    BASE_DEFENSE = "RIBBON_BASE_DEFENSE"
    BOMB = "RIBBON_BOMB"
    BUILDING_KILL = "RIBBON_BUILDING_KILL"
    BURN = "RIBBON_BURN"
    CITADEL = "RIBBON_CITADEL"
    CRIT = "RIBBON_CRIT"
    FLOOD = "RIBBON_FLOOD"
    FRAG = "RIBBON_FRAG"
    # MAIN_CALIBER = "RIBBON_MAIN_CALIBER"
    MAIN_CALIBER_NO_PENETRATION = "RIBBON_SUBRIBBON_MAIN_CALIBER_NO_PENETRATION"
    MAIN_CALIBER_OVER_PENETRATION = "RIBBON_SUBRIBBON_MAIN_CALIBER_OVER_PENETRATION"
    MAIN_CALIBER_PENETRATION = "RIBBON_SUBRIBBON_MAIN_CALIBER_PENETRATION"
    MAIN_CALIBER_RICOCHET = "RIBBON_SUBRIBBON_MAIN_CALIBER_RICOCHET"
    PLANE = "RIBBON_PLANE"
    SECONDARY_CALIBER = "RIBBON_SECONDARY_CALIBER"
    SUPPRESSED = "RIBBON_SUPPRESSED"
    TORPEDO = "RIBBON_TORPEDO"

    _type_map = {
        1: TORPEDO,
        2: BOMB,
        3: PLANE,
        4: CRIT,
        5: FRAG,
        6: BURN,
        7: FLOOD,
        8: CITADEL,
        10: BASE_CAPTURE,
        11: BASE_CAPTURE_ASSIST,
        -1: BASE_DEFENSE,
        -1: BUILDING_KILL,
        -1: MAIN_CALIBER_NO_PENETRATION,
        -1: MAIN_CALIBER_OVER_PENETRATION,
        -1: MAIN_CALIBER_PENETRATION,
        -1: MAIN_CALIBER_RICOCHET,
        -1: SECONDARY_CALIBER,
        -1: SUPPRESSED,
    }

    def __init__(self, ribbon_id):
        if ribbon_id in mxRibbon._type_map:
            self._type = mxRibbon._type_map[ribbon_id]
        else:
            self._type = mxRibbon.UNKNOWN

    _puk_map = {
        FRAG: 0.15,
        PLANE: 1.0/40,
    }

    def getPuk(self):
        if self._type in mxRibbon._puk_map:
            return mxRibbon._puk_map[self._type]
        else:
            return 0.0
