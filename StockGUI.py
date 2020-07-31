import sys
import time

print('This message will be displayed on the screen.')




def logconsole():
    with open('filename.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print("asdf")





while True:

    f = open('filename.txt', 'a')

    sys.stdout = f
    print("bruh")
    print("hello")
    time.sleep(1)

