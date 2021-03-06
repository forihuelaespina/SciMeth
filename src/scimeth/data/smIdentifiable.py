# -*- coding: utf-8 -*-
#
#File: smIdentifiable.py
#
"""
Created on Sun Mar 22 10:23:14 2020

Module ***smIdentifiable***

This module declares the mixin class ***smIdentifiable***




:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 22-Mar-2020 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 29-Mar-2020 | FOE    | - Separated module comments from class comments.     |
+-------------+--------+------------------------------------------------------+
|  5-May-2020 | FOE    | - Added comment to clearly separate this ID from     |
|             |        |   from python built-in `id()`.                       |
+-------------+--------+------------------------------------------------------+
|  8-May-2020 | FOE    | - Improved comments further clarifying the           |
|             |        |   distinction between this ID and python built-in    |
|             |        |   `id()`.                                            |
+-------------+--------+------------------------------------------------------+
| 13-May-2020 | FOE    | - Improved mixin behaviour.                          |
|             |        | - The nextID is now per subclass rather than global. |
+-------------+--------+------------------------------------------------------+
| 14-Mar-2020 | FOE    | - :meth:`__str__` now now admits parameter           |
|             |        |   `indentationLevel`.                                |
+-------------+--------+------------------------------------------------------+


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
#import warnings
#import deprecation

#import os


#from scimeth import __version__
#from scimeth import data as scimeth


## Class definition
class smIdentifiable:
	#Sphinx documentation
	"""Objects that are :class:`smIdentifiable <scimeth.data.smIdentifiable>`
	are constructred with an integer attribute :attr:`id`.
	
	Identifiable objects have a numerical ID attribute. The
	used given to the numerical id depends on both the identifiable object
	itself, and perhaps a potential container class. Exemplary uses are:
	
	* A container class can use the :attr:`id` attribute as a kind
	  of primary key, so that within the container, the object
	  :attr:`id` is unique among other instances.
	  Note that it is the container which must guarantee the uniqueness.
	* A relation of order among objects of the same class can easily
	  be established based on the :attr:`id`.
	  
	When intended use is related to uniqueness, ID should be set upon object
	construction and (to facilitate uniqueness) it is recommended 
	not to be reset (for instance the property setter may constraint or
	fully fordib its resetting. To facilitate that instances of identifiable 
	objects do not share their `id`, and a class static `nextID` value
	may keep track of the next available ID for the object instances.
	
	.. warning::
		Although new objects are created with different ID but several
		objects of the same class may still have the same ID if they
		are generated by copying an existing objects rather than
		calling the constructor `__init__`. This is not a mistake
		but intended behaviour. But it means that classes holding
		a record of
		:class:`smIdentifiable <scimeth.data.smIdentifiable>` objects
		must still implement strategies to ensure uniqueness of ID
		if this is used as a primary key.
	
	:IMPORTANT Python's id() vs attribute id:
	
	Please note that this identifier **IS NOT** the
	object identifier as given by python built-in function `id()`.
	
	* The ID provided by this interface is meant to be a simple **mutable**,
	  so it can be reset if needed, whereas python's `id()` is immutable and
	  cannot be set.
	* The ID provided by this interface can be made **persistent**. This
	  distinction is critical; python's `id()` can change after dump/reloading
	  cycle from a persistent repository, e.g.
	  loaded from file-.). Because, the :attr:`id` attribute represented by
	  this interface is just a *regular* attribute, it can be made persistent
	  and hence guaranteed to not change when reloading from a persistent
	  repository. 
	* The ID provided by this interface can be given **semantics**, that is
	  the user decides the meaning of the id. Whereas
	  python's `id()` is somewhat arbitrary. For instance, in cases like CPython
	  it is related to the position in memory. 
	* Python's `id()` enforces **uniqueness** and is used by built-in types
	  such as sets. However, since as said, it is not persistent, this prevents any
	  potential use for a relation of total order. Instead, this ID, although
	  it gives some support for keeping uniqueness, but does not enforces it.
	  This means it can also be used for either total or partial orders.
	
	Note that there is no ambiguity or loss of functionality. Without
	this attribute, you can't call `<your_object>.id`.
	
	* To access Python's object unique identifier: `id(<your_object>)`
	* To access attribute :attr:`id`: `<your_object>.id`
	
	:Example:
	
	.. code-block:: python
	
		>>> a = 2
		>>> id(a)
		140736367534512
		>>> a.id
		Traceback (most recent call last):
		File "<ipython-input-32-6dc02a833f28>", line 1, in <module> a.id
		AttributeError: 'int' object has no attribute 'id'
	
	
	:Mixin implementation:
	
	This class is implemented as a mixin class. It can be instantiated,
	but it is not intended to be used directly. Instead, it is meant
	to be use in multiple inheritance schemes to add some functionality.
	
	Because it is a mixin implementation, it already takes care of
	correctly handling multiple inheritance, but it is recommended
	that this mixin base class is declared earlier (as it is already
	prepared to pass attributes when calling super() is resolving
	which superclass constructor must be passed), and python, attribute
	resolution in multiple inheritance is performed depth-first and
	then from left to right amongst the base classes -method resolution
	order (MRO).
	
	* (https://www.python-course.eu/python3_multiple_inheritance.php)
	* (https://help.semmle.com/wiki/display/PYTHON/Conflicting+attributes+in+base+classes)
	
	For more information about mixin classes for multiple inheritance:
	
	* https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way
	* https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful

	


	"""
	
	#Private class attributes shared by all instances
	__nextID = dict() #A static member variable to keep track of the next
			   #available identifier to use (for each subclass).
			   
	
	#Class constructor
	def __init__(self, *args, **kwargs):
		#Call superclass constructor
		super().__init__(*args, **kwargs)  # forwards all unused arguments
							#Leave this for mixin implementation
		
		self.__version = '0.1'
		
		tmpKey = str(self.__class__)
		try:
			self.__nextID[tmpKey] = self.__nextID[tmpKey]+1
		except:
			self.__nextID[tmpKey] = 1
		self.__id = self.__nextID[tmpKey]
		
		return


	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	@property
	def id(self): #ID getter
		'''
		A unique numerical ID for the object instance.
		
		:getter: Gets the id.
		:setter: Sets the id.
		:type: int
		'''
		return self.__id

	@id.setter
	def id(self,newId): #ID setter
		if type(newId) is not int:
			msg = self.getClassName() + ':id: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__id = newId
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
			s = s + indentationLevel*'\t' + name[len(self.getClassName())+3:] \
								+ '\t= ' + str(value) + ';\n'
		return s + indentationLevel*'\t' + '}>'


	#Public methods
	def getClassName(self):
		'''Gets the class name.
		
		:return: The class name
		:rtype: str
		'''
		return type(self).__name__
	
