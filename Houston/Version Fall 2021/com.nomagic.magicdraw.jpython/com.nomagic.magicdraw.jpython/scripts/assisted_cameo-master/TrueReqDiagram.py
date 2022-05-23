"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.01.10
"""
# ------------------------------------------------------------------ Imports

# src
from AmbseBase import AmbseBase

# ------------------------------------------------------------------ Class Definition
class TrueReqDiagram(AmbseBase):
    """
    Provides commmon functionality to the following true req diagrams:
    - ModeReqDiagram(StateMachineDiagram)
    - InternalBlockDiagram
    - SequenceDiagram
    """
    def __init__(self,diagram):
        AmbseBase.__init__(self)
        self.diagram = diagram
        self.elements = self.diagram.getUsedModelElements()

    # -------------------------------------------------------------- Methods
    def log_diagram_elements(self):
        """
        Logs the elements of the diagram including names and types.
        """
        msg = "Current diagram: %s"%self.diagram.getDiagramType().getType()+"\n"
        msg += "Diagram Elements: \n"

        for elem in self.elements:
            msg += self.elem2str(elem)
        self.log_message(msg)


    # -------------------------------------------------------------- Helper Methods
    def elem2str(self,elem):
        """
        Returns the element type and name for logging.
        """
        try:
            return "%s : %s \n"%(elem.getClassType(),elem.getName())
            
        except Exception:
            # (k, v) = sys.exc_info()[:2]
            # self.log_message("Type : %s \n error reason : %s"%(k,v))
            return "Type %s has no name \n"%(elem.getClassType())