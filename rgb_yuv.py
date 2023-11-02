import argparse
from PIL import Image
import subprocess
import io
import numpy as np
import scipy.fftpack


###################
### ALL METHODS ###
###################


#Performing RGB to YUV conversion
def rgb_yuv(r, g, b):
    #Computing Y component
    y = (0.257 * r) + (0.504 * g) + (0.098 * b) + 16
    #Computing U component
    u = (-0.148 * r) - (0.291 * g) + (0.439 * b) + 128
    #Computing V component
    v = (0.439 * r) - (0.368 * g) - (0.071 * b) + 128
    return y, u, v

#Performing YUV to RGB conversion
def yuv_rgb(y, u, v):
    #Computing R component
    r = 1.164 * (y - 16) + 1.596 * (v - 128)
    #Computing G component
    g = 1.164 * (y - 16) - 0.813 * (v - 128) - 0.391 * (u - 128)
    #Computing B component
    b = 1.164 * (y - 16) + 2.018 * (u - 128)
    return r, g, b

#Performing image resizing using FFmpeg
def ffmpeg_resize_image(input_file, output_file, width, height):
    cmd = f'ffmpeg -i {input_file} -vf "scale={width}:{height}" {output_file}'
    try:
        subprocess.run(cmd, shell=True, check=True) #Executing the FFmpeg command
        print(f"Image resized and saved as {output_file}")
    except subprocess.CalledProcessError as e: #Error COntrol
        print(f"Error resizing image: {e}")

#Performing serpentine read on a JPEG image
def serpentine(input_image, input_width, input_height):
    input_width = int(input_width)
    input_height = int(input_height)
    #Reading the image bytes
    with open(input_image, 'rb') as file:
        image_bytes = file.read()

    #Initializing the variables
    serpentine_bytes = []
    current_x, current_y = 0, 0

    #Iterating through the image bytes using the serpentine zigzag pattern
    for byte in image_bytes:
        serpentine_bytes.append(byte)

        #Moving to the next position in the zigzag pattern
        if current_y % 2 == 0:
            current_x += 1
        else:
            current_x -= 1

        #Checking if the current position is at the end of the row
        if current_x < 0 or current_x >= input_width:
            current_y += 1

            if current_y % 2 == 0:
                current_x = input_width - 1  #Adjusting the position at the start of a new row
            else:
                current_x = 0  #Adjusting the position at the start of a new row

    #PRINTINT THE FIRST 30 DIGITS OF THE SERPENTINE BYTES SEQUENCE TO CHECK HOW MANY SEQUENCES OF ZEROS WE HAVE BEFORE THE RUN-LENGTH ENCODING :)
    print(f"Serpentine bytes: {serpentine_bytes[:30]}")
    #Returning the linear sequence of DCT coefficients
    return serpentine_bytes


#Performing image transformation to grayscale and applying compression using FFmpeg
def transform_image_with_hard_compression(input_image, output_image, crf=51):
    cmd = f'ffmpeg -i {input_image} -vf format=gray -q:v {crf} {output_image}'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"Image transformed with hardest compression (CRF={crf}) and saved as {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error transforming image: {e}")

#Performing run-length encoding on input data
def run_length_encode(serpentine_bytes):
    if len(serpentine_bytes) == 0:
        print("Please run first a JPEG Serial Conversion with --serpentine :)")
        return 0

    encoded_data = []
    current_byte = serpentine_bytes[0]
    count = 1

    for byte in serpentine_bytes[1:]:
        if byte == current_byte:
            count += 1
        else:
            if current_byte == 0:  #Checking if the current byte is zero
                encoded_data.append(0)  #Appending 0 to indicate a sequence of zeros
                encoded_data.append(count)  #Appending the count of zeros
            else:
                encoded_data.append(current_byte)
            current_byte = byte
            count = 1

    #Checking if the last byte in the sequence is zero
    if current_byte == 0:
        encoded_data.append(0)
        encoded_data.append(count)
    else:
        encoded_data.append(count)
        encoded_data.append(current_byte)

    #PRINTING THE FIRST 30 DIGITS OF THE RUN-LENGTH ENCODER SEQUENCE TO CHECK HOW MANY SEQUENCES OF ZEROS HAVE BEEN COMPRESSED WITH THE RUN-LENGTH ENCODING :)
    print(f"Run-length Encoded Data: {encoded_data[:30]}")

    return encoded_data


###############################
###   DCT CONVERTER CLASS   ###
###############################

class DCTConverter:
    def __init__(self):
        pass

    def dct(self, data):
        return scipy.fftpack.dct(data, norm='ortho')

    def idct(self, dct_data):
        return np.round(scipy.fftpack.idct(dct_data, norm='ortho'), 10)  #Rounding to 10 decimal places so we don't get 1e-16 on the output matrices :)

    def convert_to_dct(self, input_data):
        return self.dct(input_data)

    def convert_from_dct(self, dct_data):
        return self.idct(dct_data)


##################
###    MAIN    ###
##################

