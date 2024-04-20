from c64_color import C64Color as Color
import cbmcodecs2  # this import is needed for the screencode PETSCII encoding
# import xcoding

class Textel():
    """Textel is a textual representation of one position in text screen. It is a character and a color and all attributes."""

    _character: str  # 1 wide-char utf-8 character
    _color: Color  # 1 byte color
    tainted: bool  # True if this textel has changed since last draw
        
    def __init__(self) -> None:
        self._character = " "
        self._color = Color.LIGHT_BLUE
        
        
    def get_petscii(self) -> int:
        """Return the PETSCII code for the character.
        https://www.df.lth.se/~triad/krad/recode/petlc/"""
        return ord(self._character.encode(encoding='screencode_c64_lc'))
    
    
    def get_ascii(self) -> str:
        """Return the character in ASCII."""
        return self._character
    
    
    def put_char(self, char: str, color:Color|None=Color.LIGHT_BLUE) -> None:
        """Put a character into the textel."""
        self._character = char
        self._color = color if color is not None else Color.LIGHT_BLUE
        self.tainted = True
        
    def get_color_num(self) -> int:
        """Return the color of the textel as a number."""
        return self._color.value