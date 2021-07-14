#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "L1Trigger/L1TMuonBarrel/interface/L1TMuonBarrelKalmanAlgo.h"
#include "L1Trigger/L1TMuonBarrel/interface/L1TMuonBarrelKalmanTrackFinder.h"
#include "DataFormats/L1TMuon/interface/L1MuKBMTCombinedStub.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCandFwd.h"
#include "CondFormats/DataRecord/interface/L1TMuonBarrelParamsRcd.h"

//
// class declaration
//

class L1TMuonBarrelKalmanTrackProducer : public edm::stream::EDProducer<> {
public:
  explicit L1TMuonBarrelKalmanTrackProducer(const edm::ParameterSet&);
  ~L1TMuonBarrelKalmanTrackProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void beginRun(const edm::Run&, const edm::EventSetup&) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;
  edm::EDGetTokenT<std::vector<L1MuKBMTCombinedStub> > src_;
  std::vector<int> bx_;
  L1TMuonBarrelKalmanAlgo* algo_;
  L1TMuonBarrelKalmanTrackFinder* trackFinder_;
  edm::ParameterSet iConfig_;
  bool useCondDB_;
};

L1TMuonBarrelKalmanTrackProducer::L1TMuonBarrelKalmanTrackProducer(const edm::ParameterSet& iConfig)
    : iConfig_(iConfig), useCondDB_(iConfig.getParameter<bool>("useCondDB")) {
  src_ = consumes<std::vector<L1MuKBMTCombinedStub> >(iConfig_.getParameter<edm::InputTag>("src"));
  produces<L1MuKBMTrackBxCollection>();
  produces<l1t::RegionalMuonCandBxCollection>("BMTF");
}

void L1TMuonBarrelKalmanTrackProducer::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup) {
  if (useCondDB_) {  // fetch the Rcd and initialize what depends on CondDB
    edm::ESHandle<L1TMuonBarrelKalmanParams> handle;
    const L1TMuonBarrelKalmanParams* kalmanParams;
    iSetup.get<L1TMuonBarrelKalmanParamsRcd>().get(handle);
    kalmanParams = handle.product();
    algo_ = new L1TMuonBarrelKalmanAlgo(iConfig_.getParameter<edm::ParameterSet>("algoSettings"), *kalmanParams);
  } else  // if not go static
    algo_ = new L1TMuonBarrelKalmanAlgo(iConfig_.getParameter<edm::ParameterSet>("algoSettings"), "");
  // now initialize the rest (hybrid for now with both ParamsSet and CondDBParams)
  bx_ = iConfig_.getParameter<std::vector<int> >("bx");
  trackFinder_ = new L1TMuonBarrelKalmanTrackFinder(iConfig_.getParameter<edm::ParameterSet>("trackFinderSettings"));
}

L1TMuonBarrelKalmanTrackProducer::~L1TMuonBarrelKalmanTrackProducer() {
  if (algo_ != nullptr)
    delete algo_;

  if (trackFinder_ != nullptr)
    delete trackFinder_;

  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to produce the data  ------------
void L1TMuonBarrelKalmanTrackProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  Handle<std::vector<L1MuKBMTCombinedStub> > stubHandle;
  iEvent.getByToken(src_, stubHandle);

  L1MuKBMTCombinedStubRefVector stubs;
  for (uint i = 0; i < stubHandle->size(); ++i) {
    L1MuKBMTCombinedStubRef r(stubHandle, i);
    stubs.push_back(r);
  }

  std::unique_ptr<l1t::RegionalMuonCandBxCollection> outBMTF(new l1t::RegionalMuonCandBxCollection());
  std::unique_ptr<L1MuKBMTrackBxCollection> out(new L1MuKBMTrackBxCollection());
  outBMTF->setBXRange(bx_.front(), bx_.back());
  out->setBXRange(bx_.front(), bx_.back());
  for (const auto& bx : bx_) {
    L1MuKBMTrackCollection tmp = trackFinder_->process(algo_, stubs, bx);
    for (const auto& track : tmp) {
      out->push_back(bx, track);
      algo_->addBMTFMuon(bx, track, outBMTF);
    }
  }
  iEvent.put(std::move(outBMTF), "BMTF");
  iEvent.put(std::move(out));
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void L1TMuonBarrelKalmanTrackProducer::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void L1TMuonBarrelKalmanTrackProducer::endStream() {}

void L1TMuonBarrelKalmanTrackProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1TMuonBarrelKalmanTrackProducer);
