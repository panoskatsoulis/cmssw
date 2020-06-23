from DataFormats.FWLite import Handle
from FWLitePriv.Core.fwlite_module import fwlite_module
import ROOT, math, re, array, uuid
execfile("python2.7_cc7_venv/bin/activate_this.py", dict(__file__="python2.7_cc7_venv/bin/activate_this.py"))
from particle import Particle
extra_table = {  1000022 : "X1_0", # LSP
                 1000023 : "X2_0", # Neutralino
                 1000024 : "X1+",  # Chargino+
                -1000024 : "X1-",  # Chargino-
##---------------------------------------------- others
                    543  : "Bc*+",
                   -543  : "Bc*-",
                  20413  : "D1(H)+",
                 -20413  : "D1(H)-",
                  20423  : "D1(2430)+?",
                 -20423  : "D1(2430)-?"
}

def cleanGENs(gens):
    res = []
    for part in gens:
        if part.pdgId() in [2212,-2212]: # fppend protons in the list
            res.append(part)
            continue
        if part.numberOfDaughters() >= 1: # has at least 1 daughter
            if part.mother(0).pdgId() != part.daughter(0).pdgId(): # mother id is not the daughter id
                if part.pdgId() != part.daughter(0).pdgId(): # self id is not the daughter id
                    res.append(part)
        else: # the part is the last in chain
            res.append(part)
    # print "cleanning up result: before", len(gens), ", after", len(res)
    return res

def printParticle(part):
    print "particle: id:", part.pdgId(), "status:", part.status(), "|*| momentum:", part.p(),\
        "eta:", part.eta(), "phi:", part.phi(), "vertex:", part.vertex().r(),\
        "|*| mother-id:", part.mother(0).pdgId() if part.mother(0) else "-",\
        "daughter_0-id:", part.daughter(0).pdgId() if part.daughter(0) else "finished"

def eventStringId(_list):
    stringId = ""
    for part in _list:
        partname = ""
        try:
            partname = Particle.from_pdgid(part.pdgId()).name
        except AttributeError:
            try: stringId += " {} ".format(part)
            except: raise TypeError("printParticleList can handle only reco::GenParticle or string types")
            continue
        except:
            partname = extra_table[part.pdgId()]
        stringId += "({})".format(partname)
    return stringId
        
def printParticleList(_list, lvl_id=None):
    print "lvl_id :", lvl_id, "[", eventStringId(_list), "]"

def sameParticlesInLists(_list1, _list2):
    if len(_list1) != len(_list2):
        return False
    else:
        for part1,part2 in zip(_list1,_list2):
            if part1.pdgId() != part2.pdgId():
                return False
        return True

def identifyEvent(gens):
    ## clean up the gens
    cleanned_gens = cleanGENs(gens)
    ## get event roots (protons or other particles in question)
    ev_roots = []
    for part in cleanned_gens:
        # if part.numberOfMothers() == 0:
        if abs( part.pdgId() ) in [1000024,1000023]:
            ev_roots.append(part)
    # print "event roots found", len(ev_roots) # debug
    # for r in ev_roots: printParticle(r)      # debug
    ## follow the roots to produce event id
    ret_ids = []
    for r in ev_roots:
        # print "analyzing new event root", r.pdgId()
        levels = [[r]]
        # printParticleList( levels[0] )
        # print [p.daughterRefVector().empty() for p in levels[-1]]
        while not all([p.daughterRefVector().empty() for p in levels[-1]]):
            lvl_parts = levels[-1]
            new_lvl = []
            for part in lvl_parts:
                daughters = part.daughterRefVector()
                for d in range(daughters.size()):
                    new_lvl.append(daughters[d])
            levels.append(new_lvl)
            # printParticleList( new_lvl )
        ## loop over the levels to print out the event id
        evId_toret = []
        for i,lvl in enumerate(levels):
            if sameParticlesInLists(lvl, levels[i-1]):
                continue
            # printParticleList(lvl,i)
            evId_toret += lvl
            if not lvl is levels[-1]:
                evId_toret.append("->")
        # printParticleList( evId_toret )
        ret_ids.append( eventStringId(evId_toret) )
    ## return list of strings with all particles starting from roots
    # for _id in ret_ids: print _id
    return ret_ids
        
