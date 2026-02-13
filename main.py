from pvrecorder import PvRecorder
import wave, struct, sys
from datetime import datetime

file_path = sys.argv[1]

# for index, device in enumerate(PvRecorder.get_available_devices()):
#     print(f"{index}: {device}")


def run():

    recorder = PvRecorder(device_index=1, frame_length=512)
    ending_digit = 0
    ending = False
    while not ending:
        ending_digit += 1
        audio = []
        try:
            start_time = datetime.now().strftime("%Y%m%d %H:%M:%S")
            recorder.start()

            # for i in range(9375):
            for i in range(5):
                frame = recorder.read()
                audio.extend(frame)

            recorder.stop()
            with wave.open(
                f"/Users/fergushunt/OneDrive/recordingApp/audio{ending_digit}.wav", "w"
            ) as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
                print(f"Saved file: audio{ending_digit}.wav")

        except KeyboardInterrupt:
            ending = True
            recorder.stop()
            with wave.open(
                f"/Users/fergushunt/OneDrive/recordingApp/audio{ending_digit}.wav", "w"
            ) as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))

            recorder.delete()


if __name__ == "__main__":
    # start_time = datetime.now().strftime("%Y%m%d %H:%M:%S")
    run()
