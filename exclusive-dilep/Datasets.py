# inspired by Perdo Silva code: https://gitlab.cern.ch/psilva/wgammapi

import os

datasets={
    'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':{
        'v2' : ['RunIISummer20UL18NanoAODv2','Pilot_106X_upgrade2018_realistic_v15_L1v1-v2'],
        'v9' : ['RunIISummer20UL18NanoAODv9','Pilot_106X_upgrade2018_realistic_v15_L1v1-v2'],
    },
    'DYToMuMu_pomflux_Pt-30_TuneCP5_13TeV-pythia8' : {
        'v2' : ['RunIISummer20UL18NanoAODv2','106X_upgrade2018_realistic_v15_L1v1-v1'],
        'v9' : ['RunIISummer20UL18NanoAODv9','106X_upgrade2018_realistic_v16_L1v1-v1'],
    }
}
for era in ['A','B','C','D','E','F']:
    for stream in ['SingleMuon','DoubleMuon','EGamma']:
        datasets['Run2017%s_%s'%(era,stream)]={
            'v2' : ['UL2017_MiniAODv1_NanoAODv2-v1'],
            'v9' : ['UL2017_MiniAODv2_NanoAODv9-v1']
        }

for era in ['A','B','C','D']:
    for stream in ['SingleMuon','DoubleMuon','EGamma']:
        datasets['Run2018%s_%s'%(era,stream)]={
            'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
            'v9' : ['UL2018_MiniAODv2_NanoAODv9-v1']
        }

#corrections:


def ConvertToDASds(ds, v='v9'):
    if 'Run' in ds:
        return '/'+ds.split('_')[1]+'/'+('-'.join([ds.split('_')[0],datasets[ds][v][0]]))+'/NANOAOD'
    return '/'+ds+'/'+('-'.join(datasets[ds][v]))+'/NANOAODSIM'

def ConvertToEOSDirectory(ds, v='v9'):
    if 'Run' not in ds:
        return '/eos/cms/store/mc/'+datasets[ds][v][0]+'/'+ds+'/NANOAODSIM/'+datasets[ds][v][1]
    return '/eos/cms/store/data/'+ds.replace('_','/')+'/NANOAOD/'+datasets[ds][v][0]


def listDatasets(v='v9'):
    
    """ prints the available keys """

    print('The following datasets are available:')
    for ds in datasets.keys():
        fileList=getFilesForDataset(ds,v=v,eos=True)
        size=0; unit='bytes'
        for file in fileList: size+=os.path.getsize(file) 
        if (size // 1000) > 0: size/=1000; unit='kB'
        if (size // 1000) > 0: size/=1000; unit='MB'
        if (size // 1000) > 0: size/=1000; unit='GB'
        if (size // 1000) > 0: size/=1000; unit='TB'
        nfiles=len(fileList)
        msg='(No directories available in EOS for this dataset)'
        if nfiles:
            msg=('(in EOS: nfiles = %d, size = %2.2f%s)'%(nfiles,size,unit))
        print(ConvertToDASds(ds=ds,v=v),msg)
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

def getFilesForDataset(dataset, v='v9', eos=True):

    """ lists the files in a dataset directory and retrieves a list of files for analysis """

    if not eos:
        print('ERROR: dasgoclient is not available in SWAN, cannot get list of files for dataset')
        return []
    if dataset not in datasets.keys():
        print('ERROR: Unknown dataset - '+dataset)
        return []
    
    sample_dir=ConvertToEOSDirectory(dataset, v)
    fileList=getFilesFor(sample_dir, eos=eos)
    
    return fileList
