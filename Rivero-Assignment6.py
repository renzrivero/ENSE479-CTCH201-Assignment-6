import pyaudio
import wave
from array import array
from struct import pack

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# Start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
rate=RATE, input=True,
frames_per_buffer=CHUNK)
print("Recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("Finished recording.")

# Stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

# Make wave file
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# Read wave file
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
audio = pyaudio.PyAudio()
stream = audio.open(format = 
    audio.get_format_from_width(waveFile.getsampwidth()),
    channels = waveFile.getnchannels(),
    rate = waveFile.getframerate(),
    output = True)

# Reverse wave file
fullData = []
data = waveFile.readframes(1024)

while data:
    fullData.append(data)
    data = waveFile.readframes(1024)

data = ''.join(fullData)[::-1]

for i in range(0, len(data), 1024):
    stream.write(data[i:i+1024])

data = waveFile.readframes(CHUNK)

# Play reversed wave file
print("playing record in reverse...")
while len(data) > 0:
    stream.write(data)
    data = waveFile.readframes(CHUNK)

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()