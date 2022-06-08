import argparse
import nato_alphabet as nt
import sys

def cli():
    parser = argparse.ArgumentParser(prog='Morse Code Tool')
    # parser.add_argument('-s', '--source', action='store_true', help="If present, download new candles from Oanda and add them to the database")
    # parser.add_argument('-t', '--text', nargs='?', const='date_not_provided', type=str,help="Provide date in ISO format to initialize the database for the first time")
    parser.add_argument('-s', '--source', type=str, default=None, help="")
    parser.add_argument('-t', '--text', type=str, default='', help="")
    
    parser.add_argument('-m', '--mode', type=str, choices=['morse','telephony'], default='morse')
    parser.add_argument('-d', '--direction', type=str, choices=['from_text', 'to_text'], default='from_text', help="")
    parser.add_argument('-o','--output', type=str, default=None, help="")
    args = parser.parse_args()
    return args


def simple_cli():
    pass


def main(args):
    #-- Get the source text to translate
    text = ""
    if args.source:
        with open(args.source, 'r') as file_handler:
            text = file_handler.read().lower()

    else:
        text = args.text

    #-- get mode and direction of the conversion, and output file
    mode      = args.mode
    direction = args.direction
    out_file = args.output

    #-- Convert text
    output_str = ''
    if direction == 'from_text':
        if mode == 'morse':
            for letter in text:
                output_str += nt.MORSE_CODE_MAPPER.get(letter, '*') + '^'
        else:
            for letter in text:
                output_str += nt.TELEPHONY_MAPPER.get(letter, '*') + '^'
    elif direction == 'to_text':
        if mode == 'morse':
            print(text.split('^'))
            for letter in text.split('^'):
                output_str += nt.REVERSE_CODE_MAPPER.get(letter, '*')
        else:
            for letter in text:
                output_str += nt.REVERSE_TELEPHONY_MAPPER.get(letter, '*')

    #-- clean up the result a little bit
    output_str = output_str.strip('^').strip(' ')

    #-- write result to file or to the terminal
    if out_file:
        with open(out_file, 'w') as file_handler:
            file_handler.write(output_str)
    else:
        print(output_str)


if __name__ == '__main__':
    args = cli()
    main(args)