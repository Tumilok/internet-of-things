from gpiozero import Button, AngularServo
from pyowm.owm import OWM

from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)

places = ['Kraków,PL', 'Istanbul,TR', 'Stockholm,SE']
place_idx = 0

servo1 = AngularServo(17, min_angle=-90, max_angle=90)
servo1.angle = -90


def get_statuses(place):
    owm = OWM('4526d487f12ef78b82b7a7d113faea64')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    return observation.weather.detailed_status, observation.weather.status


def next_place():
    global place_idx
    place_idx = (place_idx + 1) % len(places)
    draw_weather()


def prev_place():
    global place_idx
    if place_idx == 0:
        place_idx = len(places) - 1
    else:
        place_idx = place_idx - 1
    draw_weather()


def draw_weather():
    detailed_status, status = get_statuses(places[place_idx])
    print(places[place_idx] + ': ' + status + ', ' + detailed_status)
    if status == 'Clear':
        servo1.angle = -70
    elif status == 'Clouds':
        if detailed_status == 'few clouds':
            servo1.angle = -40
        elif detailed_status == 'scattered clouds':
            servo1.angle = -20
        elif detailed_status == 'broken clouds':
            servo1.angle = 0
        else:
            servo1.angle = 20
    elif status == 'Drizzle':
        servo1.angle = 30
    elif status == 'Rain':
        servo1.angle = 40
    elif status == 'Thunderstorm':
        servo1.angle = 50
    else:
        servo1.angle = 90


@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from time import sleep

    button_next = Button(11)
    button_prev = Button(12)

    button_next.when_pressed = next_place
    button_prev.when_pressed = prev_place

    draw_weather()

    while True:
        sleep(0.1)
