import math
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import Optional


class AtomicCounter(object):

  def __init__(self,
               manager: Manager,
               total_count: int,
               print_step: Optional[int] = None):
    self._lock = manager.Lock()
    self._value = manager.Value('i', 0)
    self.total_count = total_count
    if print_step:
      self.print_step = print_step
    else:
      # Nearest (floored) power of 10 from the total count:
      # - if count is 456, the print step will be of 100
      # - if count is 55698, the print step will be of 1000
      if total_count < 10:
        self.print_step = 1
      else:
        self.print_step = int(10 ** (math.floor(math.log10(total_count))) / 10)

  def increment(self):
    with self._lock:
      self._value.value += 1
      if self._value.value % self.print_step == 0:
        print(f"Iteration count: {self._value.value}/{self.total_count}")

  def value(self):
    with self._lock:
      return self._value.value


def _process(x: int, counter: AtomicCounter):
  try:
    # Process here, you can return None
    pass
  except Exception as e:
    print(f"Exception during processing of {x}: {e}")
  finally:
    counter.increment()


if __name__ == "__main__":
  with Pool(4) as pool:
    # Add elements to process here
    elements = []
    manager = Manager()
    counter = AtomicCounter(manager, len(elements))
    print("START")
    results = pool.starmap(_process, zip(elements, cycle([counter])))
    results = [result for result in results if result]
    print("END")