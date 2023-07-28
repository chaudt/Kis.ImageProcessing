import cv2
import sys

inputfilepath = "C:\\Users\\Chau\\Downloads\\video.mp4"
outputfilepath = "C:\\Users\\Chau\\Downloads\\testvideo.mp4"

video = cv2.VideoCapture(inputfilepath)

fps = video.get(cv2.CAP_PROP_FPS)
framecount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("original fps: ", fps)
# fps = 29.4
print("writing fps: ", fps)

#writer = cv2.VideoWriter(outputfilepath, 0x00000020, fps, (width, height))
writer = cv2.VideoWriter(outputfilepath, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))



while video.isOpened():
    
    success, image = video.read()
    if not success:
        break

    writer.write(image)

writer.release()
video.release()

video = cv2.VideoCapture(outputfilepath)
fps = video.get(cv2.CAP_PROP_FPS)

# the next line will not print the same fps as I passed to cv2.VideoWriter(...) above.
print("output fps: ", fps)
video.release()