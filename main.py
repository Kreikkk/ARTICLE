from dataloader import extract, dataset_gen
from helpers import setup, split_result, get_significance, dump,\
					dump_via_path, clear_via_path, chisq_test, error, setup

from plotters import significance_plot, output_hist_plot
from config import *
from strategy_config import *

from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from time import time, sleep
from os import path, mkdir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import pickle
import ROOT as root


def reader(classifier, dataframe, variables):
	response = classifier.predict_proba(dataframe[variables].values)[:,0]
	dataframe.loc[:,"response"] = response

	SDataframe, BDataframe = dataframe[dataframe["classID"] == 0], dataframe[dataframe["classID"] == 1]

	return SDataframe, BDataframe


def main(strats, prefix=""):
	b1_flag = True

	for strat in strats:
		TrDF, TeDF = dataset_gen(backgrounds=BTRAINFILENAMES,
								 selections=SELECTIONS[strat]["zgm"])
		DF		   = extract(backgrounds=BTESTFILENAMES, 
			 				 selections=SELECTIONS[strat]["zgm"])

		print(f"\033[91m Strategy = {strat} \033[0m")

		train_variables = TR_VARS[strat]
		settings = SETTINGS[strat]

		if strat == "b3":
			for var in train_variables:
				if var in THIRD_JET_VARS:
					TrDF.loc[TrDF[var] == -1, var] = None
					TeDF.loc[TeDF[var] == -1, var] = None
					DF.loc[DF[var] == -1, var] = None

		train_data = np.array(TrDF[train_variables], dtype="float64")
		labels = np.array(TrDF["classID"], dtype="float64")


		classifier = LGBMClassifier(**settings, **GENERAL_SETTINGS)

		# classifier = XGBClassifier(**settings,
		# 						   use_label_encoder=False, 
		# 						   eval_metric="logloss",
		# 						   subsample=0.5,
		# 						   colsample_bytree=0.5,
		# 						   n_jobs=10,)

		classifier.fit(train_data, labels)

		STrainDataframe, BTrainDataframe 	= reader(classifier, TrDF, train_variables)
		STestDataframe, BTestDataframe 	 	= reader(classifier, TeDF, train_variables)
		SDataframe, BDataframe 			 	= reader(classifier, DF, train_variables)

		sig_max, sig_err, opt_cut, roc_area, \
		Ssum, Bsum, Serr, Berr, SNum, BNum = get_significance(SDataframe, BDataframe)

		SChi, BChi, SChi_over_ndof,\
		BChi_over_ndof, SPval, BPval = chisq_test(STestDataframe, BTestDataframe, STrainDataframe, BTrainDataframe)

		strat_info =  {"sig_max": sig_max,
						"sig_err": sig_err,
						"opt_cut": opt_cut,
						"roc_area": roc_area,
						"Ssum": Ssum,
						"Bsum": Bsum,
						"Serr": Serr,
						"Berr": Berr,
						"SNum": SNum,
						"BNum": BNum}
		strats_info[strat] = strat_info

		print("Sig =", sig_max, "+-", sig_err)
		print("AOC =", roc_area)

		print("SNum =", SNum)
		print("BNum =", BNum)
		print("S =", Ssum, "+-", Serr)
		print("B =", Bsum, "+-", Berr)

		print("S p-val =", SPval)
		print("B p-val =", BPval)

		print("SChi/ndof =", SChi_over_ndof)
		print("BChi/ndof =", BChi_over_ndof)

		if not path.exists("pictures"):
			mkdir("pictures")

		if CREATE_FIGS:
			output_hist_plot(STestDataframe, BTestDataframe,
							 STrainDataframe, BTrainDataframe, methodname="LGBM", uploadfile=f"{prefix}{strat}")
			# significance_plot(SDataframe, BDataframe, methodname="LGBM", uploadfile=f"{prefix}{strat}", ROC=False)

		if("b1_1" in strats_info.keys() and "b1_2" in strats_info.keys() and b1_flag):
			b1_flag = False
			print(f"\033[91m Strategy = b1 \033[0m")

			S1 = strats_info["b1_1"]["Ssum"]
			B1 = strats_info["b1_1"]["Bsum"]
			S2 = strats_info["b1_2"]["Ssum"]
			B2 = strats_info["b1_2"]["Bsum"]

			Serr1 = strats_info["b1_1"]["Serr"]
			Berr1 = strats_info["b1_1"]["Berr"]
			Serr2 = strats_info["b1_2"]["Serr"]
			Berr2 = strats_info["b1_2"]["Berr"]

			SNum1 = strats_info["b1_1"]["SNum"]
			BNum1 = strats_info["b1_1"]["BNum"]
			SNum2 = strats_info["b1_2"]["SNum"]
			BNum2 = strats_info["b1_2"]["BNum"]

			sig, sig_err = split_result(S1, B1, S2, B2, Serr1, Berr1, Serr2, Berr2)

			print("Sig =", sig, "+-", sig_err)
			print("AOC = -")

			print("SNum =", SNum1 + SNum2)
			print("BNum =", BNum1 + BNum2)
			print("S =", S1 + S2, "+-", (Serr1**2 + Serr2**2)**0.5)
			print("B =", B1 + B2, "+-", (Berr1**2 + Berr2**2)**0.5)

			print("S p-val = -")
			print("B p-val = -")

			print("SChi/ndof = -")
			print("BChi/ndof = -")

			strat_info =  {"sig_max": sig,
						   "sig_err": sig_err,
						   "opt_cut": "-",
						   "roc_area": "-",
						   "Ssum": S1 + S2,
						   "Bsum": B1 + B2,
						   "Serr": (Serr1**2 + Serr2**2)**0.5,
						   "Berr": (Berr1**2 + Berr2**2)**0.5,
						   "SNum": SNum1 + SNum2,
						   "BNum": BNum1 + BNum2}
			strats_info["b1"] = strat_info

