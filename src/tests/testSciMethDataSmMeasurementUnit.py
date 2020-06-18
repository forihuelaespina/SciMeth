# -*- coding: utf-8 -*-
#
# File: testSciMethDataSmMeasurementUnit.py
#
"""
Created on Mon Mar 30 14:03:59 2020

Module ***testSciMethDataSmMeasurementUnit***

Contains the tests for class :class:`scimeth.data.smMeasurementUnit`

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 22-Mar-2020 | FOE    | - Test module created                                |
|             |        | - Added tests:                                       |
|             |        |                                                      |
|             |        | * `test_ObjectConstructionDefaultCall`               |
|             |        | * `test_ObjectConstructionParameterizedCall`         |
|             |        | * `test_settingAttributeValues`                      |
|             |        | * `test_methodIsEqual`                               |
|             |        |                                                      |
+-------------+--------+------------------------------------------------------+
|  4-Mar-2020 | FOE    | - Updated test `test_ObjectConstructionDefaultCall`  |
|             |        |   using `try:except`.                                |
|             |        | - Improved some comments                             |
+-------------+--------+------------------------------------------------------+



.. seealso:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

import sys
import time
import unittest

#Add paths
if not sys.path[0] == '..':
	sys.path.insert(0, '..')

import scimeth as sm

class testSciMethDataSmMeasurementUnit(unittest.TestCase):
	'''A test suite for :class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>`
	'''
	
	def test_ObjectConstructionDefaultCall(self):
		'''
		Tests object creation with a default call to constructor.
		'''
		#print('Testing test_defaultConstructorCall')
		try:
			theUnit = sm.data.smMeasurementUnit()
			self.assertIsInstance(theUnit,sm.data.smMeasurementUnit,\
			   'Test: Cannot construct object with default call to constructor.')
		except:
			self.assertTrue(False)
			



	def test_ObjectConstructionParameterizedCall(self):
		'''
		Tests object creation with parameterized call to constructor.
		'''
		#print("Setting attribute values from the constructor")
		theUnit = sm.data.smMeasurementUnit(multiplier=10, name='Second', acronym = 's', isInternationalSystem = True)
		self.assertEqual(theUnit.name, 'Second')
		self.assertEqual(theUnit.acronym, 's')
		self.assertEqual(theUnit.multiplier, 10)
		self.assertEqual(theUnit.isInternationalSystem, True)

	def test_settingAttributeValues(self):
		'''
		Tests simple attribute setting.
		'''
		#print("Setting attribute values one by one")
		theUnit = sm.data.smMeasurementUnit()
		theUnit.name = 'Meter'
		theUnit.acronym = 'm'
		theUnit.multiplier = 1
		theUnit.isInternationalSystem = True
		self.assertEqual(theUnit.name, 'Meter')
		self.assertEqual(theUnit.acronym, 'm')
		self.assertEqual(theUnit.multiplier, 1)
		self.assertEqual(theUnit.isInternationalSystem, True)


	def test_methodIsEqual(self):
		'''
		Tests method :meth:`isEqual`.
		'''
		#print("Method isEqual")
		theUnit = sm.data.smMeasurementUnit(multiplier=10, name='Second', \
									  acronym = 's', isInternationalSystem = True)
		self.assertNotEqual(theUnit, sm.data.smMeasurementUnit())
		self.assertIsNot(theUnit, sm.data.smMeasurementUnit())
		self.assertNotEqual(theUnit, \
			sm.data.smMeasurementUnit(multiplier=10, name='Second', \
							 acronym = 's', isInternationalSystem = True))
		self.assertIsNot(theUnit, \
			sm.data.smMeasurementUnit(multiplier=10, name='Second', \
							 acronym = 's', isInternationalSystem = True))
		self.assertTrue(theUnit.isEqual(sm.data.smMeasurementUnit(multiplier=10, \
							 name='Second', acronym = 's', isInternationalSystem = True)))



	@staticmethod
	def runTests():
		'''
		Class executable method
		'''
		print('TESTING smMeasurementUnit')
		#The unittest is faster then the print above. Wait 1/2 sec to ensure messages are print "in order"
		time.sleep(0.5)
		t = unittest.TestLoader().loadTestsFromTestCase(testSciMethDataSmMeasurementUnit)
		unittest.TextTestRunner(verbosity=2).run(t)
		#unittest.main(verbosity=2)

if __name__ == '__main__':
	print(' ')
	testSciMethDataSmMeasurementUnit.runTests()