# Path: test_2_req_args.py
# -*- coding: utf-8 -*-
# Calculate exponentiation

import argparse


def calc_exponentiation(base: float,
                        exponent: float):
    """ Calculate exponentiation

    :param base:        float: base
    :param exponent:    float: exponent
    :return:            float: base to the power of exponent
    """

    return base ** exponent


def main() -> None:
    """ Main entry """

    parser = argparse.ArgumentParser(description="Calculate exponentiation")
    parser.add_argument("base", type=float, help="Base")
    parser.add_argument("exponent", type=float, help="Exponent")
    args = parser.parse_args()

    print(calc_exponentiation(args.base, args.exponent))

    return None


if __name__ == "__main__":
    main()


