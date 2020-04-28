class fwlite_module:
    name = "my-dummy-module-2"

    def begin(self, events):
        print("Run begin() for 'my-dummy-module-2'")
        return

    def analyze(self, event):
        aux_ev = event.eventAuxiliary()
        print "eventNumber_t:", aux_ev.event(), "module:", self.name

    def end(self, events):
        print("Run end() for 'my-dummy-module-2'")
        return

dummy_module2 = fwlite_module()
