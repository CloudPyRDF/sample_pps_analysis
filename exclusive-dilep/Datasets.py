# inspired by Perdo Silva code: https://gitlab.cern.ch/psilva/wgammapi

import os

datasets={
    'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':['RunIISummer20UL18NanoAODv9','Pilot_106X_upgrade2018_realistic_v15_L1v1-v2'],
    'DYToMuMu_pomflux_Pt-30_TuneCP5_13TeV-pythia8' : ['RunIISummer20UL18NanoAODv9','106X_upgrade2018_realistic_v16_L1v1-v1'],
}

# 2017 datasets
for stream in ['SingleMuon','DoubleMuon','SingleElectron']:
    for era in ['A','B','C','D','E','F']:
        datasets['Run2017%s_%s'%(era,stream)]=['UL2017_MiniAODv2_NanoAODv9-v1']
    
#2018 datasets
for stream in ['SingleMuon','DoubleMuon','EGamma']:
    for era in ['A','B','C','D']:
        datasets['Run2018%s_%s'%(era,stream)]=['UL2018_MiniAODv2_NanoAODv9-v1']

#corrections:


def ConvertToDASds(ds):
    if 'Run' in ds:
        return '/'+ds.split('_')[1]+'/'+('-'.join([ds.split('_')[0],datasets[ds][0]]))+'/NANOAOD'
    return '/'+ds+'/'+('-'.join(datasets[ds]))+'/NANOAODSIM'

def ConvertToEOSDirectory(ds):
    if 'Run' not in ds:
        return '/eos/cms/store/mc/'+datasets[ds][0]+'/'+ds+'/NANOAODSIM/'+datasets[ds][1]
    return '/eos/cms/store/data/'+ds.replace('_','/')+'/NANOAOD/'+datasets[ds][0]

def PrintFileSize(size, precision=2):
    unit='bytes'
    if (size // 1000) > 0: size/=1000; unit='kB'
    if (size // 1000) > 0: size/=1000; unit='MB'
    if (size // 1000) > 0: size/=1000; unit='GB'
    if (size // 1000) > 0: size/=1000; unit='TB'
    round(size,precision)
    return str(round(size,precision))+unit

def listDatasets():
    
    """ prints the available keys """

    print('The following datasets are available:')
    for ds in datasets.keys():
        fileList=getFilesForDataset(ds,eos=True)
        size=0; unit='bytes'
        for file in fileList: size+=os.path.getsize(file) 
        nfiles=len(fileList)
        msg='(No directories available in EOS for this dataset)'
        if nfiles:
            msg=('(in EOS: nfiles = %d, size = %s)'%(nfiles,PrintFileSize(size)))
        print(ConvertToDASds(ds=ds),msg)
    return

def getFilesFor(sample, eos=True):
    
    """fills with a list of files to use"""

    fileList=[]
    
    if not eos:
        print('ERROR: dasgoclient is not available in SWAN, cannot get list of files')
        return fileList
    
    if not os.path.exists(sample): return []
    
    for x in os.listdir(sample):
        url=os.path.join(sample,x)
        if os.path.isdir(url):
            fileList += getFilesFor(url)
        else:
            fileList += [url]
    
    return fileList

def getFilesForDataset(dataset, eos=True):

    """ lists the files in a dataset directory and retrieves a list of files for analysis """

    if not eos:
        print('ERROR: dasgoclient is not available in SWAN, cannot get list of files for dataset')
        return []
    if dataset not in datasets.keys():
        print('ERROR: Unknown dataset - '+dataset)
        return []
    
    sample_dir=ConvertToEOSDirectory(dataset)
    fileList=getFilesFor(sample_dir, eos=eos)
    
    return fileList
