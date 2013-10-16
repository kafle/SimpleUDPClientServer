import random

def generate_seq_no():
  return random.randint(0, 65535)

def generate_request_id(data):
  return generate_seq_no() + len(data)

def cumulative_moving_avg(t_new, count, t_avg):
  return t_avg + ((t_new - t_avg)/(count+1))
