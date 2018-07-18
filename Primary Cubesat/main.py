from time import sleep
from multiprocessing import Pipe, Process, Array
from functions import Iridium, Laser, capture_picture, clock

def main():
    file = open("/home/pi/masterLog.txt", "a+")

    t = Array("i", 2)
    laser_p, laser_c = Pipe()
    stream_p, stream_c = Pipe()
    iridium = Iridium()
    laser = Laser()

    timekeeper = Process(target=clock, args=(t,))
    broadcast = Process(target=iridium.broadcast)
    image_transmission = Process(target=iridium.image_transmission, args=(stream_p,))
    laser_transmission = Process(target=iridium.send_message, args=(laser_p,))
    registration = Process(target=iridium.register)

    imaging = Process(target=capture_picture, args=(stream_c,))
    laser_list = Process(target=laser.measure, args=(laser_c, t,))

    timekeeper.start()
    sleep(50)

    registration.start()
    file.write("The iridium started registering at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(10)
    imaging.start()
    sleep(10)
    registration.terminate()
    file.write("The iridium stopped registering at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    broadcast.start()
    file.write("The iridium started broadcasting at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(10)
    broadcast.terminate()
    file.write("The iridium stopped broadcasting at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    image_transmission.start()
    file.write("The iridium started sending the pictures at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(100)
    image_transmission.terminate()
    file.write("The iridium stopped sending the pictures at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    laser_list.start()
    file.write("The lasers started at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(10)
    laser_transmission.start()
    file.write("The iridium started sending laser data at:" + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(60)
    laser_transmission.terminate()
    file.write("The iridium stopped sending laser data at:" + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    laser_list.terminate()
    file.write("The lasers stopped at:" + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(1)
    image_transmission.start()
    file.write("The iridium started sending the pictures at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')
    sleep(649)
    image_transmission.terminate()
    file.write("The iridium stopped sending the pictures at: " + str(t[0]).zfill(2)+":"+str(t[1]).zfill(2) + '\n')

main()
