import random
from collections import deque

MIN_ID = 1000
MAX_ID = 9999
SEED = 0

class IdGenerator:
    def __init__(self, seed : int):
        random.seed(seed)
        self.ids = list(range(MIN_ID, MAX_ID+1))
        random.shuffle(self.ids)
        self.dq = deque(self.ids)

    def get_next_id(self) -> int:
        return self.dq.popleft()
    
id_generator = IdGenerator(SEED)