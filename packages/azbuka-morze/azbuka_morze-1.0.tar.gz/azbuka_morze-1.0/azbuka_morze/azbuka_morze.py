MORSE_CODE_DICT = {'A': '•—', 'B': '—•••',
                   'C': '—•—•', 'D': '—••', 'E': '•',
                   'F': '••—•', 'G': '——•', 'H': '••••',
                   'I': '••', 'J': '•———', 'K': '—•—',
                   'L': '•—••', 'M': '——', 'N': '—•',
                   'O': '———', 'P': '•——•', 'Q': '——•—',
                   'R': '•—•', 'S': '•••', 'T': '—',
                   'U': '••—', 'V': '•••—', 'W': '•——',
                   'X': '—••—', 'Y': '—•——', 'Z': '——••'}


def encrypt(message, u):
    cipher = ''
    for letter in message:
        if letter != ' ':
            if u == 1:
                cipher += " " + MORSE_CODE_DICT[letter]
            else:
                u = 1
                cipher += MORSE_CODE_DICT[letter]
        else:
            cipher += '\t'
            u = 0

    return cipher


def decrypt(message):
    message += ' '

    decipher = ''
    citext = ''
    for letter in message:
        if letter == '\t':
            decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
            decipher += ' '
            citext = ''
        elif letter != ' ':
            i = 0
            citext += letter

        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''

    return decipher


def translate(message):
    u = 0
    if any(c.isalpha() for c in message):
        result = encrypt(message.upper(), u)
        print(result)
    else:
        result = decrypt(message)
        result = result.lower()
        print(result)