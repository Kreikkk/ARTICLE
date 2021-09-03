import ROOT as root 


SFILENAME       = "ZgEWK_new.root"
BTESTFILENAMES  = ["ZgQCD1720k_2021.root",]
BTRAINFILENAMES = ["ZgQCD1720k_2021.root",]
# SFILENAME       = "ZgEWK.root"
# BTESTFILENAMES  = ["ZgQCD.root",]
# BTRAINFILENAMES = ["ZgQCD.root",]


BFILENAMES = ["ZgQCD.root", "ttgamma.root", "SinglePhoton.root", "WenuDataDriven.root",
              "Wgam.root", "WgamEWK.root", "Zllgam.root", "ZnunuFromQcd.root"]

TREENAME = "TMVA_input"

# DEFAULT_VARIABLES = ["mJJ", "deltaYJJ", "metPt", "ptBalance", "subleadJetEta",
#                      "leadJetPt", "photonEta", "ptBalanceRed", "nJets",
#                      "deltaYJPh", "sinDeltaPhiJJOver2",
#                      "thirdJetCentrality",
#                      "leadJetEta", "leadJetPhi",
#                      "subleadJetPt", "subleadJetPhi",
#                      "photonPt", "photonPhi",
#                      "thirdJetEta", "thirdJetPhi",
#                      "thirdJetPt", "phCentrality", 
#                      "nLeptons", "weightModified"]


DEFAULT_VARIABLES = ['mJ1J2',
        'mJ1J2J3',
        'ptBalance',
        'ptBalanceRed',
        'deltaYJ1J2',
        'deltaYJ1J3',
        'deltaYJ2J3',
        'deltaYJ1Ph',
        'deltaYJ2Ph',
        'deltaYJ3Ph',
        'deltaYJ1met',
        'deltaYJ2met',
        'deltaYJ3met',
        'deltaRJ1J2',
        'deltaRJ1J3',
        'deltaRJ2J3',
        'deltaRJ1Ph',
        'deltaRJ2Ph',
        'deltaRJ3Ph',
        'deltaRJ1met',
        'deltaRJ2met',
        'deltaRJ3met',
        'deltaYPhmet',
        'mmetPh',
        'mmetJ1',
        'mmetJ2',
        'mmetJ3',
        'mPhJ1',
        'mPhJ2',
        'mPhJ3',
        "deltaPhiJ1J2",
        "sinDeltaPhiJ1J2Over2",
        "deltaPtJ1J2",
        "thirdJetCentrality",
        "phCentrality",
        "jetCentrality",
        "metCentrality",
        "leadJetPt",
        "leadJetPhi",
        "leadJetEta",
        "subleadJetPt",
        "subleadJetPhi",
        "subleadJetEta",
        "thirdJetPt",
        "thirdJetPhi",
        "thirdJetEta",
        "photonPt",
        "photonPhi",
        "photonEta",
        "metPt",
        "metPhi",
        "nJets",
        #'thirdJetCentralityOffset',
        "nLeptons",
        "weightModified",]



DROP_NEGATIVE_W = False
USE_W = False

RANDOM_STATE = 32134

LIB = "XGB"


HISTOS = {"ZgEWK":{"label": "Z(#nu#nu)#gamma EWK", "color": root.kWhite,},
          "ZgQCD":{"label": "Z(#nu#nu)#gamma QCD", "color": root.kPink - 1,},
          "Wgam":{"label": "W#gamma QCD", "color": root.kOrange + 1,},
          "WgamEWK":{"label": "W#gamma EWK", "color": root.kOrange - 9,},
          "WenuDataDriven":{"label": "W(e#nu), top, t#bar{t}", "color": root.kSpring - 5,},
          "ttgamma":{"label": "tt#gamma", "color": root.kViolet - 6,},
          "SinglePhoton":{"label": "#gamma + j", "color": root.kGreen + 3,},
          "ZnunuFromQcd":{"label": "Zj, jj", "color": root.kCyan + 1,},
          "Zllgam":{"label": "Z(ll)#gamma", "color": root.kAzure + 3,},}


VARIABLES = {"mJJ":         {"label": "m_{jj} [GeV]", "margins": {"CR1": [0, 300, 0, 200], "CR2": [300, 1300, 0, 110], "Wgamma": [0, 1400, 0, 280]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "left", "CR2": "right", "Wgamma": "right",}},
             "deltaYJJ":    {"label": "#DeltaY(j_{1},j_{2})", "margins": {"CR1": [0, 3, 0, 230], "CR2": [0, 4, 0, 54], "Wgamma": [0, 5, 0, 200]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "right",}},
             "metPt":       {"label": "E_{T}^{miss} [GeV]", "margins": {"CR1": [120, 620, 0, 300], "CR2": [120, 620, 0, 68], "Wgamma": [120, 720, 0, 300]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "right",}},
             "ptBalance":   {"label": "p_{T}-balance", "margins": {"CR1": [0, 0.2, 0, 280], "CR2": [0, 0.2, 0, 70], "Wgamma": [0, 0.3, 0, 180]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "right",}},
             "subleadJetEta":{"label": "#eta(j_{2})", "margins": {"CR1": [-3.5, 3.5, 0, 230], "CR2": [-3.5, 3.5, 0, 68], "Wgamma": [-4, 4, 0, 210]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "left", "CR2": "right", "Wgamma": "right",}},
             "leadJetPt":   {"label": "p_{T}(j_{1}) [GeV]", "margins": {"CR1": [50, 400, 0, 300], "CR2": [50, 800, 0, 75], "Wgamma": [50, 1000, 0, 350]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "right",}},
             "photonEta":   {"label": "#eta(#gamma)", "margins": {"CR1": [-2.5, 2.5, 0, 180], "CR2": [-2.5, 2.5, 0, 60], "Wgamma": [-2.5, 2.5, 0, 160]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "left", "Wgamma": "right",}},
             "ptBalanceRed":{"label": "p_{T}-balance(reduced)", "margins": {"CR1": [0.2, 1, 0, 230], "CR2": [0.2, 1, 0, 66], "Wgamma": [0, 1, 0, 190]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "left",}},
             "nJets":       {"label": "N_{jets}", "margins": {"CR1": [1.5, 4.5, 0, 860], "CR2": [1.5, 4.5, 0, 180], "Wgamma": [1.5, 4.5, 0, 550]}, "nbins": {"CR1": 3, "CR2": 3, "Wgamma": 3,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "right",}},
             "sinDeltaPhiJJOver2": {"label": "sin(|#Delta#phi(j_{1},j_{2})|/2)", "margins": {"CR1": [0, 1, 0, 350], "CR2": [0, 1, 0, 160], "Wgamma": [0, 1, 0, 270]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "left", "CR2": "left", "Wgamma": "left",}},
             "deltaYJPh":   {"label": "#DeltaY(j_{1},#gamma)", "margins": {"CR1": [0, 4, 0, 225], "CR2": [0, 4, 0, 60], "Wgamma": [0, 4, 0, 200]}, "nbins": {"CR1": 10, "CR2": 10, "Wgamma": 10,}, "legpos": {"CR1": "right", "CR2": "right", "Wgamma": "right",}},}


GRAPHING_LABEL = {"CR1": "Z#gamma QCD CR 1",
                  "CR2": "Z#gamma QCD CR 2",
                  "Wgamma": "W#gamma CR",}