import Main as mainstuff
import threading

def runthing(run):
    #run = True
    thread = threading.Thread(target=mainstuff.mainstuff().abcabc())

    while run is True:
        thread.start()
        #mainstuff.mainstuff().abcabc()


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   runthing()
