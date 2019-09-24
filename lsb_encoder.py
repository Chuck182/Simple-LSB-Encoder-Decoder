# Script written by Chuck182
# This script is a simple LSB encoder/decoder.
# The message is hidden into image using LSB method
# From left to right and top to bottom
# End of message is ETX (End Of Text (ASCII 03))
import sys
import bitarray
from PIL import Image

ENCODER = 1
DECODER = 2

# Global vars
script_mode = None
src_img = None
dst_img = None
input_msg = None

# Encode Message
def encode():
    print ("Encoder mode")
    print ("Message : "+input_msg)
    print ("Source image : "+src_img)
    print ("Destination image : "+dst_img)
    msg_bits = bitarray.bitarray()
    msg_bits.frombytes(input_msg.encode('utf-8'))
    msg_bits.extend([0,0,0,0,0,0,1,1])
    #print ("Msg_bits : "+str(msg_bits))


    # Open source Image
    src = Image.open(src_img)
    pixel_map = src.load()

    # Open dst image
    dst = Image.new(src.mode, src.size)
    pixel_map_new = dst.load()

    for i in range(dst.size[0]):
        for j in range(dst.size[1]):
            r = pixel_map[i, j][0]
            g = pixel_map[i, j][1]
            b = pixel_map[i, j][2]
            if len(msg_bits) > 0:
                r = chg_bit(r, msg_bits.pop(0))
                #print ("new : "+str(bin(r)[-1]))
            if len(msg_bits) > 0:
                g = chg_bit(g, msg_bits.pop(0))
                #print ("new : "+str(bin(g)[-1]))
            if len(msg_bits) > 0:
                b = chg_bit(b, msg_bits.pop(0))
                #print ("new : "+str(bin(b)[-1]))
            pixel_map_new[i, j] = (r, g, b)

    # Closing and saving dst Image
    dst.save(dst_img)
    dst.close()

# Set pixel LSB value
def chg_bit(color_int, bit):
    mask = 1 << 0
    return (color_int & ~mask) | ((bit << 0) & mask)

# Decode message
def decode():
    msg = ""
    # Open source Image
    src = Image.open(src_img)
    pixel_map = src.load()
    # Extract_message
    byte = bitarray.bitarray()
    for i in range(src.size[0]):
        for j in range(src.size[1]):
            r = pixel_map[i, j][0]
            g = pixel_map[i, j][1]
            b = pixel_map[i, j][2]
            byte.append(int(bin(r)[-1]))
            if len(byte) >= 8:
                if byte.tobytes() == b'\x03':
                    print ("msg : "+msg)
                    sys.exit()
                else:
                    msg = msg+str(byte.tobytes())
                    byte = bitarray.bitarray()
            byte.append(int(bin(g)[-1]))
            if len(byte) >= 8:
                if byte.tobytes() == b'\x03':
                    print ("msg : "+msg)
                    sys.exit()
                else:
                    msg = msg+str(byte.tobytes())
                    byte = bitarray.bitarray()
            byte.append(int(bin(b)[-1]))
            if len(byte) >= 8:
                if byte.tobytes() == b'\x03':
                    print ("msg : "+msg)
                    sys.exit()
                else:
                    msg = msg+str(byte.tobytes())
                    byte = bitarray.bitarray()


# Display script usage
def display_usage():
    print ("USAGE :")
    print ("  > Hide text into img : lsb_encoder.py encode message source_img destination_img")
    print ("  > Decode text from img : lsb_encoder.py decode <src_img>")
    print ("")

def are_args_valid(args):
    global script_mode, src_img, dst_img, input_msg
    valid = True
    if len(args) < 3:
        valid = False
    elif args[1] == "encode":
        if len(args) < 5:
            valid = False
        else:
            script_mode = ENCODER
            input_msg = args[2]
            src_img = args[3]
            dst_img = args[4]
    elif args[1] == "decode":
        script_mode = DECODER
        src_img = args[2]
    else:
        valid = False
    return valid

if __name__ == '__main__':
    print ("=== LSB Encoder / Decoder ===")
    if not are_args_valid(sys.argv):
        display_usage()
        sys.exit()
    if script_mode == ENCODER:
        encode()
    elif script_mode == DECODER:
        decode()
