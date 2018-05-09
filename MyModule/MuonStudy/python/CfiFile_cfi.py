import FWCore.ParameterSet.Config as cms

muonStudy = cms.EDAnalyzer(
    "MuonStudy",
    #rpcHits = cms.InputTag("rpcUnpackingModule"),
    phiHits = cms.InputTag("bmtfDigis"),
    etaHits = cms.InputTag("bmtfDigis"),
    muonsData = cms.InputTag("bmtfDigis:BMTF"),
    muonsEmu = cms.InputTag("simBmtfDigis:BMTF")
)
