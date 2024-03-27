import ctypes
import os

C_libxlink = ctypes.CDLL("libxlink.so")
# C_xthin = ctypes.CDLL("xthin.so")

BANK = 0x00
ADDRESS = 0x0400
memory = 0x37

#void xlink_begin()
xlink_begin_fxn = C_libxlink.xlink_begin
def xlink_begin():
    xlink_begin_fxn()

#void xlink_end()
xlink_end_fxn = C_libxlink.xlink_end
def xlink_end():
    xlink_end_fxn()

#bool xlink_receive(uchar *data, uint size)
xlink_receive_fxn = C_libxlink.xlink_receive
xlink_receive_fxn.argtypes = [ctypes.c_char_p, ctypes.c_uint]
xlink_receive_fxn.restype = ctypes.c_bool
def xlink_receive(data: str, size: int) -> bool:
    return xlink_receive_fxn(data, size)

# bool xlink_poke(unsigned char memory, 
# 		unsigned char bank, 
# 		unsigned short address, 
# 		unsigned char value)
xlink_poke_fxn = C_libxlink.xlink_poke
xlink_poke_fxn.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_ushort, ctypes.c_char]
xlink_poke_fxn.restype = ctypes.c_bool
def xlink_poke(memory: int, bank: int, address: int, value: int) -> bool:
    return xlink_poke_fxn(memory, bank, address, value)

# bool xlink_load(unsigned char memory, 
#                 unsigned char bank, 
#                 unsigned short address, 
#                 unsigned char* data,
#                 unsigned int size)
xlink_load_fxn = C_libxlink.xlink_load
xlink_load_fxn.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_ushort, ctypes.c_char_p, ctypes.c_uint]
xlink_load_fxn.restype = ctypes.c_bool
def xlink_load(memory: int, bank: int, address: int, data: str, size: int) -> bool:
    return xlink_load_fxn(memory, bank, address, data, size)

# bool xlink_save(unsigned char memory, 
#                 unsigned char bank, 
#                 unsigned short address, 
#                 unsigned char* data,
# 		          unsigned int size) 
xlink_save_fxn = C_libxlink.xlink_save
xlink_save_fxn.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_ushort, ctypes.c_char_p, ctypes.c_uint]
xlink_save_fxn.restype = ctypes.c_bool
def xlink_save(memory: int, bank: int, address: int, data: str, size: int) -> bool:
    return xlink_save_fxn(memory, bank, address, data, size)


#==============================================================================

backup_screen = ctypes.create_string_buffer(40*25)
xthin_screen = ctypes.create_string_buffer(40*25)
# write "HONDANI" ascii logo to the xthin screen
xthin_screen[0:7] = bytes([0x48, 0x4f, 0x4e, 0x44, 0x41, 0x4e, 0x49])
thin_mode = False    

def enable_thin_mode():
    global thin_mode
    rc = xlink_poke(memory, BANK, 0xd020, 0x00)  # indicate thin mode enabled
    print(f"enter thin mode {rc}")
    rc = xlink_save(memory, BANK, ADDRESS, backup_screen, 40*25)  # save screen memory (40x25, 1 byte per character, 1 byte per color)
    print(f"saved screen {rc}")
    rc = xlink_load(memory, BANK, ADDRESS, xthin_screen, 40*25)  # load current xthin screen
    print(f"xthin screen pushed {rc}")
    thin_mode = True


def disable_thin_mode():
    global thin_mode
    rc = xlink_load(memory, BANK, ADDRESS, backup_screen, 40*25)  # load screen memory (40x25, 1 byte per character, 1 byte per color)
    print(f"restored {rc}")
    rc = xlink_poke(memory, BANK, 0xd020, 0x0e)  # indicate thin mode disabled
    print(f"exited {rc}")
    thin_mode = False


def list_directory():
    # get current directory
    pwd = os.getcwd()
    xthin_screen[40:40+len(pwd)] = pwd.encode()
    rc = xlink_load(memory, BANK, ADDRESS, xthin_screen, 40*25)  # load current xthin screen
    print(f"xthin screen pushed {rc}")


def wait_key() -> int:
    key_input: bytes = b' ';
    xlink_begin()
    while (not xlink_receive(key_input, 1)):  # wait for key input)
        xlink_begin()
    xlink_end()
    return key_input


def dispatch_key(key: int):
        key_int = int.from_bytes(key, "big")
        xlink_end()

        if key_int == 0x40:
            return

        print(key_int)

        if thin_mode == False:
            if key_int == 0x39:  # left arrow enter thin mode
                enable_thin_mode()
                return
        else:
            # thin_mode == True
            if (key_int == 0x3f): ## Run/Stop exit thin mode
                disable_thin_mode()
                return
            
            if (key_int == 0x2a):  # l
                print("list")
                list_directory()
                return                
                


if __name__ == "__main__":
    while True:
        dispatch_key(wait_key())
