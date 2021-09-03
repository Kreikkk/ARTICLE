CREATE_FIGS = True

SELECTIONS_ZGM = [("nJets", ">", 1),
				  ("nLeptons", "==", 0),]
SELECTIONS_SIG = [("nJets", ">", 1),
				  ("nLeptons", "==", 0),
				  ("mJ1J2", ">", 300),
				  ("phCentrality", "<", 0.6)]

SELECTIONS 	= {"b0":	{"zgm":	SELECTIONS_ZGM,
						 "sig":	SELECTIONS_SIG},
			   "b1_1":	{"zgm": [*SELECTIONS_ZGM, ("nJets", "==", 2)],
			   			 "sig": [*SELECTIONS_SIG, ("nJets", "==", 2)]},
			   "b1_2":	{"zgm": [*SELECTIONS_ZGM, ("nJets", ">", 2)],
			   			 "sig": [*SELECTIONS_SIG, ("nJets", ">", 2)]},
			   "b2":	{"zgm":	SELECTIONS_ZGM,
						 "sig":	SELECTIONS_SIG},
			   "b3":	{"zgm":	SELECTIONS_ZGM,
						 "sig":	SELECTIONS_SIG},}

#Для XGB (старые файлы)
# SETTINGS 	= {"b0":	{"n_estimators": 449, "max_depth": 3, "learning_rate": 0.07054427028037506},
# 			   "b1_1":	{"n_estimators": 190,  "max_depth": 3, "learning_rate": 0.06478523451955022},
# 			   "b1_2":	{"n_estimators": 1144,  "max_depth": 3, "learning_rate": 0.014791340756709726},
# 			   "b2":	{"n_estimators": 1159,  "max_depth": 3, "learning_rate": 0.02180521586544691},
# 			   "b3":	{"n_estimators": 452, "max_depth": 3, "learning_rate": 0.07190109611150454},}

#Для LGBM (старые файлы)
# SETTINGS 	= {"b0":	{"n_estimators": 1786, "max_depth": 2, "learning_rate": 0.09194896396374126},
# 			   "b1_1":	{"n_estimators": 110,  "max_depth": 3, "learning_rate": 0.09591139963796684},
# 			   "b1_2":	{"n_estimators": 432,  "max_depth": 3, "learning_rate": 0.04152949470308766},
# 			   "b2":	{"n_estimators": 235,  "max_depth": 3, "learning_rate": 0.09645511938925498},
# 			   "b3":	{"n_estimators": 1420, "max_depth": 2, "learning_rate": 0.06838846562348731},}

SETTINGS 	= {"b0":	{"n_estimators": 396,  "max_depth": 3, "learning_rate": 0.060443444828994476},
			   "b1_1":	{"n_estimators": 649,  "max_depth": 3, "learning_rate": 0.04142349091683073},
			   "b1_2":	{"n_estimators": 1013,  "max_depth": 2, "learning_rate": 0.05095083005118689},
			   "b2":	{"n_estimators": 1207,  "max_depth": 2, "learning_rate": 0.07376278326841684},
			   "b3":	{"n_estimators": 312, "max_depth": 3, "learning_rate": 0.05480222688826423},}

# GENERAL_SETTINGS = {"objective": "binary", "n_jobs": 10, "subsample": 0.5, "colsample_bytree": 0.5}

GENERAL_SETTINGS = {"objective": "binary", "n_jobs": 10}


DEFAULT_VARS	= ["mJ1J2", "phCentrality", "ptBalance", "subleadJetPt",
				   "mPhJ2", "nJets", "deltaYJ1J2", "deltaRJ1J2",
				   "deltaPhiJ1J2", "metPt"]
THIRD_JET_VARS	= ["mJ1J2J3", "thirdJetCentrality", "deltaRJ2J3",
				   "deltaYJ1J3", "deltaYJ2J3"]

# DEFAULT_VARS	= ["mJ1J2", "deltaYJ1J2", "metPt", "ptBalance",
# 				   "subleadJetEta", "leadJetPt", "photonEta", "ptBalanceRed",
# 				   "nJets", "deltaYJ1Ph", "sinDeltaPhiJ1J2Over2"]
THIRD_JET_VARS	= ["thirdJetCentrality"]


ALL_VARS		= [*DEFAULT_VARS, *THIRD_JET_VARS]

TR_VARS		= {"b0":	DEFAULT_VARS,
			   "b1_1":	DEFAULT_VARS,
			   "b1_2":	ALL_VARS,
			   "b2":	ALL_VARS,
			   "b3":	ALL_VARS,}