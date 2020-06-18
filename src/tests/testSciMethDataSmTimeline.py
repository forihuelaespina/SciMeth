# -*- coding: utf-8 -*-
#
#File: testSciMethDataSmTimeline.py
#
"""
Created on Sun Apr  5 19:44:27 2020

@author: felip
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:14:40 2020

Module ***testSciMethDataSmTimeline***

Contains the tests for class :class:`scimeth.data.smTimeline`

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
|  4-Apr-2020 | FOE    | - Test module created                                |
|             |        | - Added tests:                                       |
|             |        |                                                      |
|             |        | * `test_ObjectConstructionDefaultCall`               |
|             |        | * `test_ObjectConstructionParameterizedCall`         |
|             |        | * `test_settingAttributeValues`                      |
|             |        | * `test_methodIsEqual`                               |
|             |        | * `test_messWithNextID`                              |
|             |        |                                                      |
+-------------+--------+------------------------------------------------------+
| 17-Apr-2020 | FOE    | - Added tests:                                       |
|             |        |                                                      |
|             |        | * `test_methodAddConditions`                         |
+-------------+--------+------------------------------------------------------+



.. seealso:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

import sys
import time
import unittest
import copy

#Add paths
if not sys.path[0] == '..':
	sys.path.insert(0, '..')

import scimeth as sm

class testSciMethDataSmTimeline(unittest.TestCase):
	'''A test suite for :class:`smTimeline <scimeth.data.smTimeline>`
	'''
	
	##############################################
	##
	## WATCH OUT! I need to keep track of the id,
	## but since tests are run in parallel, there is no
	## guarantee of the order in which instructions
	## between methods will be executed.
	## Trying to circumvent
	## this, I'm actually making comparisons of id
	## "relative" to others win the same method, but
	## even this is difficult as other methods may
	## call the constructor between two calls within
	## a single test.
	##
	##############################################
	
	
	def test_ObjectConstructionDefaultCall(self):
		'''
		Tests object creation with a default call to constructor.
		'''
		#print('Testing test_defaultConstructorCall')
		try:
			theObject = sm.data.smTimeline()
			self.assertIsInstance(theObject,sm.data.smTimeline,\
			   'Test: Cannot construct object with default call to constructor.')
		except:
			self.assertTrue(False)


	def test_ObjectConstructionParameterizedCall(self):
		'''
		Tests object creation with parameterized call to constructor.
		'''
		#print("Setting attribute values from the constructor")
		theObject = sm.data.smTimeline(length = 14) 
		self.assertEqual(len(theObject.timestamps), 14)
		self.assertEqual(theObject.end, 13)
		tmpEnd = 30 #Seconds
		tmpSamplingRate = 10 #Hz
		theObject = sm.data.smTimeline(unit='Second', end = 30, samplingRate = 10) 
		self.assertEqual(len(theObject.timestamps), 1 + tmpEnd * tmpSamplingRate)
		self.assertEqual(theObject.length, 1 + tmpEnd * tmpSamplingRate)

# 	def test_settingAttributeValues(self):
# 		'''
# 		Tests simple attribute setting.
# 		'''
# 		#print("Setting new attribute values one by one")
# 		theObject = sm.data.smTimeline()
# 		theObject.id = 814
# 		theObject.tag = 'C'
# 		theObject.tag = 15 #This issues a warning, but otherwise it will be ignored.
# 		theObject.description = 'Setting attribute values'
# 		theObject.description = 15 #This issues a warning, but otherwise it will be ignored.
# 		self.assertEqual(theObject.id, 814)
# 		self.assertEqual(theObject.tag, 'C')
# 		self.assertEqual(theObject.description, 'Setting attribute values')


# 	def test_methodIsEqual(self):
# 		'''
# 		Tests method :meth:`isEqual`.
# 		'''
# 		#print("Method isEqual")
# 		theCondition = sm.data.smTimelineCondition(tag='A', description = 'The description')
# 		self.assertNotEqual(theCondition, sm.data.smTimelineCondition())
# 		self.assertIsNot(theCondition, sm.data.smTimelineCondition())
# 		self.assertNotEqual(theCondition, \
# 			sm.data.smTimelineCondition(tag='A', description = 'The description'))
# 		self.assertIsNot(theCondition, \
# 			sm.data.smTimelineCondition(tag='A', description = 'The description'))
# 		tmp = sm.data.smTimelineCondition(tag='A', description = 'The description')
# 		self.assertFalse(theCondition.isEqual(tmp))
# 				#Note that id will be different despite same attribute values,
# 				#but they still share all other attributes equal
# 		self.assertTrue(theCondition.tag, tmp.tag)
# 		self.assertTrue(theCondition.description, tmp.description)
# 		#Finally, compare against a copy of itself (e.g. same value of id)
# 		tmp2 = theCondition #Note this makes a shallow copy
# 		self.assertIs(theCondition, tmp2)
# 		self.assertTrue(theCondition.isEqual(tmp2))
# 		tmp3 = copy.deepcopy(theCondition) #Now maks a deep copy
# 		self.assertIsNot(theCondition, tmp3)
# 		self.assertTrue(theCondition.isEqual(tmp3))


	def test_messWithNextID(self):
		'''
		Tests messing with private attribute nextID
		'''
		#print("Method toSeconds")
		#Departing from samples
		theObject = sm.data.smTimeline()
		tmpNextID = theObject._smIdentifiable__nextID
		theObject.__nextID = -8 #This will create the a new attribute on the fly,
								#but it is NOT accesing the "real" __nextID
		self.assertNotEqual(theObject._smIdentifiable__nextID,theObject.__nextID)
		self.assertEqual(theObject._smIdentifiable__nextID,tmpNextID)
		


	def test_methodAddConditions(self):
		'''
		Tests method :meth:`addConditions`.
		'''
		#print("Method addConditions")
		#Departing from samples
		t = sm.data.smTimeline()
		condA = sm.data.smTimelineCondition(tag='condA')
		condB = sm.data.smTimelineCondition(tag='condB')
		t.addConditions([condA,condB]) #Added as list.
					#This should add the two conditions.
		t.addConditions({condA,condB}) #Added as set.
					#This should NOT add the two conditions becuase they
					#are repeated. It should raise a warning.
		t.addConditions(sm.data.smTimelineCondition(tag='condC'))
					#This should work. Internally it would wrap the condition
					#into a set before adding it.
		t.addConditions({sm.data.smTimelineCondition(tag='condC')})
					#This should add a new condition tagged C but with a
					#different id!!!
		self.assertTrue(len(t.conditions)==4)
		



	@staticmethod
	def runTests():
		'''
		Class executable method
		'''
		print('TESTING smTimeline')
		#The unittest is faster then the print above. Wait 1/2 sec to ensure messages are print "in order"
		time.sleep(0.5)
		t = unittest.TestLoader().loadTestsFromTestCase(testSciMethDataSmTimeline)
		unittest.TextTestRunner(verbosity=2).run(t)
		#unittest.main(verbosity=2)

if __name__ == '__main__':
	print(' ')
	testSciMethDataSmTimeline.runTests()