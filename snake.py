import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout)

from PyQt5.QtCore import Qt

class WeatherAPP(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel('enter the city name:',self)
        self.city_input =QLineEdit(self)
        self.get_weather_button =QPushButton('get wetaher', self)
        self.temperature_label =QLabel('70°F',self)
        self.emoji_label =QLabel('☀️',self)
        self.description_label =QLabel('sunny', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('weather app')

        vbox =QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label )
        vbox.addWidget(self.description_label )

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            } 
            QLabel#city_label{
                font-size: 40px;
                font-style: bold;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-=weight: bold;                        
                           
            }
            QLabel#temperature_label{
                font-size: 75px;                  
            }
            QLabel#emoji_label {
                font-size:100px;              
                font-family: Segoe UI emoji;     
            }   
            QLabel#s\description_label{
                font-size:50px;           
                                       
            }

        """)
        self.get_weather_button.clicked.connect(self.get_weather)
        
    def get_weather(self):
        api_key ='40aa0473d90d4310021b184995053a95'
        city =self.city_input.text()
        url =f'https://openweathermap.org{city}&appid={api_key}'
   
        try:
            response =requests.get(url)
            response.raise_for_status()
            data =response.json()

            if data ['cod'] ==200:
               self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error('bad request:\n plese check your input')
                case 401:
                    self.display_error('UN AUTHORIZED:\n INVALID API KEY')
                case 403:
                    self.display_error('FORBIDDEN :\n ACCESS IS DENIED ')
                case 404:
                    self.display_error('NOT FOUND:\n CITY NOT FOUND')
                case 500:
                    self.display_error('INTERNAL SERVER ERROR:\n plese TRY AGAIN LATER')
                case 502:
                    self.display_error('BAD GATEWAY :\n INVALID RESPONSE FROM THE SERVER ')
                case 503:
                    self.display_error('SERVICE UNAVAILABLE :\n SERVER IS DOWN')
                case 505:
                    self.display_error('GATEWAY TIME OUT :\n NO RESPONSE FROM THE SERVER')

                case _:
                    self.display_error(f'HTTP error accured :\n{http_error}')
        
                
        except requests.exceptions.ConnectionError:
            self.display_error('connection error:\n check your internet connection ')    
        except requests.exceptions.Timeout:
            self.display_error('time out errror:\n the request timed out')
        except requests.exceptions.TooManyRedirects:
            self.display_error('too many redirects:\n check your url')


        except requests.exceptions.RequestException as req_error:
            self.display_error(f'request error \n{req_error}')

    def display_error(self, message):
        self.temperature_label.setStyleSheet('font-size: 30px;')
        self.temperature_label.setText(message)

    def display_weather(self, data):
        self.temperature_label.setStyleSheet('font-size: 75px;')

        temperature_k= data['main']['temp']        
        temperature_f = (temperature_k * 9/5) - 459.67
        self.temperature_label.setText(f'{temperature_f:.0f}°F')

if __name__ =="__main__":
    app =QApplication(sys.argv)
    Weather_aPP = WeatherAPP()
    Weather_aPP.show()
    sys.exit(app.exec_())