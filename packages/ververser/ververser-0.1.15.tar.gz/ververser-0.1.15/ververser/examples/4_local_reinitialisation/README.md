# Ververser Example 4: Local Reinitialisation

By default, ververser will reload all scripts when one of them is modified.
However, while this might be fine for small creative coding projects, this is not always desirable. 
Especially scripts that only define functions, 
and do not define objects, or things directly related to state of the application,
can be reloaded locally, without reinitialisaing the entire application.
By passing **reinit_on_mod = False** to **import_script**, you can manage your reloads.

In contrast to the previous example;
If you modify _content/color_for_time.py_, you will see that the script will be reloaded, 
but _content/main.py_ and _content/game.py_ will not be reloaded.