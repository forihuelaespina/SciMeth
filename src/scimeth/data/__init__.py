# -*- coding: utf-8 -*-
#
# File: __init__.py
#
# This file is necessary to compile python as a package (not a module)
#
# From: https://stackoverflow.com/questions/448271/what-is-init-py-for
# The __init__.py is required to make Python treat the directories as
# containing packages; this is done to prevent directories with a common
# name, such as string, from unintentionally hiding valid modules that
# occur later (deeper) on the module search path. In the simplest case,
# __init__.py can just be an empty file, but it can also execute
# initialization code for the package or set the __all__ variable.
"""

SciMeth's data model.

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 21-Mar-2020 | FOE    | - Initial script and class smMeasurementUnit.        |
+-------------+--------+------------------------------------------------------+
| 22-Mar-2020 | FOE    | - Added interface smIdentifiable.                    |
+-------------+--------+------------------------------------------------------+
| 23-Mar-2020 | FOE    | - Added class smTimelineEvent.                       |
+-------------+--------+------------------------------------------------------+
| 24-Mar-2020 | FOE    | - Added classes smTimelineCondition and Timeline.    |
+-------------+--------+------------------------------------------------------+
| 18-Apr-2020 | FOE    | - Added classes smMeasurement.                       |
+-------------+--------+------------------------------------------------------+


.. seealso:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

#Make .data subpackage classes visible to main SciMeth package
from .smIdentifiable import smIdentifiable
from .smMeasurementUnit import smMeasurementUnit
from .smTimelineEvent import smTimelineEvent
from .smTimelineCondition import smTimelineCondition
from .smTimeline import smTimeline
from .smMeasurement import smMeasurement


