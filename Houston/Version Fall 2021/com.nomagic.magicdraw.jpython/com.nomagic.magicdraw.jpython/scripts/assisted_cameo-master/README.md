# assisted_cameo
This project adds AI assistance for Cameo Systems Modeler.

## Current Status
The *Review Diagram* action accesses all element in the current diagram and displays their type and name in a new window.

## Notes
* Jython plugin does not support scientific python packages such as `numpy`, `scipy` or `pandas`
    * Jytho plugin will be used to make HTTPS requests to a central repo to perform anything that requires scientific python. A conda env file for scientific python has been made called `ambse.yml`. This is the file that will be instantiated in the central repo