"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.02.09
"""
# ------------------------------------------------------------------ Imports

from com.nomagic.magicdraw.core import Application
# MagicDraw
from com.nomagic.magicdraw.openapi.uml import SessionManager
from com.nomagic.magicdraw.sysml.util import SysMLConstants
from com.nomagic.magicdraw.sysml.util import SysMLProfile
from com.nomagic.magicdraw.ui.notification import NotificationManager, Notification
from com.nomagic.uml2.ext.jmi.helpers import ModelHelper
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import VisibilityKindEnum

# src
from AmbseBase import AmbseBase
from TrueReqBlockDefDiagram import TrueReqBlockDefDiagram
from TrueReqDiagram import TrueReqDiagram
from TrueReqSequenceDiagram import TrueReqSequenceDiagram


# ------------------------------------------------------------------ Class Definition
# Create GUI Log Instance for GUI Notifications
def createGUILogInstance():
    GUILogInstance = Application.getInstance().getGUILog()
    GUILogInstance.openLog

    return GUILogInstance


class ProjectReviewer(AmbseBase):
    def __init__(self, project):
        """
        Responsible to managing and reviewing a CSM project according
        to 'true' model-based requirements.

        NOTE: The ProjectReviewer is instantiated when the project
        action is called (specified in SetProjectAction). Furthermore,
        review_current_diagram() is the main method that's also called.
        """
        AmbseBase.__init__(self)
        self.project = project
        self.sysml_profile = SysMLProfile.getInstance(self.project)
        self.current_diagram = project.getActiveDiagram()
        self.diagram_type = self.current_diagram.getDiagramType()
        self.elem_factory = self.project.getElementsFactory()
        self.true_req_diag = None  # TrueReq instantiation of the current diagram

    # -------------------------------------------------------------- Methods
    def review_current_diagram(self):
        """
        Simply shows the current diagram type in a window.
        """
        self.true_req_diag = TrueReqDiagram(self.current_diagram)
        self.true_req_diag.log_diagram_elements()

    def invoke_rule3(self):
        if self.diagram_type.isEqualType(self.SYSML_BLOCK_DEFINITION_DIAGRAM):
            GUILogInstance = createGUILogInstance()
            self.true_req_diag = TrueReqBlockDefDiagram(self.current_diagram)
            self.rule3(self.true_req_diag.signals, GUILogInstance)

        elif self.diagram_type.isEqualType(self.SYSML_SEQUENCE_DIAGRAM):
            GUILogInstance = createGUILogInstance()
            self.true_req_diag = TrueReqSequenceDiagram(self.current_diagram)
            self.rule3(self.true_req_diag.signals, GUILogInstance)

        else:
            self.log_message(
                "Rule 3 is not applicable to a %s diagram (yet)" % self.current_diagram.getDiagramType().getType())

    # -------------------------------------------------------------- Rule 3 Methods
    def rule3(self, signals, GUILogInstance):
        """
        Rule 3 algorithm to be done on signals
        """
        keep_going = True
        for true_req_signal in signals:
            if keep_going:

                # construct first input window
                msg = "Do you care about ranges outside " + true_req_signal.signal.getHumanName() + "? \n"
                msg += "Options: [Y/N]"
                user_input = self.get_user_input(msg)
                # NOTE: input is None if nothing is entered!

                if user_input == "N":
                    self.log_message("Condition set to 'undefined'")  # TODO: control which ones are evaluated already
                    GUILogInstance.log("Condition set to 'undefined'", True)

                elif user_input == "Y":

                    # Define range and duration
                    user_range = self.ui_define_range(true_req_signal)
                    user_duration = self.ui_define_duration(true_req_signal)

                    # Choose an action
                    msg = "Choose an action for the range of " + true_req_signal.signal.getHumanName() + "\n"
                    msg += "Options: [undefined/do same/no degredation/partial degredation]"
                    user_input = self.get_user_input(msg)

                    # Perform action
                    if user_input == "undefined":
                        self.rule3_undefined(GUILogInstance)

                    elif user_input == "do same":
                        self.rule3_do_same(true_req_signal, user_range, GUILogInstance)

                    elif user_input == "no degredation":
                        self.rule3_no_degredation(true_req_signal, user_range, user_duration, GUILogInstance)

                    elif user_input == "partial degredation":
                        self.rule_partial_degredation(true_req_signal, GUILogInstance)

                    else:  # default case is 'undefined'
                        self.log_message("Invalid input, using undefined case by default")
                        GUILogInstance.log("Invalid input, using undefined case by default", True)
                        self.rule3_undefined(GUILogInstance)

                else:
                    self.log_message("Input is invalid: %s" % user_input)
                    GUILogInstance.log("Input is invalid: %s" % user_input, True)

            else:
                break
            keep_going = False  # TODO remove after testing

    def rule3_undefined(self, GUILogInstance):
        """
        No changes to the model.
        """
        self.log_message("Undefined case called for Rule 3")
        GUILogInstance.log("Undefined case called for Rule 3", True)

    def rule3_do_same(self, tr_signal, user_range, GUILogInstance):
        """
        Defines the user range as a new property of the signal.
        """
        self.define_range_as_property(user_range, tr_signal, GUILogInstance)
        GUILogInstance.log("Condition set to 'do same'", True)

    def rule3_no_degredation(self, tr_signal, user_range, user_duration, GUILogInstance):

        # add the new range as a property of the signal
        self.define_range_as_property(user_range, tr_signal, GUILogInstance)

        # add a mode state for the degraded signal
        name = "Degraded %s: %s" % (tr_signal.signal.getName(), user_range)
        self.add_mode(name, GUILogInstance)

        # add duration
        self.add_duration_constraint(tr_signal, user_duration, GUILogInstance)
        GUILogInstance.log("Condition set to 'no degredation'", True)

    def rule_partial_degredation(self, tr_signal, GUILogInstance):
        name = "Degraded Signal: %s" % tr_signal.signal.getName()
        self.add_mode(name, GUILogInstance)

        name = "Post Degredation: %s" % tr_signal.signal.getName()
        self.add_mode(name, GUILogInstance)

        GUILogInstance.log("Condition set to 'partial degredation'", True)

    # -------------------------------------------------------------- Helper Methods
    def add_duration_constraint(self, tr_signal, user_duration, GUILogInstance):
        # get min & max val from user input
        user_str = user_duration.split(',')  # [constraint_name],[min],[max],[time_units]
        if len(user_str) == 4:

            # extract and form constraint
            min_val, max_val = user_str[1], user_str[2]
            dur_constraint = self.create_duration_constraint(min_val, max_val)

            # specify name and units
            dur_constraint.setName(user_str[0] + "[" + user_str[3] + "]")

            # constrain the signal by the duration
            elems = dur_constraint.getConstrainedElement()
            elems.add(tr_signal.signal)  # java.util.List

        else:
            self.log_message("Illegal number of inputs. Expected %d, got %d" % (4, len(user_str)))
            GUILogInstance.log("Illegal number of inputs. Expected %d, got %d" % (4, len(user_str)), True)

    def create_duration(self, value):
        """
        Creates a Duration instance using a specified value.
        """
        dur = self.elem_factory.createDurationInstance()
        val_spec = ModelHelper.createValueSpecification(self.project, dur.getType(), value, None)
        dur.setExpr(val_spec)
        return dur

    def create_duration_constraint(self, min_val, max_val):

        # make min and max Durations
        min_dur = self.create_duration(min_val)
        max_dur = self.create_duration(max_val)

        # make a Duration Interval
        duration_interval = self.elem_factory.createDurationIntervalInstance()
        duration_interval.setMin(min_dur)
        duration_interval.setMax(max_dur)

        # construct Duration Constraint
        duration_constraint = self.elem_factory.createDurationConstraintInstance()
        duration_constraint.setSpecification(duration_interval)
        return duration_constraint

    def add_mode(self, name, GUILogInstance):
        """
        Adds a state to the state machine diagram.
        """
        try:
            SessionManager.getInstance().createSession("Create Mode Requirement for Rule 3 No Degradation Action")

            # Open the mode requirement diagram
            diagrams = self.project.getDiagrams(SysMLConstants.SYSML_STATE_MACHINE_DIAGRAM)

            # create a new mode in the diagram
            if diagrams[0].isEditable():

                # create state
                state = self.elem_factory.createStateInstance()
                state.setName(name)

                # add state to state machine
                state_machine = diagrams[0].getDiagram().getOwnerOfDiagram()
                region = state_machine.getRegion().iterator().next()
                region.getOwnedElement().add(state)

                # notification manager
                msg = "Please update mode requirements. "
                msg += "New modes can be found in the same package folder as the mode requirement diagram."
                notification = Notification("notificationID", msg, None)
                NotificationManager.getInstance().showNotification(notification)

            else:
                self.log_message("State machine diagram is not editable!")
                GUILogInstance.log("State machine diagram is not editable!", True)

            SessionManager.getInstance().closeSession()  # always close the session!

        except Exception, e:
            self.log_message("Couldn't create mode requirement: %s" % e)
            GUILogInstance.log("Couldn't create mode requirement: %s" % e, True)

    def ui_define_range(self, tr_signal):
        msg = "Please define a range for " + tr_signal.signal.getHumanName() + "\n"
        msg += "Format: [property_name],[min],[max],[units]"
        return self.get_user_input(msg)

    # Add a new signal
    def ui_define_duration(self, tr_signal):
        msg = "Please define a duration constraint for " + tr_signal.signal.getHumanName() + "\n"
        msg += "Format: [constraint_name],[min],[max],[time_units]"
        return self.get_user_input(msg)

    def add_signal_property(self, property_name, value, tr_signal, GUILogInstance):
        try:
            SessionManager.getInstance().createSession("Define range as property in %s" % tr_signal.signal.getName())
            if tr_signal.signal.isEditable():

                # Create a new property
                prop = self.elem_factory.createPropertyInstance()
                prop.setName(property_name)
                prop.setType(self.sysml_profile.getString())
                prop.setVisibility(VisibilityKindEnum.PUBLIC)

                # create a value specification
                value_spec = ModelHelper.createValueSpecification(self.project, prop.getType(), value, None)
                prop.setDefaultValue(value_spec)

                # add property to owned attributes of the signal and close the session
                tr_signal.signal.getOwnedAttribute().add(prop)

                # try to remove argument from message
                # tr_signal.signal.getMessage()

                SessionManager.getInstance().closeSession()  # always close the session!

            else:
                self.log_message("Signal %s is not editable" % tr_signal.signal.getName())
                GUILogInstance.log("Signal %s is not editable" % tr_signal.signal.getName(), True)

        except Exception, e:
            self.log_message("Range couldn't be defined. Is input in the correct format? Error message: %s" % e)
            GUILogInstance.log("Range couldn't be defined. Is input in the correct format? Error message: %s" % e, True)

    def define_range_as_property(self, user_range, tr_signal, GUILogInstance):
        """
        Defines a range for the signal. Expected format: [property_name],[min],[max],[units]
        """
        user_str = user_range.split(',')  # [property_name],[min],[max],[units]
        if len(user_str) == 4:
            property_name = user_str[0]
            value = "[%s, %s] %s" % (user_str[1], user_str[2], user_str[3])  # [min, max] units
            self.add_signal_property(property_name, value, tr_signal, GUILogInstance)
        else:
            self.log_message("Illegal number of inputs. Expected %d, got %d" % (4, len(user_str)))
            GUILogInstance.log("Illegal number of inputs. Expected %d, got %d" % (4, len(user_str)), True)
