from .enums import ERegionType, ERatioType, EGameEvent
from .config import LogInfo

def GetRatioType(client_width, client_height):
    ratio = client_width / client_height
    EPSILON = 0.005
    if   abs( ratio - 16 / 9 ) < EPSILON:
        ratio_type = ERatioType.E16_9
    elif abs( ratio - 16 / 10) < EPSILON:
        ratio_type = ERatioType.E16_10
    elif abs( ratio - 64 / 27) < EPSILON:
        ratio_type = ERatioType.E64_27
    elif abs( ratio - 43 / 18) < EPSILON:
        ratio_type = ERatioType.E43_18
    elif abs( ratio - 12 / 5 ) < EPSILON:
        ratio_type = ERatioType.E12_5
    else:
        LogInfo(
            type=EGameEvent.UNSUPPORTED_RATIO.name, 
            client_width=client_width, 
            client_height=client_height,
            )
        ratio_type = ERatioType.E16_9 # default

    return ratio_type

# left, top, width, height
REGIONS = {
    # 1920 x 1080, 2560 x 1440
    ERatioType.E16_9: {
        ERegionType.GAME_START : ( 0.4470, 0.4400, 0.1045, 0.1110 ), # left, top, width, height
        ERegionType.MY_PLAYED  : ( 0.1225, 0.1755, 0.1400, 0.4270 ),
        ERegionType.OP_PLAYED  : ( 0.7380, 0.1755, 0.1400, 0.4270 ),
        ERegionType.GAME_OVER  : ( 0.4220, 0.4240, 0.1555, 0.1190 ),
        ERegionType.PHASE      : ( 0.4000, 0.4800, 0.2000, 0.0400 ),
        ERegionType.ROUND      : ( 0.4400, 0.5420, 0.1200, 0.0310 ),
        ERegionType.CENTER     : ( 0.0700, 0.3380, 0.8600, 0.0500 ),
        ERegionType.FLOW_ANCHOR: ( 0.0078, 0.3350, 0.1070, 0.3280 ), # (margin to digit center, margin to card top, card width, card height)
        ERegionType.MY_DECK    : ( 0.0000, 0.5550, 0.3250, 0.2750 ),
        ERegionType.VS_ANCHOR  : ( 0.1355, 0.3595, 0.0870, 0.2585, 0.0090 ), # left, top, width, height, margin
    },
    # 1920 x 1200, 1680 x 1050
    ERatioType.E16_10: {
        ERegionType.GAME_START : ( 0.4470, 0.4470, 0.1045, 0.0995 ),
        ERegionType.MY_PLAYED  : ( 0.1490, 0.2285, 0.1305, 0.3565 ),
        ERegionType.OP_PLAYED  : ( 0.7215, 0.2285, 0.1305, 0.3565 ),
        ERegionType.GAME_OVER  : ( 0.4220, 0.4240, 0.1555, 0.1190 ),
        ERegionType.PHASE      : ( 0.4000, 0.4800, 0.2000, 0.0400 ),
        ERegionType.ROUND      : ( 0.4400, 0.5370, 0.1200, 0.0280 ),
        ERegionType.CENTER     : ( 0.0700, 0.3540, 0.8600, 0.0500 ),
        ERegionType.FLOW_ANCHOR: ( 0.0078, 0.3550, 0.1035, 0.2850 ),
        ERegionType.MY_DECK    : ( 0.0000, 0.5500, 0.3250, 0.2500 ),
        ERegionType.VS_ANCHOR  : ( 0.1350, 0.3725, 0.0870, 0.2335, 0.0094 ),
    },
    # 2560 × 1080, 2048 x 864
    ERatioType.E64_27: {
        ERegionType.GAME_START : ( 0.4605, 0.4400, 0.0780, 0.1100 ),
        ERegionType.MY_PLAYED  : ( 0.2170, 0.1755, 0.1050, 0.4270 ),
        ERegionType.OP_PLAYED  : ( 0.6785, 0.1755, 0.1050, 0.4270 ),
        ERegionType.GAME_OVER  : ( 0.4420, 0.4250, 0.1165, 0.1190 ),
        ERegionType.PHASE      : ( 0.4000, 0.4790, 0.2000, 0.0400 ),
        ERegionType.ROUND      : ( 0.4400, 0.5410, 0.1200, 0.0320 ),
        ERegionType.CENTER     : ( 0.1000, 0.3300, 0.8000, 0.0600 ),
        ERegionType.FLOW_ANCHOR: ( 0.0050, 0.3350, 0.0800, 0.3280 ),
        ERegionType.MY_DECK    : ( 0.1260, 0.5550, 0.2440, 0.2750 ),
        ERegionType.VS_ANCHOR  : ( 0.2265, 0.3590, 0.0650, 0.2590, 0.0075 ),
    },
    # 3440 × 1440, 2150 x 900
    ERatioType.E43_18: {
        ERegionType.GAME_START : ( 0.4605, 0.4400, 0.0780, 0.1100 ),
        ERegionType.MY_PLAYED  : ( 0.2195, 0.1755, 0.1045, 0.4275 ),
        ERegionType.OP_PLAYED  : ( 0.6776, 0.1755, 0.1045, 0.4275 ),
        ERegionType.GAME_OVER  : ( 0.4420, 0.4240, 0.1165, 0.1190 ),
        ERegionType.PHASE      : ( 0.4000, 0.4790, 0.2000, 0.0400 ),
        ERegionType.ROUND      : ( 0.4400, 0.5422, 0.1200, 0.0325 ),
        ERegionType.CENTER     : ( 0.1000, 0.3300, 0.8000, 0.0600 ),
        ERegionType.FLOW_ANCHOR: ( 0.0050, 0.3350, 0.0780, 0.3280 ),
        ERegionType.MY_DECK    : ( 0.1260, 0.5550, 0.2440, 0.2750 ),
        ERegionType.VS_ANCHOR  : ( 0.2285, 0.3590, 0.0645, 0.2590, 0.0070 ),
    },
    # 3840 x 1600, 1920 x 800
    ERatioType.E12_5: {
        ERegionType.GAME_START : ( 0.4605, 0.4400, 0.0780, 0.1100 ),
        ERegionType.MY_PLAYED  : ( 0.2205, 0.1755, 0.1045, 0.4270 ),
        ERegionType.OP_PLAYED  : ( 0.6765, 0.1755, 0.1045, 0.4270 ),
        ERegionType.GAME_OVER  : ( 0.4420, 0.4240, 0.1165, 0.1190 ),
        ERegionType.PHASE      : ( 0.4000, 0.4790, 0.2000, 0.0400 ),
        ERegionType.ROUND      : ( 0.4400, 0.5400, 0.1200, 0.0345 ),
        ERegionType.CENTER     : ( 0.1000, 0.3300, 0.8000, 0.0600 ),
        ERegionType.FLOW_ANCHOR: ( 0.0055, 0.3350, 0.0790, 0.3280 ),
        ERegionType.MY_DECK    : ( 0.1260, 0.5550, 0.2440, 0.2750 ),
        ERegionType.VS_ANCHOR  : ( 0.2295, 0.3590, 0.0645, 0.2590, 0.0070 ),
    },
}