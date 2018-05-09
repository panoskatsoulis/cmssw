// -*- C++ -*-
//
// Package:    Personal/MuonStudy
// Class:      MuonStudy
// 
/**\class MuonStudy MuonStudy.cc Personal/MuonStudy/plugins/MuonStudy.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Panagiotis Katsoulis
//         Created:  Sun, 03 Sep 2017 19:10:07 GMT
//
//


// system include files
#include <memory>
#include <iostream>
#include <fstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//
// class declaration - Data Formats

#include "DataFormats/FEDRawData/interface/FEDHeader.h"
#include "DataFormats/FEDRawData/interface/FEDNumbering.h"
#include "DataFormats/FEDRawData/interface/FEDRawDataCollection.h"
#include "DataFormats/FEDRawData/interface/FEDTrailer.h"

#include "DataFormats/L1DTTrackFinder/interface/L1MuDTChambPhContainer.h"
#include "DataFormats/L1DTTrackFinder/interface/L1MuDTChambThContainer.h"

#include "EventFilter/L1TRawToDigi/interface/AMC13Spec.h"
#include "EventFilter/L1TRawToDigi/interface/Block.h"

#include "L1Trigger/L1TMuon/interface/RegionalMuonRawDigiTranslator.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

//#include "TH1.h"
#include "TH1F.h"
#include "TH1I.h"
//#include "TH2.h"
#include "TH2F.h"
#include "TH2I.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "MyModule/MuonStudy/interface/analysisTools.h"

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class MuonStudy : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit MuonStudy(const edm::ParameterSet&);
  ~MuonStudy();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
  void otherCalculation(const edm::Handle<L1MuDTChambPhContainer>, TH2I&);
  void printEvent(const L1MuDTChambPhContainer*, const L1MuDTChambThContainer*, 
		  const l1t::RegionalMuonCandBxCollection*, const l1t::RegionalMuonCandBxCollection*, 
		  const std::string);

  // edm::EDGetTokenT<FEDRawDataCollection> binToken_original;
  // edm::EDGetTokenT<FEDRawDataCollection> binToken_replica;

  edm::EDGetTokenT<L1MuDTChambPhContainer> phiToken;
  edm::EDGetTokenT<L1MuDTChambThContainer> etaToken;
  edm::EDGetTokenT<l1t::RegionalMuonCandBxCollection> muonsToken_A;
  edm::EDGetTokenT<l1t::RegionalMuonCandBxCollection> muonsToken_B;
  
  edm::Service<TFileService> fs;
  std::ofstream fout;
  TFile *file;
  TH2F phisHist;//All Etas 2D
  TH2F etasHist;
  TH2F ptHist;
  TH2I sizeHist;
  TH2I bxHist;//not yet implemented
  TH2F phisCoarse;//Coarse Etas 2D
  TH2F etasCoarse;
  TH2F ptCoarse;
  TH2I sizeCoarse;
  TH1F phisData, phisEmu;
  TH1F etasData, etasEmu;
  TH1F ptData, ptEmu;
  TH1I fineBitData, fineBitEmu;
  TH1F phisRatio;//ratios
  TH1F etasRatio;
  TH1F ptRatio;
  int phiBins, etaBins, ptBins, sizeBins, bxBins, fBBins;
  // ----------member data ---------------------------
  // float Dev;
  // float dphis, detas, dmuons;
  // int phiSize, etaSize, muonsSize;
  int notMatched;
  int filledSame;
  int filledBySearch;
  int mismatchedContainers;
  int ptMismatches;
  int phiMismatches;
  int etaMismatches;
  int sizeMismatches;
  int events;
  //other calculations
  TH2I tsTagHist;
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
MuonStudy::MuonStudy(const edm::ParameterSet& iConfig)

{
  
  // std::string labelFEDData_1("rawDataCollector");
  // binToken_original = consumes<FEDRawDataCollection>(edm::InputTag(labelFEDData_1));  


  phiToken = consumes< L1MuDTChambPhContainer >(iConfig.getParameter<edm::InputTag>("phiHits"));
  etaToken = consumes< L1MuDTChambThContainer >(iConfig.getParameter<edm::InputTag>("etaHits"));
  muonsToken_A = consumes< l1t::RegionalMuonCandBxCollection >(iConfig.getParameter<edm::InputTag>("muonsData"));
  muonsToken_B = consumes< l1t::RegionalMuonCandBxCollection >(iConfig.getParameter<edm::InputTag>("muonsEmu"));
  
  fout.open("mismatchesFile");
  usesResource("TFileService");
  file = &(fs -> file());

  //Binning
  phiBins = 100;
  etaBins = 280;
  ptBins = 300;
  sizeBins = 21;
  bxBins = 7;
  fBBins = 4;

  phisHist = TH2F("muonPhis","phis comparison", phiBins, -20, 80, phiBins, -20, 80);
  etasHist = TH2F("muonEtas","eta comparison", etaBins, -140, 140, etaBins, -140, 140);
  ptHist = TH2F("muonPt","pT comparison", ptBins, 0, 300, ptBins, 0, 300);
  sizeHist = TH2I("bmtfSize","Muons# comparison", sizeBins, 0, 20, sizeBins, 0, 20);
  bxHist = TH2I("muonBx","BX comparison", bxBins, -3, 3, bxBins, -3, 3);//not yet implemented

  phisCoarse = TH2F("muonPhis_coarse","phis comparison", phiBins, -20, 80, phiBins, -20, 80);
  etasCoarse = TH2F("muonEtas_coarse","eta comparison", etaBins, -140, 140, etaBins, -140, 140);
  ptCoarse = TH2F("muonPt_coarse","pT comparison", ptBins, 0, 300, ptBins, 0, 300);
  sizeCoarse = TH2I("bmtfSize_coarse","Muons# comparison", sizeBins, 0, 20, sizeBins, 0, 20);

  phisData = TH1F("phisData","phis data", phiBins, -20, 80);
  etasData = TH1F("etasData","eta data", etaBins, -140, 140);
  ptData = TH1F("ptData","pT data", ptBins, 0, 300);
  fineBitData = TH1I("fineBitData","fineBit data", fBBins, -1, 2);

  phisEmu = TH1F("phisEmu","phis emu", phiBins, -20, 80);
  etasEmu = TH1F("etasEmu","eta emu", etaBins, -140, 140);
  ptEmu = TH1F("ptEmu","pT emu", ptBins, 0, 300);
  fineBitEmu = TH1I("fineBitEmu","fineBit emu", fBBins, -1, 2);

  //Other Calculations
  notMatched = 0;
  filledSame = 0;
  filledBySearch = 0;
  mismatchedContainers = 0;
  ptMismatches = 0;
  phiMismatches = 0;
  etaMismatches = 0;
  sizeMismatches = 0;
  events = 0;

  tsTagHist = TH2I("tsTagHist","TsTag comparison", 2, 0, 2, 2, 0, 2);
}


MuonStudy::~MuonStudy()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
MuonStudy::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   /*   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
   */

  // //Bin Collections
  // edm::Handle<FEDRawDataCollection> binRAW;
  // iEvent.getByToken(binToken_original, binRAW);

  // edm::Handle<FEDRawDataCollection> binRAWPacked;
  // iEvent.getByToken(binToken_replica, binRAWPacked);


  //Phi Collections
  edm::Handle<L1MuDTChambPhContainer> phiInput;
  iEvent.getByToken(phiToken,phiInput);

  //Eta Collections
  edm::Handle<L1MuDTChambThContainer> etaInput;
  iEvent.getByToken(etaToken,etaInput);
   
  //Muons Collections
  edm::Handle<l1t::RegionalMuonCandBxCollection> muonsInput_A;
  iEvent.getByToken(muonsToken_A,muonsInput_A);

  edm::Handle<l1t::RegionalMuonCandBxCollection> muonsInput_B;
  iEvent.getByToken(muonsToken_B,muonsInput_B);


  //Check Event Validity
  //if (not phiInput.isValid() && not etaInput.isValid())

  //Count events
  events++;

   //====================== other calculations =========================================================
  
  otherCalculation(phiInput, tsTagHist);

   //====================== muons Handler ==============================================================
   
   // if (muonsInput_A -> size() != muonsInput_B -> size()) {
   //   std::cout << "muons size not equal" << std::endl;
   //   std::cout << "coll-A:" << muonsInput_A -> size()
   // 	       << " coll-B:" << muonsInput_B -> size() << std::endl << std::endl;
   //   muonsSize++;
   // }


  if ( (*muonsInput_A).size() == (*muonsInput_B).size() ) {
    auto imuB = muonsInput_B -> begin();
    for (auto imuA : *muonsInput_A ) {

      // //test muon print - prints muon pairs for each muons' iterations (they loop together!)
      // printMuonPair(&imuA, &(*imuB));
      
      //data 1D histograms
      phisData.Fill(imuA.hwPhi());
      etasData.Fill(imuA.hwEta());
      ptData.Fill(imuA.hwPt());
      fineBitData.Fill(imuA.hwHF());

      //emu 1D histograms
      phisEmu.Fill(imuB->hwPhi());
      etasEmu.Fill(imuB->hwEta());
      ptEmu.Fill(imuB->hwPt());
      fineBitEmu.Fill(imuB->hwHF());

      //identify correct muon - 2D histograms
      bool filled(false);//, sameMuon(false);
      if (imuA.hwPhi() != imuB->hwPhi() ||
	  imuA.hwEta() != imuB->hwEta() ||
	  imuA.hwPt() != imuB->hwPt()) {

	for (auto emuMuon: *muonsInput_B ) {//iterate in emulator muons and find a match
	  if (imuA.hwPhi() == emuMuon.hwPhi() &&
	      imuA.hwEta() == emuMuon.hwEta() &&
	      imuA.hwPt() == emuMuon.hwPt()) {
	    
	    phisHist.Fill(imuA.hwPhi(), emuMuon.hwPhi());
	    etasHist.Fill(imuA.hwEta(), emuMuon.hwEta());
	    ptHist.Fill(imuA.hwPt(), emuMuon.hwPt());

	    if (imuA.hwHF() == 0) {
	      phisCoarse.Fill(imuA.hwPhi(), emuMuon.hwPhi());
	      etasCoarse.Fill(imuA.hwEta(), emuMuon.hwEta());
	      ptCoarse.Fill(imuA.hwPt(), emuMuon.hwPt());
	    }

	    filled = true;
	    break;
	  }
	}

      }//muon is diff
      // else
      // 	sameMuon = true;

      if (filled)
	filledBySearch++;
      // else if (!filled && sameMuon) {
      // 	phisHist.Fill(imuA.hwPhi(), imuB->hwPhi());
      // 	etasHist.Fill(imuA.hwEta(), imuB->hwEta());
      // 	ptHist.Fill(imuA.hwPt(), imuB->hwPt());

      // 	if (imuA.hwHF() == 0) {
      // 	  phisCoarse.Fill(imuA.hwPhi(), imuB->hwPhi());
      // 	  etasCoarse.Fill(imuA.hwEta(), imuB->hwEta());
      // 	  ptCoarse.Fill(imuA.hwPt(), imuB->hwPt());
      // 	}

      // 	filledSame++;
      // }
      else {
	phisHist.Fill(imuA.hwPhi(), imuB->hwPhi());
      	etasHist.Fill(imuA.hwEta(), imuB->hwEta());
      	ptHist.Fill(imuA.hwPt(), imuB->hwPt());

	if (imuA.hwHF() == 0) {
	  phisCoarse.Fill(imuA.hwPhi(), imuB->hwPhi());
	  etasCoarse.Fill(imuA.hwEta(), imuB->hwEta());
	  ptCoarse.Fill(imuA.hwPt(), imuB->hwPt());
	}

	//notMatched++;
      }


      //Mismatches
      if (imuA.hwPhi() != imuB->hwPhi()) {
	phiMismatches++;
	printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "PHI");
	//printMuonPair(&imuA, &(*imuB));
      }
      if (imuA.hwEta() != imuB->hwEta()) {
	etaMismatches++;
	printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "ETA");
	//printMuonPair(&imuA, &(*imuB));
      }
      if (imuA.hwPt() != imuB->hwPt()) {
	ptMismatches++;
	printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "PT");
	//printMuonPair(&imuA, &(*imuB));
      }

      //next emu muon
      imuB++;

    }//A-itr

  }
  else {
    mismatchedContainers++;

    if ( ((*muonsInput_A).size() != 0) && ((*muonsInput_B).size() != 0) ) {
      auto imuB = muonsInput_B -> begin();
      for (auto imuA : *muonsInput_A ) {

	bool filled(false);
	if (imuA.hwPhi() != imuB->hwPhi() ||
	    imuA.hwEta() != imuB->hwEta() ||
	    imuA.hwPt() != imuB->hwPt()) {

	  for (auto emuMuon: *muonsInput_B ) {//iterate in emulator muons and find a match
	    if (imuA.hwPhi() == emuMuon.hwPhi() &&
		imuA.hwEta() == emuMuon.hwEta() &&
		imuA.hwPt() == emuMuon.hwPt()) {
	    
	      phisHist.Fill(imuA.hwPhi(), emuMuon.hwPhi());
	      etasHist.Fill(imuA.hwEta(), emuMuon.hwEta());
	      ptHist.Fill(imuA.hwPt(), emuMuon.hwPt());

	      if (imuA.hwHF() == 0) {
		phisCoarse.Fill(imuA.hwPhi(), emuMuon.hwPhi());
		etasCoarse.Fill(imuA.hwEta(), emuMuon.hwEta());
		ptCoarse.Fill(imuA.hwPt(), emuMuon.hwPt());
	      }

	      filled = true;
	      break;
	    }
	  }

	}//muon is diff

	if (filled)
	  filledBySearch++;
	else {
	  phisHist.Fill(imuA.hwPhi(), imuB->hwPhi());
	  etasHist.Fill(imuA.hwEta(), imuB->hwEta());
	  ptHist.Fill(imuA.hwPt(), imuB->hwPt());

	  if (imuA.hwHF() == 0) {
	    phisCoarse.Fill(imuA.hwPhi(), imuB->hwPhi());
	    etasCoarse.Fill(imuA.hwEta(), imuB->hwEta());
	    ptCoarse.Fill(imuA.hwPt(), imuB->hwPt());
	  }

	}
      
	//Mismatches
	if (imuA.hwPhi() != imuB->hwPhi()) {
	  phiMismatches++;
	  printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "PHI");
	  //printMuonPair(&imuA, &(*imuB));
	}
	if (imuA.hwEta() != imuB->hwEta()) {
	  etaMismatches++;
	  printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "ETA");
	  //printMuonPair(&imuA, &(*imuB));
	}
	if (imuA.hwPt() != imuB->hwPt()) {
	  ptMismatches++;
	  printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "PT");
	  //printMuonPair(&imuA, &(*imuB));
	}

	if (imuB == muonsInput_B -> end())//since they are not of the same size
	  break;
	imuB++;
      }//muon A iter
    }
    else {
      if ((*muonsInput_A).size() == 0)
	fout << "data container was empty" << std::endl;
      else
	fout << "emu container was empty" << std::endl;
    }
  }//not same containers.
    
  //Size Histogram 2D
  sizeHist.Fill((*muonsInput_A).size(), (*muonsInput_B).size());

  if ((*muonsInput_A).size() != (*muonsInput_B).size())
    printEvent(phiInput.product(), etaInput.product(), muonsInput_A.product(), muonsInput_B.product(), "SIZE");

}//analyze method


