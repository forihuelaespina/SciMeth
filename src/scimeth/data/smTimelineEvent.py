# -*- coding: utf-8 -*-
#
#File: smTimelineEvent.py
#
'''
Created on Sun Mar 22 10:01:49 2020

Module ***smTimelineEvent***

This module implements the class :class:` ***smTimelineEvent***



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 22-Mar-2020 | FOE    | - Class :class:`smTimelineCondition` created but     |
|             |        |   initial unfinished implementation                  |
+-------------+--------+------------------------------------------------------+
| 23-Mar-2020 | FOE    | - :class:`smTimelineCondition`: Added remaining      |
|             |        |   getters/setters.                                   |
+-------------+--------+------------------------------------------------------+
| 28-Mar-2020 | FOE    | - Added documentation for attributes and class       |
|             |        |   invariants.                                        |
+-------------+--------+------------------------------------------------------+
| 29-Mar-2020 | FOE    | - Separated module comments from class comments.     |
+-------------+--------+------------------------------------------------------+
|  4-Apr-2020 | FOE    | - Added methods :meth:`isInSamples` and              |
|             |        |   :meth:`isInSeconds`.                               |
+-------------+--------+------------------------------------------------------+
|  8-Apr-2020 | FOE    | - Added read-only property :attr:`version`.          |
|             |        | - Warnings due to invalid types during attribute     |
|             |        |   setting, now raise ValueError.                     |
+-------------+--------+------------------------------------------------------+
| 12-Apr-2020 | FOE    | - Added property :attr:`description`                 |
|             |        | - Added :meth:`hasOverlap`.                          |
+-------------+--------+------------------------------------------------------+
|  5-May-2020 | FOE    | - Improved some comments.                            |
|             |        | - Updated for attribute :attr:`isInternationalSystem`|
|             |        |   renaming in :class:`smMeasurementUnit              |
|             |        |   <scimeth.data.smMeasurementUnit>`.                 |
+-------------+--------+------------------------------------------------------+
| 13-May-2020 | FOE    | - Get/Set access to attributes :attr:`unit` and      |
|             |        |   :attr:`info` are now "protected" by                |
|             |        |   deepcopies to avoid side effects.                  |
|             |        | - :meth:`__str__` now identifies inherited attributes|
+-------------+--------+------------------------------------------------------+
| 14-Mar-2020 | FOE    | - :meth:`__str__` now now admits parameter           |
|             |        |   `indentationLevel`.                                |
+-------------+--------+------------------------------------------------------+


.. seealso::
	
	:class:`smTimeline <scimeth.data.smTimeline>`,
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

'''



## Import
#import os
#import warnings
#import deprecation
import copy
import re #Allow using regular expression


from interface import implements


#from scimeth import __version__
#from scimeth import data as scimeth
from .smIdentifiable import smIdentifiable
from .smMeasurementUnit import smMeasurementUnit


