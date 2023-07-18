import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BOARD)

gpio_pins = [11, 12, 13, 15, 16, 18, 22, 7]
gpiobounce = 100

for gpio in gpio_pins:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

startmovie = "/home/pi/video/start.mp4"
movies = [
    "/home/pi/video/video1.mp4",
    "/home/pi/video/video2.mp4",
    "/home/pi/video/video3.mp4",
    "/home/pi/video/video4.mp4",
    "/home/pi/video/video5.mp4",
    "/home/pi/video/video6.mp4",
    "/home/pi/video/video7.mp4",
    "/home/pi/video/video8.mp4"
]

current_video = None
start_time = time.time()

try:
    while True:
        for i, gpio in enumerate(gpio_pins):
            if GPIO.input(gpio) == GPIO.LOW:
                if current_video is not None and current_video.poll() is None:
                    if current_video.args[3] == movies[i]:
                        current_video.stdin.write(b'q')
                        current_video.stdin.flush()
                        current_video.kill()
                        current_video = None
                    else:
                        continue
                
                print(f"GPIO#{i} triggered")
                print(f"Playing video: {movies[i]}")
                current_video = subprocess.Popen(['omxplayer', '-b', '--no-osd', movies[i]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
                start_time = time.time()
                
        if current_video is not None and current_video.poll() is not None:
            if time.time() - start_time > 10:
                current_video = None

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    if current_video is not None and current_video.poll() is None:
        current_video.stdin.write(b'q')
        current_video.stdin.flush()
        current_video.kill()
    
    GPIO.cleanup()

print("Program terminated.")
