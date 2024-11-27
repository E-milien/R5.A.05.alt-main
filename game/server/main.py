from dotenv import load_dotenv
import os

from arena import Arena
from api import API

import signal
from threading import Thread

if __name__ == "__main__":
  load_dotenv() 

  id = os.environ.get("ARENA", "arena")

  arena = Arena(id)
  api = API(arena)

  main_thread = Thread(target = arena.main_loop)
  main_thread.daemon = True

  check_thread = Thread(target = arena.check_loop)
  check_thread.daemon = True

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  main_thread.start()
  check_thread.start()

  api.start()
  
  main_thread.join()