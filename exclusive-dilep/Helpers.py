import os

def PlotMe(historgam,opt=''):
    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)
    
    historgam.GetXaxis().SetTitleSize(0.04)
    historgam.GetYaxis().SetTitleSize(0.04)
    historgam.Draw(opt)
    
    label = ROOT.TLatex(); label.SetNDC(True)
    label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Work in progress}")
    label.SetTextSize(0.030); label.DrawLatex(0.790, 0.920, "#sqrt{s} = 13 TeV")
    
    return c    