serpentine_data = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert between RGB and YUV color spaces, resize image using FFMPEG and more...")
    parser.add_argument("--rgb_to_yuv", type=float, nargs=3, help="Convert RGB to YUV. Provide three values: R G B")
    parser.add_argument("--yuv_to_rgb", type=float, nargs=3, help="Convert YUV to RGB. Provide three values: Y U V")
    parser.add_argument("--resize_image", nargs=4, help="Resize an image using FFmpeg. Provide input file, output file, width, height")
    parser.add_argument("--serpentine", nargs=3, help="Perform serpentine read on a JPEG image")
    parser.add_argument("--transform_image", nargs=3, help="Transform an image to B/W and apply compression. Provide input file and output file")
    parser.add_argument("--run_length_encode", nargs=3, help="Run the run-length encoding. Provide input file, output file, width, height")
    parser.add_argument("--dct_conversion", action="store_true", help="Perform DCT Conversion using the implemented class")

    args = parser.parse_args()


    if args.rgb_to_yuv:
            r, g, b = args.rgb_to_yuv
            y, u, v = rgb_yuv(r, g, b)
            print(f"RGB({r}, {g}, {b}) -> YUV({y}, {u}, {v})")

    if args.yuv_to_rgb:
            y, u, v = args.yuv_to_rgb
            r, g, b = yuv_rgb(y, u, v)
            print(f"YUV({y}, {u}, {v}) -> RGB({r}, {g}, {b})")

    if args.resize_image:
            input_file, output_file, width, height = args.resize_image
            ffmpeg_resize_image(input_file, output_file, width, height)

    if args.serpentine:
            input_image, input_width, input_height = args.serpentine
            serpentine_data = serpentine(input_image, input_width, input_height)
            print("Serpentine data processing Completed.")

    if args.transform_image:
            input_image, output_file, crf = args.transform_image
            transform_image_with_hard_compression(input_image, output_file, crf)

    if args.run_length_encode:
            input_image, input_width, input_height = args.run_length_encode
            run_length_data = serpentine(input_image, input_width, input_height)
            encoded_data = run_length_encode(run_length_data)
            print("Run-length Encoding Completed.")

    if args.dct_conversion:
            #CHANGE THE INPUT DATA TO THE DESIRED ONE:##
            input_data = np.identity(8)
            ############################################
            dct_converter = DCTConverter()
            dct_data = dct_converter.convert_to_dct(input_data)
            decoded_data = dct_converter.convert_from_dct(dct_data)
            print("Original Data:")
            print(input_data)
            print("\nDCT Coefficients:")
            print(dct_data)
            print("\nDecoded Data:")
            print(decoded_data)



###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
#USE IN TERMINAL THE FOLLOWING COMMAND-LINE ARGUMENTS TO USE THE DIFFERENT IMPLEMENTED METHODS ABOVE:

#EXERCISE 1: CONVERT RGB TO YUV:
#python3 rgb_yuv.py --rgb_to_yuv R G B (Replace with the values we want to convert)

#EXERCISE 1: CONVERT YUV TO RGB:
#python3 rgb_yuv.py --yuv_to_rgb Y U V (Replace with the values we want to convert)

#EXERCISE 2: RESIZE INPUT IMAGE INTO OUTPUT IMAGE:
#python3 rgb_yuv.py --resize_image INPUT_IMAGE.jpeg OUTPUT_IMAGE[NAME].jpeg WIDTH HEIGHT (Total of 4ARGS)  |  TESTS ARE RUNNING: python3 rgb_yuv.py --resize_image input_image.jpeg ex_2_output_image.jpeg 960 1440

#EXERCISE 3: READ THE BYTES OF A JPEG FILE IN THE SERPENTINE WAY:
#NOTICE THAT THE FUNCTION WILL PRINT THE FIRST 30 BYTES OF THE JPEG SERIAL CONVERSION OF THE CONVERTED DCT SPECTRUM TO PLACE ALL THE HIGH FREQUENCY COMPONENTS TOGETHER TO LATER COMPRESS USING A RUN-LENGTH ENCODING.
#python3 rgb_yuv.py --serpentine INPUT_IMAGE.jpeg WIDTH HEIGHT   |   TESTS ARE RUNNING: python3 rgb_yuv.py --serpentine input_image.jpeg 1920 2879

#EXERCISE 4: TRANSFORM THE PREVIOUS IMAGE INTO B/W WITH THE HARDEST COMPRESSION POSSIBLE:
#In order to perform a hard compression to the image we will use a constant rate factor of 51
#python3 rgb_yuv.py --transform_image input_image.jpeg ex4_output_image.jpeg 51

#For this exercise the crf = 51 compression level has been used when encoding videos using the H.264/H.265 codecs.
#This high CRF indicates stronger compression and lower quality, while a lower CRF value would have preserved more quality but would result in larger file size.
#If we take a look at the output image, this level of compression results in a noticeable loss of image quality, and much smaller file size compared to the original.

#EXERCISE 5: APPLY A RUN-LENGTH ENCODING FROM A SERIES OF BYTES GIVEN:
#python3 rgb_yuv.py --run_length_encode INPUT_IMAGE.jpeg WIDTH HEIGHT   |   TESTS ARE RUNNING: python3 rgb_yuv.py --run_length_encode input_image.jpeg 1920 2879
#I HAVE BEEN ALSO APPLYING RUN-LENGTH ENCODING TO THE EX4 OUTPUT B/W IMAGE: python3 rgb_yuv.py --run_length_encode ex4_output_image.jpeg 1920 2879

#EXERCISE 6: CLASS TO CONVERT AND DECODE AN INPUT USING THE DCT
#python3 rgb_yuv.py --dct_conversion

###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
