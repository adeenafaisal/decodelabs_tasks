import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter

SAMPLE_RATE = 44100
BIT_TIME = 0.25
LOW_SOUND = 1000
HIGH_SOUND = 2000
LISTEN_SECONDS = 15


def strongest_sound(piece):
    strength = np.abs(np.fft.rfft(piece * np.hanning(len(piece))))
    all_frequencies = np.fft.rfftfreq(len(piece), 1 / SAMPLE_RATE)
    strength[0] = 0
    return all_frequencies[np.argmax(strength)]


def get_binary(audio, start):
    binary = ""
    first_bit_position = start + int(0.5 * SAMPLE_RATE)
    for number in range(18):
        begin = first_bit_position + int(number * BIT_TIME * SAMPLE_RATE) + int(0.075 * SAMPLE_RATE)
        piece = audio[begin:begin + int(0.1 * SAMPLE_RATE)]
        frequency = strongest_sound(piece)
        if abs(frequency - LOW_SOUND) < abs(frequency - HIGH_SOUND):
            binary = binary + "0"
        else:
            binary = binary + "1"
    return binary


def solve(binary):
    number1 = int(binary[0:8], 2)
    sign_binary = binary[8:10]
    number2 = int(binary[10:18], 2)
    if sign_binary == "00":
        sign = "+"
        answer = number1 + number2
    elif sign_binary == "01":
        sign = "-"
        answer = number1 - number2
    elif sign_binary == "10":
        sign = "*"
        answer = number1 * number2
    else:
        sign = "/"
        if number2 == 0:
            answer = 0
        else:
            answer = round(number1 / number2, 2)
    return number1, sign, number2, answer


print("Listening for", LISTEN_SECONDS, "seconds... now press Enter on the Transmitter PC")
recording = sd.rec(LISTEN_SECONDS * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1)
sd.wait()
audio = recording[:, 0]

b, a = butter(4, [2800, 3200], btype="band", fs=SAMPLE_RATE)
start_beep = np.abs(lfilter(b, a, audio))

if start_beep.max() < 0.05:
    print("Could not hear the start beep. Increase the volume and try again.")
    raise SystemExit

start = np.argmax(start_beep > start_beep.max() * 0.5)

b, a = butter(4, [800, 2200], btype="band", fs=SAMPLE_RATE)
clean_audio = lfilter(b, a, audio)

binary_without_filter = get_binary(audio, start)
binary_with_filter = get_binary(clean_audio, start)

n1, s1, n2, answer_without_filter = solve(binary_without_filter)
m1, t1, m2, answer_with_filter = solve(binary_with_filter)

print("\n--- WITHOUT filter ---")
print("Binary  :", binary_without_filter)
print("Received:", n1, s1, n2, "=", answer_without_filter)

print("\n--- WITH filter ---")
print("Binary  :", binary_with_filter)
print("Received:", m1, t1, m2, "=", answer_with_filter)

correct_answer = float(input("\nType the correct answer shown on the Transmitter PC: "))

if answer_without_filter == correct_answer:
    print("Without filter: CORRECT")
else:
    print("Without filter: WRONG")

if answer_with_filter == correct_answer:
    print("With filter   : CORRECT")
else:
    print("With filter   : WRONG")