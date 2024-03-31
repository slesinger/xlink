from c64_color import C64Color as Color
import cbmcodecs2
#         data64 = data.encode(encoding='petscii_c64en_lc')  # TODO get right encoding

class Textel():
    """Textel is a textual representation of one position in text screen. It is a character and a color and all attributes."""

    _character: str  # 1 wide-char utf-8 character
    color: Color  # 1 byte color
    tainted: bool  # True if this textel has changed since last draw
        
    def __init__(self) -> None:
        self._character = " "
        self.color = Color.BLUE
        
        
    def get_petscii(self) -> int:
        """Return the PETSCII code for the character."""
        return ord(self._character)  # TODO convert
    
    
    def get_ASCII(self) -> str:
        """Return the character in ASCII."""
        return self._character
    
    
    def put_char(self, char: str) -> None:
        """Put a character into the textel."""
        self._character = char
        self.tainted = True
        
    def get_color_num(self) -> int:
        """Return the color of the textel as a number."""
        return self.color.value