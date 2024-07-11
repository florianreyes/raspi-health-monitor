import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from threading import Thread
from raspi_final import Pulsesensor
from database import Schema
from telegram_send import TelegramBot


class HeartbeatMeasurementApp(App):
    def build(self):
        self.nombre_cliente = "German"
        self.db = Schema(self.nombre_cliente) 
        self.sensor = Pulsesensor(channel=0)  # Replace with actual sensor channel
        self.stable_counter = 0
        self.stable_acum = 0 
        self.final_bpm = 0
        self.eps = 5
        self.telegram_bot = TelegramBot()
        main_layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        with main_layout.canvas.before:
            Color(1, 248/255, 243/255, 1)
            self.rect = Rectangle(size=(main_layout.size), pos=(main_layout.pos))
            main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add a title
        title_label = Label(text=f"{self.nombre_cliente}'s Heartbeat Measurement Station", font_size=24, size_hint=(1, 0.2), color=(0, 0, 0, 1))
        main_layout.add_widget(title_label)

        # Horizontal layout for buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Button colors
        start_color = [117/255, 134/255, 148/255, 1]
        visualize_color = [64/255, 93/255, 114/255, 1]
          # ECCEAE

        read_pulse_button = Button(text='Start New Measurement', font_size=24, size_hint=(0.5, 1),
                                   background_color=start_color)
        read_pulse_button.bind(on_press=self.show_bpm_popup)
        button_layout.add_widget(read_pulse_button)

        query_data_button = Button(text='Visualize Last Measurements', font_size=24, size_hint=(0.5, 1),
                                   background_color=visualize_color)
        query_data_button.bind(on_press=self.query_data)
        button_layout.add_widget(query_data_button)

        main_layout.add_widget(button_layout)

        return main_layout

    def show_bpm_popup(self, instance):
        self.sensor.startAsyncBPM()

        self.bpm_label = Label(text=f'BPM: {round(self.final_bpm)}', font_size=24)
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
            self.bpm_label.text = f'Final BPM: {round((self.final_bpm)//2)}'

            # Get actual unix time
            unix_time = int(time.time())
            self.telegram_bot.trigger_send_message(self.final_bpm)
            self.db.insert_medicion(unix_time, int(round((self.final_bpm)//2)))
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
        data = self.db.query_data()
        layout = GridLayout(cols=2, spacing=10, padding=10)

        layout.add_widget(Label(text="Fecha", font_size=18))
        layout.add_widget(Label(text="BPM", font_size=18))

        for row in data:
            bsastime = row[0] - 4*3600
            human_time = time.ctime(bsastime)
            layout.add_widget(Label(text=str(human_time), font_size=16))
            layout.add_widget(Label(text=str(row[1]), font_size=16))

        popup = Popup(title='Last Measurements',
                      content=layout,
                      size_hint=(None, None), size=(400, 400))
        popup.open()


    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

if __name__ == '__main__':
    HeartbeatMeasurementApp().run()
