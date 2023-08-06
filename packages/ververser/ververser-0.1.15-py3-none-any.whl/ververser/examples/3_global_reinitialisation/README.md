# Ververser Example 3: Global Reinitialisation

To keeps things simple and avoid confusing problems, ververser will reload all scripts when only on of them is modified.
This will avoid complex problems dealing with out-of-date definitions.

If you modify _content/main.py_ or _content/game.py_ while running this app, 
you will see that both scripts will be reloaded and imported anew. 