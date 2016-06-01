import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.config import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '100')

# Wrapper instead of subclass because it doesn't work as a subclass.
class InitiativeCreator():
    
    def callback(parentInstance, buttonInstance):
        print 'Oh jeez'
        print parentInstance.nI.text
        print parentInstance.iB.text

    def __init__(self,**kwargs):
        layout = BoxLayout(orientation='horizontal', spacing=10)
        layout.size_hint = (1.0, None)
        layout.height = 100

        nameBox = BoxLayout(orientation='vertical')
        nameBox.add_widget(Label(text='Character Name'))
        nameInput = TextInput(multiline=False)
        self.nI = nameInput
        nameBox.add_widget(nameInput)

        initiativeBox = BoxLayout(orientation='vertical')
        initiativeBox.add_widget(Label(text='Initiative'))
        initiativeInput = TextInput(multiline=False)
        self.iB = initiativeInput
        initiativeBox.add_widget(initiativeInput)

        layout.add_widget(nameBox)
        layout.add_widget(initiativeBox)

        btn = Button(text='Create character')
        btn.bind(on_press=self.callback)
        layout.add_widget(btn)

        self.layout = layout

class TestApp(App):

    def build(self):
        initman = InitiativeCreator()
        return initman.layout

if __name__ == '__main__':
    TestApp().run()
