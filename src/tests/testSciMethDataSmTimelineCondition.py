# -*- coding: utf-8 -*-
#
#File: testSciMethDataSmTimelineCondition.py
#
"""
Created on Sun Apr  5 15:14:40 2020

Module ***testSciMethDataSmTimelineCondition***

Contains the tests for class :class:`scimeth.data.smTimelineCondition`

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

class testSciMethDataSmTimelineCondition(unittest.TestCase):
	'''A test suite for :class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
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
			theCondition = sm.data.smTimelineCondition()
			self.assertIsInstance(theCondition,sm.data.smTimelineCondition,\
			   'Test: Cannot construct object with default call to constructor.')
		except:
			self.assertTrue(False)


	def test_ObjectConstructionParameterizedCall(self):
		'''
		Tests object creation with parameterized call to constructor.
		'''
		#print("Setting attribute values from the constructor")
		theCondition = sm.data.smTimelineCondition(tag='A', description = 'Silly') 
		self.assertEqual(theCondition.tag, 'A')
		self.assertEqual(theCondition.description, 'Silly')
		theCondition = sm.data.smTimelineCondition(tag='B', description = 'Sillier') 
		self.assertEqual(theCondition.tag, 'B')
		self.assertEqual(theCondition.description, 'Sillier')

	def test_settingAttributeValues(self):
		'''
		Tests simple attribute setting.
		'''
		#print("Setting new attribute values one by one")
		theCondition = sm.data.smTimelineCondition()
		theCondition.id = 814
		theCondition.tag = 'C'
		try:
			theCondition.tag = 15
			self.assertTrue(False) #If the above succeded, this should crash
		except:
			self.assertTrue(True) #If the above failed, then behaviour is correct.
		theCondition.description = 'Setting attribute values'
		try:
			theCondition.description = 15
			self.assertTrue(False) #If the above succeded, this should crash
		except:
			self.assertTrue(True) #If the above failed, then behaviour is correct.
		self.assertEqual(theCondition.id, 814)
		self.assertEqual(theCondition.tag, 'C')
		self.assertEqual(theCondition.description, 'Setting attribute values')


	def test_methodIsEqual(self):
		'''
		Tests method :meth:`isEqual`.
		'''
		#print("Method isEqual")
		theCondition = sm.data.smTimelineCondition(tag='A', description = 'The description')
		self.assertNotEqual(theCondition, sm.data.smTimelineCondition())
		self.assertIsNot(theCondition, sm.data.smTimelineCondition())
		self.assertNotEqual(theCondition, \
			sm.data.smTimelineCondition(tag='A', description = 'The description'))
		self.assertIsNot(theCondition, \
			sm.data.smTimelineCondition(tag='A', description = 'The description'))
		tmp = sm.data.smTimelineCondition(tag='A', description = 'The description')
		self.assertFalse(theCondition.isEqual(tmp))
				#Note that id will be different despite same attribute values,
				#but they still share all other attributes equal
		self.assertTrue(theCondition.tag, tmp.tag)
		self.assertTrue(theCondition.description, tmp.description)
		#Finally, compare against a copy of itself (e.g. same value of id)
		tmp2 = theCondition #Note this makes a shallow copy
		self.assertIs(theCondition, tmp2)
		self.assertTrue(theCondition.isEqual(tmp2))
		tmp3 = copy.deepcopy(theCondition) #Now maks a deep copy
		self.assertIsNot(theCondition, tmp3)
		self.assertTrue(theCondition.isEqual(tmp3))


	def test_messWithNextID(self):
		'''
		Tests messing with private attribute nextID
		'''
		#print("Method toSeconds")
		#Departing from samples
		theObject = sm.data.smTimelineCondition()
		tmpNextID = theObject._smIdentifiable__nextID
		theObject.__nextID = -8 #This will create the a new attribute on the fly,
								#but it is NOT accesing the "real" __nextID
		self.assertNotEqual(theObject._smIdentifiable__nextID,theObject.__nextID)
		self.assertEqual(theObject._smIdentifiable__nextID,tmpNextID)
		



	@staticmethod
	def runTests():
		'''
		Class executable method
		'''
		print('TESTING smTimelineCondition')
		#The unittest is faster then the print above. Wait 1/2 sec to ensure messages are print "in order"
		time.sleep(0.5)
		t = unittest.TestLoader().loadTestsFromTestCase(testSciMethDataSmTimelineCondition)
		unittest.TextTestRunner(verbosity=2).run(t)
		#unittest.main(verbosity=2)

if __name__ == '__main__':
	print(' ')
	testSciMethDataSmTimelineCondition.runTests()