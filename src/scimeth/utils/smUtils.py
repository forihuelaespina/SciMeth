# -*- coding: utf-8 -*-
#
#File: smUtils.py
#
"""
A library of utilities to support package SciMeth.

Created on Tue Mar 24 23:42:31 2020


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 24-Mar-2020 | FOE    | - Library created. Added functions `partition` and   |
|             |        |   `quicksort` to sort objects by an attribute.       |
+-------------+--------+------------------------------------------------------+
| 15-May-2020 | FOE    | - Added function `methods`.                          |
+-------------+--------+------------------------------------------------------+


.. seealso:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


def methods(theObject):
	'''Retrieve the list of methods of the object.
	'''
	tmp = [func for func in dir(theObject) if callable(getattr(theObject, func)) and not func.startswith("__")]
	return tmp


def partition(array, start, end, compare_func):
	'''
	Splits an array 
	
	:Parameters:
	
	array : numpy.array
		The array of objects to be split.
	start : int
		Index to first element.
	end : int
		Index to last element.
	compare_func : a lambda function
		Function used to compare two objects.

	:Returns:

	high : int
		The index to the pivot for partitioning the array.
	'''
	pivot = array[start]
	low = start + 1
	high = end
	while True:
		while low <= high and compare_func(array[high], pivot):
			high = high - 1
		while low <= high and not compare_func(array[low], pivot):
			low = low + 1
		if low <= high:
			array[low], array[high] = array[high], array[low]
		else:
			break
	array[start], array[high] = array[high], array[start]

	return high

def quick_sort(array, start, end, compare_func):
	'''
	Sort an array of objects according to the object comparing function
	`compare_func`.
	
	Algorithm from: https://stackabuse.com/quicksort-in-python/
	
	:Parameters:
	
	array : numpy.array
		The array of objects to be split.
	start : int
		Index to first element.
	end : int
		Index to last element.
	compare_func : a lambda function
		Function used to compare two objects.

	:Returns:

	array : numpy.array
		The sorted array.
	'''
	if start >= end:
		return
	p = partition(array, start, end, compare_func)
	quick_sort(array, start, p-1, compare_func)
	quick_sort(array, p+1, end, compare_func)


