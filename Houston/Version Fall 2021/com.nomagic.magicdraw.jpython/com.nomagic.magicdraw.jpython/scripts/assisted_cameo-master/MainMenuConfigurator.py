"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.01.09
"""
# ------------------------------------------------------------------ Imports

# MagicDraw
from com.nomagic.actions import AMConfigurator
from com.nomagic.magicdraw.actions import MDActionsCategory

# src
from AmbseBase import AmbseBase
from SetProjectAction import SetProjectAction

# ------------------------------------------------------------------ Class Definition
class MainMenuConfigurator(AMConfigurator,AmbseBase):
    """
    In charge of modifying Cameo's main menu to include actions
    for the plugin.
    """
    def __init__(self):
        AmbseBase.__init__(self)


    # -------------------------------------------------------------- Interface Methods
    def configure(self,manager):
        try:
            for key in self.ACTIONS:
                category = MDActionsCategory("", "")
                category.addAction(SetProjectAction(key))
                manager.getCategories().get(0).addAction(category)
        except:
            self.log_message("Could not add action: %s"%key)
    

    def getPriority(self):
        return AMConfigurator.LOW_PRIORITY