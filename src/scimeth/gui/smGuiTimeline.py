# -*- coding: utf-8 -*-
#
#File: smGuiTimeline.py
#
'''
Created on Mon Apr 20 17:53:59 2020

Module ***smGuiTimeline***

This module implements a tkinter based user interface to manipulate
objects of :class:`smTimeline <scimeth.data.smTimeline>`. The module
provides two types of interface:
	
	* Stand alone window
	* Widget based to be embedded in other windows.



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 20-Apr-2020 | FOE    | - Module created.                                    |
+-------------+--------+------------------------------------------------------+
| 25-Apr-2020 | FOE    | - GUI designed in Pencil Project and first UI        |
|             |        |   UI elements added.                                 |
+-------------+--------+------------------------------------------------------+
| 26-Apr-2020 | FOE    | - Continued with composing the GUI.                  |
|             |        | - Separated the current from the saved Timeline.     |
+-------------+--------+------------------------------------------------------+
| 30-Apr-2020 | FOE    | - Continued with composing the GUI.                  |
|             |        | - Added support to visualize events in the conditions|
|             |        |   widget.                                            |
+-------------+--------+------------------------------------------------------+
|  4-May-2020 | FOE    | - Polsihed layout.                                   |
|             |        | - First protoype of GUI complete with without        |
|             |        |   functionality.                                     |
+-------------+--------+------------------------------------------------------+
|  4-May-2020 | FOE    | -  Added functionality to add new Conditions.        |
|             |        | - ***IMPORTANT***:                                   |
|             |        |   In the process of adding the functionality to add  |
|             |        |   conditions, I've realised of a side effect of the  |
|             |        |   shallow initialization. The timeline object was    |
|             |        |   storing the modifications despite I was never      |
|             |        |   saving the object explicitly. Of course, this makes|
|             |        |   sense, as it aligns with the python philosophy of  |
|             |        |   making every assignment a shallow copy (pass-by-   |
|             |        |   object-reference a.k.a. pass-by-assignement rather |
|             |        |   than the more classical pass-by-reference or       |
|             |        |   pass-by-value), and it is                          |
|             |        |   only my fault that I did not realize before. But   |
|             |        |   this means, I may also need to modify a few of my  |
|             |        |   other classes. Here are two nice explanations:     |
|             |        |                                                      |
|             |        |   * https://robertheaton.com/2014/02/09/pythons-pass-|
|             |        |     by-object-reference-as-explained-by-philip-k-dick|
|             |        |     /................................................|
|             |        |   * https://www.quora.com/Are-arguments-passed-by-val|
|             |        |     ue-or-by-reference-in-Python                     |
|             |        |                                                      |
+-------------+--------+------------------------------------------------------+
|  7-May-2020 | FOE    | - Added scroll bar to tabConditions.                 |
|             |        | - Callback to support adding new conditions now      |
|             |        |   re-raises warnings and errors wrapped in           |
|             |        |   messagebox.                                        |
|             |        | - Added callback to support switching time units     |
|             |        |   :meth:`callbackSwitchTimeUnits`.                   |
|             |        | - Added callback :meth:`on_exit`.                    |
|             |        | - Added callback :meth:`on_save`.                    |
|             |        | - Added timeline information control panel with      |
|             |        |   entries for the :attr:`startTime` and              |
|             |        |   :attr:`samplingRate`.                              |
+-------------+--------+------------------------------------------------------+
|  9-May-2020 | FOE    | - Added callback to support Apply changes to         |
|             |        |   conditions, but this is not yet working. I need    |
|             |        |   to add an observer pattern to notify the main      |
|             |        |   window to also update the timeline.                |
+-------------+--------+------------------------------------------------------+
| 17-May-2020 | FOE    | - Callback `callbackApplyChanges` for conditions now |
|             |        |   notify the main timeline using the Observer        |
|             |        |   pattern. There seems however to be an issue with   |
|             |        |   catching the warnings.                             |
+-------------+--------+------------------------------------------------------+
| 19-May-2020 | FOE    | - Callback `callbackApplyChanges` for conditions     |
|             |        |   is now working correctly.                          |
+-------------+--------+------------------------------------------------------+



.. seealso::
		
		:class:`smTimeline <scimeth.data.smTimeline>`,

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

'''



## Import
import sys
import os
import copy
import warnings

#Add paths
tmpPath = os.path.join('..', '..')
if not sys.path[0] == tmpPath:
	sys.path.insert(0, tmpPath)

import tkinter as tk #The tkinter module
from tkinter import ttk #The submodule for themed widgets 
						#See: https://docs.python.org/3/library/tkinter.ttk.html

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.colors as mcol
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


import scimeth as sm



##############################################################################
# Class smGuiConditionWidget
##############################################################################

