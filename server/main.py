from arena import Arena
from api import API

from threading import Thread

if __name__ == "__main__":
  arena = Arena()
  api = API(arena)

  thread = Thread(target = arena.run)

  thread.start()
  api.start()