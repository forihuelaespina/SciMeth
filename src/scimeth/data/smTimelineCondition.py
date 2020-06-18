# -*- coding: utf-8 -*-
#
#File: smTimelineCondition.py
#
'''
Created on Tue Mar 24 19:31:38 2020

Module ***smTimelineCondition***

This module implements the class :class:` ***smTimelineEvent***



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 24-Mar-2020 | FOE    | - Class :class:`smTimelineCondition` created.        |
+-------------+--------+------------------------------------------------------+
| 28-Mar-2020 | FOE    | - :class:`smTimelineCondition`: Changed default      |
|             |        |   values for tag (from 'A' to 'CondA') and           |
|             |        |   description (from None to '')                      |
|             |        | - Neither the tag nor the decription can take value  |
|             |        |   None.                                              |
|             |        | - Added documentation for attributes.                |
+-------------+--------+------------------------------------------------------+
| 29-Mar-2020 | FOE    | - Separated module comments from class comments.     |
+-------------+--------+------------------------------------------------------+
|  8-Apr-2020 | FOE    | - Added read-only property :attr:`version`.          |
|             |        | - Warnings due to invalid types during attribute     |
|             |        |   setting, now raise ValueError.                     |
+-------------+--------+------------------------------------------------------+
| 13-May-2020 | FOE    | - :meth:`__str__` now identifies inherited attributes|
+-------------+--------+------------------------------------------------------+
| 14-Mar-2020 | FOE    | - :meth:`__str__` now now admits parameter           |
|             |        |   `indentationLevel`.                                |
+-------------+--------+------------------------------------------------------+



.. seealso::
		
		:class:`smTimeline <scimeth.data.smTimeline>`,
		:class:`smTimelineEvent <scimeth.data.smTimelineEvent>`,

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

'''


## Import
#import warnings
#import deprecation
#import os
import re #Allow using regular expression


from interface import implements


#from scimeth import __version__
#from scimeth import data as scimeth
from .smIdentifiable import smIdentifiable


## Class definition
class smTimelineCondition(smIdentifiable):
	#Sphinx documentation
	''':class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
	are labels to group :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
	occurring in within a :class:`smTimeline <scimeth.data.smTimeline>`.
	
	A :class:`smTimelineCondition <scimeth.data.smTimelineCondition>` groups
	together a collection of 
	:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` ocurring in a
	:class:`smTimeline <scimeth.data.smTimeline>` under a common label.
	Note that the
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>` does ***NOT***
	keeps track of the :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`, the
	:class:`smTimeline <scimeth.data.smTimeline>` does.
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>` can
	label experimental and non-experimental
	conditions. Experimental conditions can be used but not limited to
	for instance to keep track of stimuluations, treatment administration,
	etc. Non-experimental conditions can be used but not limited to
	for instance to keep track of artefacts, data quality marking, etc.
	
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>` are
	:class:`smIdentifiable <scimeth.data.smIdentifiable>`.
	
	'''

    #Private class attributes shared by all instances
	
	#Class constructor
	def __init__(self, tag = 'CondA', description = ''):
		'''Class constructor. Creates a new instance of
		:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
		

		:Parameters:

		tag : str. optional
			Condition label. The default is 'A'.
		description : str, optional
			Description of the condition. The default is None.

		:Returns:

		A new object instance of :class:`scimeth.data.smTimelinecondition`.
		'''
		#Call superclass constructor
		super().__init__() 
		
		self.__version = '0.1'

		self.tag = tag #Condition tag. The main label to refer to the condition.
		self.description = description #A somewhat longer description of the condition.
		
		return

	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	@property
	def tag(self): #tag getter
		'''
		Condition tag.

		:getter: Gets the condition tag.
		:setter: Sets the condition tag.
		:type: str
		'''
		return self.__tag

	@tag.setter
	def tag(self,newTag): #tag setter
		if type(newTag) is not str:
			msg = self.getClassName() + ':tag: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__tag = newTag
		return None

	@property
	def description(self): #description getter
		'''
		Condition description.

		:getter: Gets the condition description.
		:setter: Sets the condition description.
		:type: str
		'''
		return self.__description

	@description.setter
	def description(self,newDescription): #description setter
		if type(newDescription) is not str:
			msg = self.getClassName() + ':description: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__description = newDescription
		return None



	@property
	def version(self): #version getter
		'''
		The object version.
		
		:getter: Gets the version.
		:type: str
		'''
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
			s = s + indentationLevel*'\t' + inheritanceStr + attributename + '\t= ' + str(value) + ';\n'
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

		obj2 : :class:`scimeth.data.smTimelineCondition`
			Object to be compared with.

		:Returns:

		Boolean. True if both objects have the same information.
		False otherwise.

		'''
		res = True
		
		res = res & (type(self) == type(obj2))
		if not res:
			return res
		
		res = res & (self.id == obj2.id)
		res = res & (self.tag == obj2.tag)
		res = res & (self.description == obj2.description)
		
		return res




