import simpleaudio as sa
import function
import serial

#Arduino data
baudrate = 9600
port = "/dev/cu.usbmodem1101"
ID = b'2'


# Parameters
OUTPUT_FILENAME = "threading1.wav"
delay_before_stoping_recording = .1#0.37

function.first_click(port, baudrate, ID)
while True:
    function.record(port, baudrate, ID, OUTPUT_FILENAME,delay_before_stoping_recording)
    wave_obj = sa.WaveObject.from_wave_file(OUTPUT_FILENAME)
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)
    data = b''
    while data != ID:
        play_object = wave_obj.play()
        data = arduino.read()
        while play_object.is_playing():
            data = arduino.read()
            if data == ID:
                play_object.stop()
                break

    arduino.close()

    
print("END.")

#play_obj.stop()
#play_obj.is_playing()