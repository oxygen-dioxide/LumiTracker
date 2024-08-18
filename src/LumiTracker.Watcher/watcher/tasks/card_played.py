from .base import TaskBase
from ..stream_filter import StreamFilter

from ..enums import EAnnType, ETaskType, ERegionType
from ..config import cfg, LogDebug, LogInfo
from ..regions import REGIONS
from ..database import ActionCardHandler, CropBox, CardName
from ..database import SaveImage
from ..stream_filter import StreamFilter

import numpy as np
import logging
import os

class CardPlayedTask(TaskBase):
    def __init__(self, db, is_op):
        super().__init__(db)
        self.task_type      = ETaskType.OP_PLAYED if is_op else ETaskType.MY_PLAYED
        self.card_handler   = ActionCardHandler()
        self.Reset()
    
    def Reset(self):
        self.filter         = StreamFilter(null_val=-1)

    def OnResize(self, client_width, client_height, ratio_type):
        region_type = ERegionType.OP_PLAYED if self.task_type == ETaskType.OP_PLAYED else ERegionType.MY_PLAYED
        box = REGIONS[ratio_type][region_type]
        left   = round(client_width  * box[0])
        top    = round(client_height * box[1])
        width  = round(client_width  * box[2])
        height = round(client_height * box[3])
        self.card_handler.OnResize(CropBox(left, top, left + width, top + height))

    def _PreTick(self, frame_manager):
        self.valid = frame_manager.game_started

    def _Tick(self, frame_manager):
        card_id, dist, dists = self.card_handler.Update(self.frame_buffer, self.db)
        if cfg.DEBUG:
            # if (self.task_type.value == 1) and True: #(card_id != -1):
            if (True) and (card_id != -1):
                LogDebug(info=f'{dists=}, {self.task_type.name}: {CardName(card_id, self.db)}')
        card_id = self.filter.Filter(card_id, dist=dist)

        if card_id >= 0:
            LogInfo(
                type=self.task_type.name,
                card_id=card_id,
                name=CardName(card_id, self.db),
                )
        
        if cfg.DEBUG_SAVE:
            import cv2
            image = cv2.cvtColor(self.feature_buffer, cv2.COLOR_BGRA2BGR)
            SaveImage(image, os.path.join(cfg.debug_dir, "save", f"{self.task_type.name}{frame_manager.frame_count}.png"))