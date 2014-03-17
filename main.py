from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.event import EventDispatcher
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty

###############################################################################
"""
Sign Maker - Version 1.3
Copyright (C) 2014 Kris Shamloo

A Mercury Labs application.
Special thanks to the Kivy development team.

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


"""
###############################################################################

colorcounter = 1
fontcounter = 3
                 
# primary application widget                
class TextWidget(FloatLayout):

    text_color = ListProperty([1,1,1,1])
    text_background_color = ListProperty([1,1,1,1])
    display_text = StringProperty("Hello")
    font_size = NumericProperty(150)
    ui_font_size = NumericProperty(Window.width/20)
    btn1_label = StringProperty("Large")
    btn2_label = StringProperty("White")
    settings_popup = ObjectProperty(None, allownone=True)

   
    # initialize the canvas
    def __init__(self, **kwargs):
        super(TextWidget,self).__init__(**kwargs)
    
      
    # text input popup
    def text_popup(self, *args):
        
        # updates the display text
        def on_text(instance, value):
            self.display_text = value
        
        # cycles through 4 preset font sizes
        def size_button(instance):
            global fontcounter

            if fontcounter == 0:
                self.font_size = 35 #small
                self.btn1_label = "Small"
                btn1.text=(self.btn1_label)
                fontcounter += 1
            
            elif fontcounter == 1:
                self.font_size = 80 #medium
                self.btn1_label = "Medium"
                btn1.text=(self.btn1_label)
                fontcounter += 1
                
            elif fontcounter == 2:
                self.font_size = 150 #large
                self.btn1_label = "Large"
                btn1.text=(self.btn1_label)
                fontcounter += 1
                
            elif fontcounter == 3:
                self.font_size = 250 #huge
                self.btn1_label = "Huge"
                btn1.text=(self.btn1_label)
                fontcounter = 0
        
            else:
                fontcounter = 0
        
        # cycles through 4 preset colors
        def color_presets(instance):
            global colorcounter
            
            if colorcounter == 0:
                self.text_color = [1,1,1,1] #white
                self.btn2_label="White"
                btn2.text=(self.btn2_label)
                colorcounter += 1
            
            elif colorcounter == 1:
                self.text_color = [.95,.25,.37,1] #red
                self.btn2_label = "Red"
                btn2.text=(self.btn2_label)
                colorcounter += 1
            
            elif colorcounter == 2:
                self.text_color = [.37,.95,.25,1] #green
                self.btn2_label = "Green"
                btn2.text=(self.btn2_label)
                colorcounter += 1
                
            elif colorcounter == 3:
                self.text_color = [.25,.37,.95,1] #blue
                self.btn2_label = "Blue"
                btn2.text=(self.btn2_label)
                colorcounter = 0
                
            else:
                colorcounter = 0


        # opens a color selection popup
        def color_button(instance):
            self.color_picker()
        
        # does a backspace on the text        
        def backspace(instance):
            t.do_backspace()
                
        # building the all important popup
        p = self.settings_popup
        
        # popup root widget
        box = BoxLayout(orientation='vertical')
        
        # popup text input, child of box
        t = TextInput(text=self.display_text,
                      background_color=[.7,.7,.7,1],
                      font_size=self.ui_font_size,
                      font_name="NanumGothic.ttf")
        t.bind(text=on_text)
        
        # this BoxLayout holds the buttons, child of box
        b = BoxLayout(orientation='horizontal',size_hint=(1,.33))

        btn1 = Button(text=self.btn1_label,font_size=self.ui_font_size)
        btn1.bind(on_press=size_button)
        
        btn2 = Button(text=self.btn2_label,font_size=self.ui_font_size)
        btn2.bind(on_press=color_presets)
        
        btn3 = Button(text='Colors',font_size=self.ui_font_size)
#        btn3.bind(on_press=flash_button)
        btn3.bind(on_press=color_button)
        
        btn4 = Button(text='<<',size_hint=(.5,1),font_size=self.ui_font_size)
        btn4.bind(on_press=backspace)
        
        # adding the buttons to our BoxLayout b, children of b
        b.add_widget(btn1)
        b.add_widget(btn2)
        b.add_widget(btn3)
        b.add_widget(btn4)

        # adding t and b to our BoxLayout box, children of box
        box.add_widget(t)
        box.add_widget(b)

        if p is None:
            self.settings_popup = p = Popup(content=box,
                                            title='Change your message.',
                                            size_hint=(.85,.4),
                                            pos_hint={'top':.95},
                                            title_size=self.ui_font_size)
        if p.content is not box:
            p.content = box
        #p.bind(on_dismiss=Keyboard.release)
        p.open()
        #keyboard.release_all_keyboards    

    # color picker popup
    def color_picker(self, *args):
        
        def on_color(instance, value):
            self.text_color = value
        clr=ColorPicker(font_size=self.ui_font_size)
        
        p = Popup(title='Change your color.',
        content=clr,
        size_hint=(.9,.6),
        pos_hint={'top':.9},
        title_size=self.ui_font_size)
        
        clr.bind(color=on_color)
        p.open()   

        
        

# application name and root framework
class SignMaker(App):
    #opens up the popup when the settings button is press
    def open_settings(self, *largs):
        print("settings!")
        self.root.text_popup()

    # note self.root, this allows us to access the popup function in the line
    # above this one with self.root.text_popup()
    def build(self):
        self.root = TextWidget()
        return self.root

# giddyup                    
if __name__ == "__main__":
    SignMaker().run()

