# -*- coding: utf-8 -*-
#
#File: smScrollableFrame.py
#
'''
Created on Thu May  7 11:57:17 2020

Module ***smTimeline***

This module implements the class :class:`smScrollableFrame <scimeth.gui.smScrollableFrame>`.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
|  7-May-2020 | FOE    | - Class :class:`smScrollableFrame` created.          |
+-------------+--------+------------------------------------------------------+



.. seealso::
	
	:class:`smTimelineEvent <scimeth.data.smTimelineEvent>`,
	:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
	:class:`smMeasurement <scimeth.data.smMeasurement>`,

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

'''
import tkinter as tk
from tkinter import ttk


class smScrollableFrame(tk.LabelFrame):
	'''A :class:`smScrollableFrame <scimeth.gui.smScrollableFrame>` 
	provides a frame with an attached ScrollBar.
	
	tkinter lacks scrollable frame. the only scrollable widget in tkinter
	is the Canvas. This provides a generic widget to equip a Frame with
	a scrollbar.
	
	Initial code for this class adapted from:
	
	* https://blog.tecladocode.com/tkinter-scrollable-frames/
	
	'''
	#Private class attributes shared by all instances
	
	
	#Class constructor
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.canvas = tk.Canvas(self)
		vscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
		hscrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
		self.scrollableFrame = tk.Frame(self.canvas)

		self.scrollableFrame.bind('<Configure>', \
			lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))

		self.canvas.create_window((0, 0), window = self.scrollableFrame, anchor = 'nw')
		self.canvas.configure(yscrollcommand = vscrollbar.set)
		self.canvas.configure(xscrollcommand = hscrollbar.set)
		vscrollbar.pack(side = 'right', fill = 'y')
		hscrollbar.pack(side = 'bottom', fill = 'x')
		self.canvas.pack(side = 'left', fill = 'both', expand = True)
# 		self.canvas.grid(row = 0, column = 0, sticky = 'e')
# 		vscrollbar.grid(row = 0, column = 1, sticky = 'w')
# 		hscrollbar.grid(row = 1, column = 0, sticky = 'e')
		return