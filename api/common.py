# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

def read_data(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]
    return data