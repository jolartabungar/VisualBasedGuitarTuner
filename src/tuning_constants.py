# Tuning Set Names
BASS_STD = 'Bass - Standard'
BASS_5_STR_STD = 'Bass - Five String Standard'
GUITAR_STD = 'Guitar - Standard'

# String names
STRING_C = 'C'
STRING_D = 'D'
STRING_E = 'E'
STRING_F = 'F'
STRING_G = 'G'
STRING_A = 'A'
STRING_B = 'B'


def bass_standard():
    return [STRING_E, STRING_A, STRING_D, STRING_G]


def bass_five_string_standard():
    return [STRING_B] + bass_standard()


def guitar_standard():
    return bass_standard() + [STRING_B, STRING_E]


def tuning_map(tuning_set):
    return {
        BASS_STD: bass_standard(),
        BASS_5_STR_STD: bass_five_string_standard(),
        GUITAR_STD: guitar_standard(),
    }[tuning_set]

