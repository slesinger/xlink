import ctypes

C_libxlink = ctypes.CDLL("libxlink.so")

#void xlink_begin()
xlink_begin_fxn = C_libxlink.xlink_begin

#void xlink_end()
xlink_end_fxn = C_libxlink.xlink_end

#bool xlink_receive(uchar *data, uint size)
xlink_receive_fxn = C_libxlink.xlink_receive
xlink_receive_fxn.argtypes = [ctypes.c_char_p, ctypes.c_uint]
xlink_receive_fxn.restype = ctypes.c_bool

# bool xlink_poke(unsigned char memory, 
# 		unsigned char bank, 
# 		unsigned short address, 
# 		unsigned char value)
xlink_poke_fxn = C_libxlink.xlink_poke
xlink_poke_fxn.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_ushort, ctypes.c_char]
xlink_poke_fxn.restype = ctypes.c_bool

# bool xlink_load(unsigned char memory, 
#                 unsigned char bank, 
#                 unsigned short address, 
#                 unsigned char* data,
#                 unsigned int size)
xlink_load_fxn = C_libxlink.xlink_load
xlink_load_fxn.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_ushort, ctypes.c_char_p, ctypes.c_uint]
xlink_load_fxn.restype = ctypes.c_bool

# bool xlink_save(unsigned char memory, 
#                 unsigned char bank, 
#                 unsigned short address, 
#                 unsigned char* data,
# 		          unsigned int size) 
xlink_save_fxn = C_libxlink.xlink_save
xlink_save_fxn.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_ushort, ctypes.c_char_p, ctypes.c_uint]
xlink_save_fxn.restype = ctypes.c_bool


class Xlink():
    def __init__(self) -> None:
        pass

    def begin(self) -> None:
        xlink_begin_fxn()

    def end(self) -> None:
        xlink_end_fxn()

    def receive(self, data: str, size: int) -> bool:
        return xlink_receive_fxn(data, size)

    def poke(self, memory: int, bank: int, address: int, value: int) -> bool:
        return xlink_poke_fxn(memory, bank, address, value)

    def load(self, memory: int, bank: int, address: int, data: bytearray, size: int) -> bool:
        return xlink_load_fxn(memory, bank, address, data, size)

    def save(self, memory: int, bank: int, address: int, data: bytearray, size: int) -> bool:
        try:
            return xlink_save_fxn(memory, bank, address, bytes(data), size)
        except Exception as e:
            print(f"save failed {e}")
            return False
