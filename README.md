
# SCAV VIDEO LAB 2
## USE IN TERMINAL THE FOLLOWING COMMAND-LINE ARGUMENTS TO USE THE DIFFERENT IMPLEMENTED METHODS:
### EXERCISE 1: CONVERT TO MP2 the Big Buck Bunny Video:

```ruby
python3 scav_video_lab_2.py --convert_to_mp2 bbb.mp4 bbb.mp2
```
### EXERCISE 1.1: GET VIDEO INFORMATION:
```ruby
python3 scav_video_lab_2.py --get_video_info bbb.mp4
```

### EXERCISE 2: CHANGE VIDEO RESOLUTION:
```ruby
python3 scav_video_lab_2.py --change_resolution bbb.mp4 resbbb.mp4 1080 720
```
### EXERCISE 3: CHANGE CHROMA SUBSAMPLING:
```ruby
python3 scav_video_lab_2.py --change_chroma_subsampling bbb.mp4 yuv420pbbb.mp4 yuv420p
```
_NOTICE THAT FOR LIBX264 ENCODER SOME PIX_FMT ARE NOT COMPATIBLE_

__TESTS HAVE BEEN RUNNING:__ _yuv420p | yuv422p | yuv444p._

For me yuv420p compression works very well :)

### EXERCISE 4: READ VIDEO INFORMATION AND PRINT DATA:
```ruby
python3 scav_video_lab_2.py --get_video_info bbb.mp4
```


### EXERCISE 5:
___AS WE CAN INTERPRET AS WE WANT THE EXERCISES I THINK IT CAN BE FUN TO APPLY SOME P1 METHODS TO A FRAME OF BBB TO CHECK THE [P1 <> P2] INTERACTION.
FOR THAT I HAVE IMPLEMENTED A FRAME EXTRACTOR FFMPEG METHOD WHICH WE WILL BE CALLING AT TIME: 00:00:20 WHICH IS A PRETTY BEAUTIFUL FRAME.___
```ruby
python3 scav_video_lab_2.py --extract_frame bbb.mp4 ex5_frame.jpeg 00:00:20
```

#### TESTS HAVE BEEN TESTING THE FOLLOWING METHODS INHERITED FROM P1:

#### RESIZE INPUT IMAGE INTO OUTPUT IMAGE:
```ruby
python3 scav_video_lab_2.py --resize_image INPUT_IMAGE.jpeg OUTPUT_IMAGE[NAME].jpeg WIDTH HEIGHT (Total of 4ARGS)
```

_TESTS ARE RUNNING:_
```ruby
python3 scav_video_lab_2.py --resize_image ex5_frame.jpeg ex_2_output_image.jpeg 960 540
```

#### READ THE BYTES OF A JPEG FILE IN THE SERPENTINE WAY:
_NOTICE THAT THE FUNCTION WILL PRINT THE FIRST 30 BYTES OF THE JPEG SERIAL CONVERSION OF THE CONVERTED DCT SPECTRUM TO PLACE ALL THE HIGH FREQUENCY COMPONENTS TOGETHER TO LATER COMPRESS USING A RUN-LENGTH ENCODING._

```ruby
python3 scav_video_lab_2.py --serpentine INPUT_IMAGE.jpeg WIDTH HEIGHT
```
_TESTS ARE RUNNING:_
```ruby
python3 scav_video_lab_2.py --serpentine ex5_frame.jpeg 1920 1080
```

#### TRANSFORM THE PREVIOUS IMAGE INTO B/W WITH THE HARDEST COMPRESSION POSSIBLE:
In order to perform a hard compression to the image we will use a constant rate factor of 51:
```ruby
python3 scav_video_lab_2.py --transform_image ex5_frame.jpeg ex4_output_image.jpeg 51
```

For this exercise the crf = 51 compression level has been used when encoding videos using the H.264/H.265 codecs.
This high CRF indicates stronger compression and lower quality, while a lower CRF value would have preserved more quality but would result in larger file size.
If we take a look at the output image, this level of compression results in a noticeable loss of image quality, and much smaller file size compared to the original.

#### APPLY A RUN-LENGTH ENCODING FROM A SERIES OF BYTES GIVEN:
```ruby
python3 scav_video_lab_2.py --run_length_encode INPUT_IMAGE.jpeg WIDTH HEIGHT
```
_TESTS ARE RUNNING:_
```ruby
python3 scav_video_lab_2.py --run_length_encode ex5_frame.jpeg 1920 1080
```
_I HAVE BEEN ALSO APPLYING RUN-LENGTH ENCODING TO THE EX4 OUTPUT B/W IMAGE:_
```ruby
python3 scav_video_lab_2.py --run_length_encode ex4_output_image.jpeg 1920 1080
```

