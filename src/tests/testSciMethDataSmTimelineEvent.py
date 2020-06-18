# -*- coding: utf-8 -*-
#
#File: testSciMethDataSmTimelineEvent.py
#
"""
Created on Sun Apr  5 13:08:24 2020

Module ***testSciMethDataSmTimelineEvent***

Contains the tests for class :class:`scimeth.data.smTimelineEvent`

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
|             |        | * `test_methodToSamples`                             |
|             |        | * `test_methodToSeconds`                             |
|             |        | * `test_messWithNextID`                              |
|             |        |                                                      |
+-------------+--------+------------------------------------------------------+
| 13-Apr-2020 | FOE    | - Added tests:                                       |
|             |        |                                                      |
|             |        | * `test_methodHasOverlap`                            |
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

class testSciMethDataSmTimelineEvent(unittest.TestCase):
	'''A test suite for :class:`smTimelineEvent <scimeth.data.smTimelineEvent>`
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
			theEvent = sm.data.smTimelineEvent()
			self.assertIsInstance(theEvent,sm.data.smTimelineEvent,\
			   'Test: Cannot construct object with default call to constructor.')
		except:
			self.assertTrue(False)


	def test_ObjectConstructionParameterizedCall(self):
		'''
		Tests object creation with parameterized call to constructor.
		'''
		#print("Setting attribute values from the constructor")
		theEvent = sm.data.smTimelineEvent(unit='Sample') 
		#self.assertEqual(theEvent.id, 2)
		self.assertEqual(theEvent.onset, 0)
		self.assertEqual(theEvent.duration, 0)
		self.assertTrue(theEvent.unit.isEqual( \
						   sm.data.smMeasurementUnit(name='Sample',acronym='samples',multiplier=0,isInternationalSystem=False)))
		self.assertEqual(theEvent.info, None)
		theEvent = sm.data.smTimelineEvent(unit='Second')
		#self.assertEqual(theEvent.id, 3)
		self.assertEqual(theEvent.onset, 0)
		self.assertEqual(theEvent.duration, 0)
		self.assertTrue(theEvent.unit.isEqual( \
						   sm.data.smMeasurementUnit(name='Second',acronym='s',multiplier=0,isInternationalSystem=True)))
		self.assertEqual(theEvent.info, None)

	def test_settingAttributeValues(self):
		'''
		Tests simple attribute setting.
		'''
		#print("Setting new attribute values one by one")
		theEvent = sm.data.smTimelineEvent()
		theEvent.id = 814
		theEvent.onset = 15
		theEvent.duration = 12.4 #Wrong, because default is Samples
		theEvent.info = 'Holita, Homer'
		self.assertEqual(theEvent.id, 814)
		self.assertEqual(theEvent.onset, 15)
		self.assertEqual(theEvent.duration, 12) #Note the rounding!
		self.assertEqual(theEvent.info, 'Holita, Homer')


	def test_methodIsEqual(self):
		'''
		Tests method :meth:`isEqual`.
		'''
		#print("Method isEqual")
		theEvent = sm.data.smTimelineEvent(onset=10, duration=5, info = 'The info')
		self.assertNotEqual(theEvent, sm.data.smTimelineEvent())
		self.assertIsNot(theEvent, sm.data.smTimelineEvent())
		self.assertNotEqual(theEvent, \
			sm.data.smTimelineEvent(unit = 'Second', onset=10, duration=5, info = 'The info'))
		self.assertIsNot(theEvent, \
			sm.data.smTimelineEvent(unit = 'Second', onset=10, duration=5, info = 'The info'))
		tmp = sm.data.smTimelineEvent(unit = 'Sample', onset=10, duration=5, info = 'The info')
		self.assertFalse(theEvent.isEqual(tmp))
				#Note that id will be different despite same attribute values,
				#but they still share all other attributes equal
		self.assertTrue(theEvent.onset, tmp.onset)
		self.assertTrue(theEvent.duration, tmp.duration)
		self.assertTrue(theEvent.end, tmp.end)
		self.assertTrue(theEvent.unit.isEqual(tmp.unit))
		self.assertTrue(theEvent.info, tmp.info)
		#Finally, compare against a copy of itself (e.g. same value of id)
		tmp2 = theEvent #Note this makes a shallow copy
		self.assertIs(theEvent, tmp2)
		self.assertTrue(theEvent.isEqual(tmp2))
		tmp3 = copy.deepcopy(theEvent) #Now maks a deep copy
		self.assertIsNot(theEvent, tmp3)
		self.assertTrue(theEvent.isEqual(tmp3))

	def test_methodToSamples(self):
		'''
		Tests method :meth:`toSamples`.
		'''
		#print("Method toSamples")
		#Departing from samples
		theEvent = sm.data.smTimelineEvent(onset =3, duration = 5)
		self.assertTrue(theEvent.isInSamples())
		theEvent.toSamples(samplingRate = 1)
		self.assertTrue(theEvent.isInSamples())
		#Departing from seconds
		theEvent = sm.data.smTimelineEvent(unit='Second', onset = 4.5, duration = 4.3)
		self.assertTrue(theEvent.isInSeconds())
		theEvent.toSamples(samplingRate = 1)
		self.assertTrue(theEvent.isInSamples())
		


	def test_methodToSeconds(self):
		'''
		Tests method :meth:`toSeconds`.
		'''
		#print("Method toSeconds")
		#Departing from samples
		theEvent = sm.data.smTimelineEvent(onset =3, duration = 5)
		self.assertTrue(theEvent.isInSamples())
		theEvent.toSeconds()
		self.assertTrue(theEvent.isInSeconds())
		#Departing from seconds
		theEvent = sm.data.smTimelineEvent(unit='Second', onset = 4.5, duration = 4.3)
		self.assertTrue(theEvent.isInSeconds())
		theEvent.toSeconds()
		self.assertTrue(theEvent.isInSeconds())
		

	def test_messWithNextID(self):
		'''
		Tests messing with private attribute nextID
		'''
		#print("Method toSeconds")
		#Departing from samples
		theEvent = sm.data.smTimelineEvent()
		tmpNextID = theEvent._smIdentifiable__nextID
		theEvent.__nextID = -8 #This will create a new attribute on the fly,
								#but it is NOT accesing the "real" __nextID
		self.assertNotEqual(theEvent._smIdentifiable__nextID,theEvent.__nextID)
		self.assertEqual(theEvent._smIdentifiable__nextID,tmpNextID)
		

	def test_methodHasOverlap(self):
		'''
		Tests method :meth:`hasOverlap`.
		'''
		#print("Method toSeconds")
		#Departing from samples
		ev1 = sm.data.smTimelineEvent(onset =3, duration = 5)
		ev2 = sm.data.smTimelineEvent(onset =4, duration = 1)
		ev3 = sm.data.smTimelineEvent(onset =8, duration = 3)
		ev4 = sm.data.smTimelineEvent(onset =9, duration = 2)
		ev1.hasOverlap(ev2)
		ev1.hasOverlap(ev3)
		ev1.hasOverlap(ev4)
		ev2.hasOverlap(ev3)
		ev2.hasOverlap(ev4)
		ev3.hasOverlap(ev4)


	@staticmethod
	def runTests():
		'''
		Class executable method
		'''
		print('TESTING smTimelineEvent')
		#The unittest is faster then the print above. Wait 1/2 sec to ensure messages are print "in order"
		time.sleep(0.5)
		t = unittest.TestLoader().loadTestsFromTestCase(testSciMethDataSmTimelineEvent)
		unittest.TextTestRunner(verbosity=2).run(t)
		#unittest.main(verbosity=2)

if __name__ == '__main__':
	print(' ')
	testSciMethDataSmTimelineEvent.runTests()