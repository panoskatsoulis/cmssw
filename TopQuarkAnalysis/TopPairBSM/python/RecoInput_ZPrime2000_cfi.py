# from /RelValQCD_Pt_3000_3500/CMSSW_2_1_0_pre6-RelVal-1213987236-IDEAL_V2-2nd/GEN-SIM-DIGI-RAW-HLTDEBUG-RECO

import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() : 
 return cms.Source("PoolSource",
                   debugVerbosity = cms.untracked.uint32(200),
                   debugFlag = cms.untracked.bool(True),
                   
                   fileNames = cms.untracked.vstring(
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_100.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_101.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_102.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_104.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_105.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_107.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_108.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_109.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_10.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_110.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_111.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_112.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_113.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_114.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_116.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_117.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_118.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_119.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_11.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_120.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_121.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_122.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_123.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_124.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_125.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_126.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_127.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_128.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_12.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_130.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_131.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_132.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_133.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_134.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_135.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_136.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_137.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_138.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_139.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_13.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_140.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_141.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_142.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_143.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_144.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_145.root', 
#     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_146.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_147.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_148.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_149.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_14.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_150.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_151.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_152.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_153.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_154.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_155.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_156.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_157.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_158.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_159.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_15.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_160.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_161.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_162.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_164.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_165.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_166.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_167.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_168.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_169.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_170.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_171.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_172.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_173.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_174.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_176.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_177.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_178.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_179.root', 
#     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_17.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_180.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_181.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_182.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_183.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_184.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_185.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_186.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_187.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_189.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_18.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_190.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_191.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_192.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_193.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_194.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_195.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_196.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_197.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_198.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_199.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_19.root', 
#     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_1.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_200.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_201.root', 
#     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_202.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_203.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_204.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_205.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_206.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_207.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_208.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_209.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_20.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_210.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_212.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_213.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_214.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_216.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_217.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_218.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_21.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_220.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_221.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_222.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_223.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_224.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_225.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_226.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_227.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_228.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_229.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_22.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_230.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_231.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_232.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_233.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_234.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_235.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_236.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_237.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_238.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_239.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_23.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_240.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_241.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_242.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_243.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_244.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_245.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_246.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_247.root', 
#     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_249.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_24.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_250.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_25.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_26.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_27.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_28.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_2.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_30.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_31.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_32.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_33.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_34.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_35.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_36.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_37.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_38.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_39.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_3.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_40.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_41.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_42.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_43.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_44.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_45.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_46.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_47.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_48.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_49.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_4.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_50.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_51.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_52.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_53.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_55.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_56.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_57.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_58.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_59.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_5.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_60.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_61.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_62.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_63.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_64.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_65.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_67.root', 
#     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_68.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_69.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_6.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_71.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_72.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_73.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_74.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_75.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_76.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_77.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_78.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_79.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_7.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_80.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_81.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_82.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_83.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_84.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_85.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_86.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_87.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_89.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_8.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_90.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_91.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_92.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_94.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_95.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_96.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_97.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_98.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_99.root', 
     'dcache:/pnfs/cms/WAX/resilient/rappocc/zprime/zprime_2000GeV_9.root'
     
     )
                   )
