from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

def read_pulse(instance):
    # Replace this function with your actual read_pulse() function
    print("Reading pulse...")
    popup = Popup(title='Info',
                  content=Label(text='Pulse reading started.'),
                  size_hint=(None, None), size=(400, 200))
    popup.open()

def query_data(instance):
    # Replace this function with your actual query_data() function
    print("Querying data...")
    popup = Popup(title='Info',
                  content=Label(text='Displaying last measurements.'),
                  size_hint=(None, None), size=(400, 200))
    popup.open()

class HeartbeatMeasurementApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        with main_layout.canvas.before:
            # set color to FFF8F3
            Color(1, 248/255, 243/255, 1)
            self.rect = Rectangle(size=(main_layout.size), pos=(main_layout.pos))
            main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add a title
        title_label = Label(text='Heartbeat Measurement Station', font_size=45, size_hint=(1, 0.2), color=(0,0,0,1))
        main_layout.add_widget(title_label)
        
        # Horizontal layout for buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Button colors
        # set start colors to 758694
        start_color = [117/255, 134/255, 148/255, 1]

        #set visualize color to 405D72
        visualize_color = [64/255, 93/255, 114/255, 1]

        
        read_pulse_button = Button(text='Start New Measurement', font_size=32, size_hint=(0.5, 1),
                                   background_color=start_color)
        read_pulse_button.bind(on_press=read_pulse)
        button_layout.add_widget(read_pulse_button)

        query_data_button = Button(text='Visualize Last Measurements', font_size=32, size_hint=(0.5, 1),
                                   background_color=visualize_color)
        query_data_button.bind(on_press=query_data)
        button_layout.add_widget(query_data_button)

        main_layout.add_widget(button_layout)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

if __name__ == '__main__':
    HeartbeatMeasurementApp().run()
