import pyaudiowpatch as pyaudio
import wave 

data_format = pyaudio.paInt16
duration = 15.0
chunk = 1000
file ="audiofile.wav"
temp_data_storage = []
with pyaudio.PyAudio() as p:
    try:
        default_speaker = p.get_default_wasapi_loopback()
        

    except OSError:
        print("WASAPI is not available on this device.exciting...")
        
    except LookupError:
        print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
        

    rate = int(default_speaker["defaultSampleRate"])
    print(rate)
    sample_size = p.get_sample_size(data_format)  # sample size = no. of bytes in it.

    wave_file = wave.open(file ,"wb")
    wave_file.setnchannels(default_speaker["maxInputChannels"])
    wave_file.setframerate(rate)
    wave_file.setsampwidth(sample_size)
    
    with p.open(
        format = data_format,
        channels = default_speaker["maxInputChannels"],
        rate = rate,
        input = True,
        input_device_index = default_speaker["index"], 
        frames_per_buffer= chunk
    ) as pipe:
        print(f"next {duration} seconds while be written to this file {file}\nReading...")
        for i in range(0,(int(rate*duration/chunk))):
            data = pipe.read(chunk)
            temp_data_storage.append(data)
            
        print("Reading done")
        for i in temp_data_storage:
            wave_file.writeframes(i)
        print("writting done!")
    wave_file.close()

print(temp_data_storage)