# -*- coding: UTF-8 -*-

import random

def get_random_uuid(random_number:int):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for _ in range(random_number):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt