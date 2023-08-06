README
######


**NAME**


``OPR - object programming runtime``


**SYNOPSIS**


| ``opr [-c|-d|-h]``
| ``opr <cmd> [key=value] [key==value]``
|


**DESCRIPTION**


``OPR`` is a runtime (program) that is intended to be programmable, with a
client program to develop modules on and a daemonised version that can run
in the background. ``OPR`` provides object persistence, an event handler and
some basic code to load modules that can provide additional functionality.


``OPR`` uses object programming (opv), the object oriented programming without
the oriented ;] Object programming is that method are seperated out into
functions that use the object as the first argument of that funcion. This gives
base class definitions a clean namespace to inherit from and to load json data
into the object's __dict__. A clean namespace prevents a json loaded attribute
to overwrite any methods.


**INSTALL**


``pip3 install opr``


**AUTHOR**


Bart Thate - operbot100@gmail.com


**COPYRIGHT**


``opr`` is placed in the Public Domain.
