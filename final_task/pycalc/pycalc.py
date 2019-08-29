import argparse
from final_task.pycalc.calculate import calculate


def main():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument("EXPRESSION", help="Please, enter an expression for calculating", type=str)
    args = parser.parse_args()
    result = calculate(args.EXPRESSION)
    print(result)


if __name__ == '__main__':
    main()
