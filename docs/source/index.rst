.. SciMeth documentation master file, created by
   sphinx-quickstart on Fri Mar 28 1:44:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SciMeth's documentation
=======================

.. toctree::
   :numbered:
   :maxdepth: 2
   :caption: Table of Contents

   intro
   logOfProgress
   sciMethFileFormatSpec


API documentation
=================

.. The :recursive: option to document elements recursively will become
   available on Sphinx release 3.1.0 but current stable realease (the
   one used by Conda is 3.0.3). So until then, I need to declare
   manually the elements to autodoc.

.. toctree::

	scimeth
.. scimeth.data
.. scimeth.data.smIdentifiable
.. scimeth.data.smMeasurement
.. scimeth.data.smMeasurementUnit
.. scimeth.data.smTimeline
.. scimeth.data.smTimelineCondition
.. scimeth.data.smTimelineEvent
.. scimeth.gui
.. scimeth.gui.smGuiTimeline
.. scimeth.gui.smScrollableFrame
.. scimeth.utils
.. scimeth.utils.smUtils

   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