// ------------ method called once each job just before starting event loop  ------------
void 
MuonStudy::beginJob()
{

}

// ------------ method called once each job just after ending the event loop  ------------
void 
MuonStudy::endJob() 
{
  //Ratios
  TH1F phiRatio("phiRatio", "phi Ratio", phiBins, -20, 80);
  TH1F etaRatio("etaRatio", "eta Ratio", etaBins, -140, 140);
  TH1F ptRatio("ptRatio", "pt Ratio", ptBins, 0, 300);
  for (int bin = 1; bin <= phiBins; bin++) {
    if (phisData.GetBinContent(bin) > 0)
      phiRatio.SetBinContent(bin, phisEmu.GetBinContent(bin)/phisData.GetBinContent(bin));
  }
  for (int bin = 1; bin <= etaBins; bin++) {
    if (etasData.GetBinContent(bin) > 0)
      etaRatio.SetBinContent(bin, etasEmu.GetBinContent(bin)/etasData.GetBinContent(bin));
  }
  for (int bin = 1; bin <= ptBins; bin++) {
    if (ptData.GetBinContent(bin) > 0)
      ptRatio.SetBinContent(bin, ptEmu.GetBinContent(bin)/ptData.GetBinContent(bin));
  }

  TList phiList;
  phiList.Add(&phisData);
  phiList.Add(&phisEmu);
  TCanvas *phiCan = analysisTools::makeCanvas(phiList, "Phis Superimposed");

  TList etaList;
  etaList.Add(&etasData);
  etaList.Add(&etasEmu);
  TCanvas *etaCan = analysisTools::makeCanvas(etaList, "Etas Superimposed");

  TList ptList;
  ptList.Add(&ptData);
  ptList.Add(&ptEmu);
  TCanvas *ptCan = analysisTools::makeCanvas(ptList, "Pts Superimposed");

  if (file -> cd()) {//it returns true in case of success
    //Drawing Customization
    phisHist.SetDrawOption("COLZ");
    phisHist.GetXaxis()->SetTitle("Data");
    phisHist.GetXaxis()->SetTitleOffset(1.2);
    phisHist.GetYaxis()->SetTitle("Emulator");
    phisHist.GetYaxis()->SetTitleOffset(1.2);
    etasHist.SetDrawOption("COLZ");
    etasHist.GetXaxis()->SetTitle("Data");
    etasHist.GetXaxis()->SetTitleOffset(1.2);
    etasHist.GetYaxis()->SetTitle("Emulator");
    etasHist.GetYaxis()->SetTitleOffset(1.2);
    ptHist.SetDrawOption("COLZ");
    ptHist.GetXaxis()->SetTitle("Data");
    ptHist.GetXaxis()->SetTitleOffset(1.2);
    ptHist.GetYaxis()->SetTitle("Emulator");
    ptHist.GetYaxis()->SetTitleOffset(1.2);
    sizeHist.SetDrawOption("COLZ");
    sizeHist.GetXaxis()->SetTitle("Data");
    sizeHist.GetXaxis()->SetTitleOffset(1.2);
    sizeHist.GetYaxis()->SetTitle("Emulator");
    sizeHist.GetYaxis()->SetTitleOffset(1.2);

    phisHist.Write();
    etasHist.Write();
    ptHist.Write();
    sizeHist.Write();

    phiRatio.Write();
    etaRatio.Write();
    ptRatio.Write();

    phisCoarse.Write();
    etasCoarse.Write();
    ptCoarse.Write();
    sizeCoarse.Write();

    phisData.Write();
    etasData.Write();
    ptData.Write();
    fineBitData.Write();

    phisEmu.Write();
    etasEmu.Write();
    ptEmu.Write();
    fineBitEmu.Write();

    phiCan->Write();
    etaCan->Write();
    ptCan->Write();

    //other calculations
    tsTagHist.Write();
  }
  else
    fout << "Cannot save the output to the file." << std::endl;

  fout << std::endl;
  fout << "SUMMARY" << std::endl;
  fout << "===================================================" << std::endl;
  fout << "Processed Events: " << events << std::endl;
  fout << "Not Matched: " << notMatched << std::endl;
  fout << "Filled by Search: " << filledBySearch << std::endl;
  fout << "Filled as Same: " << filledSame << std::endl;
  fout << "pt Mismatches: " << ptMismatches << std::endl;
  fout << "phi Mismatches: " << phiMismatches << std::endl;
  fout << "eta Mismatches: " << etaMismatches << std::endl;
  fout << "size Mismatches: " << mismatchedContainers << std::endl;
  //fout << "Muons not matched: " << muonsMissing << "\tpercent: " << 100*muonsMissing/events << "%" << std::endl;

  fout.close();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MuonStudy::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("phiHits", edm::InputTag("bmtfDigis"));
  desc.add<edm::InputTag>("etaHits", edm::InputTag("bmtfDigis"));
  desc.add<edm::InputTag>("muonsData", edm::InputTag("bmtfDigis:BMTF"));
  desc.add<edm::InputTag>("muonsEmu", edm::InputTag("simBmtfDigis:BMTF"));

  descriptions.add("muonStudy",desc);
}

