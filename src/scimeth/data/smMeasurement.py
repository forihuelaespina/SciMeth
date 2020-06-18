# -*- coding: utf-8 -*-
#
#File: smMeasurement.py
#
'''
Created on Sat Apr 18 21:32:50 2020

Module ***smTimelineCondition***

This module implements the class :class:` ***smTimelineEvent***



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 18-Apr-2020 | FOE    | - Class created with attributes :attr:`id`,          |
|             |        |   :attr:`version`, :attr:`data` and :attr:`timeline`.|
|             |        | - Added methods :meth:`__str__`,                     |
|             |        |   :meth:`getClassName`                               |
+-------------+--------+------------------------------------------------------+
| 13-May-2020 | FOE    | - :meth:`__str__` now identifies inherited attributes|
+-------------+--------+------------------------------------------------------+
| 14-Mar-2020 | FOE    | - :meth:`__str__` now now admits parameter           |
|             |        |   `indentationLevel`.                                |
+-------------+--------+------------------------------------------------------+

.. seealso::
		
		:class:`smTimeline <scimeth.data.smTimeline>`,

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

'''

## Import
#import warnings
#import deprecation
#import os
import re #Allow using regular expression

from interface import implements
import numpy as np


from .smIdentifiable import smIdentifiable
from .smTimeline import smTimeline


## Class definition
class smMeasurement(smIdentifiable):
	#Sphinx documentation
	''':class:`smMeasurement <scimeth.data.smMeasruement>` are the
	most the fundamental data containers in `scimeth`.
	
	A :class:`smMeasurement <scimeth.data.smMeasruement>` 
	is a (structured) data item i.e. a data tensor. Measurements may
	be raw or not depending on whether they are collected by a
	:class:`smMeasuringDevice <scimeth.data.smMeasurementDevice>`
	or transformed from another existing
	:class:`smMeasurement <scimeth.data.smMeasruement>`.

	It maybe static (in which case the associated
	Timeline has length 0) or dynamic.
	
	The data can be annotated through the associated
	:class:`smTimeline <scimeth.data.smTimeline>`
	
	:The data tensor:
	
	The core of a measurement is the data tensor. The data tensor is a
	rank 3 tensor where:
	
	* the first dimension encodes temporal samples,
	* the second dimension encodes spatial samples,
	* the third dimension encodes the multivariate samples,
	
	Spatial dimensions of the data itself are flattened if necessary.
	For instance topographical (2D) or tomographical (3D) data is
	vectorized.
	
	'''

    #Private class attributes shared by all instances
	

	#Class constructor
	def __init__(self, data = None, timeline = None):
		'''Class constructor. Creates a new instance of
		:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
		

		:Parameters:

		data : (3D) numpy.ndarray. optional
			The data tensor.
		timeline : :class:`smTimeline <scimeth.data.smTimeline>`, optional
			Description of the condition. The default is None.

		:Returns:

		A new object instance of :class:`scimeth.data.smMeasurement`.
		'''
		#Call superclass constructor
		super().__init__() 

		
		self.__version = '0.1'

		#Explicitly create the properties before the first call to setter.
		self.__data = np.zeros((0,0,0),dtype=float) #The data tensor.
		self.__timeline = smTimeline() #The timeline.
		
		return

	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	@property
	def data(self): #data getter
		'''
		The data tensor.
		
		The length of the :attr:`data` along the first dimension
		must coincide with the :attr:`timeline` :attr:`length`.

		:getter: Gets the data.
		:setter: Sets the data.
		:type: numpy.ndarray (of dimension 3)
		'''
		return self.__tag

	@data.setter
	def data(self,newData): #data setter
		if type(newData) is not np.ndarray:
			msg = self.getClassName() + ':data: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if self.timeline.length != np.size(newData,0):
			msg = self.getClassName() + ':data: Unexpected attribute value. ' \
				'Data along the first dimension must coincide with the ' \
				':attr:`timeline` length.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__data = newData
		return None


	@property
	def timeline(self): #timeline getter
		'''
		The measurement :class:`smTimeline <scimeth.data.smTimeline>`.
		
		The :attr:`timeline` :attr:`length` must coincide with the
		length of the :attr:`data` along the first dimension.

		:getter: Gets the timeline.
		:setter: Sets the timeline.
		:type: :class:`smTimeline <scimeth.data.smTimeline>`
		'''
		return self.__timeline

	@timeline.setter
	def timeline(self,newTimeline): #timeline setter
		if type(newTimeline) is not smTimeline:
			msg = self.getClassName() + ':timeline: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newTimeline.length != np.size(self.data,0):
			msg = self.getClassName() + ':timeline: Unexpected attribute value. ' \
				'Timeline length must coincide with the length of the data ' \
				'along the first dimension.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__timeline = newTimeline
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

			#Lists render their elements using __repr__ instead of __str__
			#Enforce use of __str__
			if attributename in ['timeline']:
				s = s + indentationLevel*'\t' + inheritanceStr + attributename \
					+ '\t=\n' + value.__str__(indentationLevel = indentationLevel + 1) \
					+ ';\n'
			else:
				s = s + indentationLevel*'\t' + inheritanceStr + attributename \
					+ '\t= ' + str(value) + ';\n'
		return s + indentationLevel*'\t' + '}>'



	
	#Public methods
	def getClassName(self):
		'''Gets the class name.
		
		:return: The class name
		:rtype: str
		'''
		return type(self).__name__
	

