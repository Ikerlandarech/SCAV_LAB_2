import argparse
import subprocess
import re
import os
import io
import numpy as np

#EXERCISE 5: INHERIT + INTERACT [P1 <> P2]:
from rgb_yuv import DCTConverter
from rgb_yuv import yuv_rgb, rgb_yuv, ffmpeg_resize_image, serpentine, transform_image_with_hard_compression, run_length_encode
###

###################
### ALL METHODS ###
###################

def convert_to_mp2(input_file, output_file):
    command = f"ffmpeg -i {input_file} -c:v mpeg2video {output_file}"
    subprocess.call(command, shell=True)

def get_video_info(input_file):
    input_video = str(input_file[0])
    #Showing the duration of the video
    command_duration = f"ffmpeg -i {input_video} 2>&1 | grep Duration | awk '{{print $2}}' | tr -d ,"
    duration = subprocess.check_output(command_duration, shell=True, stderr=subprocess.STDOUT, text=True)

    #Showing the resolution of the video
    command_resolution = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {input_video}"
    resolution = subprocess.check_output(command_resolution, shell=True, stderr=subprocess.STDOUT, text=True)

    #Showing the bitrate of the video
    command_bitrate = f"ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1 {input_video}"
    bitrate = subprocess.check_output(command_bitrate, shell=True, stderr=subprocess.STDOUT, text=True)

    #Showing the frame rate of the video
    command_framerate = f"ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1 {input_video}"
    framerate = subprocess.check_output(command_framerate, shell=True, stderr=subprocess.STDOUT, text=True)

    #Showing the video codec
    command_videocodec = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1 {input_video}"
    videocodec = subprocess.check_output(command_videocodec, shell=True, stderr=subprocess.STDOUT, text=True)

    #Showing the audio codec
    command_audiocodec = f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1 {input_video}"
    audiocodec = subprocess.check_output(command_audiocodec, shell=True, stderr=subprocess.STDOUT, text=True)

    #Showing the container format
    command_format = f"ffprobe -v error -select_streams v:0 -show_entries format=format_name -of default=noprint_wrappers=1 {input_video}"
    containerformat = subprocess.check_output(command_format, shell=True, stderr=subprocess.STDOUT, text=True)

    return (
        f"Duration: {duration.strip()}\n"
        f"Resolution: {resolution.strip()}\n"
        f"Bitrate: {bitrate.strip()}\n"
        f"Frame Rate: {framerate.strip()}\n"
        f"Video Codec: {videocodec.strip()}\n"
        f"Audio Codec: {audiocodec.strip()}\n"
        f"Container Format: {containerformat.strip()}"
    )

def change_resolution(input_video, output_video, new_width, new_height):
    command = f"ffmpeg -i {input_video} -vf scale={new_width}:{new_height} {output_video}"
    subprocess.call(command, shell=True)

def change_chroma_subsampling(input_video, output_video, pix_fmt):
    command = f"ffmpeg -i {input_video} -c:v libx264 -pix_fmt {pix_fmt} {output_video}"
    subprocess.call(command, shell=True)

def extract_frame(input_video, output_image, time):
    command = f"ffmpeg -i {input_video} -ss {time} -vframes 1 {output_image}"
    subprocess.call(command, shell=True)


##################
###    MAIN    ###
##################

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert video to .mp2, extract video info using ffmpeg and more...")
    parser.add_argument("--convert_to_mp2", nargs=2, help="Convert to mp2 input video")
    parser.add_argument("--get_video_info", nargs=1, help="Get Video Information")
    parser.add_argument("--change_resolution", nargs=4, help="Change Video Resolution")
    parser.add_argument("--change_chroma_subsampling", nargs=3, help="Change Chroma Subsampling")
    parser.add_argument("--extract_frame", nargs=3, help="Extract Frame from Video")
    parser.add_argument("--rgb_to_yuv", type=float, nargs=3, help="Convert RGB to YUV. Provide three values: R G B")
    parser.add_argument("--yuv_to_rgb", type=float, nargs=3, help="Convert YUV to RGB. Provide three values: Y U V")
    parser.add_argument("--resize_image", nargs=4, help="Resize an image using FFmpeg. Provide input file, output file, width, height")
    parser.add_argument("--serpentine", nargs=3, help="Perform serpentine read on a JPEG image")
    parser.add_argument("--transform_image", nargs=3, help="Transform an image to B/W and apply compression. Provide input file and output file")
    parser.add_argument("--run_length_encode", nargs=3, help="Run the run-length encoding. Provide input file, output file, width, height")
    parser.add_argument("--dct_conversion", action="store_true", help="Perform DCT Conversion using the implemented class")

    args = parser.parse_args()

    if args.convert_to_mp2:
        input_video, output_video = args.convert_to_mp2
        convert_to_mp2(input_video, output_video)
        print(f"Conversion completed. Output file: {output_video}")

    if args.get_video_info:
        output_video = args.get_video_info
        video_info = get_video_info(output_video)
        print("Video Information:")
        print(video_info)
    
    if args.change_resolution:
        input_video, output_video, height, width = args.change_resolution
        change_resolution(input_video, output_video, height, width)
        print(f"Conversion completed. Output file: {output_video}")

    if args.change_chroma_subsampling:
        input_video, output_video, pix_fmt = args.change_chroma_subsampling
        change_chroma_subsampling(input_video, output_video, pix_fmt)
        print(f"Conversion completed. Output file: {output_video}")

    if args.extract_frame:
        input_video, frame, time = args.extract_frame
        extract_frame(input_video, frame, time)
        print(f"Frame Extracted. Output file: {frame}")

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

