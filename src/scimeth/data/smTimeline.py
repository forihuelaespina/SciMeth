# -*- coding: utf-8 -*-
#
#File: smTimeline.py
#
'''
Created on Tue Mar 24 23:42:31 2020

Module ***smTimeline***

This module implements the class :class:`smTimelineEvent <scimeth.data.smTimeline`.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 24-Mar-2020 | FOE    | - Class :class:`smTimeline` created but unfinished.  |
+-------------+--------+------------------------------------------------------+
| 28-Mar-2020 | FOE    | - :class:`smTimeline`: Continued with initial        |
|             |        |   implementation but still unfinished.               |
+-------------+--------+------------------------------------------------------+
| 28-Mar-2020 | FOE    | - :class:`smTimeline`: Continued with initial        |
|             |        |   implementation but still unfinished.               |
|             |        | - Added methods :meth:`sortTimelineEventsById` and   |
|             |        |   :meth:`sortTimelineEventsByOnset`                  |
+-------------+--------+------------------------------------------------------+
| 29-Mar-2020 | FOE    | - :class:`smTimeline`: Continued with initial        |
|             |        |   implementation but still unfinished.               |
|             |        | - Separated module comments from class comments.     |
|             |        | - Added events handling methods.                     |
+-------------+--------+------------------------------------------------------+
|  7-Apr-2020 | FOE    | - Initial debugging.                                 |
|             |        | - The constructor can now accept any combination of  |
|             |        |   parameters.                                        |
+-------------+--------+------------------------------------------------------+
|  8-Apr-2020 | FOE    | - Added read-only property :attr:`version`.          |
|             |        | - Warnings due to invalid types during attribute     |
|             |        |   setting, now raise ValueError.                     |
|             |        | - Added new attribute :attr:`init` so that the first |
|             |        |   timestamp does NOT have to be 0. Then, revisited   |
|             |        |   the behaviour of other setters to ensure proper    |
|             |        |   behaviour.                                         |
|             |        | - Added methods :meth:`getConditionsID` and          |
|             |        |   :meth:`getEventsID`                                |
+-------------+--------+------------------------------------------------------+
|  9-Apr-2020 | FOE    | - Added method :meth:`clearConditions`.              |
|             |        | - Debugged methods related to events manipulation.   |
+-------------+--------+------------------------------------------------------+
| 10-Apr-2020 | FOE    | - Added method :meth:`getConditions`, and            |
|             |        |   :meth:`assignEvents`                               |
+-------------+--------+------------------------------------------------------+
| 12-Apr-2020 | FOE    | - Added method :meth:`getConditionsEvents` and       |
|             |        |   improved acesss to :attr:`overlapStatus`           |
+-------------+--------+------------------------------------------------------+
| 14-Apr-2020 | FOE    | - Added method :meth:`allowOverlap` and              |
|             |        |   :meth:`forbidOverlap`                              |
+-------------+--------+------------------------------------------------------+
| 30-Apr-2020 | FOE    | - Method :meth:`getConditionsEvents` now accept a    |
|             |        |   single condition to be passed directly.            |
|             |        | - Method :meth:`addEvents` now accept a              |
|             |        |   single event to be passed directly.                |
|             |        | - Bug fixing: Method :meth:`addEvents` type checking |
|             |        |   and assignment to :attr:`events` is now working    |
|             |        |   correctly.                                         |
|             |        | - Added methods :meth:`removeConditions`.            |
|             |        | - Bug fixing: Setting :attr:`conditions` and method  |
|             |        |   :meth:`addConditions` now properly ensure there is |
|             |        |   an associated entry in the conditionsEventsMap.    |
+-------------+--------+------------------------------------------------------+
|  5-May-2020 | FOE    | - Improved some comments.                            |
|             |        | - Updated for attribute :attr:`isInternationalSystem`|
|             |        |   renaming in :class:`smMeasurementUnit              |
|             |        |   <scimeth.data.smMeasurementUnit>`.                 |
|             |        | - Bug fixing: Methods :meth:`toSeconds` and          |
|             |        |   :meth:`toSamples` now rely on                      |
|             |        |   :class:`smTimelineEvent                            |
|             |        |   <scimeth.data.smTimelineEvent>`                    |
|             |        |   methods :meth:`smTimelineEvent.toSeconds` and      |
|             |        |   :meth:`smTimelineEvent.toSamples` respectively.    |
+-------------+--------+------------------------------------------------------+
| 13-May-2020 | FOE    | - :meth:`__str__` now identifies inherited attributes|
+-------------+--------+------------------------------------------------------+
| 14-Mar-2020 | FOE    | - :meth:`__str__` now now admits parameter           |
|             |        |   `indentationLevel`.                                |
+-------------+--------+------------------------------------------------------+
| 15-Mar-2020 | FOE    | - Class attributes are now encapsulated against side |
|             |        |   side effects by deepcopies.                        |
|             |        | - Added methods :meth:`setConditions` and            |
|             |        |   :meth:`setEvents`.                                 |
+-------------+--------+------------------------------------------------------+
| 17-Mar-2020 | FOE    | - Added methods :meth:`dissociateEvents`             |
|             |        | - Method :meth:`assignEvents` renamed to             |
|             |        |   :meth:`associateEvents`.                           |
|             |        |   For an interesting discussion on why not           |
|             |        |   assign/deassign, see:                              |
|             |        |   https://english.stackexchange.com/questions/59463/ |
|             |        |   antonym-to-assign                                  |
+-------------+--------+------------------------------------------------------+





.. seealso::
	
	:class:`smTimelineEvent <scimeth.data.smTimelineEvent>`,
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
	:class:`smMeasurement <scimeth.data.smMeasurement>`,

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

'''


## Import
import warnings
#import deprecation
#import os
import copy
import re #Allow using regular expression

import numpy as np
import math #Needed to calculate log
import itertools


#from interface import implements
import datetime


#from scimeth import __version__
#from scimeth import data as scimeth
from scimeth.utils import partition, quick_sort
from .smIdentifiable import smIdentifiable
from .smMeasurementUnit import smMeasurementUnit
from .smTimelineEvent import smTimelineEvent
from .smTimelineCondition import smTimelineCondition



