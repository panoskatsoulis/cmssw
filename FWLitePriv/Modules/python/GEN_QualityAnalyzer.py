from DataFormats.FWLite import Handle
from FWLitePriv.Core.fwlite_module import fwlite_module
import ROOT, math

class GEN_QualityAnalyzer_module( fwlite_module ):

    def __init__(self, name="GEN_QualityAnalyzer"):
        super(GEN_QualityAnalyzer_module, self).__init__(name)
        ## labels and handlers
        self.genParticles_label = ("genParticles"); self.genParticles_handle = Handle('std::vector<reco::GenParticle>')
        self.hepmcprod_label = ("generator"); self.hepmcprod_handle = Handle('edm::HepMCProduct')

    def begin(self, events):
        ## do stuff before the event loop
        self.mC1_dmC2_hist = ROOT.TH2F("mC1_dmC2_hist","Histogram mC1 x dmC2", 70, 50, 300, 20, 1, 20)
        self.ctau_hist = ROOT.TH1F("ctau_hist", "Histogram ctau of C1/C2", 80, 0, 20)
        return

    def analyze(self, event):
        event.getByLabel(self.genParticles_label, self.genParticles_handle)
        event.getByLabel(self.hepmcprod_label, self.hepmcprod_handle)
        gens = self.genParticles_handle.product()
        hepmc_event = self.hepmcprod_handle.product().GetEvent()
        ## testing print outs
        print "Event id:", event.eventAuxiliary().event(), "   GENs_size =", gens.size()
        print hepmc_event, "HepMC id:", hepmc_event.event_number(), "parts_barcodes =", hepmc_event.particles_size()
        print "Units used: Momentum ", ROOT.HepMC.Units(hepmc_event.momentum_unit()), ", Length ", hepmc_event.length_unit()
        ## do stuff per event
        for i,part in enumerate( gens ):
            # if abs( part.pdgId() ) in [1000024,1000037]: ## get charginos
            # if abs( part.pdgId() ) in [11,13,15]: ## get leptons
            # if abs( part.pdgId() ) in [111, 211]: ## get pions
            if abs( part.pdgId() ) in [1000024] and abs( part.daughter(0).pdgId() ) in [1000022, 24] : # get charginos before decay (daughters x0 or W)
                # print "particle: id:", part.pdgId(), "status:", part.status(), "momentum:", part.p(),\
                #     "vertex :", part.vertex().r(), "|*| mother-id:", part.mother().pdgId(),\
                #     "daughter_0-id:", part.daughter(0).pdgId() if part.daughter(0) else "finished"
                ## calc masses phase-space
                for d in range( part.numberOfDaughters() ):
                    daug = part.daughter(d)
                    if daug.pdgId() != 1000022: continue
                    # print "C1/C2 mass =", part.mass(), "deltaM =", part.mass()-daug.mass()
                    self.mC1_dmC2_hist.Fill( part.mass(), part.mass()-daug.mass() ) # fill X: mass, Y deltaM
                ## calc ctau of C1: C1_vertex - daughter_vertex
                v1 = part.vertex() # chargino vertex
                v2 = part.daughter(0).vertex() # daughter vertex
                ctau = math.sqrt( (v1.X()-v2.X())*(v1.X()-v2.X()) + (v1.Y()-v2.Y())*(v1.Y()-v2.Y()) + (v1.Z()-v2.Z())*(v1.Z()-v2.Z()) )
                # print ctau
                self.ctau_hist.Fill( ctau )
        return

    def end(self, events):
        ## do stuff after the event loop
        rootfile = ROOT.TFile.Open("GEN_QualityAnalyzer.root", "RECREATE")
        rootfile.cd()
        self.mC1_dmC2_hist.Write()
        self.ctau_hist.Write()
        return

GEN_QualityAnalyzer = GEN_QualityAnalyzer_module()
