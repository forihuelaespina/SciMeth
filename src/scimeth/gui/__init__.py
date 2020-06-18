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
SciMeths's graphical user interfaces.

Created on Mon Apr 20 17:51:28 2020


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 20-Mar-2020 | FOE    | - Initial script and module smGuiTimeline.           |
+-------------+--------+------------------------------------------------------+
|  7-May-2020 | FOE    | - Added module smScrollableFrame.                    |
+-------------+--------+------------------------------------------------------+


.. seealso:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

#Make .data subpackage classes visible to main SciMeth package
from .smGuiTimeline import smGuiTimeline
from .smScrollableFrame import smScrollableFrame


