from pvrecorder import PvRecorder
import wave
import struct
import sys
import math
from datetime import datetime

try:
    file_path = sys.argv[1]
except IndexError:
    file_path = "/Users/fergushunt/Documents/idle-recorder/assets"

# TODO: this is my second merge test commit


def select_device():
    for index, device in enumerate(PvRecorder.get_available_devices()):
        print(f"{index}: {device}")
    selected_device_index = int(input("What device would you like to record(index): "))
    return selected_device_index


def run():

    datetime_format = "%Y-%m-%d %H:%M:%S"
    time_interval = float(input("What length time intervals would you like(min): "))
    end_time_string = input(
        "What time would you like to stop recording(%Y-%m-%d %H:%M:%S): "
    )
    end_time = datetime.strptime(end_time_string, datetime_format)

    # time_interval = int(input("What length time intervals would you like(min): "))
    device_index = select_device()

    recorder = PvRecorder(device_index=device_index, frame_length=512)
    frame_length = 512 / 16000

    frame_number = math.ceil((time_interval * 60) / frame_length)

   while datetime.now() < end_time:
        audio = []
        start_time = datetime.now().strftime("%Y%m%d-%H:%M:%S")
        file_name = f"{start_time}_length{time_interval}.wav"
        try:
            recorder.start()

            # for i in range(9375):
            for i in range(frame_number):
                frame = recorder.read()
                audio.extend(frame)

            recorder.stop()
            with wave.open(
                f"{file_path}/{file_name}",
                "w",
            ) as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
                print(f"Saved file: {file_name}")

        except KeyboardInterrupt:
            recorder.stop()
            with wave.open(f"{file_path}/{file_name}", "w") as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))

            recorder.delete()


if __name__ == "__main__":
    run()
