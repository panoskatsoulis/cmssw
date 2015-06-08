// -*- C++ -*-
//
// Package:    uGMTInputProducerFromGen
// Class:      uGMTInputProducerFromGen
// 
/**\class uGMTInputProducerFromGen uGMTInputProducerFromGen.cc L1Trigger/L1TGlobalMuon/plugins/uGMTInputProducerFromGen.cc

 Description: takes generated muons and fills them in the expected collections for the uGMT

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Joschka Philip Lingemann,40 3-B01,+41227671598,
//         Created:  Thu Oct  3 10:12:30 CEST 2013
// $Id$
//
//


// system include files
#include <memory>
#include <fstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/L1TMuon/interface/L1TRegionalMuonCandidateFwd.h"
#include "DataFormats/L1TMuon/interface/L1TRegionalMuonCandidate.h"
#include "DataFormats/L1TMuon/interface/L1TGMTInputCaloSumFwd.h"
#include "DataFormats/L1TMuon/interface/L1TGMTInputCaloSum.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "TMath.h"
#include "TRandom3.h"

//
// class declaration
//
namespace l1t {
class uGMTInputProducerFromGen : public edm::EDProducer {
   public:
      explicit uGMTInputProducerFromGen(const edm::ParameterSet&);
      ~uGMTInputProducerFromGen();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      static bool compareMuons(const L1TRegionalMuonCandidate&, const L1TRegionalMuonCandidate&);
     
      // ----------member data ---------------------------
      edm::EDGetTokenT <reco::GenParticleCollection> genParticlesToken;
      int m_currEvt;
      const static int m_maxMuons = 108;
      TRandom3 m_rnd;
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
uGMTInputProducerFromGen::uGMTInputProducerFromGen(const edm::ParameterSet& iConfig) : 
  m_currEvt(0), m_rnd(0)
{
  //register your inputs:
  genParticlesToken = consumes <reco::GenParticleCollection> (std::string("genParticles"));
  //register your products
  produces<L1TRegionalMuonCandidateCollection>("BarrelTFMuons");
  produces<L1TRegionalMuonCandidateCollection>("OverlapTFMuons");
  produces<L1TRegionalMuonCandidateCollection>("ForwardTFMuons");
  produces<L1TGMTInputCaloSumCollection>("TriggerTowerSums");
}


uGMTInputProducerFromGen::~uGMTInputProducerFromGen()
{
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//



bool 
uGMTInputProducerFromGen::compareMuons(const L1TRegionalMuonCandidate& mu1, const L1TRegionalMuonCandidate& mu2) 
{
  return mu1.processor() < mu2.processor();
}

// ------------ method called to produce the data  ------------
void
uGMTInputProducerFromGen::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  std::auto_ptr<l1t::L1TRegionalMuonCandidateCollection> barrelMuons (new l1t::L1TRegionalMuonCandidateCollection());
  std::auto_ptr<l1t::L1TRegionalMuonCandidateCollection> overlapMuons (new l1t::L1TRegionalMuonCandidateCollection());
  std::auto_ptr<l1t::L1TRegionalMuonCandidateCollection> endcapMuons (new l1t::L1TRegionalMuonCandidateCollection());
  std::auto_ptr<l1t::L1TGMTInputCaloSumCollection> towerSums (new L1TGMTInputCaloSumCollection());


  std::vector<int> muIndices;
  edm::Handle<reco::GenParticleCollection> genParticles;
  // Make sure that you can get genParticles
  if (iEvent.getByToken(genParticlesToken, genParticles)) { 
    int cntr = 0;
    for (auto it = genParticles->cbegin(); it != genParticles->cend(); ++it) {
      const reco::Candidate& mcParticle = *it;
      if( abs(mcParticle.pdgId()) == 13 && mcParticle.status() == 1 )  muIndices.push_back(cntr);
      cntr++;
    }
  }
  else {
    LogTrace("GlobalMuon") << " GenParticleCollection not found." << std::endl;
  }

  l1t::L1TRegionalMuonCandidate mu;
  l1t::L1TGMTInputCaloSum tSum;
  // alternative scale (using full phi bit-width): 163.4521265553765f; 
  const float phiToInt = 91.67324722093171f;
  // alternative scale: 100.0f;
  const float etaToInt = 90.9090909090f; 
  const int maxPt = (1 << 9)-1;
  int muCntr = 0;

  double twoPi = TMath::Pi() * 2.;

  for (auto it = muIndices.begin(); it != muIndices.end(); ++it) {
    // don't really care which muons are taken... 
    // guess there ain't 108 generated anyways
    if (muCntr == m_maxMuons) break;
    int gen_idx = *it;
    const reco::Candidate& mcMuon = genParticles->at(gen_idx);
    double eta = mcMuon.eta();
    if (fabs(eta) > 2.45) continue; // out of acceptance
    int hwPt = int(mcMuon.pt() * 2);
    hwPt = (hwPt < maxPt ? hwPt : maxPt);
    int hwEta = int(eta * etaToInt);
    double phi = mcMuon.phi();
    if (phi < 0) phi += twoPi; // add 2*pi
    int hwPhi = (int(phi * phiToInt)+15)%576;
    int hwQual = 8;
    int hwCharge = (mcMuon.charge() > 0) ? 0 : 1;
    int hwChargeValid = 1;
    
    mu.setHwPt(hwPt);



    tftype tf(tftype::bmtf);
    int localPhi = hwPhi%56;
    int processor = hwPhi / 30 + 1;
    if (fabs(eta) > 0.8) {
      if (fabs(eta) < 1.2) {
        tf = (eta > 0 ? tftype::omtf_neg : tftype::omtf_pos);
        processor = hwPhi / 60 + 1;
        localPhi = hwPhi%112; 
      } else {
        tf = (eta > 0 ? tftype::emtf_neg : tftype::emtf_pos);
        processor = hwPhi / 60 + 1;
        localPhi = hwPhi%112;
      }
    }
    mu.setHwPhi(localPhi);
    mu.setProcessor(processor);
    mu.setTrackFinderType(tf);

    mu.setHwEta(hwEta);
    mu.setHwSign(hwCharge);
    mu.setHwSignValid(hwChargeValid);
    mu.setHwQual(hwQual);

    if (fabs(eta) < 0.8 && barrelMuons->size() < 36) {
      barrelMuons->push_back(mu);
      muCntr++;
    } else if (fabs(eta) < 1.2  && overlapMuons->size() < 36) {
      overlapMuons->push_back(mu);
      muCntr++;
    } else if (endcapMuons->size() < 36) {
      endcapMuons->push_back(mu);
      muCntr++;
    }
  }

  std::sort(barrelMuons->begin(), barrelMuons->end(), uGMTInputProducerFromGen::compareMuons);
  std::sort(overlapMuons->begin(), overlapMuons->end(), uGMTInputProducerFromGen::compareMuons);
  std::sort(endcapMuons->begin(), endcapMuons->end(), uGMTInputProducerFromGen::compareMuons);

  for (int i = 0; i < 1008; ++i) {
    // from where could I take the tower energies?
    int energy = int(m_rnd.Gaus(12, 6));
    if (energy < 0) energy = 0; 
    if (energy > 31) energy = 31;
    towerSums->emplace_back(energy, i/28, i%28, i);
  }
  // std::cout << std::endl;
  // std::cout << towerSums->size() << std::endl;
  iEvent.put(barrelMuons, "BarrelTFMuons");
  iEvent.put(overlapMuons, "OverlapTFMuons");
  iEvent.put(endcapMuons, "ForwardTFMuons");
  iEvent.put(towerSums, "TriggerTowerSums");
  m_currEvt++;
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
uGMTInputProducerFromGen::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
uGMTInputProducerFromGen::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
uGMTInputProducerFromGen::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
uGMTInputProducerFromGen::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
uGMTInputProducerFromGen::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
uGMTInputProducerFromGen::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
uGMTInputProducerFromGen::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
}
//define this as a plug-in
DEFINE_FWK_MODULE(l1t::uGMTInputProducerFromGen);
