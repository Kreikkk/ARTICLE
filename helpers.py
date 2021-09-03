import numpy as np
import ROOT as root
import atlasplots as aplt


def normalized_hist_to_array(hist, nbins, include_error=True):
	arr = []
	if include_error:
		for index in range(1, nbins+1):
			arr.append(hist.GetBinContent(index) + hist.GetBinErrorUp(index))
	else:
		for index in range(1, nbins+1):
			arr.append(hist.GetBinContent(index))

	sum_of_weights = hist.GetSumOfWeights()

	return np.array(arr)/sum_of_weights


def get_hist_max(hist, nbins, include_error=True):
	arr = normalized_hist_to_array(hist, nbins, include_error)
	return np.max(arr)


def error(signal_events, bg_events):
	S = np.sum(signal_events)
	B = np.sum(bg_events)

	SErr = np.sum(signal_events**2)**0.5
	BErr = np.sum(bg_events**2)**0.5

	SPart = (S + B)**(-0.5) - 0.5*S*((S + B)**(-1.5))
	BPart = -0.5*S*((S + B)**(-1.5))

	return ((SPart*SErr)**2 + (BPart*BErr)**2)**0.5


def get_contour_ys(hist, nbins):
	ylow, yup = [], []
	for index in range(1, nbins+1):
		val = hist.GetBinContent(index)
		err = hist.GetBinError(index)
		try:
			ylow.append(1 - err/val)
			yup.append(1 + err/val)
		except ZeroDivisionError:
			ylow.append(1 - 1)
			yup.append(1 + 1)

	return ylow, yup


def setup(fontsize=27):
	root.TMVA.Tools.Instance()
	aplt.set_atlas_style(fontsize)
	root.gStyle.SetErrorX(0.5)
	root.gStyle.SetEndErrorSize(0.1)


def chisq(hist_true, hist_exp, tp):
	chisq = hist_true.Chi2Test(hist_exp, option="WW CHI2")
	p_val = hist_true.Chi2Test(hist_exp, option="WW")
	chisq_over_ndof = hist_true.Chi2Test(hist_exp, option="WW CHI2/NDF")

	return chisq, chisq_over_ndof, p_val


def viewer(filename):
	root.TMVA.Tools.Instance()
	root.TMVA.TMVAGui(f"{filename}.root")
	root.gApplication.Run()


def dump(methodname, uploadfile, data):
	with open(f"results/data/{methodname}/{uploadfile}.txt", "a") as file:
		file.write(data)

def dump_via_path(filepath, data):
	with open(filepath, "a") as file:
		file.write(data)

def clear(methodname, uploadfile):
	with open(f"results/data/{methodname}/{uploadfile}.txt", "w") as _:
		pass

def clear_via_path(filepath):
	with open(filepath, "w") as _:
		pass


def get_min_max_response_value(dataframes):
	minimums, maximums = [], []
	for dataframe in dataframes:
		minimum = dataframe["response"].min()
		maximum = dataframe["response"].max()

		minimums.append(minimum)
		maximums.append(maximum)

	return min(minimums), max(maximums)


def split_result(S1, B1, S2, B2, Serr1, Berr1, Serr2, Berr2):
	err2 = 0.5*(S1+S2)/(S1+B1+S2+B2)**1.5
	err1 = 1/(S1+B1+S2+B2)**0.5 - err2

	delta_sigma = ((Serr1**2+Serr2)*err1**2 + (Berr1**2+Berr2)*err2**2)**0.5

	sigma = (S1+S2)/(S1+S2+B1+B2)**0.5

	return sigma, delta_sigma


def get_significance(SDataframe, BDataframe, ndots=1000):
	Min = np.max((np.min(SDataframe["response"]), np.min(BDataframe["response"])))
	Max = np.min((np.max(SDataframe["response"]), np.max(BDataframe["response"])))
	SWSum = np.sum(SDataframe["weightModified"])
	BWSum = np.sum(BDataframe["weightModified"])

	XData = np.linspace(Min, Max, ndots)
	SData, BData = np.array([]), np.array([])
	for cursor in XData:
		S = np.sum(SDataframe[SDataframe["response"] >= cursor]["weightModified"])
		B = np.sum(BDataframe[BDataframe["response"] >= cursor]["weightModified"])
		SData = np.append(SData, S)
		BData = np.append(BData, B)

	YData = SData/np.sqrt(SData+BData)
	SEff = SData/SWSum
	BRej = 1 - BData/BWSum

	area = 0
	for index, xval in enumerate(SEff[:-1]):
		delta = SEff[index+1] - xval
		area -= delta*BRej[index]

	peak_index = YData.argmax()
	sig_max = YData[peak_index]
	cut = XData[peak_index]

	SWCut = np.array(SDataframe[SDataframe["response"] > cut]["weightModified"])
	BWCut = np.array(BDataframe[BDataframe["response"] > cut]["weightModified"])

	err = error(SWCut, BWCut)

	Serr = ((SWCut**2).sum())**0.5
	Berr = ((BWCut**2).sum())**0.5

	Ssum = SWCut.sum()
	Bsum = BWCut.sum()

	SNum = len(SWCut)
	BNum = len(BWCut)

	return sig_max, err, cut, area, Ssum, Bsum, Serr, Berr, SNum, BNum


def chisq_test(STestDataframe, BTestDataframe,
			   STrainDataframe, BTrainDataframe):

	NBins = 20

	left, right = get_min_max_response_value((STestDataframe, BTestDataframe, STrainDataframe, BTrainDataframe))

	STestHist = root.TH1F("", "", NBins, left, right)
	BTestHist = root.TH1F("", "", NBins, left, right)
	STrainHist = root.TH1F("", "", NBins, left, right)
	BTrainHist = root.TH1F ("", "", NBins, left, right)


	for out, weight in zip(STestDataframe["response"], STestDataframe["weightModified"]):
		STestHist.Fill(out, weight)
	for out, weight in zip(BTestDataframe["response"], BTestDataframe["weightModified"]):
		BTestHist.Fill(out, weight)

	for out, weight in zip(STrainDataframe["response"], STrainDataframe["weightModified"]):
		STrainHist.Fill(out, weight)
	for out, weight in zip(BTrainDataframe["response"], BTrainDataframe["weightModified"]):
		BTrainHist.Fill(out, weight)

	SChi, SChi_over_ndof, SPval = chisq(STrainHist, STestHist, "signal")
	BChi, BChi_over_ndof, BPval = chisq(BTrainHist, BTestHist, "background")

	return SChi, BChi, SChi_over_ndof, BChi_over_ndof, SPval, BPval

	# dump(methodname, uploadfile, f"SChi:{round(SChi, 3)}\n")
	# dump(methodname, uploadfile, f"BChi:{round(BChi, 3)}\n")
	# dump(methodname, uploadfile, f"SChi_over_ndof:{round(SChi_over_ndof, 3)}\n")
	# dump(methodname, uploadfile, f"BChi_over_ndof:{round(BChi_over_ndof, 3)}\n")
	# dump(methodname, uploadfile, f"SPval:{round(SPval, 3)}\n")
	# dump(methodname, uploadfile, f"BPval:{round(BPval, 3)}\n")


