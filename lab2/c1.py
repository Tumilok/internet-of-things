from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "Living room",
    "sheet": "sheet_smarthouse.png",
    "width": 332,
    "height": 300,
    "leds": [
        {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
        {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
        {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
    ],
    "buzzers": [
        {"x": 277, "y": 9, "name": "Buzzer", "pin": 16, "frequency": 440},
    ]
}

circuit = TkCircuit(configuration)


@circuit.run
def main():
    from gpiozero import LED, Button
    import socket
    import struct

    MCAST_GRP = '236.0.0.0'
    MCAST_PORT = 3456

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def send_to_kitchen():
        print('SENT TO KITCHEN')
        sock.sendto('f1;kitchen;lamp;1;change'.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    def receive():
        command = sock.recv(10240).decode("utf-8").split(';')
        if command[0] == 'f1' or command[0] == '*':
            if command[1] == 'living_room' or command[1] == '*':
                if command[2] == 'lamp' or command[2] == '*':
                    if command[3] == '1' or command[3] == '*':
                        if command[4] == 'on':
                            led.on()
                        elif command[4] == 'off':
                            led.off()
                        elif command[4] == 'change':
                            led.toggle()

    led = LED(21)

    button1 = Button(11)
    button1.when_pressed = led.toggle

    button2 = Button(12)
    button2.when_pressed = send_to_kitchen

    while True:
        receive()
