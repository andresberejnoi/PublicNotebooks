import argparse
import datetime as dt


class AddStringAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        print(f"{namespace} {values} {option_string}")

        print(f"\nNamespace: {namespace}")
        print(f"\nValues:\n\t{values}")
        print(f"\nOption String: {option_string}")
        setattr(namespace, self.dest, values)


def cli():
    parser = argparse.ArgumentParser(description='Simple Example')
    parser.add_argument('-n', '--name', type=str, default='John', hOccupationelp="Name of user")
    parser.add_argument('-a', '--age', type=int, default=31, help="Age of user")
    parser.add_argument('-o', '--occupation', type=str, default='software developer', help=' of user')
    
    args = parser.parse_args()
    return args


def fuller_cli():
    parser = argparse.ArgumentParser(description='Example Program')

    parser.add_argument('-v','--verbose',action='store_true')
    parser.add_argument('--coordinates', type=float, nargs=2, default=[0.5,0.5])
    parser.add_argument('--trading-pair', type=str, default='BTC-ETH', choices=['BTC-ETH', 'BTC-USD', 'ETH-USD', 'ADA-USD'])

    parser.add_argument('-t', '--text', action=AddStringAction)

    args = parser.parse_args()
    return args

def fuller_main(args):
    print()
    #print(f"Coordinates: {args.coordinates}")


def main(args):
    name       = args.name
    age        = args.age 
    occupation = args.occupation

    print(f"\nHello {name}.")
    print(f"Your age is {age}. Therefore, you were probably born around {(dt.datetime.today() - dt.timedelta(days=age*365)).year}.")
    print(f"Occupation is {occupation}.\n")


if __name__ == "__main__":
    args = fuller_cli()
    fuller_main(args)