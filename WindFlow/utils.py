import numpy as np
import math

def toCircular(df, wd):

    df['sin']=np.sin(df[wd]/360*2*math.pi)

    df['cos']=np.cos(df[wd]/360*2*math.pi)

    print("toCircular columns created")

def convertToDegrees(Wd_x,Wd_y):
	'''
	Converting sine and cosine back to its circular angle depends on finding which of the the 4 circular quadrants the
	prediction will fall into. If sin and cos are both GT 0, degrees will fall in 0-90.  If sin>0 cos<0, degrees will fall into 90-180, etc.
	'''
	#quadrant1
	if Wd_x > 0 and Wd_y > 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi
	#quadrant2
	if Wd_x < 0 and Wd_y > 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi + 180
	#quadrant3
	if Wd_x < 0 and Wd_y < 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi + 180
	#quadrant4
	if Wd_x > 0 and Wd_y < 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi + 360

def v_total(wd_x,wd_y):
  return np.sqrt(wd_x**2 + wd_y**2)
