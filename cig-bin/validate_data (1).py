from PyQt6 import QtWidgets, QtCore
import pandas as pd
import re
import sys
import threading
def ex1(new_df,valid_charcters,file):
	for index,row in new_df.iterrows():
		index+=1
		for column in new_df.columns:
			for char in row[column]:
				if char not in valid_charcters:
					file.write(f"row number {index} at column {column} has invalid charcter {char} \n")
def ex2(df,spanish_french,file):
	df = df.iloc[:,10:]
	for index,row in df.iterrows():
		index+=1
		for column in df.columns:
			for char in row[column]:
				if char not in spanish_french:
					file.write(f"row number {index} at column {column} has invalid charcter {char} \n")
def ex3(df,list_of_hashtag_values,list_of_greater_than_less_than_values,file):
	for index,row in df.iterrows():
		index+=1
		for column in df.columns:
			temp_output = use_regex(row[column])
			for value in temp_output['#']:
				if value not in list_of_hashtag_values :
					file.write(f"row number {index} at column {column} has invalid charcter #{value}# \n")

			for value in temp_output['<>']:
				if value not in list_of_greater_than_less_than_values :
					file.write(f"row number {index} at column {column} has invalid charcter <{value}> \n")
def use_regex(input_text):

		dict_of_output = {}
		dict_of_output['<>']=re.findall(r'\<(.*?)\>',input_text)
		dict_of_output['#']=re.findall(r'\#(.*?)\#',input_text)
		return   dict_of_output

def main(input_file,output):
	df = pd.read_excel(input_file)
	valid_charcters = [str(x.strip(' ').strip('\n').strip('Â')) for x in open('allowed.txt', encoding="utf8").readlines()]
	spanish_french = [str(x.strip(' ').strip('\n').strip('Â')) for x in open('spanish_french.txt', encoding="utf8").readlines()]
	valid_charcters.append(' ')
	spanish_french.append(' ')
	list_of_greater_than_less_than_values=['bi','/bi']
	list_of_hashtag_values=['f','o','s1','s2']
	with open(str(output)+"/errors.txt" ,"w") as file:
		for column in df.columns:
			df[column]= df[column].astype(str)
		new_df = df.iloc[:,:10]
		t1=threading.Thread(target=ex1,args=(new_df,valid_charcters,file,))
		t2=threading.Thread(target=ex2,args=(df,spanish_french,file,))
		t3=threading.Thread(target=ex3,args=(df,list_of_hashtag_values,list_of_greater_than_less_than_values,file,))
		t1.start()
		t2.start()
		t3.start()
		t1.join()
		t2.join()
		t3.join()
## GUI CODE
class Window(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.listener = True
		self.init_ui()

	def init_ui(self) -> None:
		"""Init the UI of the obect.
		"""
		self.setWindowTitle("App")
		self.setFixedSize(QtCore.QSize(600, 200))

		central_widget = QtWidgets.QWidget()
		main_layout = QtWidgets.QGridLayout()
		central_widget.setLayout(main_layout)
		self.setCentralWidget(central_widget)

		self.input_field = QtWidgets.QLineEdit()
		input_button = QtWidgets.QPushButton("Input file")
		input_button.clicked.connect(self.get_input)

		self.output_field = QtWidgets.QLineEdit()
		output_button = QtWidgets.QPushButton("Output folder")
		output_button.clicked.connect(self.get_output)

		submit_button = QtWidgets.QPushButton("Submit")
		submit_button.clicked.connect(self.submit)

		main_layout.addWidget(self.input_field, 0, 0, 1, 1)
		main_layout.addWidget(input_button, 0, 1, 1, 1)
		main_layout.addWidget(self.output_field, 1, 0, 1, 1)
		main_layout.addWidget(output_button, 1, 1, 1, 1)
		main_layout.addWidget(submit_button, 2, 0, 1, 2)

		self.show()

	def get_input(self):
		"""get the input file path
		"""
		dialog = QtWidgets.QFileDialog(self)
		name, _ = dialog.getOpenFileName(
			self, "Choose an input file", filter="(*.xls *.xlsx)")

		self.input_field.setText(name)

	def get_output(self):
		"""Get the output folder path
		"""
		dialog = QtWidgets.QFileDialog(self)
		name = dialog.getExistingDirectory(
			self, "Choose an output folder")

		self.output_field.setText(name)

	def submit(self) -> tuple[str]:
		"""Submit both path

		Returns:
			tuple[str]: The input path and output path
		"""
		input_path = self.input_field.text()
		output_path = self.output_field.text()

		if input_path == "" or output_path == "":
			return

		main(input_path,output_path)


if __name__ == "__main__":

	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec())
