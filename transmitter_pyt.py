import sounddevice as sd
devices = sd.query_devices()
mic = None
speaker = None
for i,d in enumerate(devices):
    if d['max_input_channels']>0 and mic is None:
        mic = i
    if d['max_output_channels']>0 and speaker is None:
        speaker = i
sd.default.device = (mic, speaker)
print(f"Using mic {mic}, speaker {speaker}")

import numpy as np
import time

SAMPLE_RATE = 44100
DURATION = 0.3
FREQ_0 = 400
FREQ_1 = 800
FREQ_START = 1200
THRESHOLD = 0.02

def play(freq, dur):
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    tone = np.sin(2*np.pi*freq*t)*0.5
    sd.play(tone, SAMPLE_RATE)
    sd.wait()

def goertzel(data, freq):
    n=len(data); k=int(0.5 + (n*freq)/SAMPLE_RATE); w=2*np.pi*k/n
    coeff=2*np.cos(w); q1=q2=0.0
    for s in data:
        q0=coeff*q1 - q2 + s; q2,q1=q1,q0
    return np.sqrt(q1*q1 + q2*q2 - q1*q2*coeff)

def listen():
    rec=sd.rec(int(DURATION*SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    d=rec[:,0]
    if np.max(np.abs(d)) < THRESHOLD: return None
    m0=goertzel(d,FREQ_0); m1=goertzel(d,FREQ_1); ms=goertzel(d,FREQ_START)
    if ms>m0 and ms>m1 and ms>15: return "START"
    return '1' if m1>m0 else '0'

def to_bin(n): return format(n,'08b')
def to_bin_c(c): return format(ord(c),'08b')

def beep_binary(binary, name):
    print(f" Beeping {name}: {binary}")
    for bit in binary:
        play(FREQ_1 if bit=='1' else FREQ_0, DURATION)
        print(f"   -> {bit}")
        time.sleep(0.05)

print("=== TRANSMITTER PC ===")
play(FREQ_START, 0.8)
time.sleep(0.2)

n1 = int(input("Enter Number 1: "))
b1 = to_bin(n1)
beep_binary(b1, f"Number 1 ({n1})")
time.sleep(0.3)

n2 = int(input("Enter Number 2: "))
b2 = to_bin(n2)
beep_binary(b2, f"Number 2 ({n2})")
time.sleep(0.3)

op = input("Enter Operator (+ - * / %): ")
bOp = to_bin_c(op)
beep_binary(bOp, f"Operator ({op})")

play(FREQ_START, 0.5)
print("\nSent! Now waiting for answer from Receiver...")

print("\n[LISTENING] Waiting for answer START beep...")
binary_ans = ""
started = False

while True:
    b = listen()
    if b is None: continue
    if not started:
        if b == "START":
            print(">>> Answer START heard! Receiving answer...")
            started = True
        continue
    if b == "START":
        if len(binary_ans) >= 8:
            break
        continue
    print(f"Heard answer bit: {b} ({len(binary_ans)+1})")
    binary_ans += b
    if len(binary_ans) == 8: 
        time.sleep(0.6)
        break

print(f"\nAnswer binary received: {binary_ans}")
ans = int(binary_ans, 2)
print(f"\n==============================")
print(f"  FINAL RESULT ON TRANSMITTER: {n1} {op} {n2} = {ans}")
print(f"==============================")