// ------------ method Calculates anythng else the user needs in parallel with the validation procedure  ------------
void
MuonStudy::otherCalculation(const edm::Handle<L1MuDTChambPhContainer> phiHits, TH2I& hist2D) {

  int tsTag0_eventSize = 0, tsTag1_eventSize = 0;
  for (auto phi: *(phiHits->getContainer()) ) {//edm::Handlers arepointers to their products
    if (phi.bxNum() != 0)
      continue;

    if (phi.Ts2Tag() == 0)
      tsTag0_eventSize++;

    if (phi.Ts2Tag() == 1)
      tsTag1_eventSize++;
  }//phis

  if (tsTag0_eventSize == 0 && tsTag1_eventSize == 0)
    hist2D.Fill(0.,0.);
  else if (tsTag0_eventSize > 0 && tsTag1_eventSize == 0)
    hist2D.Fill(1.,0.);
  else if (tsTag0_eventSize == 0 && tsTag1_eventSize > 0)
    hist2D.Fill(0.,1.);
  else if (tsTag0_eventSize > 0 && tsTag1_eventSize > 0)
    hist2D.Fill(1.,1.);
  
}

void
MuonStudy::printEvent(const L1MuDTChambPhContainer* phis, const L1MuDTChambThContainer* etas,
		      const l1t::RegionalMuonCandBxCollection* muons_A, const l1t::RegionalMuonCandBxCollection* muons_B,
		      const std::string type = "UNSPECIFIED") {
  fout << "------- NEW [" << type << "] MISMATCH EVENT -------" << std::endl;

  for (int proc=0; proc<12; proc++) {
    fout << ">>> processor=" << proc << " <<<" << std::endl;

    for (int bx=-2; bx<=2; bx++) {
      fout << "--> BX=" << bx << std::endl;

      fout << "Wheel\tTs2tag\tStation\tRPC-bit\tQuality\tPhiB\tPhi" << std::endl;
      for (auto phi : *(phis->getContainer()) ) {
	if (proc != phi.scNum())
	  continue;

	if (bx != phi.bxNum())
	  continue;

	fout << phi.whNum() << "\t";
	fout << phi.Ts2Tag() << "\t";
	fout << phi.stNum() << "\t";
	fout << phi.RpcBit() << "\t";
	fout << phi.code() << "\t";
	fout << phi.phiB() << "\t";
	fout << phi.phi() << std::endl;
	// fout << "processor=" << phi.scNum() << std::endl;
	// fout << "BX=" << phi.bxNum() << "\t";
      }

      fout << "Wheel\tStation\tQuality\tEtaHits" << std::endl;
      for (auto eta : *(etas->getContainer()) ) {
	if (proc != eta.scNum())
	  continue;

	if (bx != eta.bxNum())
	  continue;

	fout << eta.whNum() << "\t";
	fout << eta.stNum() << "\t";

	//fout << "etaQual=";
	for (int i=0; i<7; i++)
	  fout << eta.quality(i);
	fout << "\t";

	//fout << "etaPos=";
	for (int i=0; i<7; i++)
	  fout << eta.position(i);
	fout << std::endl;

	// fout << "processor=" << eta.scNum() << std::endl;
	// fout << "BX=" << eta.bxNum() << "\t";
      }

    }//bx iteration 

    fout << std::endl;
  }//proc iteration

  for (int bx = muons_A->getFirstBX(); bx <= muons_A->getLastBX(); bx++) {
    //  for (auto muon : *muons_A ) {
    for (auto muon = muons_A->begin(bx); muon < muons_A->end(bx); muon++) {

      std::map<int, int> mu_TA = muon->trackAddress();
      //if (mu_TA.size() < 5)
      //return;

      fout << std::endl;
      fout << "__________DATA_____________________________________" << std::endl;
      fout << "HW_Processor=\t" << muon->processor() << std::endl;
      fout << "HW_BX=\t\t" << bx << std::endl;
      fout << "HW_Link=\t" << muon->link() << std::endl;  
      fout << "HW_Pt=\t\t" << muon->hwPt() << std::endl;
      fout << "HW_Phi=\t\t" << muon->hwPhi() << std::endl;
      fout << "HW_Eta=\t\t" << muon->hwEta() << std::endl;
      fout << "HW_fineBit=\t" << muon->hwHF() << std::endl;
      fout << "HW_Quality=\t" << muon->hwQual() << std::endl;
      fout << "HW_TrckAddress=\t" << analysisTools::toHex(mu_TA.at(2)) << analysisTools::toHex(mu_TA.at(3));
      fout << analysisTools::toHex(mu_TA.at(4)) << analysisTools::toHex(mu_TA.at(5)) << std::endl;
      fout << "HW_Sign=\t" << muon->hwSign() << std::endl;
      fout << "HW_SignValid=\t" << muon->hwSignValid() << std::endl;
    
    }//muons data
  }


  for (int bx = muons_B->getFirstBX(); bx <= muons_B->getLastBX(); bx++) {
    //  for (auto muon : *muons_B ) {
    for (auto muon = muons_B->begin(bx); muon < muons_B->end(bx); muon++) {

      std::map<int, int> mu_TA = muon->trackAddress();
      //if (mu_TA.size() < 5)
      //return;

      fout << std::endl;
      fout << "__________EMULATOR_________________________________" << std::endl;
      fout << "SW_Processor=\t" << muon->processor() << std::endl;
      fout << "SW_BX=\t\t" << bx << std::endl;
      fout << "SW_Link=\t" << muon->link() << std::endl;  
      fout << "SW_Pt=\t\t" << muon->hwPt() << std::endl;
      fout << "SW_Phi=\t\t" << muon->hwPhi() << std::endl;
      fout << "SW_Eta=\t\t" << muon->hwEta() << std::endl;
      fout << "SW_fineBit=\t" << muon->hwHF() << std::endl;
      fout << "SW_Quality=\t" << muon->hwQual() << std::endl;
      fout << "SW_TrckAddress=\t" << analysisTools::toHex(mu_TA.at(2)) << analysisTools::toHex(mu_TA.at(3));
      fout << analysisTools::toHex(mu_TA.at(4)) << analysisTools::toHex(mu_TA.at(5)) << std::endl;
      fout << "SW_Sign=\t" << muon->hwSign() << std::endl;
      fout << "SW_SignValid=\t" << muon->hwSignValid() << std::endl;

    }//muons emulator

  }//muons_BX iteration

  fout << std::endl << std::endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(MuonStudy);

   // How to access data
   // for (auto imuB : *muonsInput_B ) {
   //   //itrB++;
   //   if (imuA.hwEta() == imuB.hwEta() &&
   // 	 imuA.hwHF() == imuB.hwHF() &&
   // 	 imuA.hwPt() == imuB.hwPt() &&
   // 	 imuA.hwPhi() == imuB.hwPhi() &&
   // 	 imuA.hwQual() == imuB.hwQual() &&
   // 	 imuA.hwSign() == imuB.hwSign() &&
   // 	 imuA.hwSignValid() == imuB.hwSignValid() &&
   // 	 imuA.link() == imuB.link() &&
   // 	 imuA.processor() == imuB.processor()) {// &&
   //     //imuA.dataword() == imuB.dataword()) {
   //     found = true;
   //     break;
   //   }
   // }//B-itr



/*/// printPairMuons


    //std::map<int, int> muA_TA = muon_A.trackAddress(), muB_TA = muon_B->trackAddress();
    //if (muA_TA.size() < 5 || muB_TA.size() < 5)
    //return;

    std::cout << std::endl;
    std::cout << "__________EMULATOR_________________________________" << std::endl;
    std::cout << "HW-Muon" << "\t\t\t| " << "SW-Muon" << std::endl;
    std::cout << "HW_Processor=\t" << muon_A.processor() << "\t| " << "SW_Processor=\t" << muon_B->processor() << std::endl;
    std::cout << "HW_Link=\t" << muon_A.link() << "\t| " << "SW_Link=\t" << muon_B->link() << std::endl;  
    std::cout << "HW_Pt=\t\t" << muon_A.hwPt() << "\t| " << "SW_Pt=\t" << muon_B->hwPt() << std::endl;
    std::cout << "HW_Phi=\t\t" << muon_A.hwPhi() << "\t| " << "SW_Phi=\t" << muon_B->hwPhi() << std::endl;
    std::cout << "HW_Eta=\t\t" << muon_A.hwEta() << "\t| " << "SW_Eta=\t" << muon_B->hwEta() << std::endl;
    std::cout << "HW_fineBit=\t" << muon_A.hwHF() << "\t| " << "SW_fineBit=\t" << muon_B->hwHF() << std::endl;
    std::cout << "HW_Quality=\t" << muon_A.hwQual() << "\t| " << "SW_Quality=\t" << muon_B->hwQual() << std::endl;
    //std::cout << "HW_TrckAddress=\t" << analysisTools::toHex(muA_TA.at(2)) << analysisTools::toHex(muA_TA.at(3));
    //std::cout << analysisTools::toHex(muA_TA.at(4)) << analysisTools::toHex(muA_TA.at(5)) << "\t| ";
    //std::cout << "SW_TrckAddress= " << analysisTools::toHex(muB_TA.at(2)) << analysisTools::toHex(muB_TA.at(3));
    //std::cout << analysisTools::toHex(muB_TA.at(4)) << analysisTools::toHex(muB_TA.at(5)) << std::endl;
    std::cout << "HW_Sign=\t" << muon_A.hwSign() << "\t| " << "SW_Sign=\t" << muon_B->hwSign() << std::endl;
    std::cout << "HW_SignValid=\t" << muon_A.hwSignValid() << "\t| " << "SW_SignValid=\t" << muon_B->hwSignValid() << std::endl;

 */
