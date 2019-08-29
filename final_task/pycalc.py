import argparse
import calculate


def main():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.",
                                     prog="pycalc")
    parser.add_argument("EXPRESSION", help="Please, enter an expression for calculating", type=str)
    args = parser.parse_args()
    result = calculate(args.EXPRESSION)
    return result


if __name__ == '__main__':
    main()