## Class definition
class smTimelineEvent(smIdentifiable):
	#Sphinx documentation
	''':class:`smTimelineEvent <scimeth.data.smTimelineEvent>` represent
	temporal events to be recorded in a
	:class:`smTimeline <scimeth.data.smTimeline>`.
	Events are instances or occurences of anything that needs
	to be recorded during observations. They are part of a :class:`smTimeline`
	and can be grouped into
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
	
	The :class:`smTimelineEvent <scimeth.data.smTimelineEvent>` class represents
	events occurring during a :class:`smTimeline <scimeth.data.smTimeline>`.
	Within the container :class:`smTimeline <scimeth.data.smTimeline>` , the
	:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` can be grouped into
	:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` .
	
	:class:`smTimelineEvent <scimeth.data.smTimelineEvent>` have attributes
	:attr:`onset` and :attr:`duration` to keep track of the period it last.
	The :attr:`onset` is relative to the :class:`smTimeline <scimeth.data.smTimeline>`
	init time. The :attr:`duration` is relative to the event :attr:`onset`.
	Both, :attr:`onset` and :attr:`duration` can be stored in samples or
	a multiplier of seconds (see :attr:`unit`). Additionally, each event
	can be accompanied by some information (see :attr:`info`).
	
	:class:`smTimelineEvent <scimeth.data.smTimelineEvent>` are
	:class:`smIdentifiable <scimeth.data.smIdentifiable>`.
	

	:Class invariants:
	
	* :attr:`onset` is always greater or equal to 0 whether in Samples or Seconds.
	* :attr:`duration` is always greater or equal to 0 whether in Samples or Seconds.
	
	'''

	#Private class attributes shared by all instances
	

	#Class constructor
	def __init__(self, unit = 'Sample', onset = None, duration = None, end = None,
			  info = None, unitMultiplier = 0):
		'''Class constructor. Creates a new instance of
		:class:`smTimelineEvent <scimeth.data.smTimelineEvent>`
		
		By default, it creates a new instantaneous (duration=0) event at onset 0.
		Units are initialized to [samples]. No record of the sampling rate
		is kept.
		By default, the event has no associated information.
		
		:Invariant:
		
		:attr:`onset` + :attr:`duration` = :attr:`end`

		:Parameters:

		:param unit: Optional. Temporal unit; either 'Second' or 'Sample'.
			The default is 'Sample'
		:type unit: str.
		:param onset: Optional. Event onset. The default is 0.
		:type onset: float
		:param duration: Event duration. The default is 0.
		:type duration: float
		:param info: Optional. Information associated to the event.
			The default is `None`.
		:type info: Object, optional
		:param uitMultiplier: Optional. If your unit is 'Second', you can
			specify an unit multiplier;
			e.g. -3 for milliseconds. The default is 0 (10^0=1)
			The default is 0.
		:type unitMultiplier: float.

		:Returns:

		A new object instance of :class:`smTimelineEvent <scimeth.data.smTimelineEvent>`.
		'''

		#Figure out which parameters have been passed and the relation
		#between them.
		flagDuration = True #True if passed as parameter. False if not passed.
		if duration is None:
			duration = 0
			flagDuration = False
		flagEnd = True #True if passed as parameter. False if not passed.
		if end is None:
			end = 0
			flagEnd = False
		flagOnset = True #True if passed as parameter. False if not passed.
		if onset is None:
			onset= 0
			flagOnset = False
		#Now, try to make the best arrangement with what has been given.
		if not flagOnset and not flagDuration and not flagEnd:
			pass
		if not flagOnset and not flagDuration and flagEnd:
			onset = end-duration
		if not flagOnset and flagDuration and not flagEnd:
			end = onset + duration
		if not flagOnset and flagDuration and flagEnd:
			onset = end-duration
		if flagOnset and not flagDuration and not flagEnd:
			end = onset + duration
		if flagOnset and not flagDuration and flagEnd:
			duration = end - onset
		if flagOnset and flagDuration and not flagEnd:
			end = onset + duration
		if flagOnset and flagDuration and flagEnd:
			pass

		#Check consistency of onset, duration and end
		assert onset+duration == end, 'smTimlineEvent:__init__: Onset + duration must be equal to end.'

		#Call superclass constructor
		super().__init__() 
		
		self.__version = '0.1'
		
		#Initialize private attributes unique to this instance
		self.__unit = smMeasurementUnit(name='Sample',acronym='samples', \
												  multiplier=0, \
												  isInternationalSystem=False) #A smMeasurementUnit. Either samples or seconds.
		if type(unit) is not str:
			msg = self.getClassName() + ':unit: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if unit == 'Sample':
			pass
		elif unit == 'Second':
			self.__unit = smMeasurementUnit(name='Second',acronym='s', \
												  multiplier=unitMultiplier, \
												  isInternationalSystem=True)
		else:
			msg = self.getClassName() + ':unit: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		
		self.onset = onset #Time stamp of the event beginning in units.
		self.duration = duration #Duration of the event in units
		self.info = info #Information associated to the TimelineEvent.
		
		return
	
	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	@property
	def description(self): #description getter
		'''
		Condition description.

		:getter: Gets the event description.
		:setter: Sets the event description.
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
	def duration(self): #duration getter
		'''
		Event duration. The duration is expressed in :attr:`unit` and it
		is relative to :attr:`onset`.
		
		If unit is in samples, newDurations will be rounded to the
		closest integer.
		
		Changing the :attr:`duration`, affects the :attr:`end`.
		
		:getter: Gets the event duration.
		:setter: Sets the event duration.
		:type: float
		'''
		return self.__duration

	@duration.setter
	def duration(self,newDuration): #duration setter
		if not isinstance(newDuration,(int, float)):
			msg = self.getClassName() + ':duration: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newDuration<0:
			msg = self.getClassName() + ':duration: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if self.unit.name == 'Second':
			self.__duration = newDuration
		else: #Sample
			self.__duration = float(round(newDuration))
		return None

	@property
	def end(self): #end getter
		'''
		Event end. End is equal to onset+duration.
		
		Changing the :attr:`end`, affects the :attr:`duration`.

		:getter: Gets the event end.
		:setter: Sets the event end.
		:type: float
		'''
		return self.__onset + self.__duration

	@end.setter
	def end(self,newEnd): #end setter
		if not isinstance(newEnd,(int, float)):
			msg = self.getClassName() + ':end: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newEnd<self.onset:
			msg = self.getClassName() + ':end: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if self.unit.name == 'Second':
			self.__duration = newEnd - self.onset
		else: #Sample
			self.__duration = round(newEnd) - self.onset
		return None


	@property
	def onset(self): #onset getter
		'''
		Event onset. The onset is expressed in :attr:`unit` and it is relative
		to :class:`smTimeline` init time.
		
		If unit is in samples, newOnset will be rounded to the
		closest integer.

		:getter: Gets the event onset.
		:setter: Sets the event onset.
		:type: float
		'''
		return self.__onset

	@onset.setter
	def onset(self,newOnset): #onset setter
		if not isinstance(newOnset,(int, float)):
			msg = self.getClassName() + ':onset: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		newOnset = float(newOnset)
		if newOnset<0:
			msg = self.getClassName() + ':onset: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if self.unit.name == 'Second':
			self.__onset = newOnset
		else: #Sample
			self.__onset = round(newOnset)
		return None

	@property
	def unit(self): #unit getter
		'''
		The :class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>` in
		which the :attr:`onset` and :attr:`duration` are expressed.

		Unit can only be either seconds (with a multiplier) or samples.
		Note that there is no setter method for attr:`unit`. Instead,
		the user can used :meth:`toSeconds` and :meth:`toSamples`
		to change the attr:`unit`.
		
		:getter: Gets the time measurement unit.
		:type: :class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>`
		'''
		return copy.deepcopy(self.__unit)

	@property
	def info(self): #info getter
		'''
		Event information.

		The information associated to the event can be virtually
		anything (i.e. no type check is made on setting)
		
		:getter: Gets the event information.
		:setter: Sets the event information.
		:type: Object
		'''
		return copy.deepcopy(self.__info)

	@info.setter
	def info(self,newInfo): #info setter
		self.__info = copy.deepcopy(newInfo)
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
			
			if attributename == 'unit':
				#Increase indentation level
				s = s + indentationLevel*'\t' + inheritanceStr + attributename + \
						'\t= ' + value.__str__(indentationLevel = indentationLevel + 1) + ';\n'
			else:
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
	
	def hasOverlap(self,ev):
		'''Checks whether this element overlaps with `ev`.
		
		The two events must be expressed in the same units, whether
		'Sample' or 'Second'.
		
		:Parameters:
		
		:param ev: The event to be compared
		:type ev: :class:`smTimelineEvent <sm.data.smTimelineEvent>`
		
		:return: True if the events overlap. False otherwise.
		:rtype: bool
		'''
		#Check that they share the units
		#
		# isinstance does not work very well for user defined classes
		#
		# For instance, here, two events smTimelineEvents, the "self"
		#will have class "smTimelineEvents", but the event "ev" will
		#have class "scimeth.data.smTimelineEvent.smTimelineEvent"
		#which from the point of view of isinstance() is False.
		#
		#if isinstance(ev,type(self)):
		if ev.__class__.__name__ != self.getClassName(): #Not very elegant, and likely to fail if there are classes with the same name in different modules.
			msg = self.getClassName() + ':hasOverlap: Unexpected parameter type. ' \
				'Expected ''smTimelineEvent'', but ' + str(type(ev)) + ' found.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if not (ev.isInSeconds() or ev.isInSamples()):
			msg = self.getClassName() + ':hasOverlap: Unexpected events unit for parameter ev2. Events units must be either ''Sample'' or ''Second''.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if self.unit.name != ev.unit.name:
			msg = self.getClassName() + ':hasOverlap: Both events must share the same unit.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#(whether in samples or seconds), ensure the same (neutral) multiplier
		tmp1 = [x * 10**self.unit.multiplier for x in [self.onset, self.end]]
		tmp2 = [x * 10**ev.unit.multiplier for x in [ev.onset, ev.end]]
		#Finally, decide whether they overlap.
		res = False
		if tmp2[0] <= tmp1[0] and tmp2[1]>= tmp1[0]: #ev2.onset precedes ev1.onset, and ev2.end expand beyond ev1.onset
			res = True
		elif tmp2[0] > tmp1[0] and tmp2[0] <= tmp1[1]: #ev2.onset sucedes ev1.onset, but still initiates before ev1.end
			res = True
		return res


	def isEqual(self,obj2):
		'''
		Compares whether a second object is of the same type and have the
		same values in its properties.
		
		Note that this is different from:
		
		 * obj1 == obj2: This checks whether the objects have the same content.
		 * obj1 is obj2: This checks that both objects are referring to the
		   same instance.


		:Parameters:

		obj2 : :class:`smTimelineEvent <scimeth.data.smTimelineEvent>`
			Object to be compared with.

		:Returns:

		:return: True if both objects have the same information. False otherwise.
		:rtype: bool

		'''
		res = True
		res = res & (type(self) == type(obj2))
		if not res:
			return res
		
		res = res & (self.id == obj2.id)
		res = res & (self.onset == obj2.onset)
		res = res & (self.duration == obj2.duration)
		res = res & (self.unit.isEqual(obj2.unit))
		res = res & (self.info == obj2.info)
		
		return res

	def isInSamples(self):
		'''
		Checks whether the event is expressed in samples.

		:Returns:

		:return: True if the event is in samples. False otherwise.
		:rtype: bool

		'''
		return self.unit.name == 'Sample'


	def isInSeconds(self):
		'''
		Checks whether the event is expressed in seconds.

		:Returns:

		:return: True if the event is in seconds. False otherwise.
		:rtype: bool

		'''
		return self.unit.name == 'Second'


	def toSamples(self,samplingRate = 1):
		'''
		Choose Sample as the time unit in which
		the :attr:`onset` and :attr:`duration` are expressed.
		
		:Parameters:

		:param samplingRate: Sampling rate in [Hz]. The default is 1 Hz.
			Value must be equal or greater than 0 Hz. Otherwise, the
			conversion to Sample is not executed, a warning
			is issued and the method returns -1.
		:type samplingRate: float, optional.
		'''
		if not isinstance(samplingRate,(int, float)):
			msg = self.getClassName() + ':toSamples: Unexpected parameter type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if samplingRate <= 0:
			msg = self.getClassName() + ':toSamples: Unexpected parameter value. Sampling rate must be equal or greater than 0 Hz.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		currUnit = self.unit.name
		currMultiplier = self.unit.multiplier
		self.__unit = smMeasurementUnit(name='Sample',acronym='samples', \
								multiplier=1, \
								isInternationalSystem=False)
		#and update the onset and duration from seconds.
		if currUnit == 'Sample':
			pass
		else:
			self.onset = round(self.onset * 10**currMultiplier * samplingRate)
			self.duration = round(self.duration * 10**currMultiplier * samplingRate)
		return None


	def toSeconds(self,samplingRate = 1, newMultiplier = 0):
		'''
		Choose Second as the time unit in which
		the :attr:`onset` and :attr:`duration` are expressed.
		
		:Parameters:

		samplingRate : float, optional.
			Sampling rate in [Hz]. The default is 1 Hz.
			Value must be equal or greater than 0 Hz. Otherwise, the
			conversion to Second is not executed, a warning
			is issued and the method returns -1.
		newMultplier : int
			Seconds multiplier, e.g. -3 for milliseconds. The default is
			0 i.e. (full) seconds.

		'''
		if not isinstance(samplingRate,(int, float)) \
		   or not isinstance(newMultiplier,(int, float)) :
			msg = self.getClassName() + ':toSamples: Unexpected parameter type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if samplingRate <= 0:
			msg = self.getClassName() + ':toSamples: Unexpected parameter value. Sampling rate must be equal or greater than 0 Hz.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		currUnit = self.unit.name
		self.__unit = smMeasurementUnit(name = 'Second', acronym = 's', \
								multiplier = newMultiplier, \
								isInternationalSystem = True)
		#and update the onset and duration from samples.
		if currUnit == 'Second':
			pass
		else:
			self.onset = (self.onset / samplingRate) / 10**self.unit.multiplier
			self.duration = (self.duration / samplingRate) / 10**self.unit.multiplier
		return None
		

