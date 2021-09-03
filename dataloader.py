import uproot

import numpy as np
import pandas as pd

from config import *


def build_df(tree, variables):
	dataframe = pd.DataFrame()

	for name in variables:
		dataframe.loc[:, name] = np.array(tree[name].array())

	return dataframe


def region_selection(dataframe, region=None):
	if region == "zgamma":
		dataframe = dataframe[dataframe["nJets"] > 1]
		dataframe = dataframe[dataframe["nLeptons"] == 0]

	elif region == "signal":
		dataframe = dataframe[dataframe["nJets"] > 1]
		dataframe = dataframe[dataframe["nLeptons"] == 0]
		dataframe = dataframe[dataframe["mJJ"] > 300]
		dataframe = dataframe[dataframe["phCentrality"] < 0.6]

	return dataframe


def selection(dataframe, selections):
	for sel in selections:
		var, sign, val = sel

		if sign == "<":
			dataframe = dataframe[dataframe[var] < val]
		elif sign == ">":
			dataframe = dataframe[dataframe[var] > val]
		elif sign == "<=":
			dataframe = dataframe[dataframe[var] <= val]
		elif sign == ">=":
			dataframe = dataframe[dataframe[var] >= val]
		elif sign == "==":
			dataframe = dataframe[dataframe[var] == val]
		elif sign == "!=":
			dataframe = dataframe[dataframe[var] != val]

	return dataframe


def extract_TMVA_output(method, filename, variables):
	file 		= uproot.open(f"TMVA_outputs/{method}/{filename}.root")
	directory 	= file["models/dataloader"]

	variables = variables.copy()
	variables.extend(AUXILARY_VARIABLES)
	variables.extend(REGIONAL_VARIABLES)
	variables.append("classID")

	tree 		= directory["TrainTree"]
	TrainDF 	= build_df(tree, variables)

	tree 		= directory["TestTree"]
	TestDF 		= build_df(tree, variables)

	return TrainDF, TestDF


def extract(backgrounds, variables=DEFAULT_VARIABLES, selections=[], region=None):
	SFile = uproot.open("source/"+SFILENAME)
	STree = SFile[TREENAME]
	SDataframe = build_df(STree, variables)

	BDataframe = pd.DataFrame(columns=variables)

	for filename in backgrounds:
		BFile 	= uproot.open("source/"+filename)
		BTree 	= BFile[TREENAME]
		BDataframe = BDataframe.append(build_df(BTree, variables), ignore_index=True)

	SDataframe = region_selection(SDataframe, region)
	BDataframe = region_selection(BDataframe, region)

	SDataframe = selection(SDataframe, selections)
	BDataframe = selection(BDataframe, selections)

	SDataframe.loc[:,"classID"] = 0.0
	BDataframe.loc[:,"classID"] = 1.0
	dataframe = pd.concat((SDataframe, BDataframe), ignore_index=True).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

	return dataframe


def dataset_gen(region=None, backgrounds=None, dataframe=None, variables=DEFAULT_VARIABLES, selections=[]):
	if dataframe is None:
		dataframe = extract(backgrounds, variables, selections=selections, region=region)
	else:
		dataframe = dataframe.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

	SDataframe, BDataframe = dataframe[dataframe["classID"]==0], dataframe[dataframe["classID"]==1]

	STrainLen, BTrainLen = round(0.5*len(SDataframe)), round(0.5*len(BDataframe))

	STrainDF, STestDF = SDataframe.iloc[:STrainLen], SDataframe.iloc[STrainLen:]
	BTrainDF, BTestDF = BDataframe.iloc[:BTrainLen], BDataframe.iloc[BTrainLen:]

	TrainDF	= pd.concat((STrainDF, BTrainDF), ignore_index=True).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
	TestDF	= pd.concat((STestDF, BTestDF), ignore_index=True).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

	return TrainDF, TestDF