## Class definition
class smGuiConditionWidget(tk.Frame):
	'''
	A widget to interact and manipulate with
	:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
	in a :class:`smTimeline <scimeth.data.smTimeline>`
	'''

    #Private class attributes shared by all instances

	#Class constructor
	def __init__(self, parent, condition = sm.data.smTimelineCondition(), \
				  events = None):
		'''Class constructor. Creates a new instance of
		:class:`smGuiConditionWidget <scimeth.gui.smGuiConditionWidget>`.
		
		:Parameters:
		
		:param parent: Container frame or window
		:type parent: Container frame or window

		:param condition: A conditon, Optional
		:type condition: :class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
			By default it calls the :class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
			constructor with no parameters.
		
		:Returns:

		A new object instance of :class:`scimeth.gui.smGuiConditionWidget`.
		'''
		#Call superclass constructor
		tk.Frame.__init__(self, parent, relief = 'ridge', \
							borderwidth=1, padx=5, pady=5)

		
		self.__version = '0.1'
		self.__conditionObservers = list() #Implements the observer pattern
								#for changes in the condition.
								#(https://en.wikipedia.org/wiki/Observer_pattern and
								#https://stackoverflow.com/questions/6190468/how-to-trigger-function-on-value-change)
								#to update the main timeline upon
								#updating the condition.
								#Note that otherwise, although the condition
								#itself will update in the timeline
								#because of python "pass-by-object-reference"
								#BUT it won't properly update the rest of
								#the timeline, e.g. conditionsEventMap, etc
								 
		
		
		#Explicitly create the properties before the first call to setter.
		self.__condition = sm.data.smTimelineCondition() #The condition being manipulated
		self.__events = None #Events associated to the condition
		self.__uiElements = dict()
		
		
		#Initialize
		self.condition = condition;
		self.events = events;
		
		#Create my widget an insert it into the parent
		#Create and add the main tabbed notebook
		
		#self.text = 'Condition ' + str(self.condition.id)
		#self.relief = 'sunken'
		
		self.uiElements['label_id'] = tk.Label(self, text='Id:')
		self.uiElements['label_id'].grid(row=0, column=0, sticky='e')
		self.uiElements['entry_id'] = tk.Entry(self)
		self.uiElements['entry_id'].insert(0,self.condition.id)
		self.uiElements['entry_id'].grid(row=0, column=1, sticky='w')
		status = tk.BooleanVar() #Reset to "decouple" from the previous status variable
		status.set(True)
		self.uiElements['checkbox_Visible'] = tk.Checkbutton(self, \
											  text='Visible', variable=status,\
											  onvalue = True, offvalue = False)#,\
											  #command = self.repaintCanvasTimeline)
		self.uiElements['checkbox_Visible'].status = status 
		self.uiElements['checkbox_Visible'].grid(row=0, column=2, sticky = 'w')
		self.uiElements['label_tag'] = tk.Label(self, text='Tag:', anchor='w')
		self.uiElements['label_tag'].grid(row=1, column=0, sticky = 'e')
		self.uiElements['entry_tag'] = tk.Entry(self)
		self.uiElements['entry_tag'].insert(0,self.condition.tag)
		self.uiElements['entry_tag'].grid(row=1, column=1, sticky = 'w')
		self.uiElements['label_description'] = tk.Label(self, text='Description:', anchor="w")
		self.uiElements['label_description'].grid(row=2, column=0)
		self.uiElements['entry_description'] = tk.Text(self, \
												 width = 30, height = 6, \
												 wrap = 'word')
		self.uiElements['entry_description'].insert('1.0',self.condition.description)
		self.uiElements['entry_description'].grid(row=2, column=1, \
													rowspan = 3, columnspan = 2)
		tmpScrollBar = tk.Scrollbar(self)
		tmpScrollBar.config(command=self.uiElements['entry_description'].yview)
		self.uiElements['entry_description'].config(yscrollcommand=tmpScrollBar.set)
		tmpScrollBar.grid(row=2, column=3, rowspan = 3, sticky = 'ns')
		
		#and to display de the events
		self.uiElements['treeview_events']=ttk.Treeview(self, height = 6)
		self.uiElements['treeview_events']['columns'] = ('onset','duration','end')
		self.uiElements['treeview_events'].column('#0', width = 30, minwidth = 15, stretch = tk.NO)
		self.uiElements['treeview_events'].column('onset', width = 50, minwidth = 15, stretch = tk.NO)
		self.uiElements['treeview_events'].column('duration', width = 60, minwidth = 15, stretch = tk.NO)
		self.uiElements['treeview_events'].column('end', width = 50, minwidth = 15, stretch = tk.NO)
		self.uiElements['treeview_events'].heading('#0', text = 'id', anchor = tk.W)
		self.uiElements['treeview_events'].heading('onset', text = 'onset', anchor = tk.W)
		self.uiElements['treeview_events'].heading('duration', text = 'duration', anchor = tk.W)
		self.uiElements['treeview_events'].heading('end', text = 'end', anchor = tk.W)
		if self.events is not None:
			for iEv, ev in enumerate(self.events):
				self.uiElements['treeview_events'].insert(\
						'', iEv, iid = ev.id, \
						text = str(ev.id), \
						values = (str(ev.onset), str(ev.duration), str(ev.end)))
		self.uiElements['treeview_events'].grid(row=0, column=4, rowspan = 4,padx = (10,0))

		self.uiElements['button_applyChanges'] = \
				tk.Button(self,\
					text = 'Apply changes', command = self.callbackApplyChanges)
		self.uiElements['button_applyChanges'].grid(row=0, column=5, sticky = 'we', padx = (10,0), pady=(2,0))
		self.uiElements['button_removeCondition'] = \
				tk.Button(self,\
					text = 'Remove condition')#, command = 'callbackMethodHere')
		self.uiElements['button_removeCondition'].grid(row=1, column=5, sticky = 'we', padx = (10,0), pady=(2,0))


		return
	
	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method

	
	@property
	def condition(self): #condition getter
		'''
		The :class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
		being manipulated

		:getter: Gets the condition.
		:setter: Sets the condition.
		:type: :class:`smTimelineCondition <scimeth.data.smTimelineCondition>`
		'''
		return self.__condition

	@condition.setter
	def condition(self,newCondition): #condtion setter
		tmp = sm.data.smTimelineCondition()
		if str(newCondition.__class__) != str(tmp.__class__):
			msg = self.getClassName() + ':condition: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__condition = newCondition
		return None

	@property
	def events(self): #events getter
		'''
		The set of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		associated to the :attr:`condition`

		:getter: Gets the set of events.
		:setter: Sets the set of events.
		:type: set of :class:`smTimelineEvents <scimeth.data.smTimelineEvent>`
		'''
		return self.__events

	@events.setter
	def events(self,newEvents): #events setter
		if newEvents is not None:
			if type(newEvents) is list:
				newEvents = set(newEvents)
			if type(newEvents) is not set:
				msg = self.getClassName() + ':events: Unexpected attribute type.'
				#warnings.warn(msg,SyntaxWarning)
				raise ValueError(msg)
			tmp = sm.data.smTimelineEvent()
			for ev in newEvents:
				if str(ev.__class__) != str(tmp.__class__):
					msg = self.getClassName() + ':events: Unexpected attribute value. Elements of parameter newEvents must be of type scimeth.data.smTimelineEvent.'
					#warnings.warn(msg,SyntaxWarning)
					raise ValueError(msg)
		self.__events = newEvents
		return None

	@property
	def parent(self): #parent getter
		'''
		The parent container. This is a read-only property

		:getter: Gets the parent container.
		:type: `tk.Tk`
		'''
		return self._nametowidget(self.winfo_parent())


	
	@property
	def uiElements(self): #uiElements getter
		'''
		The list of graphical elements composing the GUI.

		:getter: Gets the uiElements.
		:setter: Sets the uiElements.
		:type: list
		'''
		return self.__uiElements

	@uiElements.setter
	def uiElements(self,newUiElements): #uiElements setter
		print(type(newUiElements))
		if type(newUiElements) is not dict:
			msg = self.getClassName() + ':uiElements: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__uiElements = newUiElements
		return None

	
	#Public methods
	def getClassName(self):
		'''Gets the class name.
		
		:return: The class name
		:rtype: str
		'''
		return type(self).__name__
	
	def callbackApplyChanges(self):
		'''Callback for button `Apply Changes` to save changes
		to condition.
		
		:return: None
		:rtype: NoneType
		'''
		tmpCondition = copy.deepcopy(self.condition)
		tmpFilters = copy.deepcopy(warnings.filters) #Keep a copy of current warning filters
		warnings.filterwarnings('error') #Turn warnings into errors
			#so that they can be catch as exceptions.
		try:
			#Beware! In most languages where the block within
			#a try statement is executed all or nothing, and if something goes
			#wrong within the try block, the system restores to the state
			#prior to the try. contrary to these, in python, the code execute
			#wihtin the tru block but before any exception is
			#raised, stays executed even if an exception is raised!!!
			self.condition.id = int(self.uiElements['entry_id'].get())
			self.condition.tag = self.uiElements['entry_tag'].get()
			self.condition.description = self.uiElements['entry_description'].get('1.0', 'end')
			#notify observers, so that they can update themselves.
			for observerCallback in self.__conditionObservers:
				observerCallback(tmpCondition.id,self.condition)
			
			for rowid in self.uiElements['treeview_events'].get_children():
				elem = self.uiElements['treeview_events'].item(rowid) #Get the full row
				ev = None
				flagFound = False
				for tmpEv in self.events:
					if tmpEv.id == int(elem['text']):
						ev = tmpEv #Note that this is a shallow copy
									#So as I make changes below. it will also automatically
 									#be updated on self.events.
						flagFound = True
						break
				if flagFound:
					ev.onset    = float(elem['values'][0])
					ev.duration = float(elem['values'][1])
					ev.end      = float(elem['values'][2])
				else:
					tk.messagebox.showwarning('Warning','Event ' + elem['text'] + ' not found.')
		except Warning as w:
			tk.messagebox.showwarning('Warning',str(w))
			#and restore the condition
			self.condition = copy.deepcopy(tmpCondition)
		except Exception as e:
			tk.messagebox.showerror('Error',str(e))
			#and restore the condition
			self.condition = copy.deepcopy(tmpCondition)
		#Now reset warnings filter status
		warnings.resetwarnings()
		warnings.filters = copy.deepcopy(tmpFilters)
		return None


	def bindConditionObserver(self, callback):
		self.__conditionObservers.append(callback)


