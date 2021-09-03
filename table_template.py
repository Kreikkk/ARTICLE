class YieldTemplate():
	head = ["\\begin{table}[ht]",
    		"\\centering",
    		"\\begin{tabular}{|c|c|c|c|c|c|c|}",
    		"\\hline",
			"&".join(["", "Вхожд.", "Вхожд.", "Кол-во", "Кол-во", "\\multirow{2}{*}{$\\sigma_{\\text{max}}$}", "\\multirow{2}{*}{AUC}"]) + "\\\\",
			"&".join(["", "сигнал", "фон", "сигнала", "фона", "", ""]) + "\\\\",
			"\\hline"]

	def __init__(self, filename="table"):
		self.filename = filename
		file = open(f"{self.filename}.txt", "w")
		for line in self.head:
			file.write(line + "\n")

		self.row_gen = self.get_row()
		file.close()

	def add_line(self, content):
		file = open(f"{self.filename}.txt", "a")
		row = next(self.row_gen)
		if row == "$B_{0}$":
			file.write("\\hline" + "\n")
			file.write("\\multicolumn{7}{|c|}{LightGBM}" + "\\\\" + "\n")
			file.write("\\hline" + "\n")

		SNum, BNum, S, Serr, B, Berr, sig, sig_err, auc = content

		S = round(S, 1)
		B = round(B, 1)
		Serr = round(Serr, 1)
		Berr = round(Berr, 1)


		if isinstance(sig, float):
			sig = round(sig, 2)
		if isinstance(sig_err, float):
			sig_err = round(sig_err, 2)
		if isinstance(auc, float):
			auc = round(auc, 3)

		line = "&".join([row, str(SNum), str(BNum), f"${S}\\pm{Serr}$", f"${B}\\pm{Berr}$",
													f"${sig}\\pm{sig_err}$", str(auc)]) + "\\"

		file.write(line + "\\" + "\n")
		file.write("\\hline" + "\n")

		if row == "$B_{3}$":
			file.write("\\end{tabular}" + "\n")
			file.write("\\end{table}" + "\n")
		file.close()

	def get_row(self):
		rows = ["До отборов", "До отборов", "До отборов", "$B_{0}$", 
				"$B_{1}^{\\text{N}_{\\text{jets}}=2}$",
				"$B_{1}^{\\text{N}_{\\text{jets}}>2}$",
				"$B_{1}$", "$B_{2}$", "$B_{3}$"]
		for row in rows:
			yield row

