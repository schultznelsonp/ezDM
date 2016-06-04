import kivy

from kivy.core.window import Window

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

WINDOW_WIDTH = 500
INIT_CREATOR_HEIGHT = 100
CHARACTER_HEIGHT = 20

# This item at the top of the init tab that is used to create characters. You can specify a
# custom callback by passing a 'callback' argument into the constructor
class InitCreator(BoxLayout):
    
    def defaultCallback(parentInstance, buttonInstance):
        print 'No callback specified'
        print parentInstance.nameInput.text
        print parentInstance.initInput.text

    def __init__(self, **kwargs):
        super(InitCreator, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint = (1.0, None)
        self.height = INIT_CREATOR_HEIGHT

        nameBox = BoxLayout(orientation='vertical')
        nameBox.add_widget(Label(text='Character Name'))
        nameInput = TextInput(multiline=False)
        self.nameInput = nameInput
        nameBox.add_widget(nameInput)

        initBox = BoxLayout(orientation='vertical')
        initBox.add_widget(Label(text='Initiative'))
        initInput = TextInput(multiline=False)
        self.initInut = initInput
        initBox.add_widget(initInput)

        self.add_widget(nameBox)
        self.add_widget(initBox)

        btn = Button(text='Create character')
        callback = kwargs.get('callback', self.defaultCallback)
        btn.bind(on_press=callback)
        self.add_widget(btn)

# This class represents one character in the initiative list. Used for easy acces to init values and
# to allow for a delete button.
class Character(BoxLayout):

    def defaultCallback(parent, button):
        print 'No callback defined!'

    def __init__(self, name, init, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1.0, None)
        self.height = CHARACTER_HEIGHT

        self.name = name
        self.init = int(init)
        self.add_widget(Label(text=name))
        self.add_widget(Label(text=init))

        btn = Button(text='X')
        callback = kwargs.get('callback', self.defaultCallback)
        btn.bind(on_press=callback)
        btn.size_hint = (None, 1.0)
        btn.width = CHARACTER_HEIGHT
        self.add_widget(btn)

# The parent layout for all initiative stuff. Defines the logic for adding characters.
class InitTab(BoxLayout):

    def creationCallback(initTab, button):
        # Get the input from the initCreator and make a new character from it.
        nameInput = initTab.initCreator.nameInput.text
        initInput = initTab.initCreator.initInut.text
        newCharacter = Character(name=nameInput, init=initInput, callback=initTab.deletionCallback)

        # We keep track of all the characters with a separate list, sorted in reverse by init value
        characters = initTab.characters
        characters.append(newCharacter)
        characters.sort(key=lambda x: x.init, reverse=True)
        
        # In order to draw the init list with the correct order, we actually have to create a new
        # box layout each time we add a character. The same effect could probably be
        # attained by using a relative layout, but this is easier.

        # We remove all the characters from list layout. If we don't do this, kivy will tell us
        # that we can't give a widget two parents, and then crash.
        for character in characters:
            initTab.initList.remove_widget(character)
        
        # Remove old initList and create a new one
        initTab.remove_widget(initTab.initList)
        initTab.initList = BoxLayout(orientation = 'vertical')

        # Add all the characters to the new init list, and then add the new initList to the init tab
        for character in characters:
            initTab.initList.add_widget(character)
        initTab.add_widget(initTab.initList)

        Window.size = (WINDOW_WIDTH, INIT_CREATOR_HEIGHT + (CHARACTER_HEIGHT * len(characters)))

    # Simply remove and resize the window; BoxLayout automatically takes care of repositioning
    def deletionCallback(initTab, button):
        characters = initTab.characters
        character = button.parent

        initTab.initList.remove_widget(character)
        characters.remove(character)
        Window.size = (WINDOW_WIDTH, INIT_CREATOR_HEIGHT + (CHARACTER_HEIGHT * len(characters)))
        

    def __init__(self, **kwargs):
        super(InitTab, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.initCreator = InitCreator(callback=self.creationCallback)
        self.add_widget(self.initCreator)

        self.initList = BoxLayout(orientation = 'vertical')
        self.add_widget(self.initList)

        self.characters = []

        Window.size = (500, 100)
        

class TestApp(App):

    def build(self):
        initman = InitTab()
        return initman

if __name__ == '__main__':
    TestApp().run()
