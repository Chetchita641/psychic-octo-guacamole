"""
Author:     Richard Tan (rickytan@vt.edu)
Version:    2020.03.03
"""
# ------------------------------------------------------------------ Imports
import sys

# MagicDraw
from com.nomagic.magicdraw.openapi.uml import SessionManager, ModelElementsManager, PresentationElementsManager
from com.nomagic.magicdraw.sysml.util import SysMLProfile
from com.nomagic.uml2.ext.jmi.helpers import ModelHelper
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import VisibilityKindEnum
from com.nomagic.magicdraw.sysml.util import SysMLConstants
from com.nomagic.uml2.ext.magicdraw.statemachines.mdbehaviorstatemachines import Region
from com.nomagic.magicdraw.ui.notification import NotificationManager, Notification
from com.nomagic.magicdraw.ui.notification.config import NotificationViewConfig
from com.nomagic.magicdraw.copypaste import CopyPasting


# src
from AmbseBase import AmbseBase
from TrueReqDiagram import TrueReqDiagram
from TrueReqBlockDefDiagram import TrueReqBlockDefDiagram
from TrueReqSequenceDiagram import TrueReqSequenceDiagram
from TrueReqSignal import TrueReqSignal


# ------------------------------------------------------------------ Class Definition
class ProjectReviewer(AmbseBase):
    def __init__(self,project):
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
        self.true_req_diag = None # TrueReq instantiation of the current diagram


    # -------------------------------------------------------------- Methods
    def review_current_diagram(self):
        """
        Simply shows the current diagram type in a window.
        """
        self.true_req_diag = TrueReqDiagram(self.current_diagram)
        self.true_req_diag.log_diagram_elements()
        self.true_req_diag.log_presentation_elements()


    def invoke_rule2(self):
        """
        For now, this function just outputs questions onto the project window.
        """
        questions = ["Do you want to prescribe a behavior in case 'Electrical power' is lost while other inputs in 'Nominal Operation' are received?",
        "Do you want to prescribe a behavior in case 'Deployment arming' and 'Deployment firing' are received in reverse sequence?",
        "Do you want to prescribe a behavior in case an instance of 'Deployment firing' is received in less than 10s after receiving 'Deployment arming'?",
        "Choose between: New behavior/Maintain behavior/No degradation/Partial degradation",
        "Do you want to prescribe a behavior in case 'Electrical power' is received while executing 'Deployment'?"]

        for i,q in enumerate(questions):
            msg = q + "\n"

            if i == 3:
                msg += "Options: [new/maintain/no-deg/partial-deg]"
            else:
                msg += "Options: [Y/N]"

            user_input = self.get_user_input(msg)
            # self.log_message(q) # logs every question above in a message window


    def invoke_rule1(self):
        if self.diagram_type.isEqualType(self.SYSML_SEQUENCE_DIAGRAM):
            self.true_req_diag = TrueReqSequenceDiagram(self.current_diagram)
            self.rule1(self.true_req_diag.signals)
        else:
            self.log_message("Rule 1 is not applicable to a %s diagram (yet)"%self.current_diagram.getDiagramType().getType())

    
    def invoke_rule3(self):
        if self.diagram_type.isEqualType(self.SYSML_BLOCK_DEFINITION_DIAGRAM):
            self.true_req_diag = TrueReqBlockDefDiagram(self.current_diagram)
            self.rule3(self.true_req_diag.signals)

        else:
            self.log_message("Rule 3 is not applicable to a %s diagram (yet)"%self.current_diagram.getDiagramType().getType())


    # -------------------------------------------------------------- Rule 1 Methods
    def rule1(self,signals):
        keep_going = True
        for true_req_signal in signals:
            if keep_going:
                
                # construct first input window
                msg = "Do you care about "+true_req_signal.signal.getHumanName()+" going missing? \n"
                msg += "Options: [Y/N]"
                user_input = self.get_user_input(msg)
                # NOTE: input is None if nothing is entered!

                if user_input == "N":
                    self.log_message("Condition set to 'undefined'") # TODO: control which ones are evaluated already

                elif user_input == "Y":
                    user_duration = self.ui_define_duration(true_req_signal)

                    # Choose an action
                    msg = "Choose an action for the signal "+true_req_signal.signal.getHumanName()+"\n"
                    msg += "Options: [undefined/maintain behaviour/new behaviour]"
                    user_input = self.get_user_input(msg)

                    # Perform action
                    if user_input == "undefined":
                        self.rule1_undefined()

                    elif user_input == "maintain behaviour":
                        self.rule1_maintain_behaviour()
                    
                    elif user_input == "new behaviour":
                        self.rule1_new_behaviour()

                    else: # default case is 'undefined'
                        self.log_message("Invalid input, using undefined case by default")
                        self.rule1_undefined()

                else:
                    self.log_message("Input is invalid: %s"%user_input)

            else:
                break
            keep_going = False # TODO remove after testing

    
    def rule1_maintain_behaviour(self):
        # make an alt fragment
        self.add_fragment(InteractionOperatorKind.ALT)


    def rule1_new_behaviour(self):
        # make an opt fragment
        self.add_fragment(InteractionOperatorKind.OPT)


    def rule1_undefined(self):
        self.log_message("Rule 1 undefined action selected")

    def add_fragment(self,operator):
        """
        Creates a new combined fragment for a sequence diagram.

        @param operator:String the InteractionOperatorKind of 
        fragment to make 
        """
        diag = self.project.getActiveDiagram()

        # check diagram type
        if self.diagram_type.isEqualType(self.SYSML_SEQUENCE_DIAGRAM):
            try:
                SessionManager.getInstance().createSession("Create Mode Requirement for Rule 3 No Degredation Action")
                
                # create the fragment
                frag = self.elem_factory.createCombinedFragmentInstance()
                frag.setInteractionOperator(operator)

                # TODO add to diagram
                # get lifelines from the signal
                # append each lifeline to 'Covered' reference list
                # frag.getCovered().append()
                
                SessionManager.getInstance().closeSession() # always close the session!

            except Exception, e:
                self.log_message("Couldn't create fragment: %s"%e)
        
        else:
            self.log_message("Current diagram is not a Sequence Diagram. Fragments may only be made in sequence diagrams.")

    # -------------------------------------------------------------- Rule 3 Methods
    def rule3(self,signals):
        """
        Rule 3 algorithm to be done on signals
        """
        keep_going = True
        for true_req_signal in signals:
            if keep_going:

                # construct first input window
                msg = "Will the system be exposed outside the ranges of Signal "+true_req_signal.signal.getHumanName()+"? \n"
                msg += "Options: [Y/N]"
                user_input = self.get_user_input(msg)
                # NOTE: input is None if nothing is entered!

                if user_input == "N":
                    self.log_message("Condition set to 'undefined'") # TODO: control which ones are evaluated already

                elif user_input == "Y":

                    # Choose an action
                    msg = "Choose an action for the range of "+true_req_signal.signal.getHumanName()+"\n"
                    msg += "Options: [undefined/do same/no degradation/partial degradation]"
                    user_input = self.get_user_input(msg)

                    # Perform action
                    if user_input == "undefined":
                        self.rule3_undefined()

                    elif user_input == "do same":
                        self.rule3_do_same(true_req_signal)

                    elif user_input == "no degradation":
                        self.rule3_no_degradation(true_req_signal)
                    
                    elif user_input == "partial degredation":
                        self.rule3_partial_degredation(true_req_signal)

                    else: # default case is 'undefined'
                        self.log_message("Invalid input, using undefined case by default")
                        self.rule3_undefined()

                else:
                    self.log_message("Input is invalid: %s"%user_input)
                    
            else:
                break
            keep_going = False # TODO remove after testing


    def rule3_undefined(self):
        """
        No changes to the model.
        """
        self.log_message("Undefined case called for Rule 3")
    

    def rule3_do_same(self,tr_signal):
        """
        Asks user to modify specific properties of the
        given signal.
        """
        self.change_signal_props(tr_signal.signal)
        

    def rule3_no_degradation(self,tr_signal):
        """
        1. Create new signal for the range in block def diagram
        2. Applies duration between new & old signal
        3. Adds a new mode requirement to mode diagram
        """
        # create new signal
        new_signal = self.create_signal(tr_signal)

        # TODO apply duration
        msg = "Specify duration the out-of-range signal %s will be active \n"%new_signal.getHumanName()
        msg += "Format: [constraint_name],[min],[max],[time_units]"
        user_input = self.get_user_input(msg)
        self.add_duration_constraint(tr_signal.signal,new_signal,user_input)

        # add new mode
        name = "Non-nominal Signal: %s"%(tr_signal.signal.getName())
        self.add_mode(name)


    def rule3_partial_degredation(self,tr_signal):
        name = "Degraded Signal: %s"%tr_signal.signal.getName()
        self.add_mode(name)

        name = "Degraded Operation: %s"%tr_signal.signal.getName()
        self.add_mode(name)


    # -------------------------------------------------------------- Helper Methods
    def add_duration_constraint(self,signal0,signal1,user_duration):
         # get min & max val from user input
        user_str = user_duration.split(',') # [constraint_name],[min],[max],[time_units]
        if len(user_str) == 4:
            SessionManager.getInstance().createSession("Add DurationConstraint")

            for msg0,msg1 in zip(signal0.get_messageOfSignature(),signal1.get_messageOfSignature()):

                # extract and form constraint
                min_val, max_val = user_str[1], user_str[2]
                dur_constraint = self.create_duration_constraint(min_val,max_val)

                # specify name and units
                dur_constraint.setName(user_str[0]+"["+user_str[3]+"]")

                # constrain the signal by the duration
                elems = dur_constraint.getConstrainedElement()
                elems.add(msg0) # java.util.List
                elems.add(msg1)

                # add DurationConstraint to sequence diagram
                msg0_pres = PresentationElementsManager.getInstance().findPresentationElement(msg0,None)
                msg1_pres = PresentationElementsManager.getInstance().findPresentationElement(msg1,None)
                PresentationElementsManager.getInstance().createPathElement(dur_constraint,msg0_pres,msg1_pres)

            SessionManager.getInstance().closeSession()

        else:
            self.log_message("Illegal number of inputs. Expected %d, got %d"%(4,len(user_str)))


    def create_duration(self,value):
        """
        Creates a Duration instance using a specified value.
        """
        dur = self.elem_factory.createDurationInstance()
        val_spec = ModelHelper.createValueSpecification(self.project,dur.getType(),value,None)
        dur.setExpr(val_spec)
        return dur


    def create_duration_constraint(self,min_val,max_val):

        # make min and max Durations
        min_dur = self.create_duration(min_val)
        max_dur = self.create_duration(max_val)

        # make a DurationInterval
        duration_interval = self.elem_factory.createDurationIntervalInstance()
        duration_interval.setMin(min_dur)
        duration_interval.setMax(max_dur)
        
        # construct DurationConstraint
        duration_constraint = self.elem_factory.createDurationConstraintInstance()
        duration_constraint.setSpecification(duration_interval)
        return duration_constraint


    def create_signal(self,tr_signal):
        """
        Creates a new signal in the block definition diagram.
        """
        try:
            SessionManager.getInstance().createSession("Create New Signal")

            # make deep copy of diag signal
            new_signal = CopyPasting.copyPasteElement(tr_signal.signal,tr_signal.signal.getObjectParent(),True)
            self.change_signal_props(new_signal) # change specific signal property

            # add to block def diagram
            PresentationElementsManager.getInstance().createShapeElement(new_signal,self.current_diagram)

            # add to relevant sequence diagrams
            # TODO: replace w/ checkboxes
            messages = tr_signal.signal.get_messageOfSignature()
            for msg in messages:
                diagram = self.project.getDiagram(msg.getInteraction().getOwnedDiagram()[0]) # DiagramPresentationElement

                # create the new message
                new_msg = CopyPasting.copyPasteElement(msg,msg.getObjectParent(),True)
                new_msg.setSignature(new_signal)

                # add to sequence diagrams
                sort = msg.getMessageSort()
                from_lifeline = diagram.findPresentationElement(msg.getSendEvent().getCovered()[0],None)
                to_lifeline = diagram.findPresentationElement(msg.getReceiveEvent().getCovered()[0],None)
                recursive = False
                diagonal = 0
                insertAfter = msg
                verticalGap = 10
                # self.log_message(from_lifeline.getRepresents().getType().getName()+", "+to_lifeline.getRepresents().getType().getName())
                PresentationElementsManager.getInstance().createSequenceMessage(new_msg,sort,from_lifeline,to_lifeline,recursive,diagonal,insertAfter,verticalGap)                

            SessionManager.getInstance().closeSession()
            return new_signal

        except Exception, e:
            self.log_message("Couldn't create Signal %s: %s"%(tr_signal.signal.getName(),e))
            return None


    def change_signal_props(self,signal):
        """
        Asks user to change properties of a particular signal.
        """
        # iterate over signal properties
        # TODO replace w/ checkbox GUI
        tr_signal = TrueReqSignal(signal)
        for prop in tr_signal.properties:
            msg = "Please define a new range for "+prop.getName()+" in signal "+signal.getName()+"\n"
            msg += "To skip, leave blank and press ENTER \n"
            msg += "Or if done, type 'DONE' \n"
            msg += "Format: [min],[max],[units]"
            user_input = self.get_user_input(msg)

            if user_input == "DONE":
                break
            elif user_input == "":
                continue
            else:
                self.modify_property(prop,user_input)
        
    
    def modify_property(self,prop,user_input):
        user_str = user_input.split(',') # [min],[max],[units]
        if len(user_str) == 3:
            value = "[%s, %s] %s"%(user_str[0],user_str[1],user_str[2]) # [min, max] units
            value_spec = ModelHelper.createValueSpecification(self.project, prop.getType(), value, None)
            prop.setDefaultValue(value_spec)
        else:
            self.log_message("Illegal number of inputs. Expected %d, got %d"%(3,len(user_str)))


    def add_mode(self,name):
        """
        Adds a state to the state machine diagram.
        """
        try:
            SessionManager.getInstance().createSession("Create Mode Requirement for Rule 3 No Degredation Action")

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
                notification = Notification("notificationID",msg,None)
                NotificationManager.getInstance().showNotification(notification)

            else:
                self.log_message("State machine diagram is not editable!")

            SessionManager.getInstance().closeSession() # always close the session!

        except Exception, e:
            self.log_message("Couldn't create mode requirement: %s"%e)


    def ui_define_duration(self,tr_signal):
        msg = "Please define a duration constraint for "+tr_signal.signal.getHumanName()+"\n"
        msg += "Format: [constraint_name],[min],[max],[time_units]"
        return self.get_user_input(msg)


    def add_signal_property(self,value,tr_signal):
        try:
            SessionManager.getInstance().createSession("Define range as property in %s"%tr_signal.signal.getName())
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

                SessionManager.getInstance().closeSession() # always close the session!
                
            else:
                self.log_message("Signal %s is not editable"%tr_signal.signal.getName())

        except Exception, e:
            self.log_message("Range couldn't be defined. Is input in the correct format? Error message: %s"%e)


    def define_range_as_property(self,user_input,tr_signal):
        """
        Defines a range for the signal. Expected format: [property_name],[min],[max],[units]
        """
        user_str = user_input.split(',') # [property_name],[min],[max],[units]
        if len(user_str) == 4:
            property_name = user_str[0]
            value = "[%s, %s] %s"%(user_str[1],user_str[2],user_str[3]) # [min, max] units
            self.add_signal_property(property_name,value,tr_signal)
        else:
            self.log_message("Illegal number of inputs. Expected %d, got %d"%(4,len(user_str)))

        