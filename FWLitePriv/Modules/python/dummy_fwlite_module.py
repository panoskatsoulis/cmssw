class fwlite_module2:
    name = "my-dummy-module"

    def begin(self, events):
        print("Run begin() for 'my-dummy-module'")
        return

    def analyze(self, event):
        aux_ev = event.eventAuxiliary()
        print "eventNumber_t:", aux_ev.event(), "module:", self.name

    def end(self, events):
        print("Run end() for 'my-dummy-module'")
        return

dummy_fwlite_module = fwlite_module2()
