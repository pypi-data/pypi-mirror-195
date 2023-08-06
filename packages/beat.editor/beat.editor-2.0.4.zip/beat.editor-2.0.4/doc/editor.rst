.. _editor-beakdowns:

===================
 Editor Breakdowns
===================

There is an editor for every BEAT object:

* Databases
* Libraries
* Dataformats
* Algorithms
* Toolchains
* Experiments
* Plotters
* Plotterparameters
* Protocoltemplates

Some of these editors are more complex than others - if you can't figure something out,
look here!

.. note:: If the images are too small, right-click on the image in your browser and click `View Image` to see the image in another tab at full resolution!

.. _generic-editor-features:

Generic Editor Features
=======================

beat.editor provides an intuitive interface to edit the various assets used by BEAT.

On the left hand side of the main window, a tree view gives access to all the assets
that are stored in the prefix.

The right hand side will show the editor dedicated to the selected asset.

All assets have common attributes like Short description which provides a summary of what
the asset is about. Longer description and information can be provided in a separate
document. To start editing it, use the Edit button at the bottom of the editor to start
you favorite text processor.

Some assets have code associated with them, using the same button you can start your
favorite code editor (or rather the one that is configured as such for the code file
type).

.. _database-editor:

Database Editor
===============

.. image:: ./img/editor_database_breakdown.png

The database editor works in tandem with the Protocol Templates Editor.

You can add as many protocol as you want each with a unique name. Once you added a
protocol, you can configure as many views on top of the data sets the protocol provides.

New databases are tied to a specific dataset. The dataset must be made available on the
web platform and the new database can only be installed after validation by a platform
administrator.


.. _protocoltemplates-editor:

Protocoltemplates Editor
========================

.. image:: ./img/editor_protocoltemplates_breakdown.png

The protocol template editor allows to design new protocols based on databases content
if the ones already provided are not covering the use case needed.

As for the database, new protocol templates must be first validated and then installed
on the web platform by one of its administrators.


.. _dataformat-editor:

Dataformat Editor
=================

.. image:: ./img/editor_dataformat_breakdown.png

This editor allows to easily create new data format by creating new fields from scratch
or combine already known data formats. Multidimensional arrays can also be created.


.. _algorithm-editor:

Algorithm Editor
================

.. image:: ./img/editor_algorithm_breakdown.png

The algorithm editor provides the means to create all types of algorithms available on
the platform.

If an old V1 algorithm is being loaded, beat.editor will automatically propose the
possibility to migrate it to V2.


.. _toolchain-editor:

Toolchain Editor
================

.. image:: ./img/editor_toolchain_breakdown.png

The toolchain editor is a graphical editor that allows to easily place the various blocks
required to create an experiment. The toolbar on the left hand side of the editor
provides access to the various possible blocks that are available based on the content
of the prefix. This ensures that when creating the experiment, users won't face an empty
selection of possible algorithms to put there.


.. _experiment-editor:

Experiment Editor
=================

The experiment editor shows each main editable elements in its own tab.

Datasets
--------

.. image:: ./img/editor_experiment_breakdown_datasets.png

The Datasets panel allows to select which database should be used.

Blocks
------

.. image:: ./img/editor_experiment_breakdown_blocks.png

The Blocks panel allows to attribute and configure algorithms for each block of the
experiment.


Loops
-----

.. image:: ./img/editor_experiment_breakdown_loops.png

In experiments using the soft loop concept, this panel will allow to select the
processor and evaluator algorithm pair that will work together.


Analyzers
---------

.. image:: ./img/editor_experiment_breakdown_analyzers.png

The Analyzers panel shows all analyzers and as for the blocks and loops panel allows to
select the appropriate algorithm that will run there.


.. _global-parameters-editor:

Global Parameters
-----------------

.. image:: ./img/editor_experiment_breakdown_global_parameters.png

The Global Parameters panel allows to configure the execution environments as well as the
various parameters of algorithms in a global fashion. This means that all algorithms
where they apply will use them unless you specifically changed them using their dedicated
parameters editor that are displayed using the Parameters button.


.. automodule:: beat.editor
