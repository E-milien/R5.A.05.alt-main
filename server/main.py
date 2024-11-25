from dotenv import load_dotenv

from arena import Arena
from api import API

import signal
from threading import Thread

if __name__ == "__main__":
  load_dotenv() 
  
  def loop_reset():
    while True:
      if arena.is_finished():
        arena = Arena("arena-1")

  arena = Arena("arena-1")
  api = API(arena)
  
  thread_check = Thread(target = loop_reset)
  thread_check.daemon = True

  thread = Thread(target = arena.loop)
  thread.daemon = True

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  thread.start()
  thread_check.start()
  
  api.start()
  thread.join()
    
  