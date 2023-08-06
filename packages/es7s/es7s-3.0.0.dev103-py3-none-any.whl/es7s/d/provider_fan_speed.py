# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from ._base import DataProvider


class FanSpeedProvider(DataProvider[dict]):
    def __init__(self):
        super().__init__("fan", "fan")

    def _collect(self) -> dict:
        vals = psutil.sensors_fans().values()
        max_speed = None
        for l in vals:
            for sf in l:
                if sf.current > 64000: # filter parasite values ≈65500, 8-bit "-1" maybe
                    continue
                max_speed = max(max_speed or 0, sf.current)
        return dict(max=max_speed)
