import sys
import datetime as dt 


def main():
    name       = sys.argv[1]
    age        = int(sys.argv[2])
    occupation = sys.argv[3]

    print(f"\nHello {name}.")
    print(f"Your age is {age}. Therefore, you were probably born around {(dt.datetime.today() - dt.timedelta(days=age*365)).year}.")
    print(f"Occupation is {occupation}.\n")


if __name__ == '__main__':
    main()