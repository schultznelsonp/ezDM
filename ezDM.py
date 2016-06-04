import kivy

from kivy.core.window import Window

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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
        self.height = 100

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

# This class is mostly needed to have easy access to the characters initiative values.
class Character(BoxLayout):

    def __init__(self, name, init, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint=(1.0, None)
        self.height = 20

        self.name = name
        self.init = int(init)
        self.add_widget(Label(text=name))
        self.add_widget(Label(text=init))

# The parent layout for all initiative stuff. Defines the logic for adding characters.
class InitTab(BoxLayout):

    def creationCallback(parent, button):
        # Get the input from the initCreator and make a new character from it.
        nameInput = parent.initCreator.nameInput.text
        initInput = parent.initCreator.initInut.text
        newCharacter = Character(name=nameInput, init=initInput)

        # We keep track of all the characters with a separate list, sorted in reverse by init value
        characters = parent.characters
        characters.append(newCharacter)
        characters.sort(key=lambda x: x.init, reverse=True)
        
        # In order to draw the init list with the correct order, we actually have to create a new
        # box layout each time we add (or remove) a character. The same effect could probably be
        # attained by using a relative layout, but this is easier.

        # We remove all the characters from list layout. If we don't do this, kivy will tell us
        # that we can't give a widget two parents, and then crash.
        for character in characters:
            parent.initList.remove_widget(character)
        
        # Remove old initList and create a new one
        parent.remove_widget(parent.initList)
        parent.initList = BoxLayout(orientation = 'vertical')

        # Add all the characters to the new init list, and then add the new initList to the init tab
        for character in characters:
            parent.initList.add_widget(character)
        parent.add_widget(parent.initList)

        Window.size = (500, 100 + (20 * len(characters)))
        

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
