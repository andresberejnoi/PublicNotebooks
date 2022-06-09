import argparse
import nato_alphabet as nt


def cli():
    parser = argparse.ArgumentParser(description='Morse Code Tool')
    parser.add_argument('-s', '--source', type=str, default=None, 
                        help="File containing the text to translate.")

    parser.add_argument('-t', '--text', type=str, default='', 
                        help="""Enter text to translate directly. If `--source`
                                is provided, then this option (`--text`) is ignored.""")
    
    parser.add_argument('-m', '--mode', type=str, choices=['morse','telephony'], default='morse', 
                        help="""Choose mode of operation: morse or telephony.""")

    parser.add_argument('-d', '--direction', type=str, choices=['from_text', 'to_text'], default='from_text', 
                        help="""Select the direction of the convertion. 
                                If the source text needs to be converted to 
                                morse code, then choose `from_text` (this is the default)
                                and if the source text is already morse code
                                and you want to decrypt it, choose `to_text`.""")

    parser.add_argument('-o','--output', type=str, default=None, 
                        help="""File where to save the output. If this flag is not
                                provided, the output will be printed to the terminal.""")
                                
    args = parser.parse_args()
    return args


def main(args):
    #-- Get the source text to translate
    text = ""
    if args.source:
        with open(args.source, 'r') as file_handler:
            text = file_handler.read()

    else:
        text = args.text

    text = text.lower()

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
        text = text.strip('^').strip()
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