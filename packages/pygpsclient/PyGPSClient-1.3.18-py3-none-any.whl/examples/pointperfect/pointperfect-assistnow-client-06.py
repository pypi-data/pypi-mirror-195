
"""
    u-blox PointPerfect MQTT client with AssistNow v0.6

    python --version
    Python 3.10.1

    Run with -h (or --help) to see supported command line arguments:
    python pointperfect-assistnow-client.py -h

    Command line example:
    python pointperfect-assistnow-client.py -P <COM USB serial device> -i <CLIENT_ID> --region <DATA STREAM> --echo

    Download <Client key> and <Client certificate> from 
    "Thingstream > Location services > location thing > credentials" 
    to the same directory containing the client.  

"""


import argparse
import enum
import ssl
import struct
import time

# pip install paho-mqtt
import paho.mqtt.client as mqtt
# pip install pyserial
import serial


class Record:
    """Write timestamped binary records into a file.
    Each record has the following format:

    Field     | Length  | Content
    ----------+---------+------------------------------------------------
    magic     | 2 bytes | 0xAA 0x55
    timestamp | 4 bytes | Time since instantiation of the object [ms]
    kind      | 2 bytes | Identifier for the type of data in the payload
    len       | 4 bytes | Length of the payload that follows [bytes]
    payload   | n bytes | Variable-length payload
    """

    @enum.unique
    class Kind(enum.Enum):
        UNKNOWN = 0
        KEY = 1
        GGA = 2
        SFRBX = 3
        TIMELS = 4
        SPARTN = 5
        ZDA = 6
        PMP = 7
        GST = 8

    def __init__(self, file_name=None):
        if file_name:
            self.stream = open(file_name, 'wb')
            self.time_base = time.monotonic_ns()
        else:
            self.stream = None

    def add(self, kind=Kind.UNKNOWN, data=b''):
        if self.stream:
            millis = (time.monotonic_ns() - self.time_base) // 1000000
            encoded = struct.pack('>ccLHL', b'\xaa', b'\x55',
                                  millis, kind.value, len(data))
            self.stream.write(encoded)
            self.stream.write(data)

    def close(self):
        if self.stream:
            self.stream.flush()
            self.stream.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker; subscribing\n")
        client.subscribe(userdata['topics'])
    else:
        print("Connection failed!")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('Received', msg.topic, len(msg.payload) )
    # send payload to the GNSS receiver over serial
    userdata['gnss'].write(msg.payload)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-P', '--port', required=True, help='Serial port[@baudrate] of GNSS receiver')
    ap.add_argument('-i', '--client_id', required=True, help='The MQTT client ID to use')
    ap.add_argument('-s', '--server', default='pp.services.u-blox.com', help='MQTT server address')
    ap.add_argument('--region', default='uk', help='Service region. Default: uk')
    ap.add_argument('-e', '--echo', action='store_true', help='Echo position data received from GNSS')
    ap.add_argument('-r', '--record', action='store_true', help='Record position to a binary logfile')
    args = ap.parse_args()

    if args.record:
        nowstr = time.strftime('%Y%m%d_%H%M%S')
        fname = f'test_data_{nowstr}.bin'
        print('Recording log to file:', fname)
        record = Record(fname)
    else:
        record = Record()  # null-record for simplicity

    serial_params = args.port.split('@')  # split optional baudrate from port argument
    if len(serial_params) == 2:
        (port, baud) = (serial_params[0], int(serial_params[1]))
    else:
        (port, baud) = (serial_params[0], 115200)

    gnss = serial.Serial(port=port, baudrate=baud, timeout=0.1)

    # Topic names and QoS
    mqtt_topics = [(f"/pp/ip/{args.region}", 0), ("/pp/ubx/mga", 0), ("/pp/ubx/0236/ip", 0)]
    #mqtt_topics = [(f"/pp/ip/{args.region}", 0), ("/pp/ubx/mga", 0), ("/pp/ubx/0236/Lp", 0)]

    print(mqtt_topics)

    userdata = { 'gnss': gnss, 'topics': mqtt_topics }
    client = mqtt.Client(client_id=args.client_id, userdata=userdata)
    client.on_connect = on_connect
    client.on_message = on_message

    # Thingstream > Location Services > PointPerfect Thing > Credentials
    # Replace with your own file names when not using standard naming
    client.tls_set(certfile=f'device-{args.client_id}-pp-cert.crt', keyfile=f'device-{args.client_id}-pp-key.pem')
    while True:
        try:
            client.connect(args.server, port=8883)
            break
        except KeyboardInterrupt:
            pass 
        except:
            print("Trying to connect ...")
        time.sleep(3)
    try:
        client.loop_start()
        while True:
            #client.loop(timeout=0.1)  # run the client loop in the same thread, as callback access gnss
            if args.echo:
                for line in gnss.readlines():
                    if line.startswith(b'$GNGGA'):
                        record.add(Record.Kind.GGA, line)
                        print(line.decode().strip())
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        record.close()


if __name__ == '__main__':
    main()
