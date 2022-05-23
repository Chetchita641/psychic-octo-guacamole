"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2019.10.30
"""

# ------------------------------------------------------------------ Imports
import os

# MagicDraw
from com.nomagic.magicdraw.actions import ActionsConfiguratorsManager

# Java
from javax.swing import JOptionPane

# src
from MainMenuConfigurator import MainMenuConfigurator

# ------------------------------------------------------------------ Execution

# Signal to user the plugin is active
print("Starting script, descriptor", pluginDescriptor)
JOptionPane.showMessageDialog(None, "A-MBSE Plugin Active")


# Add customized menu for plugin
ActionsConfiguratorsManager.getInstance().addMainMenuConfigurator( MainMenuConfigurator() )