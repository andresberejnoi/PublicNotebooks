import argparse
import datetime as dt


def cli():
    parser = argparse.ArgumentParser(prog='Simple Example')
    parser.add_argument('-n', '--name', type=str, default='John', help="Name of user")
    parser.add_argument('-a', '--age', type=int, default=31, help="Age of user")
    parser.add_argument('-o', '--occupation', type=str, default='software developer', help='Occupation of user')
    
    args = parser.parse_args()
    return args


def main(args):
    name       = args.name
    age        = args.age 
    occupation = args.occupation

    print(f"\nHello {name}.")
    print(f"Your age is {age}. Therefore, you were probably born around {(dt.datetime.today() - dt.timedelta(days=age*365)).year}.")
    print(f"Occupation is {occupation}.\n")


if __name__ == "__main__":
    args = cli()
    main(args)