##############################################################################
# Class smGuiTimeline
##############################################################################

## Class definition
class smGuiTimeline(tk.Frame):
	'''
	Provides a basic graphical user interface to interact and manipulate
	objects of :class:`smTimeline <scimeth.data.smTimeline>`.
	'''

    #Private class attributes shared by all instances

	#Class constructor
	def __init__(self, parent = None, timeline = sm.data.smTimeline()):
		'''Class constructor. Creates a new instance of
		:class:`smGuiTimeline <scimeth.gui.smGuiTimeline>`.
		
		:Parameters:
		
		:param parent: Container, Optional
		:type parent: Container
			Set to None for main window, or parent window for widget mode.

		:param timeline: A timeline, Optional
		:type timeline: :class:`smTimeline <scimeth.data.smTimeline>`.
			By default it calls the :class:`smTimeline <scimeth.data.smTimeline>`
			constructor with no parameters.
		
		:Returns:

		A new object instance of :class:`scimeth.gui.smGuiTimeline`.
		'''
		#Call superclass constructor
		flagMode = True
		if parent is None:
			flagMode = False
			parent = tk.Tk()
			parent.title('smGuiTimeline')
		tk.Frame.__init__(self, parent)
		
		
		self.__version = '0.1'
		
		width   = round(parent.winfo_screenwidth() *9/10)
		height  = round(parent.winfo_screenheight()*8.5/10)
		posLeft = round(parent.winfo_screenwidth() *0.2/10)
		posTop  = round(parent.winfo_screenheight()*0.2/10)
		if not flagMode:
			parent.geometry(f'{width}x{height}+{posLeft}+{posTop}')

		#Explicitly create the properties before the first call to setter.
		self.__currentTimeline = sm.data.smTimeline() #The timeline to work with.
		self.__savedTimeline = sm.data.smTimeline() #The last saved timeline back up.
		self.__mode = flagMode #True for widget, False for main window
		self.__uiElements = dict()
		
		#Initialize
		self.savedTimeline = timeline;
		self.currentTimeline = copy.deepcopy(timeline);
			#Ensure I work with a deep copy to avoid unwanted side effects.
		
		#Create my widget an insert it into the parent
		self.uiElements['toolbar'] = tk.Frame(self, borderwidth = 1, relief = 'raised')
		self.uiElements['toolbar'].pack(fill='x')
		self.uiElements['button_exit'] = \
				tk.Button(self.uiElements['toolbar'],\
					text = 'Exit', command = self.on_exit)
		self.uiElements['button_exit'].grid(row=0, column=0, sticky = 'w')
		self.uiElements['button_saveTimeline'] = \
				tk.Button(self.uiElements['toolbar'],\
					text = 'Save', command = self.on_save)
		self.uiElements['button_saveTimeline'].grid(row=0, column=1, sticky = 'w')
		
		#Create and add the main tabbed notebook
		self.uiElements['notebook']      = ttk.Notebook(self)
		self.uiElements['tabTimeline']   = tk.Frame(self.uiElements['notebook'], borderwidth = 1)
		self.uiElements['tabConditions'] = tk.Frame(self.uiElements['notebook'], borderwidth = 1)
		self.uiElements['tabOverlapping'] = tk.Frame(self.uiElements['notebook'], borderwidth = 1)
		self.uiElements['notebook'].add(self.uiElements['tabTimeline'],   text = 'Timeline')
		self.uiElements['notebook'].add(self.uiElements['tabConditions'], text = 'Conditions')
		self.uiElements['notebook'].add(self.uiElements['tabOverlapping'], text = 'Overlapping')
		self.uiElements['notebook'].select(self.uiElements['tabTimeline'])
		self.uiElements['notebook'].enable_traversal()
		self.uiElements['notebook'].pack()
		self.uiElements['notebook'].bind("<<NotebookTabChanged>>", self.on_tab_selected)
		
		#Add content to tab Timeline
		self.uiElements['tabTimeline'].grid_columnconfigure(0,weight=1)
		self.uiElements['tabTimeline_EventDisplayFrame'] = \
				tk.LabelFrame(self.uiElements['tabTimeline'], \
						 borderwidth = 1, relief = 'sunken', \
						 text = 'Conditions and events', padx = 5, pady = 5)
		self.uiElements['tabTimeline_EventDisplayFrame'].grid(row=0, column=0, columnspan = 2, sticky='we')
		self.uiElements['tabTimeline_TimelineControlFrame'] = \
				tk.LabelFrame(self.uiElements['tabTimeline'], \
						 borderwidth = 1, relief = 'sunken', \
						 text = 'Timeline information', padx = 5, pady = 5)
		self.uiElements['tabTimeline_TimelineControlFrame'].grid(row=1, column=0, \
																 sticky='nswe', padx = (5,5))
		self.uiElements['tabTimeline_EventControlFrame'] = \
				tk.LabelFrame(self.uiElements['tabTimeline'], \
						 borderwidth = 1, relief = 'sunken', \
						 text = 'Event information', padx = 5, pady = 5)
		self.uiElements['tabTimeline_EventControlFrame'].grid(row=1, column=1, \
																 sticky='nswe', padx = (5,5))

		if len(self.currentTimeline.conditions) == 0:
			self.uiElements['label_NoCondition'] = tk.Label(self.uiElements['tabTimeline_EventDisplayFrame'], \
											  text='There are no conditions', anchor="w")
			self.uiElements['label_NoCondition'].grid(row = 0, column = 0)

