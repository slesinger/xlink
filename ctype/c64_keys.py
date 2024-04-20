from enum import Enum

from matplotlib.pyplot import install_repl_displayhook

class C64Key():
    xthin_keycode = 0
    def __init__(self, xthin_keycode, utf, name=None, printable:bool=True) -> None:
        self.xthin_keycode:int = xthin_keycode
        self.utfval:str = utf
        self.name:str = name if name else utf
        
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, __value: int) -> bool:
        assert isinstance(__value, int)
        return self.xthin_keycode == __value
    
    def utf(self) -> str:
        return self.utfval

class C64Keys():
    @staticmethod
    def get_key_by_idx(idx:int) -> C64Key:
        members = [attr for attr in dir(C64Keys) if not callable(getattr(C64Keys, attr)) and not attr.startswith("__")]
        for key in members:
            k = vars(C64Keys).get(key)
            if k and isinstance(k, C64Key) and k.xthin_keycode == idx:
                return k
        print(f"ERROR: Key not found: {idx}")
        return C64Keys.NO_KEY
    
    DEL = C64Key(0x00, u"\u001b[3~", "DEL")
    RETURN = C64Key(0x01, u"\u000a", "RETURN")
    CRSR_RIGHT = C64Key(0x02, u"\u001b[1D", "CRSR_RIGHT")
    F7 = C64Key(0x03, u"\u001b[18~", "F7")
    F1 = C64Key(0x04, u"\u001b[11~", "F1")
    F3 = C64Key(0x05, u"\u001b[13~", "F3")
    F5 = C64Key(0x06, u"\u001b[15~", "F5")
    CRSR_DOWN = C64Key(0x07, u"\u001b[1B", "CRSR_DOWN")
    THREE = C64Key(0x08, "3")
    w = C64Key(0x09, "w")
    a = C64Key(0x0a, "a")
    FOUR = C64Key(0x0b, "4")
    z = C64Key(0x0c, "z")
    s = C64Key(0x0d, "s")
    e = C64Key(0x0e, "e")
    UNKNOWN1 = C64Key(0x0f, "???")
    FIVE = C64Key(0x10, "5")
    r = C64Key(0x11, "r")
    d = C64Key(0x12, "d")
    SIX = C64Key(0x13, "6")
    c = C64Key(0x14, "c")
    f = C64Key(0x15, "f")
    t = C64Key(0x16, "t")
    x = C64Key(0x17, "x")
    SEVEN = C64Key(0x18, "7")
    y = C64Key(0x19, "y")
    g = C64Key(0x1a, "g")
    EIGHT = C64Key(0x1b, "8")
    b = C64Key(0x1c, "b")
    h = C64Key(0x1d, "h")
    u = C64Key(0x1e, "u")
    v = C64Key(0x1f, "v")
    NINE = C64Key(0x20, "9")
    i = C64Key(0x21, "i")
    j = C64Key(0x22, "j")
    ZERO = C64Key(0x23, "0")
    m = C64Key(0x24, "m")
    k = C64Key(0x25, "k")
    o = C64Key(0x26, "o")
    n = C64Key(0x27, "n")
    PLUS = C64Key(0x28, "+", "PLUS")
    p = C64Key(0x29, "p")
    l = C64Key(0x2a, "l")
    MINUS = C64Key(0x2b, "-", "MINUS")
    FULL_STOP = C64Key(0x2c, ".", "FULL_STOP")
    COLON = C64Key(0x2d, ":", "COLON")
    AT = C64Key(0x2e, "@", "AT")
    COMMA = C64Key(0x2f, ",", "COMMA")
    POUND = C64Key(0x30, "£", "POUND")
    ASTERISK = C64Key(0x31, "*", "ASTERISK")
    SEMICOLON = C64Key(0x32, ";", "SEMICOLON")
    HOME = C64Key(0x33, u"\u001b[1~", "HOME")
    UNKNOWN2 = C64Key(0x34, "????")
    EQUALS = C64Key(0x35, "=", "EQUALS")
    UP_ARROW = C64Key(0x36, "↑", "UP_ARROW")
    SOLIDUS = C64Key(0x37, "/", "SOLIDUS")
    ONE = C64Key(0x38, "1")
    LEFT_ARROW = C64Key(0x39, "←", "LEFT_ARROW")
    UNKNOWN3 = C64Key(0x3a, "?????")
    TWO = C64Key(0x3b, "2")
    SPACE = C64Key(0x3c, " ", "SPACE")
    UNKNOWN4 = C64Key(0x3d, "??????")
    q = C64Key(0x3e, "q")
    STOP = C64Key(0x3f, u"\u0009", "STOP")

    # NO_KEY with Joystick
    NO_KEY = C64Key(0x40, "", "NO_KEY")
    # C64Key(0x41, u"\u000a", "RETURN"),
    # C64Key(0x42, u"\u001b[1D", "CRSR_RIGHT"),
    # C64Key(0x43, u"\u001b[18~", "F7"),
    # C64Key(0x44, u"\u001b[11~", "F1"),
    # C64Key(0x45, u"\u001b[13~", "F3"),
    # C64Key(0x46, u"\u001b[15~", "F5"),
    # C64Key(0x47, u"\u001b[1B", "CRSR_DOWN"),
    # C64Key(0x48, "3"),
    # C64Key(0x49, "w"),
    # C64Key(0x4a, "a"),
    # C64Key(0x4b, "4"),
    # C64Key(0x4c, "z"),
    # C64Key(0x4d, "s"),
    # C64Key(0x4e, "e"),
    # C64Key(0x4f, "???"),
    # C64Key(0x50, "5"),
    # C64Key(0x51, "r"),
    # C64Key(0x52, "d"),
    # C64Key(0x53, "6"),
    # C64Key(0x54, "c"),
    # C64Key(0x55, "f"),
    # C64Key(0x56, "t"),
    # C64Key(0x57, "x"),
    # C64Key(0x58, "7"),
    # C64Key(0x59, "y"),
    # C64Key(0x5a, "g"),
    # C64Key(0x5b, "8"),
    # C64Key(0x5c, "b"),
    # C64Key(0x5d, "h"),
    # C64Key(0x5e, "u"),
    # C64Key(0x5f, "v"),
    # C64Key(0x60, "9"),
    # C64Key(0x61, "i"),
    # C64Key(0x62, "j"),
    # C64Key(0x63, "0"),
    # C64Key(0x64, "m"),
    # C64Key(0x65, "k"),
    # C64Key(0x66, "o"),
    # C64Key(0x67, "n"),
    # C64Key(0x68, "+", "PLUS"),
    # C64Key(0x69, "p"),
    # C64Key(0x6a, "l"),
    # C64Key(0x6b, "-", "MINUS"),
    # C64Key(0x6c, ">", "GREATER"),
    # C64Key(0x6d, "[", "LEFT_SQUARE_BRACKET"),
    # C64Key(0x6e, "@", "AT"),
    # C64Key(0x6f, "<", "LESS"),
    # C64Key(0x70, "£", "POUND"),
    # C64Key(0x71, "*", "ASTERISK"),
    # C64Key(0x72, "]", "RIGHT_SQUARE_BRACKET"),
    # C64Key(0x73, u"\u001b[1~", "HOME"),
    # C64Key(0x74, "????"),
    # C64Key(0x75, "=", "EQUALS"),
    # C64Key(0x76, u"\u001b[1A", "CRSR_UP"),
    # C64Key(0x77, "?", "QUESTION_MARK"),
    # C64Key(0x78, "1"),
    # C64Key(0x79, u"\u001b[1C", "CRSR_LEFT"),
    # C64Key(0x7a, "?????"),
    # C64Key(0x7b, "2"),
    # C64Key(0x7c, " ", "SPACE"),
    # C64Key(0x7d, "??????"),
    # C64Key(0x7e, "q"),
    # C64Key(0x7f, u"\u0009", "STOP"),  # TODO what to do with this?

    # # C= with all keys
    C_DEL = C64Key(0x80, "", "C_DEL")
    C_RETURN = C64Key(0x81, u"\u000a", "C_RETURN")
    C_CRSR_RIGHT = C64Key(0x82, u"\u001b[1D", "C_CRSR_RIGHT")
    C_F7 = C64Key(0x83, u"\u001b[18~", "C_F7")
    C_F1 = C64Key(0x84, u"\u001b[11~", "C_F1")
    C_F3 = C64Key(0x85, u"\u001b[13~", "C_F3")
    C_F5 = C64Key(0x86, u"\u001b[15~", "C_F5")
    C_CRSR_DOWN = C64Key(0x87, u"\u001b[1B", "C_CRSR_DOWN")
    C_THREE = C64Key(0x88, u"\001b[31m", "C_3")
    C_W = C64Key(0x89, ".", "C_w")
    C_A = C64Key(0x8a, ".", "C_a")
    C_FOUR = C64Key(0x8b, u"\001b[36m", "C_4")
    C_Z = C64Key(0x8c, ".", "C_z")
    C_S = C64Key(0x8d, ".", "C_s")
    C_E = C64Key(0x8e, ".", "C_e")
    C_UNKNOWN = C64Key(0x8f, "???")
    C_FIVE = C64Key(0x90, u"\001b[35m", "C_5")
    C_R = C64Key(0x91, ".", "C_r")
    C_D = C64Key(0x92, ".", "C_d")
    C_SIX = C64Key(0x93, u"\001b[32m", "C_6")
    C_C = C64Key(0x94, ".", "C_c")
    C_F = C64Key(0x95, ".", "C_f")
    C_T = C64Key(0x96, ".", "C_t")
    C_X = C64Key(0x97, ".", "C_x")
    C_SEVEN = C64Key(0x98, u"\001b[34m", "C_7")
    C_Y = C64Key(0x99, ".", "C_y")
    C_G = C64Key(0x9a, ".", "C_g")
    C_EIGHT = C64Key(0x9b, u"\001b[93m", "C_8")
    C_B = C64Key(0x9c, ".", "C_b")
    C_H = C64Key(0x9d, ".", "C_h")
    C_U = C64Key(0x9e, ".", "C_u")
    C_V = C64Key(0x9f, ".", "C_v")
    C_NINE = C64Key(0xa0, u"\001b[7m", "C_9")
    C_I = C64Key(0xa1, ".", "C_i")
    C_J = C64Key(0xa2, ".", "C_j")
    C_ZERO = C64Key(0xa3, u"\001b[27m", "C_0")
    C_M = C64Key(0xa4, ".", "C_m")
    C_K = C64Key(0xa5, ".", "C_k")
    C_O = C64Key(0xa6, ".", "C_o")
    C_N = C64Key(0xa7, ".", "C_n")
    C_PLUS = C64Key(0xa8, ".", "C_PLUS")
    C_P = C64Key(0xa9, ".", "C_p")
    C_L = C64Key(0xaa, ".", "C_l")
    C_MINUS = C64Key(0xab, ".", "C_MINUS")
    C_COMMA = C64Key(0xac, ">", "C_COMMA")
    C_COLON = C64Key(0xad, "[", "C_COLON")
    C_AT = C64Key(0xae, ".", "C_AT")
    C_FULL_STOP = C64Key(0xaf, "<", "C_FULL_STOP")
    C_POUND = C64Key(0xb0, ".", "C_POUND")
    C_ASTERISK = C64Key(0xb1, ".", "C_ASTERISK")
    C_SEMICOLON = C64Key(0xb2, "]", "C_SEMICOLON")
    C_HOME = C64Key(0xb3, u"\u001b[1J", "C_HOME")  # Clear from cursor till beginning of screen, see ANSI Erase in Display
    C_UNKNOWN2 = C64Key(0xb4, "C_????")
    C_EQUALS = C64Key(0xb5, "=", "C_EQUALS")
    C_UP_ARROW = C64Key(0xb6, "↑", "C_UP_ARROW")
    C_SOLIDUS = C64Key(0xb7, "?", "C_SOLIDUS")
    C_ONE = C64Key(0xb8, u"\001b[30m", "C_1")
    C_LEFT_ARROW = C64Key(0xb9, "←", "C_LEFT_ARROW")
    C_UNKNOWN3 = C64Key(0xba, "C_?????")
    C_TWO = C64Key(0xbb, u"\001b[97m", "C_2")
    C_SPACE = C64Key(0xbc, " ", "C_SPACE")
    C_UNKNOWN4 = C64Key(0xbd, "C_??????")
    C_Q = C64Key(0xbe, ".", "C_q")
    C_STOP = C64Key(0xbf, u"\u001b[Z", "C_STOP")  # TODO what to do with this? LOAD in BASIC

    # Shift with all keys
    INS = C64Key(0xc0, "\u001b[2~", "INS")
    SHIFT_RETURN = C64Key(0xc1, u"\u000a", "SHIFT_RETURN")
    CRSR_LEFT = C64Key(0xc2, u"\u001b[1C", "CRSR_LEFT")  # TODO NO_KEY
    F8 = C64Key(0xc3, u"\u001b[19~", "F8")
    F2 = C64Key(0xc4, u"\u001b[12~", "F2")
    F4 = C64Key(0xc5, u"\u001b[14~", "F4")
    F6 = C64Key(0xc6, u"\u001b[17~", "F6")
    CRSR_UP = C64Key(0xc7, u"\u001b[1A", "CRSR_UP")  # TODO NO_KEY
    NUMBER_SIGN = C64Key(0xc8, "#", "NUMBER_SIGN")
    W = C64Key(0xc9, "W")
    A = C64Key(0xca, "A")
    DOLLAR_SIGN = C64Key(0xcb, "$", "DOLLAR_SIGN")
    Z = C64Key(0xcc, "Z")
    S = C64Key(0xcd, "S")
    E = C64Key(0xce, "E")
    UNKNOWN1 = C64Key(0xcf, "???")
    PERCENT_SIGN = C64Key(0xd0, "%", "PERCENT_SIGN")
    R = C64Key(0xd1, "R")
    D = C64Key(0xd2, "D")
    AMPERSAND = C64Key(0xd3, "&", "AMPERSAND")
    C = C64Key(0xd4, "C")
    F = C64Key(0xd5, "F")
    T = C64Key(0xd6, "T")
    X = C64Key(0xd7, "X")
    APOSTROPHE = C64Key(0xd8, "'", "APOSTROPHE")
    Y = C64Key(0xd9, "Y")
    G = C64Key(0xda, "G")
    LEFT_PARENTHESIS = C64Key(0xdb, "(", "LEFT_PARENTHESIS")
    B = C64Key(0xdc, "B")
    H = C64Key(0xdd, "H")
    U = C64Key(0xde, "U")
    V = C64Key(0xdf, "V")
    RIGHT_PARENTHESIS = C64Key(0xe0, ")", "RIGHT_PARENTHESIS")
    I = C64Key(0xe1, "I")
    J = C64Key(0xe2, "J")
    SHIFT_ZERO = C64Key(0xe3, "0", "SHIFT_ZERO")
    M = C64Key(0xe4, "M")
    K = C64Key(0xe5, "K")
    O = C64Key(0xe6, "O")
    N = C64Key(0xe7, "N")
    SHIFT_PLUS = C64Key(0xe8, "+", "SHIFT_PLUS")
    P = C64Key(0xe9, "P")
    L = C64Key(0xea, "L")
    SHIFT_MINUS = C64Key(0xeb, "-", "SHIFT_MINUS")
    GREATER = C64Key(0xec, ">", "GREATER")
    LEFT_SQUARE_BRACKET = C64Key(0xed, "[", "LEFT_SQUARE_BRACKET")
    SHIFT_AT = C64Key(0xee, "@", "SHIFT_AT")
    LESS = C64Key(0xef, "<", "LESS")
    SHIFT_POUND = C64Key(0xf0, "£", "SHIFT_POUND")
    SHIFT_ASTERISK = C64Key(0xf1, "*", "SHIFT_ASTERISK")
    RIGHT_SQUARE_BRACKET = C64Key(0xf2, "]", "RIGHT_SQUARE_BRACKET")
    CLR = C64Key(0xf3, u"\u001b[0J", "CLR")  # Clear from cursor till end of screen, see ANSI Erase in Display
    UNKNOWN2 = C64Key(0xf4, "????")
    SHIFT_EQUALS = C64Key(0xf5, "=", "SHIFT_EQUALS")
    SHIFT_UP_ARROW = C64Key(0xf6, "↑", "SHIFT_UP_ARROW")
    QUESTION_MARK = C64Key(0xf7, "?", "QUESTION_MARK")
    EXCLAMATION_MARK = C64Key(0xf8, "!", "EXCLAMATION_MARK")
    SHIFT_LEFT_ARROW = C64Key(0xf9, "←", "SHIFT_LEFT_ARROW")
    UNKNOWN3 = C64Key(0xfa, "?????")
    QUOTATION_MARK = C64Key(0xfb, "\"", "QUOTATION_MARK")
    SHIFT_SPACE = C64Key(0xfc, " ", "SHIFT_SPACE", printable=False)
    UNKNOWN4 = C64Key(0xfd, "??????")
    Q = C64Key(0xfe, "Q")
    RUN = C64Key(0xff, u"\u001b[Z", "RUN")  # TODO what to do with this? LOAD in BASIC
