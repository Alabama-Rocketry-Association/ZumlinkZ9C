# zumlink

from serial import Serial
import bson
import time
from datetime import date
import json

def log(msg, verbose):
    if verbose:
        print(msg)

class Radio(Serial):

    def __init__(self, dev, baudrate=115200, verbose=False):
        super().__init__(dev, baudrate=baudrate)
        print("Radio Initialized: {0}-{1}Baud".format(dev, baudrate))
        self.transmissions = {}
        self.v = verbose
        self.count = 0

    def packetizeSerialize(self, data: dict):
        bsonObject = bson.dumps(data)
        size = len(bsonObject)
        start = "A{0}A".format(size).encode()
        bsonObject = start + bsonObject
        return bsonObject

    def parsePacketized(data: bytes):
        # basic transmitting format
        if data[0] == 65 and data[-1] == 122:
            data = data[0, len(data) - 1]
            size = b''
            i = 1
            while True:
                if data[i] == 65:
                    break
                else:
                    size = size + data[i]
            size = size.decode()
        else:
            raise Exception("Corrupted Data")

    def debug(self):
        # debug terminal to set env variables
        assert super().isOpen() == True
        while 1:
            req = input("term>>>")
            if req == "exit()":
                break
            req = req.encode()
            super().write(req + b'\r\n')
            output = b''
            time.sleep(0.5)  # set at half second, if device doesnt res increment
            while super().inWaiting() > 0:
                output = super().read(1)
                if output != '':
                    print(output.decode(), end='')

    def transmit(self, data: dict):
        data = self.packetizeSerialize(data)
        log(super().write(data), self.v)
        time.sleep(0.1)

    def listen(self):
        while True:
            log("Waiting:{0} Bytes".format(super().inWaiting()), self.v)
            while True:
                buffer = super().read(1).decode()
                size = ""
                if buffer == 'A':
                    while True:
                        buffer = super().read(1).decode()
                        if buffer == 'A':
                            break #breaks right before the message body
                        else:
                            size += buffer
                            continue
                    log("Message Size:{0} Bytes".format(size), self.v)
                    size = int(size)  # converts string literal number into a number datatype
                    try:
                        data = bson.loads(super().read(size))
                    except Exception("Corrupted Data"):
                        continue
                    self.dump(data)
                    self.count += 1
                else:
                    continue

    def dump(self, data:dict):
        with open("transmission{0}.packet".format(), "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()

if __name__ == "__main__":
    dummy = {"dummy": 0}
    # print(dummy)
    # ZumlinkZ9.packetizeSerialize(dummy)
    com = Radio(dev="COM12", verbose=True)
    com.transmit(dummy)
