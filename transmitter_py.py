import winsound
import time

FREQ_0 = 400
FREQ_1 = 800
FREQ_START = 1200
DURATION = 300

def to_binary(num):
    return format(num, '08b')
def to_binary_char(c):
    return format(ord(c), '08b')

n1 = int(input("Enter Number 1: "))
n2 = int(input("Enter Number 2: "))
op = input("Enter Operator (+ - * / %): ")

bin1 = to_binary(n1)
bin2 = to_binary(n2)
binOp = to_binary_char(op)
full = bin1 + bin2 + binOp

print(f"\nSending: {full}")
print("START beep...")
winsound.Beep(FREQ_START, 800)
time.sleep(0.3)

for bit in full:
    if bit == '1':
        print(f"Sending 1 --- (800Hz)")
        winsound.Beep(FREQ_1, DURATION)
    else:
        print(f"Sending 0 ___ (400Hz)")
        winsound.Beep(FREQ_0, DURATION)
    time.sleep(0.05)

winsound.Beep(FREQ_START, 500)
print("Done!")