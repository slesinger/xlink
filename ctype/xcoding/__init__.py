"""CBM "encodings" Package

Encodings for PETSCII generated with gencodec.py from the Unicode mappings
defined by Linus Walleij, see
http://www.df.lth.se/~triad/krad/recode/petscii.html

The screencode mappings were written by Honza Slesinger.

petscii_c64en_lc - Mixed-case mapping used by the Commodore 64
petscii_c64en_uc - Upper-case/graphics mapping used by the Commodore 64
screencode_c64_lc - Mixed-case mapping to screencodes (POKE) used by the Commodore 64 and Vic20
screencode_c64_uc - Upper-case/graphics mapping to screencodes (POKE) used by the Commodore 64 and Vic20
"""
import codecs

from . import keycodes_c64en
from . import screencode_c64_lc
# from . import screencode_c64_uc

__version__ = '1.0'
__all__ = []

petscii_codecs = {
    # backwards compatibility encoding names:
    'keycodes_c64en': keycodes_c64en.getregentry(),
    'screencode-c64-lc': screencode_c64_lc.getregentry(),
    'screencode_c64_lc': screencode_c64_lc.getregentry(),
    # 'screencode_c64_uc': screencode_c64_uc.getregentry()
}


def search_fn(encoding):
    return petscii_codecs.get(encoding, None)


codecs.register(search_fn)
