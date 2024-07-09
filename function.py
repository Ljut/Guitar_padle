import queue
import threading
import time
import wave
import pyaudio
import serial

# Parameters
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sample rate
FRAMES_PER_BUFFER = 1024  # Buffer size
frames = []


def createWave(OUTPUT_FILENAME, pAudio):
    #to clear wav file
    #open("OUTPUT_FILENAME", "w").close()
    waveFile = wave.open(OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pAudio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    frames[:] = []
    return

def first_click(port, baudrate, ID):
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)
    #Whait before use
    print("Press Paddle to START recording.")

    while True:
        data = arduino.read()
        if data == ID:
            break
    #data = b''
    arduino.close()
    print("Paddle record START.")
    #time.sleep(2)
    print("START.")
    return


def record(port, baudrate, ID, OUTPUT_FILENAME, delay_before_stoping_recording):
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)

    # Queue to hold Arduino data
    arduino_queue = queue.Queue()

    # Queue to hold audio data
    audio_queue = queue.Queue()

    #Event signal for threading
    stop_event = threading.Event()

    # Define the callback function for the audio stream
    def audio_callback(in_data, frame_count, time_info, status):
        if status:
            print(status)
        audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    # Function to read from Arduino
    def read_arduino():
        while not stop_event.is_set():
            data = arduino.read()  # Adjust read method and parameters as needed
            arduino_queue.put(data)
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=FRAMES_PER_BUFFER,
                    stream_callback=audio_callback)


    # Start the audio stream
    stream.start_stream()

    # Start the Arduino reading thread
    arduino_thread = threading.Thread(target=read_arduino)
    arduino_thread.daemon = True
    arduino_thread.start()

    try:
        stop_loop = 0
        while True:
            # Process audio data
            while not audio_queue.empty():
                audio_data = audio_queue.get()
                frames.append(audio_data)
                # Do something with audio_data (e.g., save to a file, process it, etc.)

            # Process Arduino data
            while not arduino_queue.empty():
                arduino_data = arduino_queue.get()
                print("\n\t"+str(arduino_data)+"\n")
                if arduino_data == ID:
                    stop_loop = 1
            
            if stop_loop == 1:
                #delay_before_stoping_recording
                time.sleep(delay_before_stoping_recording)
                break
                # Do something with arduino_data (e.g., process it, etc.)

            #time.sleep(0.1)  # Sleep to prevent 100% CPU usage
    except KeyboardInterrupt:
        print("except")
        print("Recording stopped by user.")
        #createWave(OUTPUT_FILENAME, p)
        stream.stop_stream()
        stream.close()
        p.terminate()
        arduino.close()
        

    createWave(OUTPUT_FILENAME, p)
    stream.stop_stream()
    stream.close()
    p.terminate()

    stop_event.set()
    arduino_thread.join()
    print("Function END.")
    pass