#EXERCISE 1: CONVERT TO MP2 the Big Buck Bunny Video:
#python3 scav_video_lab_2.py --convert_to_mp2 bbb.mp4 bbb.mp2

#EXERCISE 1: GET VIDEO INFORMATION:
#python3 scav_video_lab_2.py --get_video_info bbb.mp4

#EXERCISE 2: CHANGE VIDEO RESOLUTION:
#python3 scav_video_lab_2.py --change_resolution bbb.mp4 resbbb.mp4 1080 720

#EXERCISE 3: CHANGE CHROMA SUBSAMPLING:
#python3 scav_video_lab_2.py --change_chroma_subsampling bbb.mp4 yuv420pbbb.mp4 yuv420p
#NOTICE THAT FOR LIBX264 ENCODER SOME PIX_FMT ARE NOT COMPATIBLE, TESTS HAVE BEEN RUNNING: yuv420p | yuv422p | yuv444p.
#For me yuv420p compression works very well :)

#EXERCISE 4: READ VIDEO INFORMATION AND PRINT DATA:
#python3 scav_video_lab_2.py --get_video_info bbb.mp4

#EXERCISE 5:
#AS WE CAN INTERPRET AS WE WANT THE EXERCISES I THINK IT CAN BE FUN TO APPLY SOME P1 METHODS TO A FRAME OF BBB TO CHECK THE [P1 <> P2] INTERACTION.
#FOR THAT I HAVE IMPLEMENTED A FRAME EXTRACTOR FFMPEG METHOD WHICH WE WILL BE CALLING AT TIME: 00:00:20 WHICH IS A PRETTY BEAUTIFUL FRAME.
#python3 scav_video_lab_2.py --extract_frame bbb.mp4 ex5_frame.jpeg 00:00:20


#TESTS HAVE BEEN TESTING THE FOLLOWING METHODS INHERITED FROM P1:

#RESIZE INPUT IMAGE INTO OUTPUT IMAGE:
#python3 scav_video_lab_2.py --resize_image INPUT_IMAGE.jpeg OUTPUT_IMAGE[NAME].jpeg WIDTH HEIGHT (Total of 4ARGS)  |  TESTS ARE RUNNING: python3 scav_video_lab_2.py --resize_image ex5_frame.jpeg ex_2_output_image.jpeg 960 540

#READ THE BYTES OF A JPEG FILE IN THE SERPENTINE WAY:
#NOTICE THAT THE FUNCTION WILL PRINT THE FIRST 30 BYTES OF THE JPEG SERIAL CONVERSION OF THE CONVERTED DCT SPECTRUM TO PLACE ALL THE HIGH FREQUENCY COMPONENTS TOGETHER TO LATER COMPRESS USING A RUN-LENGTH ENCODING.
#python3 scav_video_lab_2.py --serpentine INPUT_IMAGE.jpeg WIDTH HEIGHT   |   TESTS ARE RUNNING: python3 scav_video_lab_2.py --serpentine ex5_frame.jpeg 1920 1080

#TRANSFORM THE PREVIOUS IMAGE INTO B/W WITH THE HARDEST COMPRESSION POSSIBLE:
#In order to perform a hard compression to the image we will use a constant rate factor of 51
#python3 scav_video_lab_2.py --transform_image ex5_frame.jpeg ex4_output_image.jpeg 51

#For this exercise the crf = 51 compression level has been used when encoding videos using the H.264/H.265 codecs.
#This high CRF indicates stronger compression and lower quality, while a lower CRF value would have preserved more quality but would result in larger file size.
#If we take a look at the output image, this level of compression results in a noticeable loss of image quality, and much smaller file size compared to the original.

#EXERCISE 5: APPLY A RUN-LENGTH ENCODING FROM A SERIES OF BYTES GIVEN:
#python3 scav_video_lab_2.py --run_length_encode INPUT_IMAGE.jpeg WIDTH HEIGHT   |   TESTS ARE RUNNING: python3 scav_video_lab_2.py --run_length_encode ex5_frame.jpeg 1920 1080
#I HAVE BEEN ALSO APPLYING RUN-LENGTH ENCODING TO THE EX4 OUTPUT B/W IMAGE: python3 scav_video_lab_2.py --run_length_encode ex4_output_image.jpeg 1920 1080

###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################