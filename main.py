__version__ = '1.4'

import kivy
kivy.require('1.7.2')

'''
# hard setting the width and height for testing use only
from kivy.config import Config
Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')
'''

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty


'''

Sign Maker - Version 1.4
Copyright (C) 2014 Kris Shamloo

A Mercury Labs application.
Special thanks to the Kivy team.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


# reading the saved message
f = open('message.txt')
message = f.read()
f.close()

class TextWidget(FloatLayout):

    text_color = ListProperty ([[1,1,1,1],
                                [.95,.25,.37,1],
                                [.37,.95,.25,1],
                                [.25,.37,.95,1]])
                                
    color_labels = ListProperty (["White",
                                  "Red",
                                  "Green",
                                  "Blue"])
                                
    save_labels = ListProperty (["Save your message","Reset to saved message"])
    
    font_size = ListProperty([Window.width/20, Window.width/4])
                        
    display_text = StringProperty(str(message))
    display_color = ListProperty([1,1,1,1])
    display_pos = ListProperty([Window.width/10,Window.height/10])

    settings_popup = ObjectProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        super(TextWidget,self).__init__(**kwargs)

    def popup(self, *args):
        
        # links the contents of the popup and the display text
        def on_text(instance, value):
            self.display_text = value

        # testing function to make sure callbacks are working properly
        def button_callback(instance):
            print("You called?", instance)
        
        # links the color of the display text to the color of the button
        def color_change(instance):
            self.display_color = instance.background_color

        # saves the current message to message.txt
        def save_message(instance):
            print("We are saving:", t.text)
            f = open('message.txt', 'w')
            f.write(t.text)
            f.close()
            
        # resets to center and to saved message
        def reset_message(instance):
            print("We are resetting!")
            self.display_pos = [Window.width/10,Window.height/10]
            f = open('message.txt')
            self.display_text = str(f.read())
            f.close()
            
        
        # creates and opens the save menu popup
        def save_callback(instance):
        
            grid = GridLayout(rows=2)
            
            # save button
            btn1 = Button(text=self.save_labels[0],
                          font_size=self.font_size[0])
            btn1.bind(on_press=save_message)
            grid.add_widget(btn1)
            
            # reset button
            btn2 = Button(text=self.save_labels[1],
                          font_size=self.font_size[0])
            btn2.bind(on_press=reset_message)
            grid.add_widget(btn2)
            
            # build the popup    
            p = Popup(content=grid, title='Save or reset your message.',
                      size_hint=(.85,.4),pos_hint={'top':.95},
                      title_size=self.font_size[0])
                      
            p.open()       
                     
        # creates and opens the color selection popup
        def color_callback(instance):
            
            grid = GridLayout(cols=2)
            
            for i in range (len(self.text_color)):
                button = Button(text=self.color_labels[i],
                                color=self.text_color[i],
                                background_color=self.text_color[i],
                                background_down = 'buttondown.png',
                                background_normal = 'buttonnormal.png',
                                border = [32,32,32,32],
                                font_size=self.font_size[0])
                                
                button.bind(on_press=color_change)
                grid.add_widget(button)
                
            p = Popup(content=grid, title='Change your color.',
                      size_hint=(.85,.4),pos_hint={'top':.95},
                      title_size=self.font_size[0])
                      
            p.open()
        
        # backspace button callback
        def backspace_callback(instance):
            t.do_backspace()
            
        # popup contents are being created bellow, starting from the bottom up              
        box = BoxLayout(orientation='vertical')
        btnbox = BoxLayout(orientation='horizontal', size_hint=(1,.33))

        # text input, sends its contents to on_text()  
        t = TextInput(text=self.display_text,
                      background_color=[.7,.7,.7,1],
                      font_size=self.font_size[0])
        t.bind(text=on_text)
        box.add_widget(t)
        
        # save button
        btn1 = Button(text="Save", font_size=self.font_size[0])
        btn1.bind(on_press=save_callback)
        btnbox.add_widget(btn1)

        # color button, opens up a new popup for colors
        btn2 = Button(text="Color", font_size=self.font_size[0])
        btn2.bind(on_press=color_callback)
        btnbox.add_widget(btn2)

        # backspace button, deletes a character from the text input
        btn3 = Button(text="<<", font_size=self.font_size[0])
        btn3.bind(on_press=backspace_callback)
        btnbox.add_widget(btn3)

        box.add_widget(btnbox)

        # linking p and the settings_popop property
        p = self.settings_popup
        
        # checks if the popup exists, if not, creates it
        if p is None:
            self.settings_popup = p = Popup(content=box,
                                            title='Change your message.',
                                            size_hint=(.85,.4),
                                            pos_hint={'top':.95},
                                            title_size=self.font_size[0])
        
        # checks if the popup was created correctly
        if p.content is not box:
            p.content = box
        
        # opens the popup
        p.open()


# application name        
class SignMaker(App):

    # calls the popup function when the settings button is pressed
    def open_settings(self, *largs):
        self.root.popup()

    # builds and assigns TextWidget as the root widget
    def build(self):
        self.root = TextWidget()
        return self.root


# giddyup
if __name__ == "__main__":
    SignMaker().run()
