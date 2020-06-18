# Test.py
#import os
import sys

#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#from matplotlib.figure import Figure
##from matplotlib.backend_bases import KeyEvent, MouseEvent
#from skimage import io

#import copy #Permits deep copying objects

import scimeth as sm
#Add paths
#if not sys.path[0] == './test':
#	sys.path.insert(0, './test')

#import app as ocapp
#from app import *

#import testSciMethDataSmMeasurementUnit as testSciMethDataSmMeasurementUnit
import tests as myTests


##MAIN
def main():
	print(' ')
	print('=================================================================')
	myTests.testSciMethDataSmMeasurementUnit.runTests()
	print(' ')
	print('=================================================================')
	myTests.testSciMethDataSmTimelineEvent.runTests()
	print(' ')
	print('=================================================================')
	myTests.testSciMethDataSmTimelineCondition.runTests()
	print(' ')
	print('=================================================================')
	myTests.testSciMethDataSmTimeline.runTests()
	print(' ')


	

if __name__ == "__main__":
	main()
	print("Done.")
	

	
