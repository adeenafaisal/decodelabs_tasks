import numpy as np
import sounddevice as sd

# Audio & Communication Parameters
FS = 44100  # Sampling frequency
BIT_DURATION = 0.15  # Duration of each bit in seconds
FREQ_0 = 1200  # Frequency for binary '0'
FREQ_1 = 2200  # Frequency for binary '1'
START_FREQ = 3000  # Synchronization start tone


def text_to_bits(text):
  """Converts text/characters into an 8-bit binary list."""
  bits = []
  for char in text:
    b = format(ord(char), '08b')
    bits.extend([int(bit) for bit in b])
  return bits


def bits_to_audio(bits):
  """Modulates binary bits into audible frequency tones (FSK)."""
  # Play a start tone for synchronization (0.3 seconds)
  start_t = np.linspace(0, 0.3, int(FS * 0.3), endpoint=False)
  start_tone = 0.5 * np.sin(2 * np.pi * START_FREQ * start_t)
  audio = [start_tone]

  # Generate tones for each bit
  for bit in bits:
    t = np.linspace(0, BIT_DURATION, int(FS * BIT_DURATION), endpoint=False)
    freq = FREQ_1 if bit == 1 else FREQ_0
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    audio.append(tone)

  # Add short trailing silence
  silence = np.zeros(int(FS * 0.2))
  audio.append(silence)
  return np.concatenate(audio)


def transmit(text):
  """Transmits a string value via acoustic sound pulses."""
  print(f"\n[Transmitting] '{text}'...")
  bits = text_to_bits(text)
  print(f"Binary: {''.join(map(str, bits))}")
  audio = bits_to_audio(bits)
  sd.play(audio, FS)
  sd.wait()
  print("Transmission complete.")


def detect_start_tone():
  """Listens via microphone for the receiver's start tone."""
  print("\n[Listening] Waiting for response from receiver...")
  chunk_duration = 0.1
  chunk_samples = int(FS * chunk_duration)

  while True:
    audio = sd.rec(chunk_samples, samplerate=FS, channels=1, dtype='float32')
    sd.wait()
    audio = audio.flatten()

    fft_res = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1 / FS)
    peak_freq = freqs[np.argmax(np.abs(fft_res))]
    peak_amp = np.max(np.abs(fft_res))

    # Detect 3000 Hz start tone with amplitude threshold
    if abs(peak_freq - START_FREQ) < 100 and peak_amp > 10:
      print("Start tone detected from receiver!")
      return


def receive_response(num_chars=10):
  """Decodes incoming sound pulses back into characters."""
  detect_start_tone()
  sd.sleep(int(300))  # Wait out start tone duration

  total_bits = num_chars * 8
  bits = []
  samples_per_bit = int(FS * BIT_DURATION)

  for _ in range(total_bits):
    audio = sd.rec(samples_per_bit, samplerate=FS, channels=1, dtype='float32')
    sd.wait()
    audio = audio.flatten()

    fft_res = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1 / FS)
    power = np.abs(fft_res) ** 2

    idx_0 = np.argmin(np.abs(freqs - FREQ_0))
    idx_1 = np.argmin(np.abs(freqs - FREQ_1))

    energy_0 = np.sum(power[max(0, idx_0 - 2) : idx_0 + 3])
    energy_1 = np.sum(power[max(0, idx_1 - 2) : idx_1 + 3])

    bits.append(1 if energy_1 > energy_0 else 0)

  # Convert bits back to characters
  chars = []
  for i in range(0, len(bits), 8):
    byte_bits = bits[i : i + 8]
    byte_str = "".join(map(str, byte_bits))
    chars.append(chr(int(byte_str, 2)))

  result_str = "".join(chars).strip()
  return result_str


if __name__ == "__main__":
  print("=== ACOUSTIC TRANSMITTER ===")

  # 1. Get and transmit Number 1
  num1 = input("Enter Number 1 (e.g., 5): ")
  transmit(num1)

  # 2. Get and transmit Operator
  op = input("Enter Operator (+, -, *, /): ")
  transmit(op)

  # 3. Get and transmit Number 2
  num2 = input("Enter Number 2 (e.g., 3): ")
  transmit(num2)

  # 4. Receive final result from receiver PC
  final_result = receive_response(num_chars=8)
  print(f"\n>> Received Calculation Result from Receiver: {final_result}")