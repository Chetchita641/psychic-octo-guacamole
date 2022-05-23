"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.02.08
"""
# ------------------------------------------------------------------ Imports

# MagicDraw
from com.nomagic.uml2.ext.magicdraw.interactions.mdbasicinteractions import Lifeline, Message
from com.nomagic.uml2.ext.magicdraw.commonbehaviors.mdsimpletime import DurationConstraint

# src
from TrueReqDiagram import TrueReqDiagram
from TrueReqSignal import TrueReqSignal

# ------------------------------------------------------------------ Class Definition
class TrueReqSequenceDiagram(TrueReqDiagram):

    def __init__(self,diagram):
        TrueReqDiagram.__init__(self,diagram)
        self.lifelines, self.messages, self.durations, self.others = self.extract_elements()
        # self.log_message("lifelines: %d, messages: %d, others: %d"%(len(self.lifelines),len(self.messages),len(self.others)))
        self.signals = self.extract_signals(self.messages)
        

    # -------------------------------------------------------------- Methods
    def extract_signals(self,messages):
        """
        Extracts signals from a list of messages
        """
        signals = []
        for m in messages:
            signals.append(TrueReqSignal(m.getSignature()))
        return signals


    def extract_elements(self):
        """
        Separates elements in a sequence diagram into the following 
        groups:
        - lifelines
        - messages
        - durations
        - others
        """
        lifelines, messages, durations, others = ([] for i in range(4))

        for elem in self.elements:
            if elem.getClassType() == Lifeline:
                lifelines.append(elem)
            elif elem.getClassType() == Message:
                messages.append(elem)
            elif elem.getClassType() == DurationConstraint:
                durations.append(elem)
            else:
                others.append(elem)
        
        return lifelines, messages, durations, others