def print_stats():
	sel = [("nJets", ">", 1), ("nJets", "==", 2), ("nJets", ">", 2)]
	cutnames = ("N > 1", "N = 2", "N > 2")
	for selection, cutname in zip(sel, cutnames):
		print(f"\033[91m Cut: {cutname} \033[0m")
		DF = extract(backgrounds=BTESTFILENAMES, 
				 	 selections=[*SELECTIONS_SIG, selection])

		sig = DF[DF["classID"] == 0]["weightModified"].sum() / (DF[DF["classID"] == 0]["weightModified"].sum() + DF[DF["classID"] == 1]["weightModified"].sum())**0.5
		sig_err = error(DF[DF["classID"] == 0]["weightModified"], DF[DF["classID"] == 1]["weightModified"])

		print("Sig =", sig, "+-", sig_err)
		print("AOC = -")

		print("SNum =", len(DF[DF["classID"] == 0]))
		print("BNum =", len(DF[DF["classID"] == 1]))
		print("S =", DF[DF["classID"] == 0]["weightModified"].sum(), "+-", (DF[DF["classID"] == 0]["weightModified"]**2).sum()**0.5)
		print("B =", DF[DF["classID"] == 1]["weightModified"].sum(), "+-", (DF[DF["classID"] == 1]["weightModified"]**2).sum()**0.5)

		print("S p-val = -")
		print("B p-val = -")

		print("SChi/ndof = -")
		print("BChi/ndof = -")

		strat_info =  {"sig_max": sig,
						"sig_err": sig_err,
						"opt_cut": "-",
						"roc_area": "-",
						"Ssum": DF[DF["classID"] == 0]["weightModified"].sum(),
						"Bsum": DF[DF["classID"] == 1]["weightModified"].sum(),
						"Serr": (DF[DF["classID"] == 0]["weightModified"]**2).sum()**0.5,
						"Berr": (DF[DF["classID"] == 1]["weightModified"]**2).sum()**0.5,
						"SNum": len(DF[DF["classID"] == 0]),
						"BNum": len(DF[DF["classID"] == 1])}
		strats_info[cutname] = strat_info


def dump_latex(data, key_order):
	from table_template import YieldTemplate
	table = YieldTemplate()

	for key in key_order:
		info = data[key]
		table.add_line([info["SNum"], info["BNum"], info["Ssum"], info["Serr"], info["Bsum"], info["Berr"],
						info["sig_max"], info["sig_err"], info["roc_area"]])



if __name__ == "__main__":
	root.gErrorIgnoreLevel = root.kWarning
	strats_info = {}

	if CREATE_FIGS:
		setup()


	strats = ("b0", "b1_1", "b1_2", "b2", "b3",)
	print_stats()
	main(strats=strats, prefix="model_")

	dump_latex(strats_info, ["N > 1", "N = 2", "N > 2", "b0", "b1_1", "b1_2", "b1", "b2", "b3"])