# 		#The matplotlib canvas uses pack() for layout, so I need to
# 		#embed it into a Frame so that it does not clash with my grid
# 		#layout.
# 		self.uiElements['canvasFrame_Timeline'] = \
# 				tk.Frame(self.uiElements['tabTimeline_EventDisplayFrame'])
# 		self.uiElements['tabTimeline_EventDisplayFrame'].grid(row = 0, column = 1, rowspan = len(self.currentTimeline.conditions))
		resolutionDPI = 100 #dpi
		figWidth  = (width * 9/10) / resolutionDPI
		figHeight = (height * 6/10) / resolutionDPI
		fig = Figure(figsize=(figWidth, figHeight), dpi=resolutionDPI) #Fig size in inches
		#fig.patch.set_facecolor('white')
		fig.patch.set_visible(False)
		self.uiElements['figure_eventsDisplay'] = fig
		#t = np.arange(0, 3, .01)
		#fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
		ax = fig.add_axes([0.1, 0.15, 0.85, 0.8])
		#ax.patch.set_visible(False)
		#ax.patch.set_alpha(0.0)
		self.uiElements['axes_eventsDisplay'] = ax
		#ax.fill([0,0,1,1],[0,1,1,0],'w') #Not sure it is needed but it is NOT shoing anything right now.


#		self.uiElements['canvas_Timeline'] = FigureCanvasTkAgg(fig, \
#								 master=self.uiElements['canvasFrame_Timeline'])  # A tk.DrawingArea.
		self.uiElements['canvas_Timeline'] = FigureCanvasTkAgg(fig, \
								 master=self.uiElements['tabTimeline_EventDisplayFrame'])  # A tk.DrawingArea.
		self.uiElements['canvas_Timeline'].draw()
