"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.01.10
"""
# ------------------------------------------------------------------ Imports

# MagicDraw
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import Property, Class as Interface
from com.nomagic.uml2.ext.magicdraw.commonbehaviors.mdcommunications import Signal
from com.nomagic.uml2.ext.magicdraw.compositestructures.mdports import Port

# src
from TrueReqDiagram import TrueReqDiagram
from TrueReqSignal import TrueReqSignal


# ------------------------------------------------------------------ Class Definition
class TrueReqBlockDefDiagram(TrueReqDiagram):

    def __init__(self,diagram):
        TrueReqDiagram.__init__(self,diagram)

        # For a block def diagram, properties are separated from blocks
        self.properties, self.signals, self.interfaces, self.ports, self.other_elems = self.extract_elements()


    # -------------------------------------------------------------- Methods
    def extract_elements(self):
        """
        Separates elements in a block def diagram into the following 
        groups:

        - properties
        - signals
        - interfaces
        - ports
        - other
        """
        properties, signals, interfaces, ports, others = ([] for i in range(5))
        
        # Sort elements into proper class category
        for elem in self.elements:
            if elem.getClassType() == Property:
                properties.append(elem)
            elif elem.getClassType() == Signal:
                signals.append(TrueReqSignal(elem))
            elif elem.getClassType() == Interface:
                interfaces.append(elem)
            elif elem.getClassType() == Port:
                ports.append(elem)
            else:
                others.append(elem)
        
        return properties, signals, interfaces, ports, others