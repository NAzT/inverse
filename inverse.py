import serial, sys, time, re, os
import threading
import logging
import time, struct

# import paho.mqtt.client as mqtt
# import paho.mqtt.client as paho
# import paho.mqtt.publish as _publish
from numpy import interp

# import numpy as np
#reload(sys)
#sys.setdefaultencoding('utf8')

running = False
step = ""

# def publish(msg):
#   # print msg
#   output = _publish.single("hello", payload=msg, qos=0,
#       retain=False, hostname="localhost", port=1883,
#       keepalive=60, will=None,  tls=None, protocol=mqtt.MQTTv31)
 
# def on_message(client1, userdata, message):
#     print("message received  "  , str(message.payload.decode("utf-8")))
#     global running, step
#     step = str(message.payload.decode("utf-8"))
#     print(step)
#     control(int(step))
#     running = True



device = '/dev/tty.usbserial-14210'
baud = 115200

if not device:
    # devicelist = commands.getoutput("ls /dev/ttyAMA*")
    if devicelist[0] == '/':
        device = devicelist
    if not device:
        print("Fatal: Can't find usb serial device.")
        sys.exit(0);
    else:
        print("Success: device = %s"% device)

ser = serial.Serial(
    port=device,
    baudrate=baud,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# client = paho.Client()
# client.on_publish = on_publish
# client.on_message = on_message 
# client.connect("mqtt.cmmc.io", 1883)
# client.loop_start() 
# client.subscribe("pendulum/$/command")


def handle_data(data):
    print(data)

#https://stackoverflow.com/a/27628622
def readline(a_serial, eol=b'\r\n'):
    leneol = len(eol)
    line = bytearray()
    while True:
        c = a_serial.read(1)
        # print(c)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return (line)

def str2hexstr(line):
  return " ".join(hex(ord(n)) for n in line)

print("reading...")
def read_from_port(ser):
    while True:
        try:
            line = readline(ser)
            pendulum_angle, pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B = line.decode("utf-8").strip().split(",")
            # status = (float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B)
            status = (float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B)
            print(status)

            theta = status[0]
            if theta < 0:
                theta = 180.0 - status[0]
            # print(status)
            # print('pendulum pendulum_angle', pendulum_angle)
            # theta = interp(abs(float(status[0])), [0, 180], [0, 360])
            # print('theta', float(status[0])

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("closing serial port...")
            ser.close()
            sys.exit()
        finally:
            pass


def control(mode, step):
    # print("do control", step)
    global ser
    command = [0xff, mode]
    command += list(struct.pack(">h", step))
    # print("Q", step, (struct.pack(">h", step)))

    data_sum = 0
    for x in command:
        data_sum += x

    our_checksum = (~data_sum & 0xFF)
    command.append(our_checksum)
    # print(command)
    # print(command)
    # # for l in range(1, data_len-1-1):
    # #   d = port.read()
    # #   data_out.append(ord(d))
    # #   # print "%s"% (hexdump.dump(d))
    # # mcu_checksum = ord(port.read())
    # # our_checksum = (~data_sum & 0xFF)
    ser.write(command)
    running = False


thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

t = .2
v = 300
mode = 0x02

# for x in xrange(60, 400):
#     for y in range(2):
#         print(x)
#         control(mode, v)
#         time.sleep(t)
#         control(mode, -v)
#         time.sleep(t)

# t = .2
# v = 30
# mode = 0x02

# # action = env.action_space.sample() # your agent here (this takes random actions)
# # observation, reward, done, info = env.step(action)
# # time.sleep(.2)
# # print("FPS: ", 1.0 / (time.time() - start_time))

# control(mode, v)
# # time.sleep(1)
# for x in range(0, 500):
#     for y in range(4):
#         # v = x          
#         print(x)
#         control(mode, v)
#         time.sleep(t)
#         control(mode, -v)
#         time.sleep(t)
