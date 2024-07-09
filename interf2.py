import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from threading import Thread
from raspi_final import Pulsesensor
from database import Schema

class HeartbeatMeasurementApp(App):
    def build(self):
        self.db = Schema("cliente") 
        self.sensor = Pulsesensor(channel=0)  # Replace with actual sensor channel
        self.stable_counter = 0
        self.stable_acum = 0 
        self.final_bpm = 0
        self.eps = 5
        main_layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        with main_layout.canvas.before:
            Color(0.07, 0.10, 0.26, 1)  # 131842
            self.rect = Rectangle(size=(main_layout.size), pos=(main_layout.pos))
            main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add a title
        title_label = Label(text='Heartbeat Measurement Station', font_size=24, size_hint=(1, 0.2), color=(1, 1, 1, 1))
        main_layout.add_widget(title_label)

        # Horizontal layout for buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Button colors
        button_color = [236/255, 206/255, 174/255, 1]  # ECCEAE

        read_pulse_button = Button(text='Start New Measurement', font_size=24, size_hint=(0.5, 1),
                                   background_color=button_color)
        read_pulse_button.bind(on_press=self.show_bpm_popup)
        button_layout.add_widget(read_pulse_button)

        query_data_button = Button(text='Visualize Last Measurements', font_size=24, size_hint=(0.5, 1),
                                   background_color=button_color)
        query_data_button.bind(on_press=self.query_data)
        button_layout.add_widget(query_data_button)

        main_layout.add_widget(button_layout)

        return main_layout

    def show_bpm_popup(self, instance):
        self.sensor.startAsyncBPM()

        self.bpm_label = Label(text=f'BPM: {self.final_bpm}', font_size=24)
        self.bpm_popup = Popup(title='Real-time BPM',
                               content=self.bpm_label,
                               size_hint=(None, None), size=(400, 200))

        self.bpm_popup.bind(on_dismiss=self.stop_bpm)
        self.bpm_popup.open()

        Clock.schedule_interval(self.update_bpm_label, 1)


    def update_bpm_label(self, dt):
        print(self.stable_acum)
        print(self.stable_counter)
        if self.stable_counter == 0:
            self.stable_acum = self.sensor.BPM
            self.stable_counter+=1
        elif self.stable_counter == 4:
            self.final_bpm = self.stable_acum/self.stable_counter
            self.sensor.stopAsyncBPM()
            self.bpm_label.text = f'Final BPM: {round(self.final_bpm)}'

            # Get actual unix time
            unix_time = int(time.time())

            self.db.insert_medicion(unix_time, int(self.final_bpm))
            self.final_bpm, self.stable_acum, self.stable_counter = (0,0,0)
            print(self.db.query_data())
            Clock.unschedule(self.update_bpm_label)
        else:
            if abs((self.stable_acum/self.stable_counter)-self.sensor.BPM) < self.eps and self.sensor.BPM > 30:
                self.stable_counter+=1
                self.stable_acum += self.sensor.BPM
            else:
                self.stable_acum = 0
                self.stable_counter = 0
            self.bpm_label.text = f'BPM: {round((self.sensor.BPM)//2)}'

    def stop_bpm(self, instance):
        self.sensor.stopAsyncBPM()
        Clock.unschedule(self.update_bpm_label)

    def query_data(self, instance):
        print("Querying data...")
        popup = Popup(title='Info',
                      content=Label(text='Displaying last measurements.'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

if __name__ == '__main__':
    HeartbeatMeasurementApp().run()
