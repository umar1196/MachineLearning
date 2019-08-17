from sklearn import preprocessing
from sklearn.model_selection import train_test_split 
import pandas
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def gene_prediction(input_file): # similarty matrix 

	input_file = input_file

	#data reading
	df = pandas.read_excel(input_file)

	#data prep
	le = preprocessing.LabelEncoder()
	df['Class'] = le.fit_transform(df['Class'])
	#print(df.head())
	sourcevars = df.iloc[: , 1:-1]
	#print(targetvars)
	targetvars = df.iloc[: ,-1]
	#print(sourcevars)

	linreg = LinearRegression()
	linreg.fit(sourcevars , targetvars)
	target_pred = linreg.predict(sourcevars)
	print(metrics.accuracy_score(targetvars , target_pred.round() , normalize = False))

	sourcevars_train, sourcevars_test, targetvars_train, targetvars_test = train_test_split(sourcevars , targetvars , test_size = 0.4 , random_state = 4)
	#print(sourcevars_train.shape , sourcevars_test.shape)
	linreg.fit(sourcevars_train , targetvars_train)
	targetvars_pred = linreg.predict(sourcevars_test)
	print("accuracy score " , metrics.accuracy_score(targetvars_test , targetvars_pred.round() , normalize = False))
	print("confusion matrix\n" , metrics.confusion_matrix(targetvars_test , targetvars_pred.round()))#form confusion matrix
	print(metrics.classification_report(targetvars_test , targetvars_pred.round()))
	

	#applying randomforest algorithm
	clf = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0)
	clf.fit(sourcevars_train , targetvars_train)
	target_pred = clf.predict(sourcevars)
	print("accuracy score " , metrics.accuracy_score(targetvars_test , targetvars_pred.round() , normalize = False))

#function calling
infile = 'similarity_matrix.xlsx'
gene_pred = gene_prediction(infile)	


