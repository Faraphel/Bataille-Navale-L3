import pyglet


# Créer une fenêtre
window = pyglet.window.Window(resizable=True)

# Créer un texte "Hello World !"
label = pyglet.text.Label(
    "Hello World !",
    anchor_x="center",
    anchor_y="center"
)


# Lorsque la fenêtre change de taille, change la position du texte pour le centrer
@window.event
def on_resize(width: int, height: int):
    label.x = width // 2
    label.y = height // 2


# Lorsqu'une touche est enfoncée
@window.event
def on_key_press(symbol, modifiers):
    print(
        pyglet.window.key.symbol_string(symbol),
        pyglet.window.key.modifiers_string(modifiers)
    )


# À chaque frame, rafraichi la fenêtre et dessine le texte
@window.event
def on_draw():
    window.clear()
    label.draw()


# Lance la fenêtre
pyglet.app.run()
