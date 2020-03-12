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

    def __init__(self, dev, baudrate=115200, debug=False):
        super().__init__(dev, baudrate=baudrate)
        log("Radio Initialized: {0}-{1}Baud".format(dev, baudrate), debug)
        self.transmissions = {}
        self.v = debug
        self.count = 0

    def serialize(self, data: dict):
        bsonObject = bson.dumps(data)
        size = len(bsonObject)
        start = "A{0}A".format(size).encode()
        bsonObject = start + bsonObject
        return bsonObject

    def debug(self):
        # debug terminal to set env variables
        #press the button on the side of the dev board to access the cli
        assert super().isOpen() == True
        while 1:
            req = input("<ZUMLINK>")
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
        data = self.serialize(data)
        log(super().write(data), self.v)
        time.sleep(0.1)

    def listen(self):
        while True:
            log("Waiting:{0} Bytes".format(super().inWaiting()), self.v)
            while True:
                buffer = super().read(1)
                size = ""
                log(buffer, self.v)
                if buffer == b'A':
                    while True:
                        buffer = super().read(1)
                        log(buffer, self.v)
                        if buffer == b'A':
                            break #breaks right before the message body
                        else:
                            size += buffer.decode()
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
                    log("Buffer: {0} Bytes".format(super().inWaiting()), self.v)
                    continue

    def dump(self, data:dict):
        with open("transmission{0}.packet".format(self.count), "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()

if __name__ == "__main__":
    dummy = {"shit": 0}
    # print(dummy)
    # ZumlinkZ9.packetizeSerialize(dummy)
    com = Radio(dev="COM12", debug=True)
    com.transmit(dummy)