# 		self.uiElements['canvasToolbar_Timeline'] = NavigationToolbar2Tk(\
# 								 self.uiElements['canvas_Timeline'], \
# 								 self.uiElements['canvasFrame_Timeline'])
# 		self.uiElements['canvasToolbar_Timeline'] = NavigationToolbar2Tk(\
# 								 self.uiElements['canvas_Timeline'], \
# 								 self.uiElements['tabTimeline_EventDisplayFrame'])
# 		self.uiElements['canvasToolbar_Timeline'].update()
		self.uiElements['canvas_Timeline'].get_tk_widget().grid(row = 0, \
														  column = 0, columnspan = 6)
		
		self.uiElements['label_ShowHide'] = tk.Label(self.uiElements['tabTimeline_EventDisplayFrame'], \
											  text='Show / Hide:', anchor="w")
		self.uiElements['label_ShowHide'].grid(row=1, column=0, sticky = 'w')
		status = tk.BooleanVar()
		status.set(False)
		self.uiElements['checkbox_Id'] = tk.Checkbutton(self.uiElements['tabTimeline_EventDisplayFrame'], \
											  text='Id', variable=status,\
											  onvalue = True, offvalue = False,\
											  command = self.repaintCanvasTimeline)
		self.uiElements['checkbox_Id'].status = status 
		self.uiElements['checkbox_Id'].grid(row=1, column=1, sticky = 'w')
		status = tk.BooleanVar() #Reset to "decouple" from the previous status variable
		status.set(False)
		self.uiElements['checkbox_Onset'] = tk.Checkbutton(self.uiElements['tabTimeline_EventDisplayFrame'], \
											  text='Onset', variable=status,\
											  onvalue = True, offvalue = False,\
											  command = self.repaintCanvasTimeline)
		self.uiElements['checkbox_Onset'].status = status 
		self.uiElements['checkbox_Onset'].grid(row=1, column=2, sticky = 'w')
		status = tk.BooleanVar() #Reset to "decouple" from the previous status variable
		status.set(False)
		self.uiElements['checkbox_Duration'] = tk.Checkbutton(self.uiElements['tabTimeline_EventDisplayFrame'], \
											  text='Duration', variable=status,\
											  onvalue = True, offvalue = False,\
											  command = self.repaintCanvasTimeline)
		self.uiElements['checkbox_Duration'].status = status 
		self.uiElements['checkbox_Duration'].grid(row=1, column=3, sticky = 'w')
		status = tk.BooleanVar() #Reset to "decouple" from the previous status variable
		status.set(False)
		self.uiElements['checkbox_End'] = tk.Checkbutton(self.uiElements['tabTimeline_EventDisplayFrame'], \
											  text='End', variable=status,\
											  onvalue = True, offvalue = False,\
											  command = self.repaintCanvasTimeline)
		self.uiElements['checkbox_End'].status = status 
		self.uiElements['checkbox_End'].grid(row=1, column=4, sticky = 'w')
		self.uiElements['button_selectUnits'] = \
				tk.Button(self.uiElements['tabTimeline_EventDisplayFrame'],\
					text = 'Switch units', command = self.callbackSwitchTimeUnits)
		self.uiElements['button_selectUnits'].grid(row=1, column=5, sticky = 'e')
		self.repaintCanvasTimeline()
		
		
		self.uiElements['label_TimelineId'] = tk.Label(self.uiElements['tabTimeline_TimelineControlFrame'], \
											  text='Id:', anchor="w")
		self.uiElements['label_TimelineId'].grid(row=0, column=0, sticky='e')
		self.uiElements['entry_TimelineId'] = tk.Entry(self.uiElements['tabTimeline_TimelineControlFrame'], \
												width = 10, \
												validate='focusout', \
												validatecommand = self.callbackEntryTimelineId)
		self.uiElements['entry_TimelineId'].insert(0, str(self.currentTimeline.id))
		self.uiElements['entry_TimelineId'].grid(row=0, column=1, sticky='w')
		self.uiElements['label_StartTime'] = tk.Label(self.uiElements['tabTimeline_TimelineControlFrame'], \
											  text='Absolute start time:', anchor="w")
		self.uiElements['label_StartTime'].grid(row=1, column=0, sticky='e')
		self.uiElements['entry_StartTime'] = tk.Entry(self.uiElements['tabTimeline_TimelineControlFrame'], \
												width = 30)
		self.uiElements['entry_StartTime'].insert(0, str(self.currentTimeline.startTime))
		self.uiElements['entry_StartTime'].grid(row=1, column=1, sticky='w')
		self.uiElements['label_SamplingRate'] = tk.Label(self.uiElements['tabTimeline_TimelineControlFrame'], \
											  text='Sampling rate [Hz]:', anchor="w")
		self.uiElements['label_SamplingRate'].grid(row=2, column=0, sticky='e')
		self.uiElements['entry_SamplingRate'] = tk.Entry(self.uiElements['tabTimeline_TimelineControlFrame'], \
												width = 10)
		self.uiElements['entry_SamplingRate'].insert(0, self.currentTimeline.samplingRate)
		self.uiElements['entry_SamplingRate'].grid(row=2, column=1, sticky='w')
		self.uiElements['label_TimeMultiplier'] = tk.Label(self.uiElements['tabTimeline_TimelineControlFrame'], \
												  text='Timestamps units [sec*10^multiplier]:', anchor="w")
		self.uiElements['label_TimeMultiplier'].grid(row=3, column=0, sticky='e')
		self.uiElements['entry_TimeMultiplier'] = tk.Entry(self.uiElements['tabTimeline_TimelineControlFrame'], \
												width = 10)
		self.uiElements['entry_TimeMultiplier'].insert(0, str(self.currentTimeline.timeMultiplier))
		self.uiElements['entry_TimeMultiplier'].grid(row=3, column=1, sticky='w')
		
		
		self.uiElements['label_EventId'] = tk.Label(self.uiElements['tabTimeline_EventControlFrame'], \
											  text='Id:', anchor="w")
		self.uiElements['label_EventId'].grid(row=0, column=0)
		self.uiElements['entry_EventId'] = tk.Entry(self.uiElements['tabTimeline_EventControlFrame'])
		self.uiElements['entry_EventId'].insert(0, 0)
		self.uiElements['entry_EventId'].grid(row=0, column=1)
		self.uiElements['label_Onset'] = tk.Label(self.uiElements['tabTimeline_EventControlFrame'], \
											  text='Onset:', anchor="w")
		self.uiElements['label_Onset'].grid(row=1, column=0)
		self.uiElements['entry_Onset'] = tk.Entry(self.uiElements['tabTimeline_EventControlFrame'])
		self.uiElements['entry_Onset'].insert(0, 0)
		self.uiElements['entry_Onset'].grid(row=1, column=1)
		self.uiElements['label_Duration'] = tk.Label(self.uiElements['tabTimeline_EventControlFrame'], \
											  text='Duration:', anchor="w")
		self.uiElements['label_Duration'].grid(row=2, column=0)
		self.uiElements['entry_Duration'] = tk.Entry(self.uiElements['tabTimeline_EventControlFrame'])
		self.uiElements['entry_Duration'].insert(0, 0)
		self.uiElements['entry_Duration'].grid(row=2, column=1)
		self.uiElements['label_End'] = tk.Label(self.uiElements['tabTimeline_EventControlFrame'], \
											  text='End:', anchor="w")
		self.uiElements['label_End'].grid(row=3, column=0)
		self.uiElements['entry_End'] = tk.Entry(self.uiElements['tabTimeline_EventControlFrame'])
		self.uiElements['entry_End'].insert(0, 0)
		self.uiElements['entry_End'].grid(row=3, column=1)
		self.uiElements['label_AssignedConditions'] = tk.Label(self.uiElements['tabTimeline_EventControlFrame'], \
											  text='Assigned to conditions:', anchor="w")
		self.uiElements['label_AssignedConditions'].grid(row=0, column=2)
		self.uiElements['listbox_AssignedConditions'] = \
				tk.Listbox(self.uiElements['tabTimeline_EventControlFrame'],\
						   height = 6)
		for cond in self.currentTimeline.conditions:
			self.uiElements['listbox_AssignedConditions'].insert('end', cond.tag)
		self.uiElements['listbox_AssignedConditions'].grid(row=0, column=3, rowspan = 4)
		self.uiElements['button_addEvent'] = \
				tk.Button(self.uiElements['tabTimeline_EventControlFrame'],\
					text = 'Add event')#, command = 'callbackMethodHere')
		self.uiElements['button_addEvent'].grid(row=0, column=4, sticky='we',padx=(5,0),pady=(2,0))
		self.uiElements['button_removeEvent'] = \
				tk.Button(self.uiElements['tabTimeline_EventControlFrame'],\
					text = 'Remove event')#, command = 'callbackMethodHere')
		self.uiElements['button_removeEvent'].grid(row=1, column=4, sticky='we',padx=(5,0),pady=(2,0))
		self.uiElements['button_updateEvent'] = \
				tk.Button(self.uiElements['tabTimeline_EventControlFrame'],\
					text = 'Update event')#, command = 'callbackMethodHere')
		self.uiElements['button_updateEvent'].grid(row=2, column=4, sticky='we', padx=(5,0),pady=(2,0))
		
		
		
		#Add content to tab Conditions
		self.uiElements['tabConditions'].grid_rowconfigure(1, weight=1)
		self.uiElements['tabConditions'].grid_columnconfigure(0, weight=1)
		self.uiElements['button_addNewCondition'] = \
				tk.Button(self.uiElements['tabConditions'],\
					text = 'Add new condition', command = self.callbackAddNewCondition)
		self.uiElements['button_addNewCondition'].grid(row=0, sticky='w')
		self.uiElements['button_removeAllConditions'] = \
				tk.Button(self.uiElements['tabConditions'],\
					text = 'Remove all conditions')#, command = 'callbackMethodHere')
		self.uiElements['button_removeAllConditions'].grid(row=0, sticky='e')

		self.uiElements['tabConditions_ConditionsDisplayFrame'] = \
				sm.gui.smScrollableFrame(self.uiElements['tabConditions'], \
						 borderwidth = 1, relief = 'sunken', \
						 text = 'Conditions list', padx = 5, pady = 5)
		self.uiElements['tabConditions_ConditionsDisplayFrame'].grid(row=1, sticky='nswe')

		self.uiElements['label_NoConditions2'] = \
			 tk.Label(self.uiElements['tabConditions_ConditionsDisplayFrame'], \
										  text='There are no conditions', anchor="w")
		self.uiElements['label_NoConditions2'].pack(side='top', fill='x')
		if len(self.currentTimeline.conditions) != 0:
			self.uiElements['label_NoConditions2'].pack_forget()
				#Labels do not have the visible property, so the way to
				#hide it is using pack_forget
		for cond in self.currentTimeline.conditions:
			tmpUIElemTag = 'condWidget_' + str(cond.id)
			condEvents = self.currentTimeline.getConditionsEvents(cond)
			self.uiElements[tmpUIElemTag] = smGuiConditionWidget( \
								self.uiElements['tabConditions_ConditionsDisplayFrame'].scrollableFrame, \
											  condition=cond, \
											  events = condEvents)
			self.uiElements[tmpUIElemTag].pack(fill='x', expand = 1, pady=5)
			#Register observer to update the timeline if
			#the condition is updated
			self.uiElements[tmpUIElemTag].bindConditionObserver(self.on_update_conditionWidget)
		
		
		
		
		#Add content to tab Overlapping
		resolutionDPI = 100 #dpi
		figWidth  = (width * 9/10) / resolutionDPI
		figHeight = (height * 9/10) / resolutionDPI
		fig = Figure(figsize=(figWidth, figHeight), dpi=resolutionDPI) #Fig size in inches
		#fig.patch.set_facecolor('white')
		fig.patch.set_visible(False)
		self.uiElements['figure_overlappingDisplay'] = fig
		#t = np.arange(0, 3, .01)
		#fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
		ax = fig.add_axes([0.1, 0.15, 0.85, 0.8])
		#ax.patch.set_visible(False)
		#ax.patch.set_alpha(0.0)
		self.uiElements['axes_overlappingDisplay'] = ax
		#ax.fill([0,0,1,1],[0,1,1,0],'w') #Not sure it is needed but it is NOT shoing anything right now.