## Class definition
class smTimeline(smIdentifiable):
	#Sphinx documentation
	'''A :class:`smTimeline <scimeth.data.smTimeline>` keeps track of samples
	timestamps as well as experimental and non-experimental 
	:class:`smTimelineEvents <scimeth.data.smTimelineEvent>`.

	:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` can be group into
	:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` in a
	many-to-many relation.
	A :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` may be associated
	to many
	:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` s, and a
	:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` can
	hold any number of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`.
	:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` may not be associated to
	any :class:`smTimelineConditions <scimeth.data.smTimelineCondition>`.
	
	:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` can be
	allowed or not to be overalapping, even itself. That is, their associated
	:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` can
	overlap or not the :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
	of the other :class:`smTimelineConditions <scimeth.data.smTimelineCondition>`.
	
	:class:`smTimeline <scimeth.data.smTimeline>` can be uniformly sampled
	at a given :attr:`samplingRate` or non-uniformly sampled. In the first
	case, the sampling rate is strictly positive (>0), while in the second
	case, the sampling rate is set to -1.

	* ***Uniformly sampled timelines***: The timeline is considered to
	  represent an equispaced sampling process.
	  
	  * The :attr:`samplingRate` is strictly positive.
	  * :attr:`timestamps` follow the timing rule set by the :attr:`samplingRate`.
	  * :attr:`length`,:attr:`init`,:attr:`end`,:attr:`timeMultiplier` and
	    :attr:`samplingRate` are related by:
	    
	    .. math::
			
			samplingRate &= (length-1) / ((end-init) * 10^timeMultiplier) \\
			                     &= (length-1) / ((duration) * 10^timeMultiplier)
			
	    * A rounding error smaller than 1/(2*:attr:`samplingRate`) is
	      tolerated.
	    
	
	* ***Non-uniformly sampled timelines***: The timeline is
	  considered to represent a non-equispaced sampling process.
	  
	  * The :attr:`samplingRate` is -1.
	  * :attr:`timestamps` do not follow any specific timing rule.
	  * No specific relation is expected between :attr:`length` and
	    :attr:`end`.
	  
	:class:`smTimeline <scimeth.data.smTimeline>` are
	:class:`smIdentifiable <scimeth.data.smIdentifiable>`.
	
	
	:class:`smTimelineEvents <scimeth.data.smTimelineEvents>` are
	internally expressed in :attr:`unit`, whether 'Sample' or 'Second'.
	The :attr:`unit` can be set during object construction, or changed
	later using :meth:`toSeconds` and :meth:`toSamples`.

	:Class invariants:
	
	* All :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` 
	  in the :class:`smTimeline <scimeth.data.smTimeline>` have different IDs.
	* All :class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
	  in the :class:`smTimeline <scimeth.data.smTimeline>` have different IDs.
	* :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` cannot last
	  beyond the end (if :attr:`unit` is in 'Second') or
	  length (if :attr:`unit` is in 'Sample') of the Timeline.
	* :attr:`timestamps` are all positive (>=0), different and sorted. It
	  follows that:
	  
	  * :attr:`init` >= 0
	  * :attr:`end` >= 0
	  * :attr:`end` >= :attr:`init`
	  * :attr:`duration` >= 0 and is 0 only if :attr:`end` == :attr:`init`
	  

	'''

	#Private class attributes shared by all instances
	

	#Class constructor
	def __init__(self, startTime = datetime.datetime.now(),
						unit = 'Sample',
						length = None,
						samplingRate = None,
						init = 0,
						end = None,
						timeMultiplier = None):
		'''
		Class constructor. Creates a new instance of
		:class:`smTimeline <scimeth.data.smTimeline>`.
		
		By default, the new object instance is equally sampled at `samplingRate`.
		The number of initial timestamps can be controlled using
		either `length`, `end` or both (as long as they are
		compatible i.e. `length / samplingRate = end * 10^timeMultiplier`).
		You may later change this behaviour non equally sampled timelines.
		
		By default, the :class:`smTimeline <scimeth.data.smTimeline>` instance
		has no associated events or conditions.
		
		
		:Parameters:
		
		startTime : :class:`datetime.datetime`, optional
			Absolute initial time. The default is :meth:`datetime.datetime.now()`.
		unit : str, optional
			Temporal units in which the :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`
			are expressed. Either 'Sample' or 'Second'. The default is 'Sample'.
		length : int, optional
			Number of timestamps or length of the timeline in samples.
			The default is 100.
		samplingRate : float, optional
			Sampling rate in [Hz]. During construction it has to be strictly 
			positive (>0). The default is 1 Hz.
		init : float, optional
			Init of the timeline in [seconds * 10^timeMultiplier].
			This is the value of the first timestamp, and it is relative
			to the startTime. The default is 0.
		end : float, optional
			End of the timeline in [seconds * 10^timeMultiplier].
			This is the value of the last timestamp, and it is relative
			to the startTime. The default is 99.
		timeMultiplier : float, optional
			Multiplier for timestamps [second] units in base 10.
			The default is 0 for full seconds (10^0).

		:Returns:
		
		None.

		'''
		#Figure out which parameters have been passed and the relation
		#between them.
		#
		# Note that if default values are indicated in the method signature
		#it will not be possible to distinguish which ones have been passed.
		#Hence, default values in the signature are indicated as None, and
		#later gave default values to the remaining non-set parameters here.
		#
		# Default values:
		# unit = 'Sample',
		# length = 100,
		# samplingRate = 1,
		# end = 99, #Note that default range goes from 0 to 99 (i.e. length = 100).
		# timeMultiplier = 0
		#
		flagLength = True #True if passed as parameter. False if not passed.
		if length is None:
			length = 100
			flagLength = False
		flagSamplingRate = True #True if passed as parameter. False if not passed.
		if samplingRate is None:
			samplingRate = 1
			flagSamplingRate = False
		flagEnd = True #True if passed as parameter. False if not passed.
		if end is None:
			end = 99
			flagEnd = False
		flagTimeMultiplier = True #True if passed as parameter. False if not passed.
		if timeMultiplier is None:
			timeMultiplier = 0
			flagTimeMultiplier = False
		#Now, try to make the best arrangement with what has been given.
		#Note that I never need to guess init. Either it is given, or fix to 0.
		#There are 16(=2^4) possible cases:
		if flagLength and flagSamplingRate and flagEnd and flagTimeMultiplier:
			#Everything has been set. Nothing to guess or tune.
			#Just check below that the relation holds.
			pass
		elif flagLength and flagSamplingRate and flagEnd and not flagTimeMultiplier:
			#Figure out the timeMultiplier
			timeMultiplier = math.log( (length-1) / ((end-init) * samplingRate ) ,10)
		elif flagLength and flagSamplingRate and not flagEnd and flagTimeMultiplier:
			#Figure out the end
			end = init + (length-1) / (samplingRate * 10**timeMultiplier)
		elif flagLength and flagSamplingRate and not flagEnd and not flagTimeMultiplier:
			#Fix the timeMultiplier to 0, and figure out the end
			end = init + (length-1) / (samplingRate * 10**timeMultiplier)
		elif flagLength and not flagSamplingRate and flagEnd and flagTimeMultiplier:
			#Figure out the samplingRate
			samplingRate = (length-1) / ((end-init) * 10**timeMultiplier)
		elif flagLength and not flagSamplingRate and flagEnd and not flagTimeMultiplier:
			#Fix the timeMultiplier to 0, and figure out the samplingRate
			samplingRate = (length-1) / ((end-init) * 10**timeMultiplier)
		elif flagLength and not flagSamplingRate and not flagEnd and flagTimeMultiplier:
			#Fix the samplingRate to 1, and figure out the end
			end = init + (length-1) / (samplingRate * 10**timeMultiplier)
		elif flagLength and not flagSamplingRate and not flagEnd and not flagTimeMultiplier:
			#Fix the timeMultiplier to 0, the samplingRate to 1, and figure out the end
			end = init + (length-1) / (samplingRate * 10**timeMultiplier)
		elif not flagLength and flagSamplingRate and flagEnd and flagTimeMultiplier:
			#Figure out the length
			length = int(1+ (end-init) * samplingRate * 10**timeMultiplier)
		elif not flagLength and flagSamplingRate and flagEnd and not flagTimeMultiplier:
			#Fix the timeMultiplier to 0 and figure out the length
			length = int(1+ (end-init) * samplingRate * 10**timeMultiplier)
		elif not flagLength and flagSamplingRate and not flagEnd and flagTimeMultiplier:
			#Fix the length to 100, and figure out the end
			end = init + (length-1) / (samplingRate * 10**timeMultiplier)
		elif not flagLength and flagSamplingRate and not flagEnd and not flagTimeMultiplier:
			#Fix the timeMultiplier to 0 and figure out the length
			length = int(1+ (end-init) * samplingRate * 10**timeMultiplier)
		elif not flagLength and not flagSamplingRate and flagEnd and flagTimeMultiplier:
			#Fix the samplingRate to 1 and figure out the length
			length = int(1+ (end-init) * samplingRate * 10**timeMultiplier)
		elif not flagLength and not flagSamplingRate and flagEnd and not flagTimeMultiplier:
			#Fix the the timeMultiplier to 0, the samplingRate to 1 and figure out the length
			length = int(1+ (end-init) * samplingRate * 10**timeMultiplier)
		elif not flagLength and not flagSamplingRate and not flagEnd and flagTimeMultiplier:
			#Fix the length to 100, the end to 100 and figure out the samplingRate
			samplingRate = (length-1) / ((end-init) * 10**timeMultiplier)
		elif not flagLength and not flagSamplingRate and not flagEnd and not flagTimeMultiplier:
			#Just leave default values
			pass
		
		
		#Call superclass constructor
		super().__init__() 
		
		self.__version = '0.1'

		
		#Check consistency of length, init, end, sampling rate and timeMultiplier
		assert samplingRate > 0, 'smTimline:__init__: Sampling rate must be strictly positive during construction.'
		assert ((end-init) > (((length-1) / (samplingRate * 10**timeMultiplier)) - (1/2*samplingRate)) \
		    and (end-init) < (((length-1) / (samplingRate * 10**timeMultiplier)) + (1/2*samplingRate))), \
			'smTimline:__init__: The chosen relation between length, end, timeMultiplier and sampling rate is inconsistent.'

		self.startTime = startTime #Absolute initial time.
		#Temporal measurement unit.
		self.__unit = smMeasurementUnit(name = 'Sample', acronym = 'sample',\
								 multiplier = 0, \
								 isInternationalSystem = False)
		if unit == 'Sample':
			pass
		elif unit == 'Second':
			self.__unit = smMeasurementUnit(name = 'Second', acronym = 's',\
								 multiplier = timeMultiplier, \
								 isInternationalSystem = True)
		else:
			msg = self.getClassName() + ':__init__: Unexpected parameter value for unit. Setting unit to ''Sample''.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)

		#Do not remove. Explicitly create the properties before the first call to setter.
		self.__samplingRate = samplingRate
		self.__timeMultiplier = timeMultiplier
		self.__timestamps = np.linspace(init, end, length, dtype=None)
		self.__conditions = set() #List of conditions
		self.__events = set()
		self.__conditionEventsMap = dict() #Pairing between conditions (keys)
										 #and list of associated events IDs (values)
										 #as a dictionary
		self.__overlapStatus = set() #Set of pairwise conditions overlapping status.
									#Pairs in this set are allowed to overlap.
									#A condition may or may not be allowed to
									#overlap with itself.
		
		return

	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	#Note that python does not have constants nor static constants,
	#so in order to have a constant, a new property is defined
	#with only a getter method and no setter.
	@property
	def OVERLAP(self): #OVERLAP getter
		'''
		Constant OVERLAP = True		
		Permits overlapping behaviour among conditions.
		
		:getter: Gets constant OVERLAP.
		:type: bool
		'''
		return True
	
	@property
	def NON_OVERLAP(self): #NON_OVERLAP getter
		'''
		Constant NON_OVERLAP = False		
		Forbids overlapping behaviour among conditions.
		
		:getter: Gets constant NON_OVERLAP.
		:type: bool
		'''
		return False
	


	@property
	def overlapStatus(self): #overlapStatus getter
		'''
		Set of pairwise conditions overlapping status.
		Pairs in this set are allowed to overlap, and pairs
		not in this list are automatically not allowed to overlap.
		
		A condition may or may not be allowed to overlap with itself.
		Conditions are by default not allowed to overlap with itself
		nor with other conditions.
		
		When setting a non-overlap status between conditions, the events of these
		conditions must not be in conflict, i.e. they must not overlap.
		Otherwise, an error is raised. Ensure that you remove all conflicts
		before setting the overlap between the conditions.
		
		:getter: Gets the overlapping status.
		:setter: Sets the overlapping status.
		:type: set of conditions id pairs.
			Each pair is a list of length 2 of int.
			Ids of conditions not declared in the timeline will be discarded.
			A list can also be provided, but duplicates will be ignored.
		
		.. seealso: :meth:`allowOverlap`, :meth:`forbidOverlap`,
			:attr:`OVERLAP`, :attr:`NON_OVERLAP`
		
		'''
		return copy.deepcopy(self.__overlapStatus)

	@overlapStatus.setter
	def overlapStatus(self,newOverlap): #overlapStatus setter
		if type(newOverlap) is list:
			newOverlap = set(newOverlap)
		if type(newOverlap) is not set:
			msg = self.getClassName() + ':allowOverlap: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Check that it is a set of pairs
		condid = [cond.id for cond in self.conditions];
		for elem in newOverlap:
			if not (type(elem) is list and len(elem)==2 \
				   and type(elem[0]) is int and type(elem[1]) is int):
				msg = self.getClassName() + ':allowOverlap: Unexpected attribute value. At least one element is not a pair of conditions ids.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
			#Discard those pairs which do contain the ID of a non contained condition
			if elem[0] not in condid or elem[1] not in condid:
				msg = self.getClassName() + ':allowOverlap: Inexistent id found. Ignoring entry ' + str(elem) + '.'
				warnings.warn(msg,SyntaxWarning)
				newOverlap.remove(elem)
			#Sort the pair by id
			elem.sort()
		#At this point, newOverlap contains for sure only a set of pairs of
		#existing IDs.
		try:
			self.__overlapStatus = copy.deepcopy(newOverlap)
			self._checkOverlapConflicts()
		except:
			raise
		return None


	@property
	def conditions(self): #conditions getter
		'''
		Set of conditions.
		
		Conditions are by default ***not*** allowed to overlap with itself
		nor with other conditions.
		
		:getter: Gets the set of conditions.
		:setter: Sets the set of conditions. Note that this will overwrite
			any existing condition. If you just want to add a new condition
			use :meth:`addConditions`. IF you just want to modify some but
			not all conditions, use :meth:`setConditions`
		:type: set of :class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
			A list may also be provided, but duplicates (same ID) will be ignored.
		
		.. seealso: :meth:`addConditions`, :meth:`setConditions`,
			:meth:`removeConditions`, :meth:`clearConditions`,
			:meth:`allowOverlap`, :meth:`forbidOverlap`,
		
		'''
		return copy.deepcopy(self.__conditions)

	@conditions.setter
	def conditions(self,newConditions): #conditions setter
		tmp = smTimelineCondition()
		if type(newConditions) is list:
			newConditions = set(newConditions)
		if type(newConditions) is not set:
			msg = self.getClassName() + ':conditions: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Ensure all are conditions and gather ids
		tmpID = list()
		for cond in newConditions:
			if str(cond.__class__) != str(tmp.__class__):
				msg = self.getClassName() + ':conditions: Unexpected attribute type. At least one element of conditions list is not a smTimelineCondition.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
			tmpID.append(cond.id)
		#Check for duplicate ids
		if len(set(tmpID)) == len(tmpID):
			#Without duplicates
			self.__conditions = copy.deepcopy(newConditions)
		else:
			#With duplicates
			msg = self.getClassName() + ':conditions: At least one repeated condition. Repeated conditions will be added only once.'
			warnings.warn(msg,SyntaxWarning)
			tmpID = set(tmpID)
			for cond in newConditions:
				if cond.id in tmpID:
					self.__conditions.append(copy.deepcopy(cond))
					self.__conditionsEventsMap[cond.id] = set()
					tmpID.remove(cond.id)
		return None




	@property
	def duration(self): #duration getter
		'''
		Duration of the :class:`smTimeline <scimeth.data.smTimeline>`.
		The duration is the :attr:`end`-:attr:`init` in
		[seconds * 10^:attr:`timeMultipler`].
		
		If :attr:`samplingRate` is strictly positive, then the 
		:class:`smTimeline <scimeth.data.smTimeline>` is uniformly sampled
		and :attr:`length`,:attr:`duration` and :attr:`samplingRate`
		are related by:
		
		* :attr:`samplingRate` = :attr:`duration` / ((:attr:`length` - 1) * 10^:attr:`timeMultiplier`)
		
		with a rounding error smaller than 1/(2*:attr:`samplingRate`).
		
		:attr:`duration` is a read-only property. If you need to alter
		the :attr:`duration` please consider changing either :attr:`init`,
		:attr:`end` or both.
		
		:getter: Gets the duration.
		:type: float
		'''
		return self.__timestamps[-1] - self.__timestamps[0]



	@property
	def end(self): #end getter
		'''
		End of the :class:`smTimeline <scimeth.data.smTimeline>`.
		The end is the value of the last timestamp in
		[seconds * 10^:attr:`timeMultipler`].
		
		If :attr:`samplingRate` is strictly positive, then the 
		:class:`smTimeline <scimeth.data.smTimeline>` is uniformly sampled
		and :attr:`length`,:attr:`init`,:attr:`end` and :attr:`samplingRate`
		are related by:
		
		* :attr:`samplingRate` = (:attr:`end`-:attr:`init`) / ((:attr:`length` - 1) * 10^:attr:`timeMultiplier`) = (:attr:`duration`) / ((:attr:`length` - 1) * 10^:attr:`timeMultiplier`)
		
		with a rounding error smaller than 1/(2*:attr:`samplingRate`).
		
		Changing the :attr:`end` may affect the :attr:`timestamps` and
		:attr:`events`.

		* In uniformly sampled timelines (i.e. :attr:`samplingRate` is
		  strictly positive `>0`), a new sampling rate and new timestamps
		  will be recalculated. :attr:`length` will be kept.
		
		* In non-uniformly sampled timelines, (i.e. :attr:`samplingRate` = -1),
		  the number of timestamps (:attr:`length`) will kept and
		  :attr:`timestamps` will be adjusted from the end to
		  guarantee that they are still positive (>=0), different and sorted.
		  Note that in this case, if the `newEnd` is smaller than
		  the minimum numeric representation (np.spacing(1)) times
		  the :attr:`length`, such invariant cannot be kept and an error
		  will be raised.
		
		***Note***: Changing the :attr:`end` may affect the associated
		:attr:`events`. If the `newEnd` is smaller than the previous one,
		then some events may be cropped or removed.
		Events with onsets beyond the `newEnd`
		will be removed. Events lasting beyond the `newEnd` will be
		cropped.
		
		
		:getter: Gets the end.
		:setter: Sets the end. Must be greater than :attr:`init`
		:type: float
		'''
		return self.__timestamps[-1]

	@end.setter
	def end(self,newEnd): #end setter
		if not isinstance(newEnd,(int,float)):
			msg = self.getClassName() + ':end: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newEnd<(self.timestamps[0]+np.spacing(1) * self.length):
			msg = self.getClassName() + ':end: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if self.samplingRate <= 0: #Non-uniformly space
			#No change in length, but amend timestamps if necessary
			#Generate the worst possible end for each timestamps 
			latestTimestamps = newEnd * np.ones(len(self.timestamps)) \
				- np.flip(np.spacing(1) * np.arange(0,len(self.timestamps),1))
			#Find timestamps beyond their latest possible values
			idx = np.argwhere(self.timestamps > latestTimestamps);
			#Substitute the offending timestamps
			self.__timestamps[idx] = latestTimestamps[idx]
			assert (self.__timestamps>=0).all(), \
				   self.getClassName() + ':end: newEnd is ' \
					   + 'smaller than the minimum numeric representation ' \
					   + '(np.spacing(1)) times the :attr:`length`.'
		else: #Uniformly space
			#Reestimate timestamps and samplingRate
			self.__timestamps = np.linspace(self.init, newEnd, self.length, dtype=None)
			self.__samplingRate = (self.length-1) /((newEnd-self.init) * 10**self.timeMultiplier)

		#Finally, remove or crop events as needed.
		self._trimEvents()
		return None

	@property
	def events(self): #events getter
		'''
		Set of events. This is a read-only property.
		
		To add or remove events, refer to :meth:`addEvents`,
		and :meth:`removeEvents`.
		
		To clear the set of events, refer to :meth:`clearEvents`
		
		.. seealso:: :meth:`addEvents`, :meth:`removeEvents`
					  and :meth:`clearEvents`
		
		:getter: Gets the set of events.
		:type: list of :class:`smTimelineEvent <scimeth.data.smTimelineEvent>`.
		'''
		return copy.deepcopy(self.__events)


	@property
	def init(self): #init getter
		'''
		Init of the :class:`smTimeline <scimeth.data.smTimeline>`.
		The init is the value of the first timestamp in
		[seconds * 10^:attr:`timeMultipler`].
		
		If :attr:`samplingRate` is strictly positive, then the 
		:class:`smTimeline <scimeth.data.smTimeline>` is uniformly sampled
		and :attr:`length`,:attr:`init`,:attr:`end` and :attr:`samplingRate`
		are related by:
		
		.. math::
			
			 samplingRate = (end-init) / ((length - 1) * 10^timeMultiplier)
			             &= (duration) / ((length - 1) * 10^timeMultiplier)
		
		with a rounding error smaller than 1/(2*:attr:`samplingRate`).
		
		Changing the :attr:`init` affects the :attr:`timestamps`. It
		shifts all timestamps by the difference between the `newInit`
		and the current :attr:`init`.
		
		Changing the :attr:`init` may affect the :attr:`events` of those
		moving to "negative" times or samples.

		Note that this affects the :attr:`end` but not the :attr:`duration`,
		and thus, if the 
		:class:`smTimeline <scimeth.data.smTimeline>` is uniformly sampled
		the above relation still holds.
		
		
		
		:getter: Gets the init.
		:setter: Sets the init.
		:type: float
		'''
		return self.__timestamps[0]

	@init.setter
	def init(self,newInit): #end setter
		if not isinstance(newInit,(int,float)):
			msg = self.getClassName() + ':end: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newInit<0:
			msg = self.getClassName() + ':end: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)

		shift = newInit - self.__timestamps[0]
		self.__timestamps = self.__timestamps + shift
		#Finally, shift and trim events
		self._shiftEvents(shift)

		return None

	@property
	def startTime(self): #startTime getter
		'''
		:class:`smTimeline <scimeth.data.smTimeline>` absolute start time.
		
		:getter: Gets the startTime.
		:setter: Sets the startTime.
		:type: :class:`datetime.datetime`
		'''
		return copy.deepcopy(self.__startTime)

	@startTime.setter
	def startTime(self,newInitTime): #startTime setter
		if not type(newInitTime) is datetime.datetime:
			msg = self.getClassName() + ':startTime: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__startTime = copy.deepcopy(newInitTime)
		return None


	@property
	def length(self): #length getter
		'''
		Number of samples of the :class:`smTimeline <scimeth.data.smTimeline>`.
		This is the number of :attr:`timestamps`.
		
		If :attr:`samplingRate` is strictly positive, then the 
		:class:`smTimeline <scimeth.data.smTimeline>` is uniformly sampled
		and :attr:`length`,:attr:`end`, :attr:`timeMultiplier` and
		:attr:`samplingRate` are related by:
		
		.. math::
			
			length = 1 + (end-init) / (samplingRate * 10^timeMultiplier)
		
		with a rounding error smaller than 1/(2*:attr:`samplingRate`).
		
		Changing the :attr:`length` affects the :attr:`timestamps` and
		hence :attr:`end`, :attr:`end` and :attr:`duration`.
		
		* If newLength is smaller than current length, timestamps
		  beyond current length will be removed. 
		
		* If newLength is greater than current length, new timestamps
		  will be added. 
		
		  * If the timeline is uniformly spaced (i.e. :attr:`samplingRate` is
		    strictly positive >0) then new timestamps are equispaced according
		    to the :attr:`samplingRate`
		  
		  * If the timeline is non-uniformly spaced (i.e. :attr:`samplingRate` = -1),
		    then new timestamps are added equispaced according to the mean
		    separation (average sampling rate) of previous timestamps.
		  
			
		In all cases, end will be updated accordingly to the
		value of the new last timestamp.
		
		***Note***: Changing the :attr:`length` may affect the :attr:`end`.
		If :attr:`samplingRate` is strictly positive, the :attr:`end`
		will be set accordingly.
		
		***Note***: Changing the :attr:`length` may affect the associated
		events :attr:`events`. Events with onsets beyond the newLength
		will be removed. Events lasting beyond the newLength will be
		cropped.
		
		:getter: Gets the length.
		:setter: Sets the length. newLength must be positive (>=0).
		:type: int
		'''
		return len(self.__timestamps)

	@length.setter
	def length(self,newLength): #length setter
		if not type(newLength) is int:
			msg = self.getClassName() + ':length: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newLength<=0:
			msg = self.getClassName() + ':length: Unexpected attribute value.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		if newLength < self.length:
			#Just crop
			self.__timestamps = np.resize(self.__timestamps,newLength)
		elif newLength > self.length:
			#Add new timestamps
			currLength = self.length
			currEnd = self.end
			self.__timestamps = np.resize(self.__timestamps,newLength)
			#Get or estimate the sampling rate
			if self.samplingRate > 0: #Uniformly spaced
				tmpSamplingRate = self.samplingRate
			else: #Non-uniformly spaced
				tmpSamplingRate = 1/np.average(np.diff(self.timestamps,n=1) * 10**self.timeMultiplier)
			self.__timestamps[currLength:] = currEnd + \
				(1/tmpSamplingRate) * np.arange(1, 1+newLength-currLength, 1, \
						dtype=None) #Timestamps in [seconds] (scaled by timestampsMultiplier)
		else:
			#Same length
			pass
		
		#Finally, remove or crop events as needed.
		self._trimEvents()
		return None

	@property
	def samplingRate(self): #samplingRate getter
		'''
		Sampling rate in [Hertz] at which samples are acquired.
		
		If :attr:`samplingRate` is strictly positive, then the
		:class:`smTimeline <scimeth.data.smTimeline>` is considered
		to be uniformly sampled. :attr:`timestamps` are equally spaced
		at `1/samplingRate`.
		There will be a relation (with 1/2*samplingRate tolerance) between
		:attr:`samplingRate`, :attr:`length`, :attr:`end`, and
		:attr:`timeMultiplier`:
		
		.. math::
			
			samplingRate = (length-1) / ((end-init) * 10^timeMultiplier)
		
		If :attr:`samplingRate` is negative or 0, then the
		:class:`smTimeline <scimeth.data.smTimeline>` is considered
		to be non-uniformly sampled, and :attr:`timestamps` do not
		follow any specific spacing.
		
		Altering the sampling rate in uniformly sampled
		mode (i.e. :attr:`samplingRate` > 0), updates all :attr:`timestamps`
		whilst maintaining the :attr:`length` and :attr:`init`.
		Attributes :attr:`end` and :attr:`duration` are however altered
		as appropriate.
		
		Altering the sampling rate in non-uniformly sampled
		mode (i.e. :attr:`samplingRate` = -1), does not affect
		:attr:`timestamps`, and hence the attributes :attr:`length`,
		:attr:`init`, :attr:`end` and :attr:`duration` are left unchanged.
		
		If `newSamplingRate` is negative or zero, it will automatically
		set to -1.
		
		:getter: Gets the sampling rate in [Hz].
		:setter: Sets the sampling rate in [Hz].
		:type: float
		'''
		return self.__samplingRate

	@samplingRate.setter
	def samplingRate(self,newSamplingRate, flagKeepLength = True): #onset setter
		if not isinstance(newSamplingRate,(int,float)):
			msg = self.getClassName() + ':samplingRate: Unexpected attribute type.'
			warnings.warn(msg,SyntaxWarning)
		newSamplingRate = float(newSamplingRate)
		if newSamplingRate>=0: #Uniformly spaced
			self.__samplingRate = newSamplingRate
			newEnd = self.init + (self.length-1) / (newSamplingRate * 10**self.timeMultiplier)
			self.__timestamps = np.linspace(self.init, newEnd, self.length, dtype=None)
		else:
			self.__samplingRate = -1
		return None

	@property
	def timeMultiplier(self): #timeMultiplier getter
		'''
		Time multiplier in base 10 in which the 
		:attr:`timestamps` are expressed.
		
		Changing the :attr:`timeMultiplier`
		automatically updates the :attr:`timestamps`.
		Note that the :attr:`end` is scaled accordingly.
		:attr:`events` are expressed in :attr:`unit` and hence are not
		affected.
		
		:getter: Gets the timeMultiplier.
		:setter: Sets the timeMultiplier.
		:type: float
		'''
		return self.__timeMultiplier

	@timeMultiplier.setter
	def timeMultiplier(self,newMultiplier): #timeMultiplier setter
		if not isinstance(newMultiplier,(int,float)):
			msg = self.getClassName() + ':timeMultiplier: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		newMultiplier = float(newMultiplier)
		#Adjust end and timestamps
		currMultiplier = self.__timeMultiplier
		self.__timestamps = self.timestamps / 10**(newMultiplier-currMultiplier)
		#...and set the new timeMultiplier
		self.__timeMultiplier = newMultiplier
		return None

	@property
	def timestamps(self): #timestamps getter
		'''
		List (numpy.array) of samples timestamps in [second * 10^:attr:`timeMultiplier`]
		
		Changing the :attr:`timestamps` affects the :attr:`length`
		:attr:`init`, :attr:`end`, :attr:`duration` and :attr:`samplingRate`
		of the :class:`smTimeline <scimeth.data.smTimeline>`.
		
		Timestamps will be automatically sorted, and duplicates eliminated.
		
		:getter: Gets the list of timestamps.
		:setter: Sets the list of timestamps.
		:type: :class:`np.array`
		'''
		return copy.deepcopy(self.__timestamps)

	@timestamps.setter
	def timestamps(self,newTimestamps): #timeMultiplier setter
		if type(newTimestamps) is list:
			#attempt to convert to np.array
			try:
				newTimestamps = np.array(newTimestamps).astype(float)
			except:
				msg = self.getClassName() + ':timestamps: Some elements of list timestamps may not be numeric.'
				warnings.warn(msg,SyntaxWarning)
				return None
		#WATCH OUT! nd.array dtypes are NOT really float but np.float64
		if not (type(newTimestamps) is np.ndarray \
			  and newTimestamps.ndim == 1):
			msg = self.getClassName() + ':timestamps: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		try:
			newTimestamps = newTimestamps.astype(float)
		except:
			msg = self.getClassName() + ':timestamps: Some elements of array timestamps may not be numeric.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__timestamps = np.unique(newTimestamps)
		#Estimate new sampling rate
		tmpSamplingRate = 1/np.average(np.diff(self.__timestamps,n=1) * 10**self.timeMultiplier)
		if (np.diff(self.__timestamps,n=1) < (1.5/tmpSamplingRate)).all():
			self.__samplingRate = tmpSamplingRate
		else:
			self.__samplingRate = -1 #Non-uniformly spaced
		#and remove or crop events as needed.
		self._trimEvents()
		return None

	@property
	def unit(self): #unit getter
		'''
		:class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>` in
		which the :attr:`onset` and
		:attr:`end` are expressed.

		Unit can only be either seconds (with a multiplier) or samples.
		Note that there is no setter method for attr:`unit`. Instead,
		the user can used :meth:`toSeconds` and :meth:`toSamples`
		to change the attr:`unit`.
		
		:getter: Gets the time measurement unit.
		:type: :class:`smMeasurementUnit <scimeth.data.smMeasurementUnit>`
		'''
		return copy.deepcopy(self.__unit)


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
			if attributename in ['conditions','events']:
				s = s + indentationLevel*'\t' + attributename + '\t= [\n'
				for elem in getattr(self,attributename):
					s = s + indentationLevel*'\t' + \
						elem.__str__(indentationLevel = indentationLevel + 1) \
						+ ',\n'
				s = s + indentationLevel*'\t' + ']\n'
			elif attributename == 'unit':
				s = s + indentationLevel*'\t' + inheritanceStr + attributename + '\t= ' + value.__str__(indentationLevel = indentationLevel + 1) + ';\n'
			else:
				s = s + indentationLevel*'\t' + inheritanceStr + attributename + '\t= ' + str(value) + ';\n'
		return s + indentationLevel*'\t' + '}>'

	#Protected methods
	def _checkOverlapConflicts(self):
		'''
		Check for any existing conflicts between events in non-overlapping
		:class:`smTimelineConditions <scimeth.data.smTimelineConditions>`.
		
		If any conflict is found an error is raised.
		'''
		#Get the list of non-overlapping pairs by complementing the
		#list of overlapping conditions.
		fullPairings = set(itertools.combinations(self.getConditionsID(), 2))
		nonOverlapping = fullPairings - self.overlapStatus
		
		#Check conflicts among non-overlapping pairs
		for elem in nonOverlapping:
			cond1events = self.getConditionsEvents(theConditions = elem[0])
			cond2events = self.getConditionsEvents(theConditions = elem[1])
			for ev1 in cond1events:
				for ev2 in cond2events:
					if ev1.hasOverlap(ev2):
						msg = self.getClassName() + ':allowOverlap: Conditions ' \
								+ elem[0] + ' and ' + elem[1] + \
								' have conflicting events. Resolve conflict before allowing overlap.'
						#warnings.warn(msg,SyntaxWarning)
						raise ValueError(msg)
		return None


	def _shiftEvents(self,shift):
		'''
		Shift :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		in the :class:`smTimeline <scimeth.data.smTimeline>`
		
		Shift events by a certain amount of samples or time.
		Events are trimmed after shfiting (see :meth:`_trimEvents`)
		
		'''
		#Remove or crop events as needed.
		for ev in self.events:
			ev.onset = ev.onset + shift
		self._trimEvents()
		return

	def _trimEvents(self):
		'''
		Trim :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		in the :class:`smTimeline <scimeth.data.smTimeline>`
		
		* Removes events whose onset are beyond the
		  :class:`smTimeline <scimeth.data.smTimeline>` :attr:`length`
		  (if the timeline :attr:`unit` is in 'Sample') or 
		  :attr:`end` (if the timeline :attr:`unit` is in 'Second')
		* Removes events whose end are before 0
		  (if the timeline :attr:`unit` is in 'Sample') or 
		  :attr:`init` (if the timeline :attr:`unit` is in 'Second')
		* Crop events whose end are beyond the
		  :class:`smTimeline <scimeth.data.smTimeline>` :attr:`length`
		  (if the timeline :attr:`unit` is in 'Sample') or 
		  :attr:`end` (if the timeline :attr:`unit` is in 'Second')
		* Crop events whose init are before 0
		  (if the timeline :attr:`unit` is in 'Sample') or 
		  :attr:`init` (if the timeline :attr:`unit` is in 'Second')
		
		'''
		#Remove or crop events as needed.
		if self.unit.name == 'Sample':
			for ev in self.events:
				if ev.onset > self.length or ev.end < 0: #Remove
					#Delete from conditions
					for cond in self.conditionEventsMap.iterkeys():
						if ev.id in self.conditionEventsMap[cond]:
							self.conditionEventsMap[cond].remove(ev.id)
					#and remove from the list of events
					self.events.remove(ev)
				if ev.end > self.length: #Crop
					ev.end = self.length
				if ev.init < 0: #Crop
					ev.init = 0
		else: #Units in 'Second'
			for ev in self.events:
				if ev.onset > self.end or ev.end < self.init: #Remove
					#Delete from conditions
					for cond in self.conditionEventsMap.iterkeys():
						if ev.id in self.conditionEventsMap[cond]:
							self.conditionEventsMap[cond].remove(ev.id)
					#and remove from the list of events
					self.events.remove(ev)
				if ev.end > self.end: #Crop
					ev.end = self.end
				if ev.init < self.init: #Crop
					ev.init = self.init
					
		return

	
	#Public methods
	def getClassName(self):
		'''Gets the class name.
		
		:return: The class name
		:rtype: str
		'''
		return type(self).__name__
	
	

	def addConditions(self,newConditions):
		'''Add a collection of
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` to the
		:class:`smTimeline <scimeth.data.smTimeline>`.
		
		The new conditions cannot have ID which may conflict with other
		conditions already included in the timeline.
		
		:Parameters:
		
		:param newConditions: Set of new
			:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		:type newConditions: set of :class:`smTimelineConditions <scimeth.data.smTimelineCondition>`.
			A list can be provided, but duplicates will be discarded.
			
		:return: None.
		:rtype: NoneType
		
		.. seealso:: :meth:`assignEvents`

		'''
		tmp = smTimelineCondition()
		if type(newConditions) is list:
			msg = self.getClassName() + ':addConditions: Converting list to set. Duplicate events will be discarded.'
			warnings.warn(msg,SyntaxWarning)
			newConditions = set(newConditions)
		elif str(newConditions.__class__) == str(tmp.__class__):
			#Wrap the single condition into a set.
			newConditions = {newConditions}
		if type(newConditions) is not set:
			msg = self.getClassName() + ':addConditions: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Check all are conditions
		for cond in newConditions:
			if str(cond.__class__) != str(tmp.__class__):
				msg = self.getClassName() + ':addConditions: Unexpected attribute type. At least one element of `newConditions` is not a `smTimelineCondition`.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
	
		#Merge sets of conditions excluding repeated conditions if any
			#Note that attempting a direct merge of sets:
			#   self.conditions.union(newConditions)
			#will only capture conditions that are the SAME object, but this is
			#insufficient since two different objects may still have the
			#same id.
		#Remove duplicate events with the same id
		seenIDs  = set([cond.id  for cond in self.conditions])
		seenTags = set([cond.tag for cond in self.conditions])
		flagSeenID  = False
		flagSeenTag = False
		#Python does not allow iterate over a set while changing its size,
		#so just create a copy for iterating over it, but still remove
		#from the original
		newConditions = copy.deepcopy(newConditions)
		for cond in newConditions:
			if cond.id in seenIDs:
				newConditions.remove(cond)
				flagSeenID = True
			else:
				seenIDs.add(cond.id)
			if cond.tag in seenTags:
				flagSeenTag = True
			else:
				seenTags.add(cond.tag)
		if flagSeenID is True:
				msg = self.getClassName() + ':addConditions: At least one new ' \
					'condition has a repeated id. Conditions with duplicate ' \
					'ids will be discarded.'
				warnings.warn(msg,SyntaxWarning)
		if flagSeenTag is True:
				msg = self.getClassName() + ':addConditions: At least one new ' \
					'condition has a repeated tag. Condition tags do not need ' \
					'to be unique within a timeline, however, it is a good ' \
					'practice to keep them distinct.'
				warnings.warn(msg,SyntaxWarning)
		#Update the remaining conditions
		self.__conditions = self.__conditions.union(newConditions)
		#Ensure there is the associated entry in the conditionEventsMap
		for cond in newConditions:
			try:
				self.__conditionEventsMap[cond.id] #If there is no such entry, it will raise a KeyError
			except:
				self.__conditionEventsMap[cond.id] = set()
		#In principle, there is no need to declare the condition neither
		#in the overlappingStatus.
		return None
		


	def addEvents(self,newEvents):
		'''Add a collection of
		:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` to the
		:class:`smTimeline <scimeth.data.smTimeline>`.
		
		The new events cannot have ID which may conflict with other
		events already included in the timeline.
		
		:Parameters:
		
		:param newEvents: Set of new
			:class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		:type newEvents: set of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`.
			A list can be provided, but duplicates will be discarded.
			A single event can be provided.
		
		:return: None.
		:rtype: NoneType
		
		.. seealso:: :meth:`assignEvents`
		
		'''
		tmp = smTimelineEvent()
		if str(newEvents.__class__) == str(tmp.__class__):
			newEvents = {newEvents}
		if (type(newEvents) is list):
			#msg = self.getClassName() + ':addEvents: Converting list to set. Duplicate events will be discarded.'
			#warnings.warn(msg,SyntaxWarning)
			newEvents = set(newEvents)
		if (type(newEvents) is not set):
			msg = self.getClassName() + ':addEvents: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Check all are events
		for ev in newEvents:
			if str(ev.__class__) != str(tmp.__class__):
				msg = self.getClassName() + ':addEvents: Unexpected attribute type. At least one element of `newEvents` is not a `smTimelineEvent`.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
	
		#Merge sets of events excluding repeated events if any
			#Note that attempting a direct merge of sets:
			#   self.events + newEvents
			#will only capture events that are the SAME object, but this is
			#insufficient since two different objects may still have the
			#same id.
		#Remove duplicate events with the same id
		seenIDs = set([ev.id for ev in self.events])
		flagSeenID = False
		#Python does not allow iterate over a set while changing its size,
		#so just create a copy for iterating over it, but still remove
		#from the original
		newEvents = copy.deepcopy(newEvents)
		for ev in newEvents:
			if ev.id in seenIDs:
				newEvents.remove(ev)
				flagSeenID = True
			else:
				seenIDs.add(ev.id)
		if flagSeenID is True:
				msg = self.getClassName() + ':addEvents: At least one new event has a repeated id. Events with duplicate ids will be discarded.'
				warnings.warn(msg,SyntaxWarning)
		#Finally, update the remaining events
		self.__events = self.events.union(newEvents)
		return None
		

	def allowOverlap(self,newOverlap):
		'''
		Add pairs of
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`' ids
		allow to overlap.
		
		If any pair of conditions were already allow to overlap, this status
		remain unchanged. 
		
		Pairs including one or two ids corresponding to
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		not declared in the
		:class:`smTimeline <scimeth.data.smTimeline>` will be ignored.
		
		.. seealso:: :attr:`overlapStatus`, :meth:`forbidOverlap`
		
		:Parameters:
		
		:param newOverlap: Set of pairs of conditions' ids.
		:type newOverlap: set of pairs. Each pair is a list of ids.
			A list can also be provided, but duplicates will be ignored.
		'''
		if type(newOverlap) is list:
			newOverlap = set(newOverlap)
		if type(newOverlap) is not set:
			msg = self.getClassName() + ':allowOverlap: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Check that it is a set of pairs
		condid = [cond.id for cond in self.conditions];
		newOverlap = copy.deepcopy(newOverlap)
		for elem in newOverlap:
			if not (type(elem) is list and len(elem)==2 \
				   and type(elem[0]) is int and type(elem[1]) is int):
				msg = self.getClassName() + ':allowOverlap: Unexpected attribute value. At least one element is not a pair of conditions ids.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
			#Discard those pairs which do contain the ID of a non contained condition
			if elem[0] not in condid or elem[1] not in condid:
				msg = self.getClassName() + ':allowOverlap: Inexistent id found. Ignoring entry ' + str(elem) + '.'
				warnings.warn(msg,SyntaxWarning)
				newOverlap.remove(elem)
			#Sort the pair by id
			elem.sort()

		#At this point, newOverlap contains for sure only a set of pairs of
		#existing IDs.
		try:
			self.__overlapStatus = self.__overlapStatus.union(newOverlap)
			self._checkOverlapConflicts()
		except:
			raise

		return None

	def associateEvents(self,eventsIDSet = set(), conditionsIDSet = set()):
		'''
		Link :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` to
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`.
		
		All events will be linked to all conditions.
		
		IDs of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` or
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` 
		which do not already exist in the
		:class:`smTimeline <scimeth.data.smTimeline>` will be ignored.
		
		:Parameters:
		
		:param eventsIDSet: Set of events' id.
		:type eventsIDSet: set of int
			A list can also be provided but duplicates will be ignored.
		:param conditionsIDSet: Set of conditions' id.
		:type conditionsIDSet: set of int
			A list can also be provided but duplicates will be ignored.

		:return: None.
		:rtype: NoneType
		
		.. seealso:: :meth:`deassignEvents`

		'''
		#Check entries
		if type(eventsIDSet) is list:
			eventsIDSet = set(eventsIDSet)
		if type(eventsIDSet) is not set:
			msg = self.getClassName() + ':deassignEvents: Unexpected attribute type for parameter eventsIDSet.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		for elem in eventsIDSet:
			if type(elem) is not int:
				msg = self.getClassName() + ':deassignEvents: Unexpected attribute value. At least one event ID is not an int.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
		if type(conditionsIDSet) is list:
			conditionsIDSet = set(conditionsIDSet)
		if type(conditionsIDSet) is not set:
			msg = self.getClassName() + ':deassignEvents: Unexpected attribute type for parameter conditionsIDSet.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		for elem in conditionsIDSet:
			if type(elem) is not int:
				msg = self.getClassName() + ':deassignEvents: Unexpected attribute value. At least one condition ID is not an int.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
		#Discard entries not already in the timeline
		eventsIDSet     = copy.deepcopy(eventsIDSet)
		conditionsIDSet = copy.deepcopy(conditionsIDSet)
		eventsIDs = set([ev.id for ev in self.events])
		existingEvents = set(eventsIDSet).intersection(eventsIDs)
		conditionsIDs  = set([cond.id for cond in self.conditions])
		existingConditions = set(conditionsIDSet).intersection(conditionsIDs)
		#Now is a matter of pairing the existingEvents with those in existingConditions
		try:
			for condid in existingConditions:
				self.__conditionEventsMap[condid] = self.__conditionEventsMap[condid].union(existingEvents)
			self._checkOverlapConflicts()
		except:
			raise
		return None
		


	
	def clearConditions(self):
		'''Remove all
		:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` from the
		:class:`smTimeline <scimeth.data.smTimeline>`.
		'''
		#Reset the list of conditions
		self.__conditions = set()
		#and clear associations with conditions.
		self.__conditionEventsMap = dict()
		self.__overlappingStatus = set()
		return None

	
	def clearEvents(self):
		'''Remove all
		:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` from the
		:class:`smTimeline <scimeth.data.smTimeline>`.
		'''
		#Reset the list of events
		self.__events = set()
		#and clear associations with conditions.
		for k in self.conditionEventsMap.iterkeys():
			self.conditionEventsMap[k] = set()
		return None


	def dissociateEvents(self,eventsIDSet = set(), conditionsIDSet = set()):
		'''
		Unlinks :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` from
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`.
		
		All events will be unlinked from all conditions.
		
		IDs of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>` or
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>` 
		which do not already exist in the
		:class:`smTimeline <scimeth.data.smTimeline>` will be ignored.
		
		:Parameters:
		
		:param eventsIDSet: Set of events' id.
		:type eventsIDSet: set of int
			A list can also be provided but duplicates will be ignored.
		:param conditionsIDSet: Set of conditions' id.
		:type conditionsIDSet: set of int
			A list can also be provided but duplicates will be ignored.

		:return: None.
		:rtype: NoneType
		
		.. seealso:: :meth:`assignEvents`

		'''
		#Check entries
		if type(eventsIDSet) is list:
			eventsIDSet = set(eventsIDSet)
		if type(eventsIDSet) is not set:
			msg = self.getClassName() + ':assignEvents: Unexpected attribute type for parameter eventsIDSet.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		for elem in eventsIDSet:
			if type(elem) is not int:
				msg = self.getClassName() + ':assignEvents: Unexpected attribute value. At least one event ID is not an int.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
		if type(conditionsIDSet) is list:
			conditionsIDSet = set(conditionsIDSet)
		if type(conditionsIDSet) is not set:
			msg = self.getClassName() + ':assignEvents: Unexpected attribute type for parameter conditionsIDSet.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		for elem in conditionsIDSet:
			if type(elem) is not int:
				msg = self.getClassName() + ':assignEvents: Unexpected attribute value. At least one condition ID is not an int.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
		#Discard entries not already in the timeline
		eventsIDSet     = copy.deepcopy(eventsIDSet)
		conditionsIDSet = copy.deepcopy(conditionsIDSet)
		eventsIDs = set([ev.id for ev in self.events])
		existingEvents = set(eventsIDSet).intersection(eventsIDs)
		conditionsIDs  = set([cond.id for cond in self.conditions])
		existingConditions = set(conditionsIDSet).intersection(conditionsIDs)
		#Now is a matter of pairing the existingEvents with those in existingConditions
		for condid in existingConditions:
			self.__conditionEventsMap[condid] = self.__conditionEventsMap[condid].remove(existingEvents)
		return None
		



	def forbidOverlap(self,forbidOverlap):
		'''
		Forbid pairs of
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`' ids
		allow to overlap.
		
		If any pair of conditions were already allow to overlap, this status
		remain unchanged. 
		
		If any pair contains two
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		which have associated overlapping
		:class:`smTimelineEvents <scimeth.data.smTimelineEvent>`,
		an error will be raised.
		
		
		Pairs including one or two ids corresponding to
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		not declared in the
		:class:`smTimeline <scimeth.data.smTimeline>` will be ignored.
		
		.. seealso:: :attr:`overlapStatus`, :meth:`forbidOverlap`
		
		:Parameters:
		
		:param forbidOverlap: Set of pairs of conditions' ids.
		:type forbidOverlap: set of pairs. Each pair is a list of ids.
			A list can also be provided, but duplicates will be ignored.
		'''
		if type(forbidOverlap) is list:
			forbidOverlap = set(forbidOverlap)
		if type(forbidOverlap) is not set:
			msg = self.getClassName() + ':forbidOverlap: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Check that it is a set of pairs
		condid = [cond.id for cond in self.conditions];
		forbidOverlap = copy.deepcopy(forbidOverlap)
		for elem in forbidOverlap:
			if not (type(elem) is list and len(elem)==2 \
				   and type(elem[0]) is int and type(elem[1]) is int):
				msg = self.getClassName() + ':forbidOverlap: Unexpected attribute value. At least one element is not a pair of conditions ids.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
			#Discard those pairs which do contain the ID of a non contained condition
			if elem[0] not in condid or elem[1] not in condid:
				msg = self.getClassName() + ':forbidOverlap: Inexistent id found. Ignoring entry ' + str(elem) + '.'
				warnings.warn(msg,SyntaxWarning)
				forbidOverlap.remove(elem)
			#Sort the pair by id
			elem.sort()
			
		#At this point, forbidOverlap contains for sure only a set of pairs of
		#existing IDs to be removed from the list of overlapping pairs.
		try:
			self.__overlapStatus = self.__overlapStatus.difference(forbidOverlap)
			self._checkOverlapConflicts()
		except:
			raise

		return None


	def getConditions(self,idSet = None):
		'''Retrieve the set of
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		with the given IDs.
		
		:Parameters:
		
		:param idSet: Set of conditions' IDs. If empty, all conditions
			will be retrieved.
		:param idSet: set.
			A list may also be provided, but only one copy of the conditions
			will be returned if any is repeated.
		
		:returns: set of :class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		:rtype: set
		'''
		if idSet is None:
			return self.events
		if idSet is list:
			idSet = set(idSet)
		theConditions = set()
		for id in idSet:
			for cond in self.conditions:
				if type(cond) is not int:
					msg = self.getClassName() + ':getConditions: Unexpected id type. Ignoring element.'
					warnings.warn(msg,SyntaxWarning)
				elif cond.id == id:
					theConditions.add(cond)
					break
		return copy.deepcopy(theConditions)


	def getConditionsID(self):
		'''Get the set of conditions' id.
		
		:return: The set of id from the conditions
		:rtype: set
		'''
		return set([cond.id for cond in self.conditions])

	def getConditionsEvents(self, theConditions = None):
		'''Get the set of events associated to the conditions.
		
		Unrecognised conditions will be ignored.
		
		:Parameters:
		
		:param theConditions: Set of
			:class:`smTimelineConditions <sm.data.smTimelineCondition>`
			or conditions' id
		:type theConditions: set
			A list may also be provided but duplicates will be ignored.
			A single condition can be provided.
			
		:return: The set of 
			:class:`smTimelineEvents <sm.data.smTimelineEvent>` of the 
			:class:`smTimelineConditions <sm.data.smTimelineCondition>`
		:rtype: set
		'''
		tmp = smTimelineCondition()
		if str(theConditions.__class__) == str(tmp.__class__): #if only one condition is passed.
			theConditions = {theConditions}
		if type(theConditions) is list:
			theConditions = set(theConditions)
		if type(theConditions) is not set:
			msg = self.getClassName() + ':getConditionsEvents: Unexpected parameter type for parameter theConditions.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		#Check all elements are conditions or ids and gather the ids.
		theConditionsIDs = set()
		for elem in theConditions:
			if str(elem.__class__) == str(tmp.__class__):
				theConditionsIDs.add(elem.id)
			elif type(elem) is int:
				theConditionsIDs.add(elem)
			else:
				msg = self.getClassName() + ':getConditionsEvents: Unexpected parameter value for parameter theConditions. At least one element is not a condition or condition id.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
		#Discard those which may not be declared
		condid = set([cond.id for cond in self.__conditions])
		theConditionsIDs = theConditionsIDs.intersection(condid)
		if len(theConditionsIDs) != len(theConditions):
			msg = self.getClassName() + ':getConditionsEvents: Duplicate conditions found. Ignoring duplicate conditions.'
			warnings.warn(msg,SyntaxWarning)
		#Collect the events id from the conditionEventsMap
		theEventsIDs = set()
		for condid in theConditionsIDs:
			theEventsIDs = theEventsIDs.union(self.__conditionEventsMap[condid])
		#Finally retrieve the events
		return self.getEvents(theEventsIDs)


	def getEvents(self,idSet = None):
		'''Retrieve the set of
		:class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		with the given IDs.
		
		:Parameters:
		
		:param idSet: Set of events' IDs. If empty, all events
			will be retrieved.
		:param idSet: set.
			A list may also be provided, but only one copy of the events
			will be returned if any is repeated.
		
		:returns: set of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		:rtype: set
		'''
		if type(idSet) is list:
			idSet = set(idSet)
		if type(idSet) is not set:
			msg = self.getClassName() + ':getEvents: Unexpected parameter type for parameter idSet.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		flagNotID = False
		theEvents = set()
		for oid in idSet:
			if type(oid) is not int:
				flagNotID = True
			else:
				flagFound = False
				for ev in self.__events:
					if ev.id == oid:
						theEvents.add(ev)
						flagFound = True
						break
				if not flagFound:
					msg = self.getClassName() + ':getEvents: Id ' + str(oid) + \
							' not found. Ignoring unrecognized events ids.'
					warnings.warn(msg,SyntaxWarning)
		if flagNotID:
			msg = self.getClassName() + ':getEvents: Unexpected parameter value for parameter idSet. At least one element is not an ID. Ignoring non ID elements.'
			warnings.warn(msg,SyntaxWarning)
			
		return copy.deepcopy(theEvents)
		

	def getEventsID(self):
		'''Get the set of events' id.
		
		:return: The set of id from the events
		:rtype: set
		'''
		return set([ev.id for ev in self.events])


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

		Boolean. True if both objects have the same information.
		False otherwise.

		'''
		res = True
		res = res & (str(self.__class__) == str(obj2.__class__))
		if not res:
			return res
		

		res = res & (self.id == obj2.id)
		res = res & (self.startTime == obj2.startTime).all
		res = res & (self.samplingRate == obj2.samplingRate)
		res = res & (self.unit.isEqual(obj2.unit))
		
		res = res & (self.timestamps == obj2.timestamps).all


		res = res & (self.conditions == obj2.conditions)
		res = res & (self.events == obj2.events)
		res = res & (self.overlappingStatus == obj2.overlappingStatus).all
		res = res & (self.conditionEventsMap == obj2.conditionEventsMap )
		
		return res


	def removeConditions(self,theConditions):
		'''Remove the 
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		from the
		:class:`smTimeline <scimeth.data.smTimeline>`.
		
		:Parameters:
		
		:param theConditions: Set of conditions to be removed. It can be
			provided as a collection of conditions' ids (int) or
			:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`,
		:type theConditions: set
			A list can also be provided.
		'''
		if type(theConditions) is list:
			theConditions = set(theConditions)
		if type(theConditions) is not set:
			msg = self.getClassName() + ':removeEvents: Unexpected parameter type.'
			raise ValueError(msg)
		
		#Collect the ids
		tmp = smTimelineEvent()
		tmpIDs = set()
		for cond in theConditions:
			if type(cond) is int:
				tmpIDs.add(cond)
			elif str(cond.__class__) == str(tmp.__class__):
				tmpIDs.add(cond.id)
			else:
				msg = self.getClassName() + ':removeConditions: Unexpected id type. Ignoring element.'
				warnings.warn(msg,SyntaxWarning)
		
		#Remove conditions
			#A simple substraction of sets won't work, as it will
			#only remove objects that are equal the SAME, and not
			#different objects with the same id.
		#self.conditions = self.conditions - theConditions
		for cond in self.conditions:
			if cond.id in tmpIDs:
				self.conditions.remove(cond)
				#and clear its entry in the conditionsEventsMap
				del self.conditionEventsMap[cond.id]
		return None


	def removeEvents(self,theEvents):
		'''Remove the 
		:class:`smTimelineEvents <scimeth.data.smTimelineEvent>` from the
		:class:`smTimeline <scimeth.data.smTimeline>`.
		
		:Parameters:
		
		:param theEvents: Set of events to be removed. It can be
			provided as a collection of events' ids (int) or
			:class:`smTimelineEvents <scimeth.data.smTimelineEvent>`,
		:type theEvents: set
			A list can also be provided.
		'''
		if type(theEvents) is list:
			theEvents = set(theEvents)
		if type(theEvents) is not set:
			msg = self.getClassName() + ':removeEvents: Unexpected parameter type.'
			raise ValueError(msg)
		
		#Collect the ids
		tmpIDs = set()
		for ev in theEvents:
			if type(ev) is int:
				tmpIDs.add(ev)
			elif type(ev) is smTimelineEvent:
				tmpIDs.add(ev.id)
			else:
				msg = self.getClassName() + ':removeEvents: Unexpected id type. Ignoring element.'
				warnings.warn(msg,SyntaxWarning)

		#Remove events
			#A simple substraction of sets won't work, as it will
			#only remove objects that are equal the SAME, and not
			#different objects with the same id.
		#self.events = self.events - theEvents
		for ev in self.events:
			if ev.id in tmpIDs:
				self.events.remove(ev)
		#and clear associations with conditions.
		for k in self.conditionEventsMap.iterkeys():
			self.conditionEventsMap[k] = self.conditionEventsMap[k].difference(tmpIDs)
		return None
	

	def setConditions(self,conditionsIDSet,newConditions):
		'''
		Updates a (sub-)set of existing conditions.
		
		This methods replaces some condition with new ones. Conditions can
		be fully updated including their :attr:`id`. The updated conditions
		keep their assigned events.
		
		**IMPORTANT**: This method does **NOT** alter the events.
		
		If you are planning to overwrites all conditions you can
		directly assign the new set to the :attr:`conditions` attribute,
		but beware that in that case, associated events are cleared.
		
		:Example:
		
		.. code-block::
		
			>>> theTimeline.conditions = conditionsSet
		
		
		:Parameters:
		
		:param conditionsIDSet: The list of conditions' id of the conditions
			to be modified. If any of id does not correspond to an existing
			condition, the id and its companion condition in 
			`newConditions` will be ignored
		:type conditionsIDSet: list of int.
			The order is important as conditions will be paired to those
			in newConditions in the same order as declared.
			For updating only one condition, a single `id` (int) can also be provided.
		:param newConditions: A list of new conditions to substitute
			existing ones.
		:type newConditions: list of :class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
			For updating only one condition, a single 
			:class:`smTimelineCondition <scimeth.data.smTimelineCondition>` 
			can also be provided.
			The length of `conditionsIDSet` and `newConditions`
			must be the same.
		
		:return: None
		:rtype: NoneType
		'''
		tmp = smTimelineCondition()
		if type(conditionsIDSet) is int:
			conditionsIDSet = [conditionsIDSet]
		if type(conditionsIDSet) is not list:
			msg = self.getClassName() + ':setConditions: Unexpected parameter ''conditionsIDSet'' type.'
			raise ValueError(msg)
		if str(newConditions.__class__) == str(tmp.__class__):
			newConditions = [newConditions]
		if type(newConditions) is not list:
			msg = self.getClassName() + ':setConditions: Unexpected parameter ''newConditions'' type.'
			raise ValueError(msg)
		if len(conditionsIDSet) != len(newConditions):
			msg = self.getClassName() + ':setConditions: Unexpected parameter ' \
					+ 'value. ''conditionsIDSet'' and ''newConditions'' ought ' \
					+ 'to have the same number of elements.'
			raise ValueError(msg)
		for elem in conditionsIDSet:
			if type(elem) is not int:
				msg = self.getClassName() + ':setConditions: Unexpected ' \
					+ 'parameter value. At least one element of ''conditionsIDSet'' ' \
					+ 'is not an int.'
				raise ValueError(msg)
		for cond in newConditions:
			if str(cond.__class__) != str(tmp.__class__):
				msg = self.getClassName() + ':setConditions: Unexpected ' \
					+ 'parameter value. At least one element of ''newConditions'' ' \
					+ 'is not a ''smTimelineCondition''.'
				raise ValueError(msg)
		
		newConditions = copy.deepcopy(newConditions)
		tmpCondIds = self.getConditionsID()
		for idx, elem in enumerate(conditionsIDSet):
			if elem in tmpCondIds: #Check that the condition exist
				for cond in self.__conditions:
					if elem == cond.id: #condition found
						#Check that the new id
						#does not conflict other existing IDs in the timeline.
						reducedCondIds = copy.deepcopy(tmpCondIds)
						reducedCondIds.remove(cond.id)
						if newConditions[idx].id in reducedCondIds:
							msg = self.getClassName() + ':setConditions: New ' \
								+ 'id ' + str(newConditions[idx].id) \
								+ ' already exist in smTimeline.'
							warnings.warn(msg,RuntimeWarning)
						else:
							#Substitute the condition
							self.__conditions.remove(cond)
							self.__conditions.add(newConditions[idx])
							if cond.id != newConditions[idx].id:
								#Change the entry in the conditionsEventsMap
								#Note that dictionary keys cannot be changed. One can
								#only copy to a new copy a remove the old one.
								self.__conditionEventsMap[newConditions[idx].id] = \
									 self.__conditionEventsMap[cond.id]
								del self.__conditionEventsMap[cond.id]
								#and update the overlapStatus
								for pair in self.__overlapStatus:
									if pair[0] == cond.id:
										pair[0] == newConditions[idx].id
									if pair[1] == cond.id:
										pair[1] == newConditions[idx].id
						break
			else:
				msg = self.getClassName() + ':setConditions: Id ' \
							+ str(elem) + ' not found in smTimeline.'
				warnings.warn(msg,RuntimeWarning)
		return None


	def setEvents(self,eventsIDSet,newEvents):
		'''
		Updates a (sub-)set of existing events.
		
		This methods replaces some events with new ones. Events can
		be fully updated including their :attr:`id`. The updated events
		do not change their assignments to conditions.
		
		**IMPORTANT**: This method does **NOT** alter the conditions.
		
		If any updated event violates the overlapping status, an
		error is raised.
		
		
		:Parameters:
		
		:param eventsIDSet: The list of events' id of the events
			to be modified. If any of id does not correspond to an existing
			event, the id and its companion event in 
			`newEvents` will be ignored
		:type eventsIDSet: list of int.
			The order is important as events will be paired to those
			in newEvents in the same order as declared.
			For updating only one event, a single `id` (int) can also be provided.
		:param newEvents: A list of new events to substitute
			existing ones.
		:type newEvents: list of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
			For updating only one event, a single 
			:class:`smTimelineEvent <scimeth.data.smTimelineEvent>`
			can also be provided.
			The length of `eventsIDSet` and `newEvents`
			must be the same.
		
		:return: None
		:rtype: NoneType
		'''
		tmp = smTimelineEvent()
		if type(eventsIDSet) is int:
			eventsIDSet = [eventsIDSet]
		if type(eventsIDSet) is not list:
			msg = self.getClassName() + ':setEvents: Unexpected parameter ''eventsIDSet'' type.'
			raise ValueError(msg)
		if str(newEvents.__class__) == str(tmp.__class__):
			newEvents = [newEvents]
		if type(newEvents) is not list:
			msg = self.getClassName() + ':setEvents: Unexpected parameter ''newEvents'' type.'
			raise ValueError(msg)
		if len(eventsIDSet) != len(newEvents):
			msg = self.getClassName() + ':setEvents: Unexpected parameter ' \
					+ 'value. ''eventsIDSet'' and ''newEvents'' ought ' \
					+ 'to have the same number of elements.'
			raise ValueError(msg)
		for elem in eventsIDSet:
			if type(elem) is not int:
				msg = self.getClassName() + ':setEvents: Unexpected ' \
					+ 'parameter value. At least one element of ''eventsIDSet'' ' \
					+ 'is not an int.'
				raise ValueError(msg)
		for ev in newEvents:
			if str(ev.__class__) != str(tmp.__class__):
				msg = self.getClassName() + ':setEvents: Unexpected ' \
					+ 'parameter value. At least one element of ''newEvents'' ' \
					+ 'is not a ''smTimelineEvent''.'
				raise ValueError(msg)
		
		newEvents = copy.deepcopy(newEvents)
		tmpEvIds = self.getEventsID()
		try:
			for idx, elem in enumerate(eventsIDSet):
				if elem in tmpEvIds:
					for ev in self.__events:
						if elem == ev.id:
							#Substitute the condition
							self.__events.remove(ev)
							self.__events.add(newEvents[idx])
							if ev.id != newEvents[idx].id:
								#Update the entries in the conditionsEventsMap
								for key, values in self.__conditionEventsMap.items():
									#Substitute the id in the values and update the dictionary
									values.remove(ev.id)
									values.add(newEvents[idx].id)
									self.__conditionEventsMap[key] = values
			self._checkOverlapConflicts()
		except:
			raise
		return None


	@staticmethod
	def sortTimelineEventsById(theEvents):
		'''
		Sort a list of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`
		by id (Note that id is unique.)
		
		:Example:
			
			Let be the events A=(id=1, onset = 2, end =3),
			B=(id=2, onset = 1, end =3),
			C=(id=3, onset = 2, end =2) and
			D=(id=4, onset = 2, end =3)
			
			Then, the order is A<B<C<D.

		:Parameters:

		theEvents : List of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`
			The list of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>` to be sorted.

		:Returns:

		The sorted list of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`.

		'''
		#Sort in inverse order, first by id, then by end and finally
		#by onset
		return quick_sort(theEvents, 0, len(theEvents) - 1, lambda x, y: x.id < y.id)

	def sortTimelineEventsByOnset(theEvents):
		'''
		Sort a list of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`
		first by onset and later by end. Events with the same onset and
		end are further ordered by id (Note that id is unique.)
		
		:Example:
			
			Let be the events A=(id=1, onset = 2, end =3),
			B=(id=2, onset = 1, end =3),
			C=(id=3, onset = 2, end =2) and
			D=(id=4, onset = 2, end =3)
			
			Then, the order is B<C<A<D.

		:Parameters:

		theEvents : List of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`
			The list of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>` to be sorted.

		:Returns:

		The sorted list of :class:`smTimelineEvents <scimeth.data.smTimelineEvents>`.

		'''
		#Sort in inverse order, first by id, then by end and finally
		#by onset
		theEvents = quick_sort(theEvents, 0, len(theEvents) - 1, lambda x, y: x.id < y.id)
		theEvents = quick_sort(theEvents, 0, len(theEvents) - 1, lambda x, y: x.end < y.end)
		return quick_sort(theEvents, 0, len(theEvents) - 1, lambda x, y: x.onset < y.onset)


	def toSeconds(self):
		'''
		The events units are updated to [second * 10^:attr:`timeMultiplier`].
		
		* If :attr:`unit` is in 'Sample', then:
		
		  * Events :attr:`onset` take the value of the onset-th :attr:`timestamps`.
		  * Events :attr:`end` take the value of the (onset+end)-th
		    :attr:`timestamps` minus the new onset.
		
		* If :attr:`unit` is in 'Second', then the events unit multiplier
		  is updated to :attr:`timeMultiplier` (the same scale as the timestamps),
		  and the events :attr:`onset` and :attr:`duration` are scaled
		  accordingly.
		
		'''
		if self.unit.name == 'Sample':
			for ev in self.events:
				ev.toSeconds(samplingRate = self.samplingRate, \
							newMultiplier = self.unit.multiplier)
		else: #Seconds
			for ev in self.events:
				ev.unit.multiplier = self.timeMultiplier - ev.unit.multiplier
		
		self.__unit = smMeasurementUnit(name='Second',acronym='s', \
								 multiplier = self.timeMultiplier, \
								 isInternationalSystem = True)

		
		return
		

	def toSamples(self):
		'''
		The events units are updated to [samples].
		
		* If :attr:`unit` is already in 'Sample', then nothing is change.
		* If :attr:`unit` is in 'Second':
		
		  * Events :attr:`onset` take the value of the index to the 
		    :attr:`timestamps` closest to the current onset.
		  * Events :attr:`end` take the value of the difference
		    of indexes in the :attr:`timestamps` between the event end
		    and onset.

		'''
		if self.unit.name == 'Second':
			for ev in self.events:
				ev.toSamples(samplingRate = self.samplingRate)
		self.__unit = smMeasurementUnit(name='Sample',acronym='sample', \
								 multiplier = 0, \
								 isInternationalSystem = False)
		return