class GEN_QualityAnalyzer_module( fwlite_module ):

    def __init__(self, name="GEN_QualityAnalyzer"):
        super(GEN_QualityAnalyzer_module, self).__init__(name)
        ## labels and handlers
        self.genParticles_label = ("genParticles"); self.genParticles_handle = Handle('std::vector<reco::GenParticle>')
        # self.genParticles_label = ("prunedGenParticles") ## for MINIAOD
        # self.packedGenParts_label = ("packedGenParticles"); self.packedGenParts_handle = Handle('std::vector<pat::PackedGenParticle>') ## for MINIAOD
        self.hepmcprod_label = ("generator"); self.hepmcprod_handle = Handle('edm::HepMCProduct')

    def begin(self, events):
        ## do stuff before the event loop
        self.mcProcesses = {}
        self.mC1_dmC2_hist = ROOT.TH2F("mC1_dmC2_hist","Histogram mC1 x dmC2", 70, 50, 300, 20, 1, 20)
        self.ctau_hist = ROOT.TH1F("ctau_hist", "Histogram ctau of C1/C2", 5*80, 0, 20)
        self.lep_ptHist = ROOT.TH1F("lep_ptHist", "lepton pt", 15, 0, 30)
        self.lep_etaHist = ROOT.TH1F("lep_etaHist", "lepton eta", 70, -3.5, 3.5)
        self.lep_phiHist = ROOT.TH1F("lep_phiHist", "lepton phi", 60, -3.3, 3.3)
        self.lep_pdgId = ROOT.TH1F("lep_pdgId", "lepton pdgid", 81, -40, 41)
        self.ele_ptHist = ROOT.TH1F("ele_ptHist", "electron pt", 60, 0, 30)
        self.ele_etaHist = ROOT.TH1F("ele_etaHist", "electron eta", 70, -3.5, 3.5)
        self.ele_phiHist = ROOT.TH1F("ele_phiHist", "electron phi", 60, -3.3, 3.3)
        self.ele_pdgId = ROOT.TH1F("ele_pdgId", "electron pdgid", 81, -40, 41)
        self.mu_ptHist = ROOT.TH1F("mu_ptHist", "muon pt", 60, 0, 30)
        self.mu_etaHist = ROOT.TH1F("mu_etaHist", "muon eta", 70, -3.5, 3.5)
        self.mu_phiHist = ROOT.TH1F("mu_phiHist", "muon phi", 60, -3.3, 3.3)
        self.mu_pdgId = ROOT.TH1F("mu_pdgId", "muon pdgid", 81, -40, 41)
        self.boson_ptHist = ROOT.TH1F("boson_ptHist", "boson from ele/mu;pt", 15, 0, 30)
        self.boson_etaHist = ROOT.TH1F("boson_etaHist", "boson from ele/mu;eta", 70, -3.5, 3.5)
        self.boson_phiHist = ROOT.TH1F("boson_phiHist", "boson from ele/mu;phi", 60, -3.3, 3.3)
        self.boson_pdgId = ROOT.TH1F("boson_pdgId", "boson from ele/mu;pdgid", 81, -40, 41)
        self.met_ptHist = ROOT.TH1F("met_ptHist", "MET from x1_0/nu;pt", 50, 0, 100)
        self.met_etaHist = ROOT.TH1F("met_etaHist", "MET from x1_0/nu;eta", 70, -3.5, 3.5)
        self.met_phiHist = ROOT.TH1F("met_phiHist", "MET from x1_0/nu;phi", 60, -3.3, 3.3)
        self.met_ids = {}
        return

    def analyze(self, event):
        try:
            event.getByLabel(self.genParticles_label, self.genParticles_handle)
            event.getByLabel(self.hepmcprod_label, self.hepmcprod_handle)
            gens = self.genParticles_handle.product()
            hepmc_event = self.hepmcprod_handle.product().GetEvent()
        except:
            event.getByLabel(self.packedGenParts_label, self.packedGenParts_handle)
            gens = self.packedGenParts_handle.product()
        # print gens
        # printParticleList(gens)
        ## testing print outs
        # print "Event id:", event.eventAuxiliary().event(), "   GENs_size =", gens.size()
        # print hepmc_event, "HepMC id:", hepmc_event.event_number(), "parts_barcodes =", hepmc_event.particles_size()
        # hepmc_event.write_units()
        ## do stuff per event
        for i,part in enumerate( gens ):
            # if abs( part.pdgId() ) in [1000024,1000037]: ## get charginos
            # if abs( part.pdgId() ) in [11,13,15]: ## get leptons
            # if abs( part.pdgId() ) in [111, 211]: ## get pions
            if abs( part.pdgId() ) in [1000024, 1000023] and abs( part.daughter(0).pdgId() ) in [1000022, 24] : # get charginos before decay (daughters x0 or W)
                ## calc masses phase-space
                # print part.numberOfDaughters()
                for d in range( part.numberOfDaughters() ):
                    daug = part.daughter(d)
                    if daug.pdgId() != 1000022: continue
                    # print "N0/C1/C2 mass =", part.mass(), "deltaM =", part.mass()-daug.mass()   # debug
                    self.mC1_dmC2_hist.Fill( part.mass(), part.mass()-daug.mass() ) # fill X: mass, Y deltaM
                ## calc ctau of C1: C1_vertex - daughter_vertex
                v1 = part.vertex() # chargino vertex
                v2 = part.daughter(0).vertex() # daughter vertex
                ctau = math.sqrt( (v1.X()-v2.X())*(v1.X()-v2.X()) + (v1.Y()-v2.Y())*(v1.Y()-v2.Y()) + (v1.Z()-v2.Z())*(v1.Z()-v2.Z()) )
                # print ctau
                self.ctau_hist.Fill( ctau )
        ## identify event
        ids_found = identifyEvent(gens)
        for _id in ids_found:
            process = re.match("(^[^>]* -> [^>]* -> [^> ]*) *.*",_id).groups()[0]
            if process in self.mcProcesses: # check if key exists
                self.mcProcesses[process] += 1
            else:
                self.mcProcesses[process] = 1
        ## is the event leptonic?
        isLeptonic = False
        for _id in ids_found:
            process = re.match("^[^>]* -> [^>]* -> ([^> ]*) *.*",_id).groups()[0]
            # print _id
            if re.match(".*W[\+\-][^>]* -> [^>]*mu[\+\-]\)\(nu\(mu.*",_id) or re.match(".*W[\+\-][^>]* -> [^>]*e[\+\-]\)\(nu\(e.*",_id):
            # if process in ["(mu-)(nu(mu)~)", "(mu+)(nu(mu))", "(e-)(nu(e)~)", "(e+)(nu(e))"]:
                # print "its leptonic"
                isLeptonic = True
        ## clean the gen collection from duplicates - to be used from this point on
        selected_gens = cleanGENs(gens)
        ## fill plots for leptonic events
        if isLeptonic:
            # try: ## for MINIAOD
            #     event.getByLabel(self.packedGenParts_label, self.packedGenParts_handle)
            #     gens = self.packedGenParts_handle.product()
            # except:
            #     raise RuntimeError("Unable to fetch the PackedGenParticles")
            for part in selected_gens:
                if abs( part.pdgId() ) in [11, 13]:
                    # printParticle( part )
                    motherid = abs( part.mother(0).pdgId() )
                    p = part
                    while motherid == abs( part.pdgId() ):
                        # print motherid
                        p = p.mother(0)
                        motherid = abs( p.mother(0).pdgId() )
                    # print motherid, "->", part.pdgId()
                    if motherid != 24: continue # plot only leptons coming from Ws
                    boson = p.mother(0)
                    # printParticle( boson )
                    # print "will plot..."
                    self.lep_ptHist.Fill( part.pt() )
                    self.lep_etaHist.Fill( part.eta() )
                    self.lep_phiHist.Fill( part.phi() )
                    self.lep_pdgId.Fill( part.pdgId() )
                    self.boson_ptHist.Fill( boson.pt() )
                    self.boson_etaHist.Fill( boson.eta() )
                    self.boson_phiHist.Fill( boson.phi() )
                    self.boson_pdgId.Fill( boson.pdgId() )
                    if abs( part.pdgId() ) == 11:
                        self.ele_ptHist.Fill( part.pt() )
                        self.ele_etaHist.Fill( part.eta() )
                        self.ele_phiHist.Fill( part.phi() )
                        self.ele_pdgId.Fill( part.pdgId() )
                    if abs( part.pdgId() ) == 13:
                        self.mu_ptHist.Fill( part.pt() )
                        self.mu_etaHist.Fill( part.eta() )
                        self.mu_phiHist.Fill( part.phi() )
                        self.mu_pdgId.Fill( part.pdgId() )
        ## calc and fill MET
        MET = ROOT.TLorentzVector()
        part_tmp = ROOT.TLorentzVector()
        for part in selected_gens:
            if abs( part.pdgId() ) in [12,14,16,1000022]: # any netrino or the LSP
                part_tmp.SetPtEtaPhiE( part.pt(), part.eta(), part.phi(), part.energy() )
                MET += part_tmp
                if part.pdgId() in self.met_ids: # check if key exists
                    self.met_ids[part.pdgId()] += 1
                else:
                    self.met_ids[part.pdgId()] = 1
        self.met_ptHist.Fill( MET.Pt() )
        self.met_etaHist.Fill( MET.Eta() )
        self.met_phiHist.Fill( MET.Phi() )       
        return

    def end(self, events):
        ## do stuff after the event loop
        rootfile = ROOT.TFile.Open("GEN_QualityAnalyzer_{}.root".format(uuid.uuid4()), "RECREATE")
        rootfile.cd()
        self.mC1_dmC2_hist.Write()
        self.ctau_hist.Write()
        self.lep_ptHist.Write()
        self.lep_etaHist.Write()
        self.lep_phiHist.Write()
        self.lep_pdgId.Write()
        self.boson_ptHist.Write()
        self.boson_etaHist.Write()
        self.boson_phiHist.Write()
        self.boson_pdgId.Write()
        self.ele_ptHist.Write()
        self.ele_etaHist.Write()
        self.ele_phiHist.Write()
        self.ele_pdgId.Write()
        self.mu_ptHist.Write()
        self.mu_etaHist.Write()
        self.mu_phiHist.Write()
        self.mu_pdgId.Write()
        self.met_ptHist.Write()
        self.met_etaHist.Write()
        self.met_phiHist.Write()
        ## make met pdgid TH1
        met_pdgId = ROOT.TH1I()
        met_pdgId.SetNameTitle("met_pdgId", "MET from x1_0/nu;pdgid")
        met_pdgId.SetBins(len(self.met_ids),0,len(self.met_ids))
        for _bin,pdgid in enumerate( sorted(self.met_ids.keys()) ): ## for making the met ids
            met_pdgId.SetBinContent(_bin+1, self.met_ids[pdgid]) # bin 0 is underflow
            met_pdgId.GetXaxis().SetBinLabel(_bin+1, str(pdgid))
        met_pdgId.Write()
        ## make processes TH1
        hist_procs = ROOT.TH1I()
        hist_procs.SetNameTitle("hist_procs", "Processes Included in the MC")
        hist_procs.SetBins(len(self.mcProcesses),0,len(self.mcProcesses))
        for _bin,proc in enumerate( sorted(self.mcProcesses.keys()) ): ## for making the processes tags
            hist_procs.SetBinContent(_bin+1, self.mcProcesses[proc]) # bin 0 is underflow
            hist_procs.GetXaxis().SetBinLabel(_bin+1, str(proc))
        hist_procs.Write()
        ## print out the list of processes
        for key in self.mcProcesses.keys():
            print  self.mcProcesses[key], "|", key
        return

GEN_QualityAnalyzer = GEN_QualityAnalyzer_module()
