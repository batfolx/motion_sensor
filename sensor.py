try:
    import RPi.GPIO as GPIO
except:
    pass
import send_notification
import time

def init_board():
    try:
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        # read input from 11 pin on rpi GPIO
        GPIO.setup(11, GPIO.IN)
    except:
        pass


def motion_detect():
    thresh = 0
    while True:
        movement = GPIO.input(11)
        #movement = 1
        if movement == 0:
            # no movement detected
            thresh = 0
            print('no movement detected')
        elif movement == 1:
            # movement has been detected
            thresh += 1
            print('movement detected')
            if thresh > 0:
                thresh = 0
                time.sleep(1)
                filename = send_notification.capture_picture()
                send_notification.send_text(filename)
                print("Sleeping 5 seconds to reset...")
                time.sleep(4)

        time.sleep(1)

if __name__ == '__main__':
    send_notification.init()
    init_board()
    motion_detect()