#		self.uiElements['canvas_Overlapping'] = FigureCanvasTkAgg(fig, \
#								 master=self.uiElements['canvasFrame_Overlapping'])  # A tk.DrawingArea.
		self.uiElements['canvas_Overlapping'] = FigureCanvasTkAgg(fig, \
								 master=self.uiElements['tabOverlapping'])  # A tk.DrawingArea.
		self.uiElements['canvas_Overlapping'].draw()
# 		self.uiElements['canvasToolbar_Overlapping'] = NavigationToolbar2Tk(\
# 								 self.uiElements['canvas_Overlapping'], \
# 								 self.uiElements['canvasFrame_Overlapping'])
# 		self.uiElements['canvasToolbar_Overlapping'] = NavigationToolbar2Tk(\
# 								 self.uiElements['canvas_Overlapping'], \
# 								 self.uiElements['tabOverlapping'])
# 		self.uiElements['canvasToolbar_OVerlapping'].update()
		self.uiElements['canvas_Overlapping'].get_tk_widget().grid(row = 0, column = 0)
		self.repaintCanvasOverlapping()
		
		
		
		#Insert the guiTimeline widget on the parent
		self.place(x=0, y=0, relwidth=1, relheight=1)
			#Right now is occupying the whole window body, but I may need
			#to change this later on
		if not self.mode: #If main window
			self.runEventMainLoop()
		
		return


	#Properties getters/setters
	#
	# Remember: Sphinx ignores docstrings on property setters so all
	#documentation for a property must be on the @property method


	@property
	def mode(self): #mode getter
		'''
		True for widget, False for main window. This is a read-only property.

		:getter: Gets the mode.
		:setter: Sets the mode.
		:type: bool
		'''
		return self.__mode


	@property
	def parent(self): #parent getter
		'''
		The parent container. This is a read-only property

		:getter: Gets the parent container.
		:type: `tk.Tk`
		'''
		return self._nametowidget(self.winfo_parent())


	@property
	def currentTimeline(self): #currentTimeline getter
		'''
		The :class:`smTimeline <scimeth.data.smTimeline>` object
		being manipulated.
		
		This is the timeline being represented in the GUI and does not
		necessarily match the last saved one.
		
		.. see also:: :attr:`savedTimeline`
		
		:getter: Gets the currentTimeline.
		:setter: Sets the currentTimeline.
		:type: :class:`smTimeline <scimeth.data.smTimeline>`
		'''
		return self.__currentTimeline

	@currentTimeline.setter
	def currentTimeline(self,newTimeline): #timeline setter
		tmp = sm.data.smTimeline()
		#if not isinstance(newTimeline,type(sm.data.smTimeline())):
		if str(newTimeline.__class__) != str(tmp.__class__):
			msg = self.getClassName() + ':currentTimeline: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__currentTimeline = newTimeline
		return None

	@property
	def savedTimeline(self): #savedTimeline getter
		'''
		The last saved :class:`smTimeline <scimeth.data.smTimeline>` object
		acting as back up.
		
		This is the las t saved timeline and does not necessarily match 
		the one being represented in the GUI.
		
		.. see also:: :attr:`currentTimeline`
		
		:getter: Gets the savedTimeline.
		:setter: Sets the savedTimeline.
		:type: :class:`smTimeline <scimeth.data.smTimeline>`
		'''
		return self.__savedTimeline

	@savedTimeline.setter
	def savedTimeline(self,newTimeline): #timeline setter
		tmp = sm.data.smTimeline()
		#if not isinstance(newTimeline,type(sm.data.smTimeline())):
		if str(newTimeline.__class__) != str(tmp.__class__):
			msg = self.getClassName() + ':savedTimeline: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__savedTimeline = newTimeline
		return None

	@property
	def uiElements(self): #uiElements getter
		'''
		The list of graphical elements composing the GUI.

		:getter: Gets the uiElements.
		:setter: Sets the uiElements.
		:type: list
		'''
		return self.__uiElements

	@uiElements.setter
	def uiElements(self,newUiElements): #uiElements setter
		if type(newUiElements) is not dict:
			msg = self.getClassName() + ':uiElements: Unexpected attribute type.'
			#warnings.warn(msg,SyntaxWarning)
			raise ValueError(msg)
		self.__uiElements = newUiElements
		return None



	#Private methods
	def __str__(self):
		'''Provides a string representation for the objects of the class.
		
		:return: A string representation for the object
		:rtype: str
		'''
		s = '<' + self.getClassName() + ': {\n'
		#Grab Class attributes (note that this will only pick class attributes
		#but not instance attributes)
		#The filter ignores python __ attributes e.g. __repr__
		iters = dict((name,value) for name,value in self.__dict__.items() if name[:2] != '__')
		#Update with the instance items
		iters.update(self.__dict__)
		#Finally build the string
		for name,value in iters.items():
			attrName = name[len(self.getClassName())+3:]
			#Lists render their elements using __repr__ instead of __str__
			s = s + '\t' + attrName + '\t= ' + str(value) + ';\n'
		return s + '}>'
	


	#Protected methods

	#Public methods
	def getClassName(self):
		'''Gets the class name.
		
		:return: The class name
		:rtype: str
		'''
		return type(self).__name__
	


	def callbackAddNewCondition(self):
		'''
		Callback method for the `button_addNewCondition`.
		
		When the button `button_addNewCondition` is pressed, it adds a new
		:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
		
		:return: None
		:rtype: NoneType
		'''
		c = sm.data.smTimelineCondition()
		c.tag = 'Cond_' + str(c.id)
		try:
			self.currentTimeline.addConditions(c)
		except Warning as w:
			tk.messagebox.showwarning('Warning',str(w))
		except Exception as e:
			tk.messagebox.showerror('Error',str(e))
		self.repaintConditionsDisplayFrame()
		return None
	

	def callbackEntryTimelineId(self):
		'''
		Callback method for the update of `entry_TimelineId`.
		
		When the entry `entry_TimelineId` loses focus, the entry
		textvar is validated (and stored in the current timeline).
		
		:return: None
		:rtype: NoneType
		'''
		try:
			self.currentTimeline.id = int(self.uiElements['entry_TimelineId'].get())
		except Exception as e:
			tk.messagebox.showerror('Error',str(e))
		return None


	def callbackSwitchTimeUnits(self):
		'''
		Callback method for the `button_addNewCondition`.
		
		When the button `button_addNewCondition` is pressed, it adds a new
		:class:`smTimelineCondition <scimeth.data.smTimelineCondition>`.
		
		:return: None
		:rtype: NoneType
		'''
		
		if self.currentTimeline.unit.name == 'Sample':
			self.currentTimeline.toSeconds()
		else:
			self.currentTimeline.toSamples()
		self.repaintCanvasTimeline()
		
		return None
	
	
	def on_exit(self):
		'''
		Closes the window and exit
		'''
		self.parent.destroy()
		return None

	def on_save(self):
		'''
		Saves the timeline.
		'''
		self.savedTimeline = copy.deepcopy(self.currentTimeline)
		return None


	def on_tab_selected(self,event):
		'''
		Updates the tabs contents upon changing tab focus.
		
		:return: None
		:rtype: NoneType
		'''
		selected_tab = event.widget.select()
		tab_text = event.widget.tab(selected_tab, 'text')
		if tab_text == 'Timeline':
			self.repaintCanvasTimeline()
		if tab_text == 'Conditions':
			pass
		if tab_text == 'Overlapping':
			self.repaintCanvasOverlapping()
		
		return None


	def on_update_conditionWidget(self, theId, theCondition):
		'''
		Observer of smGuiConditionWidgets si that the timeline
		updates itself when the condition gets updated.
		
		:return: None
		:rtype: NoneType
		'''
		self.currentTimeline.setConditions(theId,theCondition)
		return None

	def repaintCanvasOverlapping(self):
		'''
		Refresh the content of the overlapping axes (uiElement
		'axes_overlappingDisplay')
		within the uiElement 'canvas_Overlapping' which
		is the one displaying the overlapping behaviour among
		:class:`smTimelineConditions <scimeth.data.smTimelineCondition>`
		in the :class:`smTimeline <scimeth.data.smTimeline>`.
		
		:return: None
		:rtype: NoneType
		'''
		tmpCanvas = self.uiElements['canvas_Overlapping']
		#tmpFig    = self.uiElements['figure_overlappingDisplay']
		tmpAxes   = self.uiElements['axes_overlappingDisplay']
		#Clear axes
		tmpAxes.cla()
		#tmpAxes.patch.set_facecolor('blue')
		tmpAxes.patch.set_alpha(0.0) #Not working. But apparently
									 #this is a know bug.
									 #https://github.com/matplotlib/matplotlib/issues/9007

		#Convert list of overlapping pairs to array
		nConditions = len(self.currentTimeline.conditions)
		tmpOverlapStatusArray = self.currentTimeline.NON_OVERLAP \
								* np.ones((nConditions,nConditions),dtype=float)
		condIds = self.currentTimeline.getConditionsID()
		for pair in self.currentTimeline.overlapStatus:
			idx1 = condIds.index(pair(0))
			idx2 = condIds.index(pair(1))
			tmpOverlapStatusArray[idx1,idx2] = self.currentTimeline.OVERLAP

		#Choose colormap
		cmap = plt.cm.get_cmap(name = 'bwr', lut = 2)
			#lut is the number of colors. However, to access the
			#such number of levels, call cmap.N
		#Redraw overlapping status
