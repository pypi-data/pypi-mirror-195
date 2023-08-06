from tqdm import tqdm
import time


def test():
    print('OK')


def test_p_bar():
    for _ in tqdm(range(20)):
        time.sleep(0.1)
