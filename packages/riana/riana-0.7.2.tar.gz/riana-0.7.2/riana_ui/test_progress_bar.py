# Path: test_progress_bar.py
# -*- coding: utf-8 -*-
# Test out progress bar with one argument

import argparse
import tqdm
import time

def progress_bar(steps: int,
                 wait: float) -> None:
    """ Progress bar """

    # This uses tqdm to create a progress bar
    # for i in tqdm.tqdm(range(steps)):
    #     time.sleep(wait)

    # This uses print to create a progress bar
    for i in range(steps):
        print(f"Progress: {i + 1}/{steps}", end="\r")
        time.sleep(wait)

    return None


def main() -> None:
    """ Main entry """

    parser = argparse.ArgumentParser(description="Test out progress bar")
    parser.add_argument("-s", "--steps", type=int, help="Number of steps in the progress bar", default=100)
    parser.add_argument("-w", "--wait", type=float, help="Wait time between each step", default=0.1)

    args = parser.parse_args()

    print(progress_bar(args.steps, args.wait))

    return None


if __name__ == "__main__":
    main()


