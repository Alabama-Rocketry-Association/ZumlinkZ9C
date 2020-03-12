#spams data through to test software
from radio import zumlinkZ9C
if __name__ == "__main__":
    spamRadio = zumlinkZ9C.Radio(dev = "COM11", debug= True)
    SPAM = {"SPAM": "Gross Meat"}
    while(True):
        spamRadio.transmit(SPAM)
