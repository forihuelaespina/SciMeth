# -*- coding: utf-8 -*-
#
# File: smMeasurementUnit.py
#
"""
Created on Sat Mar 21 10:01:49 2020

Module ***smMeasurementUnit***

This module implements the class :class:`smMeasurementUnit`.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 21-Mar-2020 | FOE    | - Class :class:`smMeasurementUnit` created.          |
+-------------+--------+------------------------------------------------------+
| 23-Mar-2020 | FOE    | - :class:`smMeasurementUnit`: Added method           |
|             |        |   :meth:`isEqual`.                                   |
+-------------+--------+------------------------------------------------------+
| 29-Mar-2020 | FOE    | - Separated module comments from class comments.     |
+-------------+--------+------------------------------------------------------+
|  8-Apr-2020 | FOE    | - Added read-only property :attr:`version`.          |
|             |        |   :meth:`isEqual`.                                   |
|             |        | - Warnings due to invalid types during attribute     |
|             |        |   setting, now raise ValueError.                     |
+-------------+--------+------------------------------------------------------+
|  5-May-2020 | FOE    | - Setting attributes :attr:`name`, :attr:`acronym`,  |
|             |        |   :attr:`mutliplier` and :attr:`isIS` can no longer  |
|             |        |   accept `None`. Note that before, attempting to set |
|             |        |   `None` was simply changing the value to some       |
|             |        |   default.                                           |
|             |        | - attributes :attr:`isIS` renamed as                 |
|             |        |   :attr:`isInternationalSystem`.                     |
|             |        | - Improved some comments.                            |
+-------------+--------+------------------------------------------------------+
| 13-Mar-2020 | FOE    | - :class:`smMeasurementUnit` is now                  |
|             |        |   :class:`smIdentifiable`.                           |
|             |        | - :meth:`__str__` now identifies inherited attributes|
+-------------+--------+------------------------------------------------------+
| 14-Mar-2020 | FOE    | - :meth:`__str__` now now admits parameter           |
|             |        |   `indentationLevel`.                                |
+-------------+--------+------------------------------------------------------+


.. seealso:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""



## Import
#import os
#import warnings
#import deprecation
import re #Allow using regular expression


#from scimeth import __version__
#from scimeth import data as sm
from .smIdentifiable import smIdentifiable


## Class definition
class smMeasurementUnit(smIdentifiable):
	#Sphinx documentation
	"""Measurement units provide the standard scale in which measurements
	are expressed.
	Measurement units are at the core of measurement systems and provide
	the standard scale in which measurements are expressed.
	
	A :class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>`
	holds information about
	a measurement unit e.g. Meters, seconds, Coulomb,
	etc, and the multiplier in which data is expressed e.g. nano (10^-9), etc.
	
	:Parameters:
	
	:param name: Optional. The unit name, e.g. 'seconds'.
		The default is 'arbitrary'.
	:type name: str
	:param acronym: Optional. The unit acronym, e.g. 's'
		The default is 'a.u.'.
	:type acronym: str
	:param multiplier: Optional. The unit multiplier in base 10 (as in 10^multiplier).
		The default is 0.
	:type multiplier: float
	:param isInternationalSystem: Optional. A flag indicating whether the
		variable is part of the International System
		The default is `False`.
	:type isInternationalSystem: bool
	"""

	#Private class attributes shared by all instances

	#Class constructor
	def __init__(self, name = 'arbitrary', acronym = 'a.u.', multiplier = 0, \
			  isInternationalSystem = False):
		#Call superclass constructor
		super().__init__() 
		
		self.__version = '0.1'

		#Initialize private attributes unique to this instance
		self.name = name #Unit name e.g. Meter, Seconds, Coulomb, etc.
		self.acronym = acronym #The short representation for the unit, e.g. s for seconds, m for meters, etc
		self.multiplier = multiplier #In base 10. For instance, use;
							#-9 for nano, -6 for micro, -3 for milli, 1 for no scaling, 3 for kilo, 6 for mega, etc
		self.isInternationalSystem = isInternationalSystem #Does the unit belong to the International System?
						  # True if the unit belongs to the International System. False, otherwise.
		
		return


	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	@property
	def name(self): #name getter
		"""
		A logical name for the unit, e.g. Meter, Second, Joule, Volt, etc.
		
		:getter: Gets the unit name.
		:setter: Sets the unit name.
		:type: str
		"""
		return self.__name

	@name.setter
	def name(self,newName): #name setter
		if type(newName) is not str:
			msg = self.getClassName() + ':name: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__name = newName
		return None
		

	@property
	def acronym(self): #acronym getter
		"""
		An acronym for the unit, e.g. m for Meter, s for Second, etc.
		
		:getter: Gets the unit acronym.
		:setter: Sets the unit acronym.
		:type: str
		"""
		return self.__acronym

	@acronym.setter
	def acronym(self,newAcronym): #acronym setter
		if type(newAcronym) is not str:
			msg = self.getClassName() + ':acronym: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__acronym = newAcronym
		return None
		
	@property
	def multiplier(self): #multiplier getter
		"""
		The unit multipler in base 10. For instance, use;
		-9 for nano, -6 for micro, -3 for milli, 0 for no scaling,
		1 for deca, 3 for kilo, 6 for mega, etc

		:getter: Gets the unit multiplier.
		:setter: Sets the unit multiplier.
		:type: int or float
		"""
		return self.__multiplier

	@multiplier.setter
	def multiplier(self,newMultiplier): #multiplier setter
		if not isinstance(newMultiplier,(int,float)):
			msg = self.getClassName() + ':multiplier: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__multiplier = float(newMultiplier)
		return None
		
	@property
	def isInternationalSystem(self): #isInternationalSystem getter
		"""
		Indicates whether the unit is an International System (IS) unit.
		True if the unit belongs to the International System. False, otherwise.
		
		Note that this is ***NOT*** checked against a list of IS units.
		This is a declaration that the user does.
		
		:getter: Asks whether the unit is an International System unit.
		:setter: Sets whether the unit is an International System unit.
		:type: bool
		"""
		return self.__isInternationalSystem

	@isInternationalSystem.setter
	def isInternationalSystem(self,newValue): #multiplier setter
		if (type(newValue) is not bool):
			msg = self.getClassName() + ':isInternationalSystem: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__isInternationalSystem = newValue
		return None

	@property
	def version(self): #version getter
		"""
		The object version.
		
		This is a read-only proerty
		
		:getter: Gets the version.
		:type: str
		"""
		return self.__version




	#Private methods
	def __str__(self, indentationLevel=1):
		'''Provides a string representation for the objects of the class.
		
		:Parameters:
		
		:param indentationLevel: Indentation level. Number of \t inserted
			in front of the attribute names. Default is 1. Must be positive or 0.
		:type indentationLevel: int
		
		:return: A string representation for the object
		:rtype: str
		'''
		if type(indentationLevel) is not int:
			msg = self.getClassName() + ':__str__: Unexpected parameter type. IndentationLevel must be of type int.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if indentationLevel < 0:
			msg = self.getClassName() + ':__str__: Unexpected parameter value. IndentationLevel must be positive or 0.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
			
		
		s = '<' + self.getClassName() + ': {\n'
		#Grab Class attributes (note that this will only pick class attributes
		#but not instance attributes)
		#The filter ignores python __ attributes e.g. __repr__
		iters = dict((name,value) for name,value in self.__dict__.items() if name[:2] != '__')
		#Update with the instance items
		iters.update(self.__dict__)
		#Finally build the string
		for name,value in iters.items():
			#Deal with python namemangling
			classprefix = re.match('_\S*__',name)
			classname = '';
			attributename = name
			if classprefix: #if there is a match
				classname = classprefix.group()[1:-2]
				attributename = name[len(classname)+3:]
			#Check if attribute is inherited
			inheritanceStr = ''
			if classname != self.getClassName():
				inheritanceStr = '(*' + classname + ') '
			s = s + indentationLevel*'\t' + inheritanceStr + attributename + \
							'\t= ' + str(value) + ';\n'
		return s + indentationLevel*'\t' + '}>'

	
	
	#Public methods
	def getClassName(self):
		'''Gets the class name.
		
		:return: The class name
		:rtype: str
		'''
		return type(self).__name__
	


	def isEqual(self,obj2):
		'''
		Compares whether a second object is of the same type and have the
		same values in its properties.
		
		Note that this is different from:
		
		 * obj1 == obj2: This checks whether the objects have the same content.
		 * obj1 is obj2: This checks that both objects are referring to the
		   same instance.

		:Parameters:

		obj2 : :class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>`
			Object to be compared with.

		:Returns:

		Boolean. True if both objects have the same information.
		False otherwise.

		'''
		res = True
		
		res = res & (str(self.__class__) == str(obj2.__class__))
		if not res:
			return res
		
		res = res & (self.name == obj2.name)
		res = res & (self.acronym == obj2.acronym)
		res = res & (self.multiplier == obj2.multiplier)
		res = res & (self.isInternationalSystem == obj2.isInternationalSystem)
		
		return res

