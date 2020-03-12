#testing listening function
from radio.zumlinkZ9C import Radio
if __name__ == "__main__":
    recv = Radio(dev = "COM12", debug=True)
    recv.listen()