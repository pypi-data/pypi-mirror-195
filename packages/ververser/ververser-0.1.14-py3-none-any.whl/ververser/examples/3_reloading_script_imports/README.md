# Ververser Example 3: Reloading Script Imports

When a ververser app is running and you make changes to the hosted scripts, they are automatically hot reloaded in the app. 
In case of any errors, the app is paused, and will try to reload again when the files are updated again. 
In this example, not only changes form main.py are hot-reloaded, but also changes in game.py.

The python import system is relatively complex. 
It does some clever caching, but does not allow us to easily unload modules. 
This is a problem when loading modules in ververser;
When reloading a script, not all logic might be refreshed due to caching. 
Ververser therefore wraps scripts as objects when importing them. 
When reloading a script, the imported script objects will be removed by the garbage collection, 
and replaced with new instances, effectively doing a proper reload of the module. 

Ververser only reloads scripts that are actually imported by other scripts. 
However, ververser intentionally does not try to do anything clever for reloading modules. 
Ververser is not aware of dependencies between scripts/modules.
Simply, when a python file is changed, the entire program as served by ververser is re-initialised. 
This might mean your entire program reboots while you only meant to change a minor thing.
This is something that might be tackled in later versions of ververser.
This is specifically true for reloading scripts. 
Reloading other types of assets will not result in a full reload, but will just reload that specific asset.  
