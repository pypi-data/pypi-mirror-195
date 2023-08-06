# Path: test_3_req_args.py
# -*- coding: utf-8 -*-
# Calculate mass to weigh for a given volume, molecular weight, and molarity

import argparse


def calc_digestion_mass(vol: float,
                        molarity: float,
                        mw: float) -> float:
    """ Calculate mass to weigh for a given volume, molecular weight, and molarity

    :param vol:         float: volume (L)
    :param molarity:    float: molarity (mol/L)
    :param mw:          float: molecular weight (g/mol)
    :return:            float: mass to weigh (g)

    """

    return vol * molarity * mw


def main() -> None:
    """ Main entry """

    parser = argparse.ArgumentParser(description="Calculate mass to weigh for a "
                                                 "given volume, molecular weight, and molarity")
    parser.add_argument("vol", type=float, help="<required> Volume (L)")
    parser.add_argument("molarity", type=float, help="<required> Molarity (mol/L)")
    parser.add_argument("-m", "--mol_weight", type=float, help="<optional> Molecular weight (g/mol) "
                                                               "[default: DTT: 154.253]",
                        default=154.253)

    args = parser.parse_args()

    print(calc_digestion_mass(args.vol, args.molarity, args.mol_weight))

    return None


if __name__ == "__main__":
    main()


