''' fwlite module template

class MyModule( fwlite_module ):

  def __init__(self, name):
    super().__init__(name)

'''

class fwlite_module:
    # this class cannot be used as is
    # it must be inherited in order to create each module

    def __init__(self, name="dummy"):
        self.name = name

    def begin(self, events):
        print("Run begin() for 'my-dummy-module'")
        return

    def analyze(self, event):
        aux_ev = event.eventAuxiliary()
        print "eventNumber_t:", aux_ev.event(), "module:", self.name

    def end(self, events):
        print("Run end() for 'my-dummy-module'")
        return
