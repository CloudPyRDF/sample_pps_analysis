# inspired by Perdo Silva code: https://gitlab.cern.ch/psilva/wgammapi

import os

datasets={
    'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':{
        'v2' : ['RunIISummer20UL18NanoAODv2','Pilot_106X_upgrade2018_realistic_v15_L1v1-v2'],
        'v9' : ['RunIISummer20UL18NanoAODv9','Pilot_106X_upgrade2018_realistic_v15_L1v1-v2'],
    },
    'DYToMuMu_pomflux_Pt-30_TuneCP5_13TeV-pythia8' : {
        'v2' : ['RunIISummer20UL18NanoAODv2','106X_upgrade2018_realistic_v16_L1v1-v1'],
        'v9' : ['RunIISummer20UL18NanoAODv9','106X_upgrade2018_realistic_v16_L1v1-v1'],
    },
    'Run2018A_DoubleMuon': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv1_NanoAODv9-v1']
    },
    'Run2018B_DoubleMuon': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v2'],
        'v9' : ['UL2018_MiniAODv1_NanoAODv9-v1']
    },
    'Run2018C_DoubleMuon': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv1_NanoAODv9-v1']
    },
    'Run2018D_DoubleMuon': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv1_NanoAODv9-v1']
    },
    'Run2018A_EGamma': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv2_NanoAODv9-v1']
    },
    'Run2018B_EGamma': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv2_NanoAODv9-v1']
    },
    'Run2018C_EGamma': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv2_NanoAODv9-v1']
    },
    'Run2018D_EGamma': {
        'v2' : ['UL2018_MiniAODv1_NanoAODv2-v1'],
        'v9' : ['UL2018_MiniAODv2_NanoAODv9-v1']
    },    
}

def ConvertToDASds(ds, v='v2'):
    if 'Run' in ds:
        return '/'+ds.split('_')[1]+'/'+('-'.join([ds.split('_')[0],datasets[ds][v][0]]))+'/NANOAOD'
    return '/'+ds+'/'+('-'.join(datasets[ds][v]))+'/NANOAODSIM'

def ConvertToEOSDirectory(ds, v='v2'):
    if 'Run' not in ds:
        return '/eos/cms/store/mc/'+datasets[ds][v][0]+'/'+ds+'/NANOAODSIM/'+datasets[ds][v][1]
    ds=ds.split('_')
    return '/eos/cms/store/data/'+ds.replace('_','/')+'/NANOAOD/'+datasets[ds][v][0]


def listDatasets(v='v2'):
    
    """ prints the available keys """

    print('The following datasets are available:')
    for ds in datasets.keys():
        print(ConvertToDASds(ds=ds,v=v))
    return

def getFilesFor(sample, eos=True):
    
    """fills with a list of files to use"""

    fileList=[]
    
    if not eos:
        print('ERROR: dasgoclient is not available in SWAN, cannot get list of files')
        return fileList
    
    for x in os.listdir(sample):
        url=os.path.join(sample,x)
        if os.path.isdir(url):
            fileList += getFilesFor(url)
        else:
            fileList += [url]
    
    return fileList

def getFilesForDataset(dataset):

    """ lists the files in a dataset directory and retrieves a list of files for analysis """

    try:
        sample_dir=datasetDirectories[dataset]
        fileList=getFilesFor(sample_dir)
    except:
        print('No directories available for dataset=',dataset,'returning an empty list')
        fileList=[]

    return fileList
