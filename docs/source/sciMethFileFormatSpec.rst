.. _rst-sciMethFileFormatSpec:

sciMeth (.xml/.tar) File Format Specification
=============================================

* File: sciMeth (.xml/.tar) File Format Specification
* Version: 0.1 
* Authors: Felipe Orihuela-Espina and Patrick Heyer-Wollenberg
* Created: March 21, 2020
* Revised: March 21, 2020
* Copyright (c) 2019 INAOE

.. _secVersionLog:


Version Log
-----------


=======  =======================  =========== ===========
Version  Change Description       Date        Responsible
=======  =======================  =========== ===========
0.1      Initial description	  21/Mar/2020 Felipe Orihuela-Espina
=======  =======================  =========== ===========


.. _secIntro:

Introduction
------------


.. _secPurpose:

Purpose
^^^^^^^

   2.1.1 This specification is intended to define a cross-platform,
   interoperable file storage and transfer format to encode a variety
   of experiments of different nature. Scientific studies are understood
   here according to constructs commonly defined in the branch of
   statistics concerning the analysis and design of experiments.

   

.. _secScope:

Scope
^^^^^

   2.2.1. TAR (Tape ARchiver) is a file format that can wrap
   files and directories so that they can be treated as a single file. It
   was originally developed to store data in a magnetic tape, but has
   since then survived and thrived being a popular choice as an option
   when a pipe among programs is needed as well as to serve for remote
   access. The standard specification of TAR files can be found in
   http://www.gnu.org/software/tar/
   
   2.2.2. XML (Extensible Markup Language) specification defines an XML
   document as a well-formed text, meaning that it satisfies a list of
   syntax rules provided in the specification. XML is a W3C recommendation
   that was designed for ease of implementation and for interoperability
   with both SGML and HTML. XML files are plain text files encoding an XML
   compliant XML document having both a logical and a physical structure.
   The standard specification of XML files can be found in
   https://www.w3.org/TR/xml/
   
   
   2.2.3. The scientific method is a mathematical formalization of the
   scientific experimental process. In this mathemtical formalization
   a number of mathematical objects co-exist and are related permitting
   controlling and informing scientists about the bias and uncertainty
   associated to measurements and experiments.
   
   2.2.4. The scientific method file format provides a way to encode
   all the mathematical objects related to a scientific study. The file
   format exploits the TAR and XML specifications as a base file format,
   describing only the internal contents of the main TAR file and some of
   its internal content in terms of XML files contained in the root TAR folder.
   
   2.2.5. In principle, the scientific method file format is thought to
   support generic scientific studies and experiments from different branches
   of science.
   

.. _secTrademarks:

Trademarks
^^^^^^^^^^

   2.3.1 TAR is free software distributed under the terms of the
   GNU General Public License as published by the Free Software Foundation.
   The scientific method file format belongs to INAOE but it is licensed
   also under the terms of the GNU General Public License.
   Other marks referenced within this document appear for identification
   purposes only and are the property of their respective owners.
   
   
   
.. _secPOermittedUse:

Permitted Use
^^^^^^^^^^^^^ 

   2.4.1 This scientific method File Format Specification is the
   exclusive property of INAOE.  Use of the information contained in this 
   document is permitted solely for the purpose of creating products, 
   programs and processes that read and write files in the scientific
   method TAR File Format subject to the terms and conditions herein.

   2.4.2 Use of the content of this document within other publications is 
   permitted only through reference to this document.  Reproduction
   or distribution of this document in whole or in part is permitted
   by giving appropriate credit to INAOE as owner of
   this file format as long as it is not used for commercial purposes.


.. _secDisclaimer:

Disclaimer
^^^^^^^^^^

   2.5.1 The file format specification is provided as is. INAOE is not
   responsible under any circumstances for any damage derived from its use.
   The information relating to the subject programs
   and/or the file formats created or accessed by the subject
   programs and/or the algorithms used by the subject programs is
   subject to change without notice.   

   


.. _secSciMethTAR:

The scientific method TAR Files
-------------------------------

   3.0.1 A scientific method document encloses information about one
   scientific study as well as additional generic document information and
   client software settings. All this is stored within the root of the
   wrapping TAR folder.
   
   
.. _secGenericDocInfo:

Generic document information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   3.1.1 This collects information related to the document itself such as
   file version, the creation and last moditification date, etc. This
   information is stored in
   a single ``docinfo.xml`` file located in the .tar root folder.
   
   3.1.2 ***PENDING*** definition of the associated XML Document Type Declaration (DTD)
   
   
.. _secSWsettings:


Client software settings
^^^^^^^^^^^^^^^^^^^^^^^^

   3.2.1 This collects information related to settings of the client software
   using the file format such as user preferences and software directives. This
   information is stored in
   a single ``config.xml`` file located in the .tar root folder.
   
   
   3.2.2 ***PENDING*** definition of the associated XML Document Type Declaration (DTD)
   
.. _secStudy:


Scientific study 
^^^^^^^^^^^^^^^^

   3.3.0.1 This collects information related to the scientific study. A
   scientific study is a collection of observations from a set of experimental
   units (referred collectively as cohort) according to some set of
   acquisition rules referred to as study design. The information is stored
   in 3 files and a list of folders;
   
   * ``study.xml`` - Contains information about the elements included in
     the study indexing the cohort, design and observations
   * ``cohort.xml`` - Contains information about the cohort i.e. experimental
     units
   * ``design.xml`` - Contains information about the study design e.g.
     experimental groups, factors, endpoints, etc
   * ``observationXXX`` - A folder containig information about a single
     observation, where XXX is a numerical ID of the observation which is
     unique within the study. Note that an observation may in turn contain
     information about many data items.
   


.. _secStudyXML:

study.xml 
^^^^^^^^^

   3.3.1.1 ***PENDING*** definition of the associated XML Document Type Declaration (DTD)


.. _secCohortXML:

cohort.xml 
^^^^^^^^^^

   3.3.2.1 ***PENDING*** definition of the associated XML Document Type Declaration (DTD)

   
   

.. _secDesignXML:

design.xml 
^^^^^^^^^^  


   3.3.3.1 ***PENDING*** definition of the associated XML Document Type Declaration (DTD)

 
   

.. _secObservationFolder:

Observation folder 
^^^^^^^^^^^^^^^^^^

   3.3.4.1 ***PENDING*** definition of the associated internal structure


   
   
    
    
Acknowledgements
----------------

We would like to extend our special thanks to Dr. Rodrigo Matsui from the
Instiuto de Oftalmología Conde de Valenciana in Mexico City. 




   