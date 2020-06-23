#!/usr/bin/env python
from __future__ import print_function
import argparse

parser = argparse.ArgumentParser(description='Executable for CMSSW FWLite.')
parser.add_argument('--source', '-s', type=str, help='Comma separated list of files to create the cmssw source.')
parser.add_argument('--modules', '-m', type=str, help='Comma separated list of python modules to create the cmssw path.')
parser.add_argument('--events', '-ev', default=-1, type=int, help='Number of events to run.')
parser.add_argument('--print-every', '-i', default=1, type=int, help='Print every this number of events.')
args = parser.parse_args()
# print(args)

def loadFWLite():
    print("Loading FW Lite ... ", end='')
    import ROOT
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.gSystem.Load("libDataFormatsFWLite.so")
    try:
        ROOT.gROOT.ProcessLine("FWLiteEnabler::enable()")
    except:
        print("Couldn't enable FWLite, check CMSSW version.")
        quit(1)
    print("[ok]")

def loadSource(files):
    source = files.split(',')
    return source

def loadModules(modules):
    path = []
    for module in modules.split(','):
        try:
            import_cmd = "from FWLitePriv.Modules.{m} import {m} as path_element".format(m = module)#; print(import_cmd)
            print("Loading module from FWLitePriv/Modules/python/{}.py ... ".format(module), end='')
            exec( import_cmd )
            path.append( path_element )
            print("name: '{}' ".format(path_element.name), end='')
            print("[ok]")
        except Exception as err:
            print("[failed]")
            print("Raised Exception:", err)
            print("Module {} couldn't be loaded properly.".format(module))
            quit(1)
    return path

def cmsRun(source, path):
    from DataFormats.FWLite import Events
    ## make the evet loop from the source
    events = Events(source)
    print( "Loaded {} events by the source list:".format(events.size()))
    print( source )
    ## run the begin functions
    for module in path:
        module.begin(events)
    ## run the analyze functions for each event
    for iev,event in enumerate(events):
        if args.events != -1 and iev+1 > args.events: break
        if iev % args.print_every == 0:
            print( "Running on event {} ...".format(iev) )
        for module in path:
            module.analyze( event ) # for each module in path, call analyze passing the edm::Event
    ## run the end functions
    for module in path:
        module.end(events)   

if __name__ == "__main__":
    # loadFWLite()
    cms_source = loadSource(args.source)
    cms_path = loadModules(args.modules)
    cmsRun(cms_source, cms_path)
