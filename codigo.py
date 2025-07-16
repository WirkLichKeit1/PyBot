import random

def codigo():
  return ''.join(str(random.randint(0, 9)) for _ in range(5))