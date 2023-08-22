#!/usr/bin/python3

import random
from collections import deque
from time import sleep, time

import readchar

# display
D = "🔴"
K = "🔵"

# key bindings (capitalized if alphabet)
KEY_D = ("F", "J")
KEY_K = ("D", "K")

# training settings
MINSIZE = 2
MAXSIZE = 7
RANDOM_POS = False

# ┌─
# │
# ├─
# │
# └─

# init
NOTES = (D, K)
KEY_MAPPING = (
    {
        KEY_D[0]: D,
        KEY_K[0]: K,
    },
    {KEY_D[1]: D, KEY_K[1]: K},
)
PRINT_LENGTH = 3 * MAXSIZE + 7
begin_pos = 0
POS_TEXT = ("L", "R")
counter = [0, 0]
total_notes = [0, 0]
total_errors = [0, 0]
total_duration = [0, 0]
total_first_note_duration = [0, 0]

try:
    if MINSIZE > MAXSIZE:
        raise ValueError("MINSIZE should not exceed MAXSIZE.")
    if MAXSIZE < 2:
        raise ValueError("MAXSIZE should be at least 2")
    print(" %s TaikoLab v2 %s \nPlease turn on Caps Lock" % NOTES)
    for i in range(3, 0, -1):
        print(i, end="\r")
        sleep(1)
    print()
except ValueError:
    print()
    exit(0)
except KeyboardInterrupt:
    print()
    exit(0)


def judge(note):
    global pos
    global errors
    global input_print
    ch = readchar.readkey()
    input_note = KEY_MAPPING[pos].get(ch, ":(")
    if input_note != note:
        errors += 1
    input_print += input_note + " "
    print(input_print + "\r", end="")
    pos = 1 - pos


# main loop
while True:
    # generate beatmap
    if RANDOM_POS:
        begin_pos = random.randint(0, 1)
    beatmap = deque()
    for i in range(length := random.randint(MINSIZE, MAXSIZE)):
        beatmap.append(random.choice(NOTES))
    print("┌" + "─" * PRINT_LENGTH)
    print("│ (%s)  " % POS_TEXT[begin_pos] + " ".join(beatmap))
    print("└" + "─" * PRINT_LENGTH)

    # input
    pos = begin_pos
    errors = 0
    input_print = ">>>    "
    print(input_print + "\r", end="")
    start_time = time()
    try:
        first_note = beatmap.popleft()
        judge(first_note)
        first_note_duration = time() - start_time
        total_first_note_duration[begin_pos] += first_note_duration
        for cur_note in beatmap:
            judge(cur_note)
    except KeyboardInterrupt:
        break
    else:
        end_time = time()
        counter[begin_pos] += 1
        total_notes[begin_pos] += length
        total_errors[begin_pos] += errors
        duration = end_time - start_time
        total_duration[begin_pos] += duration

        # print result
        print(
            "\n--- %s%d(%d) ---"
            % (POS_TEXT[begin_pos], counter[begin_pos], sum(counter))
        )
        if sum(counter) > 0:
            print(
                "acc/fnr/rpn = %.2f%%/%.2fs/%.2fs"
                % (100 * (1 - errors / length), first_note_duration, duration / length)
            )
        else:
            print("N/A")
    finally:
        begin_pos = pos

print("--- TaikoLab training statistics ---")
print("beatmap length: [%d, %d]" % (MINSIZE, MAXSIZE))
print(
    "counter: %s/%s/T = %d/%d/%d"
    % (POS_TEXT[0], POS_TEXT[1], counter[0], counter[1], sum(counter))
)
for i in range(len(POS_TEXT)):
    if total_notes[i] > 0:
        print(
            "%savg: acc/fnr/rpn = %.2f%%/%.2fs/%.2fs"
            % (
                POS_TEXT[i],
                100 * (1 - total_errors[i] / total_notes[i]),
                total_first_note_duration[i] / counter[i],
                total_duration[i] / total_notes[i],
            )
        )
    else:
        print("%savg: acc/fnr/rpn = N/A" % POS_TEXT[i])