# 		tmpAxes.imshow(tmpOverlapStatusArray, \
# 				extent=[0.5, nConditions+0.5, 0.5, nConditions+0.5], \
# 				cmap = cmap)
		if nConditions != 0:
			tmpAxes.imshow(tmpOverlapStatusArray, \
					origin = 'upper', cmap = cmap)
				#Note: There is also matshow but it is actually a wrapper over
				#imshow with some predifined settings.
		#Collect conditions ids and tags
		labelStr = list()
		for cond in self.currentTimeline.conditions:
			labelStr.append(str(cond.id) + ':' + cond.tag)
		
		#Beautify
		tmpAxes.set_xlabel('Conditions')
		tmpAxes.set_ylabel('Conditions')
		#tmpAxes.set_xticks(ticks = list(range(1,nConditions+1)))
		tmpAxes.set_xticks(ticks = list(range(0,nConditions)))
		tmpAxes.set_xticklabels(labels = labelStr)
		tmpAxes.xaxis.tick_top()
		#tmpAxes.set_yticks(ticks = list(range(1,nConditions+1)))
		tmpAxes.set_yticks(ticks = list(range(0,nConditions)))
		tmpAxes.set_yticklabels(labels = labelStr)
		tmpCanvas.draw()
		return None
	
	
	def repaintCanvasTimeline(self):
		'''
		Refresh the content of the events axes (uiElement 'axes_eventsDisplay')
		within the uiElement 'canvas_Timeline' which
		is the one displaying the conditions and events timecourses.
		
		:return: None
		:rtype: NoneType
		'''
		tmpCanvas = self.uiElements['canvas_Timeline']
		tmpAxes   = self.uiElements['axes_eventsDisplay']
		#Clear axes
		tmpAxes.cla()
		#tmpAxes.patch.set_facecolor('blue')
		tmpAxes.patch.set_alpha(0.0) #Not working. But apparently
									 #this is a know bug.
									 #https://github.com/matplotlib/matplotlib/issues/9007

		#Choose colormap
		nConditions = len(self.currentTimeline.conditions)
		cmap = plt.cm.get_cmap(name = 'jet', \
							   lut = nConditions)
			#lut is the number of colors. However, to access the
			#such number of levels, call cmap.N
		#Redraw events
		pos=0
		labelStr = list()
		for idx, cond in enumerate(self.currentTimeline.conditions):
			labelStr.append(str(cond.id) + ':' + cond.tag)
			condEvents = self.currentTimeline.getConditionsEvents(cond)
			pos=idx+1
			for ev in condEvents:
				#colorIdx = float(idx)/cmap.N
				colorIdx = idx
				tmpAxes.fill([ev.onset, ev.end, ev.end, ev.onset],\
							 [pos-0.4, pos-0.4, pos+0.4, pos+0.4],\
							 color = cmap(colorIdx))
				#Show/Hide event information
				s = 'id = ' + str(ev.id)
				tmp = tmpAxes.text(x = ev.onset, y = pos+0.3, s = s, \
						   color = 'w')
				tmp.set_visible(self.uiElements['checkbox_Id'].status.get())
				s = 'o = ' + str(ev.onset)
				tmp = tmpAxes.text(x = ev.onset, y = pos+0.1, s = s, color = 'w')
				tmp.set_visible(self.uiElements['checkbox_Onset'].status.get())
				s = 'd = ' + str(ev.duration)
				tmp = tmpAxes.text(x = ev.onset, y = pos-0.1, s = s, color = 'w')
				tmp.set_visible(self.uiElements['checkbox_Duration'].status.get())
				s = 'e = ' + str(ev.end)
				tmp = tmpAxes.text(x = ev.onset, y = pos-0.3, s = s, color = 'w')
				tmp.set_visible(self.uiElements['checkbox_End'].status.get())
		
		#Beautify
		if self.currentTimeline.unit.name == 'Sample':
			tmpAxes.set_xlim(left=0, right=self.currentTimeline.length-1, auto = False)
		else:
			tstamps = self.currentTimeline.timestamps
			tmpAxes.set_xlim(left =tstamps[0], right=tstamps[-1], auto = False)
		if nConditions != 0: #Adjust limits only if pos != 0
			tmpAxes.set_ylim(bottom = 0.5, top = pos+0.5, auto = False)
		
		tmpAxes.set_xlabel('Time [' + self.currentTimeline.unit.acronym + ']')
		tmpAxes.set_ylabel('Conditions')
		tmpAxes.set_yticks(ticks = list(range(1,nConditions+1)))
		tmpAxes.set_yticklabels(labels = labelStr)
		tmpCanvas.draw()
		return None
	
	
	def repaintConditionsDisplayFrame(self):
		'''
		Refresh the content of the condition display frame
		(uiElement 'tabConditions_ConditionsDisplayFrame')
		within the uiElement 'tabConditions' which
		is the one displaying the conditions list.
		
		:return: None
		:rtype: NoneType
		'''
		#Labels do not have the visible property, so the way to
		#hide it is using pack_forget
		if len(self.currentTimeline.conditions) == 0:
			self.uiElements['label_NoConditions2'].pack()
		else:
			self.uiElements['label_NoConditions2'].pack_forget()
		for cond in self.currentTimeline.conditions:
			tmpUIElemTag = 'condWidget_' + str(cond.id)
			if tmpUIElemTag in self.uiElements:
				pass
			else:
				condEvents = self.currentTimeline.getConditionsEvents(cond)
				self.uiElements[tmpUIElemTag] = \
					 smGuiConditionWidget(self.uiElements['tabConditions_ConditionsDisplayFrame'].scrollableFrame, \
												  condition=cond, \
												  events = condEvents)
				self.uiElements[tmpUIElemTag].pack(fill='x', pady=5)
				#Register observer to update the timeline if
				#the condition is updated
				self.uiElements[tmpUIElemTag].bindConditionObserver(self.on_update_conditionWidget)

		return
	
	def runEventMainLoop(self):
		'''
		Executes the events main loop to listen to 

		'''
		if not self.mode: #If main window
			print(self.getClassName() + ':runEventMainLoop: Starting events loop')
			self.parent.mainloop()
		



if __name__ == "__main__":
	#Call it as a stand alone window
	theGui = sm.gui.smGuiTimeline()
	print("Done.")
	
