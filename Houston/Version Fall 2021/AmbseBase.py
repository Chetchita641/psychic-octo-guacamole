"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.01.15
"""
# ------------------------------------------------------------------ Imports

# MagicDraw
from com.nomagic.magicdraw.sysml.util import SysMLConstants

# Java
from javax.swing import JOptionPane

# ------------------------------------------------------------------ Class Definition
class AmbseBase:
    """
    Provides common functionality across the plugin (e.g. logging).
    """
    def __init__(self):
        self.SYSML_SEQUENCE_DIAGRAM = SysMLConstants.SYSML_SEQUENCE_DIAGRAM
        self.SYSML_BLOCK_DEFINITION_DIAGRAM = SysMLConstants.SYSML_BLOCK_DEFINITION_DIAGRAM
        self.SYSML_INTERNAL_BLOCK_DIAGRAM = SysMLConstants.SYSML_INTERNAL_BLOCK_DIAGRAM
        self.SYSML_STATE_MACHINE_DIAGRAM = SysMLConstants.SYSML_STATE_MACHINE_DIAGRAM

        self.ACTIONS = {
            "REVIEW_DIAGRAM" : "Review Current Diagram",
            "RULE_5": "Invoke Rule 5",
            "RULE_4": "Invoke Rule 4",
            "RULE_3": "Invoke Rule 3",
            "RULE_2": "Invoke Rule 2",
            "RULE_1": "Invoke Rule 1"
        }
    
    # -------------------------------------------------------------- Methods
    def log_message(self,msg):
        """
        Prints message to console and to a window.
        """
        print(msg)
        JOptionPane.showMessageDialog(None, msg)

    def get_user_input(self,msg):
        return JOptionPane.showInputDialog(None, msg)