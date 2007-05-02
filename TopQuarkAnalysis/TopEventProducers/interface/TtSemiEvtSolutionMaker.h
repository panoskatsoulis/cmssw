// -*- C++ -*-
//
// Package:    TtSemiEvtSolutionMaker
// Class:      TtSemiEvtSolutionMaker
// 
/**\class TtSemiEvtSolutionMaker TtSemiEvtSolutionMaker.cc AnalysisDataFormats/TopObjectsProducers/src/TtSemiEvtSolutionMaker.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Jan Heyninck
//         Created:  Thu May 18 18:11:01 CEST 2006
// $Id: TtSemiEvtSolutionMaker.h,v 1.1 2007/04/30 10:45:30 heyninck Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "AnalysisDataFormats/TopObjects/interface/TtSemiEvtSolution.h"
#include "TopQuarkAnalysis/TopKinFitter/interface/TtSemiKinFitterEtEtaPhi.h"
#include "TopQuarkAnalysis/TopKinFitter/interface/TtSemiKinFitterEtThetaPhi.h"
#include "TopQuarkAnalysis/TopKinFitter/interface/TtSemiKinFitterEMom.h"
#include "AnalysisDataFormats/TopObjects/interface/BestMatching.h"
//#include "TopQuarkAnalysis/TopJetCombination/interface/TtJetCombinationProbability.h"
#include <string>
#include <vector>
#include <iostream>
#include <fstream>

using namespace std;
using namespace reco;


//
// class decleration
//

class TtSemiEvtSolutionMaker : public edm::EDProducer {
   public:
      explicit TtSemiEvtSolutionMaker(const edm::ParameterSet&);
      ~TtSemiEvtSolutionMaker();


      virtual void produce(edm::Event&, const edm::EventSetup&);
   private:
      TtSemiKinFitterEtThetaPhi * myKinFitterEtThetaPhi;
      TtSemiKinFitterEtEtaPhi   * myKinFitterEtEtaPhi;
      TtSemiKinFitterEMom       * myKinFitterEMom;
      //std::vector<TtJetCombinationProbability> jetCombProbs;
      string leptonFlavour_;
      string jetInput_;
      bool addJetCombProb_, doKinFit_, matchToGenEvt_;
      int maxNrIter_;
      double maxDeltaS_, maxF_;
      int param_;
      vector<int> constraints_;
};
