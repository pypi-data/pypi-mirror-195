# Ververser Example 1: Minimal Setup

When a ververser app is running and you make changes to the hosted scripts, they are automatically hot reloaded in the app. 
In case of any errors, the app is paused, and will try to reload again when the files are updated again. 

Ververser needs to be instantiated with a path to a content folder.
The content folder should contain a main.py, which will be the entrypoint for ververser.
Ververser supports 3 functions within the script that can be called by the engine:

- vvs_init - called by ververser when the script is instantiated
- vvs_update - called by ververser every frame
- vvs_draw - called by ververser every frame (clearing and flipping the main buffer is done for you by ververser)

Besides these functions that are invoked by ververser, the script can contain any additional logic you'd like. 

