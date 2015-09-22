__author__ = 'Jian Yang'
__date__ = '9/17/15'

import random
import argparse
import os

DIRECTIONS = {0:(1, 0), 1:(0, 1), 2:(-1, 0), 3:(0, -1)}

def isc(state, i, j, d, c, step):
    pi = i + DIRECTIONS[d][0] * step
    pj = j + DIRECTIONS[d][1] * step
    if pi in range(0, 7) and pj in range(0, 7):
        return state[pi][pj] == c
    return False

def get_random(state):
    iter_times = 0
    while True:
        i = random.randint(0, 6)
        j = random.randint(0, 6)
        direction = random.randint(0, 3)

        if isc(state, i, j, direction, 'X', 0) and isc(state, i, j, direction, '0', 1) and isc(state, i, j, direction, '0', 2):
            return (i, j), direction

        iter_times += 1
        if iter_times >= 100000:
            break
    return None, None

def setstate(state, vp, vd, step, c):
    pi = vp[0] + DIRECTIONS[vd][0] * step
    pj = vp[1] + DIRECTIONS[vd][1] * step
    state[pi] = state[pi][:pj] + c + state[pi][pj+1:]

def move(state, vp, vd):
    setstate(state, vp, vd, 0, '0')
    setstate(state, vp, vd, 1, 'X')
    setstate(state, vp, vd, 2, 'X')

def random_generate(max_step):
    state = ['--000--', '--000--', '0000000', '000X000', '0000000', '--000--', '--000--']

    steps = random.randint(1, max_step)

    for i in xrange(steps):
        valid_pos, valid_direction = get_random(state)
        if valid_pos is None:
            # print 'no valid'
            break

        move(state, valid_pos, valid_direction)
    return state

def parse(argvs):
    parser = argparse.ArgumentParser(description="HomeWork One")
    parser.add_argument("--input", type = str)
    parser.add_argument("--flag", type = int)
    args = parser.parse_args(argvs.split())
    return args

def generate(max_step, num_case):
    dir_order = 0
    while os.path.isdir('../testcase/random_%d' % (dir_order)):
        dir_order += 1

    basedir = '../testcase/random_%d' % (dir_order)
    os.mkdir(basedir)
    print 'random dir: ', basedir

    for i in xrange(num_case):
        state = random_generate(max_step)
        casename = '%s/grandom_%d.txt' % (basedir, i)
        with open(casename, 'w') as f:
            print >> f, ','.join(state)

if __name__ == "__main__":
    generate(20, 100)