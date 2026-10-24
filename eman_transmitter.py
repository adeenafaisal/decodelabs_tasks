import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
BIT_TIME = 0.25
LOW_SOUND = 1000
HIGH_SOUND = 2000
START_SOUND = 3000


def make_beep(frequency, seconds):
    time = np.linspace(0, seconds, int(SAMPLE_RATE * seconds), endpoint=False)
    return np.sin(2 * np.pi * frequency * time)
number1 = int(input("Enter the first number: "))
sign = input("Enter the operator (+, -, *, /): ")
number2 = int(input("Enter the second number: "))

number1_binary = format(number1, "08b")
number2_binary = format(number2, "08b")

if sign == "+":
    sign_binary = "00"
elif sign == "-":
    sign_binary = "01"
elif sign == "*":
    sign_binary = "10"
else:
    sign_binary = "11"

full_binary = number1_binary + sign_binary + number2_binary

print("First number in binary :", number1_binary)
print("Operator in binary     :", sign_binary)
print("Second number in binary:", number2_binary)
print("Full binary to send    :", full_binary)

if sign == "+":
    answer = number1 + number2
elif sign == "-":
    answer = number1 - number2
elif sign == "*":
    answer = number1 * number2
else:
    answer = round(number1 / number2, 2)

print("The correct answer is:", answer)

sound = make_beep(START_SOUND, 0.5)

for bit in full_binary:
    if bit == "0":
        beep = make_beep(LOW_SOUND, BIT_TIME)
    else:
        beep = make_beep(HIGH_SOUND, BIT_TIME)
    sound = np.concatenate((sound, beep))

input("Start Receiver on the other PC then press Enter here.")
sd.play(sound * 0.8, SAMPLE_RATE)
sd.wait()
print("Done! The sound has been sent.")