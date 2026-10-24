import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 44100
DURATION = 0.3
FREQ_0, FREQ_1, FREQ_START = 400, 800, 1200
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

print("=== RECEIVER PC ===")
print("Waiting for START beep...")
binary=""; started=False
while True:
    b=listen()
    if b is None: continue
    if not started:
        if b=="START":
            print("START heard! Receiving...")
            started=True
        continue
    if b=="START" and len(binary)>=24: break
    if b=="START": continue
    print(f"Heard: {b} ({len(binary)+1}/24)")
    binary+=b
    if len(binary)==24: break

b1,b2,bOp = binary[0:8], binary[8:16], binary[16:24]
n1,n2,op = int(b1,2), int(b2,2), chr(int(bOp,2))
if op=='+': res=n1+n2
elif op=='-': res=n1-n2
elif op=='*': res=n1*n2
elif op=='/': res=n1//n2 if n2!=0 else 0
elif op=='%': res=n1%n2
else: res=0

print(f"\nReceived: {n1} {op} {n2} = {res}")

# Beep back answer
time.sleep(1)
print(f"Beeping back answer {res}...")
play(FREQ_START, 0.8)
time.sleep(0.2)
bin_res = format(res,'08b')
for bit in bin_res:
    play(FREQ_1 if bit=='1' else FREQ_0, DURATION)
    print(f" -> {bit}")
    time.sleep(0.05)
play(FREQ_START, 0.5)
print("Answer sent!")