from .base import TaskBase
from ..stream_filter import StreamFilter

from ..enums import EAnnType, EGameEvent, ERegionType
from ..config import cfg, override, LogDebug, LogInfo
from ..regions import REGIONS
from ..feature import ActionCardHandler, CropBox, CardName
from ..database import SaveImage
from ..stream_filter import StreamFilter

import numpy as np
import logging
import os

class CardPlayedTask(TaskBase):
    def __init__(self, frame_manager, is_op):
        super().__init__(frame_manager)
        self.event_type   = EGameEvent.OP_PLAYED if is_op else EGameEvent.MY_PLAYED
        self.card_handler = ActionCardHandler()
        self.Reset()
    
    @override
    def Reset(self):
        self.filter = StreamFilter(null_val=-1)

    @override
    def OnResize(self, client_width, client_height, ratio_type):
        region_type = ERegionType.OP_PLAYED if self.event_type == EGameEvent.OP_PLAYED else ERegionType.MY_PLAYED
        box = REGIONS[ratio_type][region_type]
        left   = round(client_width  * box[0])
        top    = round(client_height * box[1])
        width  = round(client_width  * box[2])
        height = round(client_height * box[3])
        self.card_handler.OnResize(CropBox(left, top, left + width, top + height))

    @override
    def Tick(self):
        card_id, dist, dists = self.card_handler.Update(self.frame_buffer, self.db)
        if cfg.DEBUG and False:
            # if (self.event_type == EGameEvent.MY_PLAYED) and True: #(card_id != -1):
                # SaveImage(self.card_handler.region_buffer, os.path.join(cfg.debug_dir, "save", f"{self.event_type.name}{self.fm.frame_count}.png"))
            if (True) and (card_id != -1):
                LogDebug(info=f'{dists=}, {self.event_type.name}: {CardName(card_id, self.db)}')
        card_id = self.filter.Filter(card_id, dist=dist)

        self.card_id_signal = card_id

        if card_id >= 0:
            LogInfo(
                type=self.event_type.name,
                card_id=card_id,
                name=CardName(card_id, self.db),
                )

        if cfg.DEBUG_SAVE:
            image = self.card_handler.region_buffer
            SaveImage(image, os.path.join(cfg.debug_dir, "save", f"{self.event_type.name}{self.fm.frame_count}.png"))