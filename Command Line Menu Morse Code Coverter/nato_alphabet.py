"""
This alphabet specification follows the NATO phonetic alphate (International Radiotelephony Spelling Alphabet),
according to this entry on Wikipedia:
https://en.wikipedia.org/wiki/NATO_phonetic_alphabet
"""

MORSE_CODE_MAPPER = {
    'a' : '.-',
    'b' : '-...',
    'c' : '-.-.',
    'd' : '-..',
    'e' : '.',
    'f' : '..-.',
    'g' : '--.',
    'h' : '....',
    'i' : '..',
    'j' : '.---',
    'k' : '-.-',
    'l' : '.-..',
    'm' : '--',
    'n' : '-.',
    'o' : '---',
    'p' : '.--.',
    'q' : '--.-',
    'r' : '.-.',
    's' : '...',
    't' : '-',
    'u' : '..-',
    'v' : '...-',
    'w' : '.--',
    'x' : '-..-',
    'y' : '-.--',
    'z' : '--..',
    ' ' : '^',
    '0' : '-----',
    '1' : '.----',
    '2' : '..---',
    '3' : '...--',
    '4' : '....-',
    '5' : '.....',
    '6' : '-....',
    '7' : '--...',
    '8' : '---..',
    '9' : '----.',
}
REVERSE_CODE_MAPPER = {
    '.-'   : 'a',
    '-...' : 'b',
    '-.-.' : 'c',
    '-..'  : 'd',
    '.'    : 'e',
    '..-.' : 'f',
    '--.'  : 'g',
    '....' : 'h',
    '..'   : 'i',
    '.---' : 'j',
    '-.-'  : 'k',
    '.-..' : 'l',
    '--'   : 'm',
    '-.'   : 'n',
    '---'  : 'o',
    '.--.' : 'p',
    '--.-' : 'q',
    '.-.'  : 'r',
    '...'  : 's',
    '-'    : 't',
    '..-'  : 'u',
    '...-' : 'v',
    '.--'  : 'w',
    '-..-' : 'x',
    '-.--' : 'y',
    '--..' : 'z',
    '^'    : ' ',
    '-----': '0',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9'
}

TELEPHONY_MAPPER = {
    'a' : 'alpha',
    'b' : 'bravo',
    'c' : 'charlie',
    'd' : 'delta',
    'e' : 'echo',
    'f' : 'foxtrot',
    'g' : 'golf',
    'h' : 'hotel',
    'i' : 'india',
    'j' : 'juliett',
    'k' : 'kilo',
    'l' : 'lima',
    'm' : 'mike',
    'n' : 'november',
    'o' : 'oscar',
    'p' : 'papa',
    'q' : 'quebec',
    'r' : 'romeo',
    's' : 'sierra',
    't' : 'tango',
    'u' : 'uniform',
    'v' : 'victor',
    'w' : 'whiskey',
    'x' : 'xray',
    'y' : 'yankee',
    'z' : 'zulu',
    ' ' : ' ',
    '0' : 'zero',
    '1' : 'one',
    '2' : 'two',
    '3' : 'three',
    '4' : 'four',
    '5' : 'five',
    '6' : 'six',
    '7' : 'seven',
    '8' : 'eight',
    '9' : 'nine',
}
REVERSE_TELEPHONY_MAPPER = {
    'alpha'   : 'a',
    'bravo'   : 'b',
    'charlie' : 'c',
    'delta'   : 'd',
    'echo'    : 'e',
    'foxtrot' : 'f',
    'golf'    : 'g',
    'hotel'   : 'h',
    'india'   : 'i',
    'juliett' : 'j',
    'kilo'    : 'k',
    'lima'    : 'l',
    'mike'    : 'm',
    'november': 'n',
    'oscar'   : 'o',
    'papa'    : 'p',
    'quebec'  : 'q',
    'romeo'   : 'r',
    'sierra'  : 's',
    'tango'   : 't',
    'uniform' : 'u',
    'victor'  : 'v',
    'whiskey' : 'w',
    'xray'    : 'x',
    'yankee'  : 'y',
    'zulu'    : 'z',
    ' '       : ' ',
    'zero'    : '0',
    'one'     : '1',
    'two'     : '2',
    'three'   : '3',
    'four'    : '4',
    'five'    : '5',
    'six'     : '6',
    'seven'   : '7',
    'eight'   : '8',
    'nine'    : '9'
}
