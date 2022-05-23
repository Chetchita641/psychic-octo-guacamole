"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2019.01.15
"""
# ------------------------------------------------------------------ Imports

# src
from AmbseBase import AmbseBase


# ------------------------------------------------------------------ Class Definition
class TrueReqSignal(AmbseBase):
    def __init__(self,signal):
        self.signal = signal # from SysML diagram
        self.properties = self.signal.getOwnedAttribute()


    # -------------------------------------------------------------- Methods
    def display_properties(self):
        msg = "Current Signal: %s"%self.signal.getHumanName()+"\n"
        msg += "Signal Properties: \n"

        for prop in self.properties:
            msg += prop.getName()+"\n"
        self.log_message(msg)

