from dotenv import load_dotenv

from arena import Arena
from api import API

import signal
from threading import Thread

if __name__ == "__main__":
  load_dotenv() 

  arena = Arena("arena-1")
  api = API(arena)

  thread = Thread(target = arena.loop)
  thread.daemon = True

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  thread.start()
  api.start()
  
  thread.join()