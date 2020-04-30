''' fwlite module template
import FWLitePriv.Core.fwlite_module
import ROOT

class NAME_module( fwlite_module ):

    def __init__(self, name="NAME"):
      super().__init__(name)

    def begin(self, events):
        ## do stuff before the event loop
        return

    def analyze(self, event):
        ## do stuff per event
        return

    def end(self, events):
        ## do stuff after the event loop
        return

NAME = NAME_module()
'''

class fwlite_module:
    # this class cannot be used as is
    # it must be inherited in order to create each module

    def __init__(self, name="dummy"):
        self.name = name

