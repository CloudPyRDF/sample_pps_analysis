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
float SelectProtonXi(const rvec_f &proton_xi, const rvec_i &proton_arm, float xi_ll, int arm)
{
    size_t nobjs(proton_xi.size());   
    float out_xi = -999;
    
    //loop over the list protons
    for(size_t i=0; i<nobjs; i++) {
        
        if(proton_arm[i]!=arm) continue;
        
        if(abs(xi_ll-proton_xi[i])<abs(xi_ll-out_xi)) // select proton with closest xi value to xi reconstructed from the central system
            out_xi=proton_xi[i];
       
    }
    
    return out_xi;
}

