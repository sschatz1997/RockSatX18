from time import sleep
import serial

log = ["The iridium started sending at: ", "The iridium stopped sending at: ")
o = open("masterLog.txt", "a+")
      
class Iridium:
    o.write(log[0] + time.strftime('%H:%M:%S') + '\n')
    def __init__(self, port):
        self.ser = serial.Serial(port=port, baudrate=19200, xonxoff=True)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def broadcast(self):
        while True:
            self.ser.write('AT+SBDWRT=I\'m alive'.encode())
            sleep(.1)
            self.ser.write('AT+SBDIX\r'.encode())
            self.ser.flush()

    def sendMessage(self, m):
        self.ser.write(('AT+SBDWRT= ' + m + '\r').encode())
        sleep(.1)
        self.ser.reset_input_buffer()
        self.ser.write('AT+SBDIX\r'.encode())
        strip = str.maketrans( '', '', '\r\n,')
        returned = self.ser.read(size=self.ser.in_waiting).decode().translate(strip).split(" ")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        if returned is not None:
            if len(returned) > 1:
                if returned[0] == '+SBDIX:':
                    if returned[1] != '0':
                        self.sendMessage(m)

o.write(log[1] + time.strftime('%H:%M:%S') + '\n')
o.close()
