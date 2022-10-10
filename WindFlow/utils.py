import numpy as np
import math

def toCircular(df, wd):

    df['sin']=np.sin(df[wd]/360*2*math.pi)

    df['cos']=np.cos(df[wd]/360*2*math.pi)

    print("toCircular columns created")

def convertToDegrees(sin_prediction,cos_prediction):
	'''
	Converting sine and cosine back to its circular angle depends on finding which of the the 4 circular quadrants the
	prediction will fall into. If sin and cos are both GT 0, degrees will fall in 0-90.  If sin>0 cos<0, degrees will fall into 90-180, etc.
	'''
	inverseSin=np.degrees(np.arcsin(sin_prediction))
	inverseCos=np.degrees(np.arccos(cos_prediction))
	radians_sin=[]
	radians_cos=[]
	for a,b,c,d in zip(sin_prediction, cos_prediction, inverseSin, inverseCos):
		if(a>0 and b>0):
			radians_sin.append(c)
			radians_cos.append(d)
		elif(a>0 and b<0):
			radians_sin.append(180-c)
			radians_cos.append(d)
		elif(a<0 and b<0):
			radians_sin.append(180-c)
			radians_cos.append(360-d)
		elif(a<0 and b>0):
			radians_sin.append(360+c)
			radians_cos.append(360-d)
	radians_sin=np.array(radians_sin)
	radians_cos=np.array(radians_cos)
	return radians_sin, radians_cos


from sklearn.svm import SVR

def train_predict(train_test_data, c_,g_, cos=False):
	i=0
	x = []
	y = []
	while i <total:
		if(cos):

			x.append(train_test_data.cos.values[i:recordsBack+i])
			y.append(train_test_data.cos.values[recordsBack+i])
		else:
			x.append(train_test_data.sin.values[i:recordsBack+i])
			y.append(train_test_data.sin.values[recordsBack+i])
		i+=1

	svr_rbf = SVR(kernel='rbf', C=c_ ,gamma=g_)
	y_rbf = svr_rbf.fit(x[:trainSet], y[:trainSet]).predict(x)
	y_rbf[y_rbf > 1] = 1
	y_rbf[y_rbf < -1] = -1
	mae = mean_absolute_error(y[trainSet:], y_rbf[trainSet:])
	mse = mean_squared_error(y[trainSet:], y_rbf[trainSet:])
	rmse = sqrt(mse)

	return y_rbf[trainSet:], rmse
