"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.01.09
"""
# ------------------------------------------------------------------ Imports
import sys
from com.nomagic.magicdraw.actions import MDAction
# MagicDraw
from com.nomagic.magicdraw.core import Application

# src
from AmbseBase import AmbseBase
from ProjectReviewer import ProjectReviewer


# ------------------------------------------------------------------ Class Definition
class SetProjectAction(MDAction, AmbseBase):
    """
    Defines the mapping of actions to function calls.
    """

    def __init__(self, key):
        AmbseBase.__init__(self)
        MDAction.__init__(self, "", self.ACTIONS[key], None, None)
        self.action = key

    # -------------------------------------------------------------- Interface Methods
    def actionPerformed(self, event):
        """
        Calls the function that performs the action.
        """
        try:
            project = Application.getInstance().getProject()
            if project == None:
                self.log_message("There is no project.")

            else:
                reviewer = ProjectReviewer(project)
                if self.action == "REVIEW_DIAGRAM":
                    reviewer.review_current_diagram()

                elif self.action == "RULE_1":
                    reviewer.invoke_rule1()

                elif self.action == "RULE_2":
                    reviewer.invoke_rule2()

                elif self.action == "RULE_3":
                    reviewer.invoke_rule3()

                elif self.action == "RULE_4":
                    reviewer.invoke_rule4()

                elif self.action == "RULE_5":
                    reviewer.invoke_rule5()

                else:
                    self.log_message("%s not implemented yet"%self.action)

        except Exception:
            (k, v) = sys.exc_info()[:2]
            self.log_message("Type : %s \n error reason : %s"%(k,v))
