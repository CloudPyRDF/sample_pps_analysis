/*
Selector tools are folked from 
https://gitlab.cern.ch/psilva/wgammapi
Writen by Pedro Silva
*/

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "Math/Vector4D.h"

#include <vector>

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float>;
using rvec_i = const RVec<int>;
using rvec_b = const RVec<bool>;

//
rvec_b crossClean(const rvec_f &eta1,const rvec_f &phi1, const rvec_f &eta2, const rvec_f &phi2,float coneSize=0.4)
{
    size_t nobjs(eta1.size());
    std::vector<bool> isIso(nobjs,false);
    
    size_t ntestobjs(eta2.size());
    
    //loop over the first list of objects
    for(size_t i=0; i<nobjs; i++) {
        
        //find the min. distance with respect to the second list of objects
        float minDR(9999.);
        for(size_t j=0; j<ntestobjs; j++) {         
            float dR=DeltaR(eta1[i],eta2[j],phi1[i],phi2[j]);
            if(dR>minDR) continue;
            minDR=dR;
        }
        
        //if above the required cone size the object is isolated
        if(minDR>coneSize) isIso[i]=true;
    }

    return rvec_b(isIso.begin(), isIso.end());
}


