import cv2
import numpy as np
import skimage.exposure
from PIL import Image
import io
from rembg import remove
import os
def test():    
    frame = cv2.imread('C:\\Users\\Chau\\Downloads\\change_bg\\Photo11.bmp')
    #image = cv2.imread('E:\\KisData\\Database\\Screens\\ChangeBackgroundColor\\bggradbrown_sample.png')
    #frame = cv2.resize(frame, (640, 750))
    #frame = cv2.resize(frame, (640, 480))
    #frame = cv2.resize(frame, (135, 179))
    #image = cv2.resize(image, (135, 179))
  
  
    u_green = np.array([104, 153, 70])
    l_green = np.array([30, 30, 0])
  
    mask = cv2.inRange(frame, l_green, u_green)
    #res = cv2.bitwise_and(frame, frame, mask = mask)
  
    ####
    img = frame
    # convert to LAB
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

    # extract A channel
    A = lab[:,:,1]

    # threshold A channel
    thresh = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # blur threshold image
    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX=5, sigmaY=5, borderType = cv2.BORDER_DEFAULT)

    # stretch so that 255 -> 255 and 127.5 -> 0
    mask = skimage.exposure.rescale_intensity(blur, in_range=(127.5,255), out_range=(0,255)).astype(np.uint8)

    # add mask to image as alpha channel
    result = img.copy()
    result = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)
    result[:,:,3] = mask

    # save output
    #cv2.imwrite('greenscreen_thresh.png', thresh)
    #cv2.imwrite('greenscreen_mask.png', mask)
    cv2.imwrite('greenscreen_antialiased.png', result)

    # Display various images to see the steps
    cv2.imshow('Result',result)

    cv2.imshow("video", frame)
    # ####  
    #f = frame - res
    #f = np.where(f == 0, image, f)
    # img_rmbg = remove(frame)

    # cv2.imwrite('chau.png',img_rmbg)

    # cv2.imshow("video", frame)
    #cv2.imshow("mask", f)
    print('adssad')
    #cv2.imwrite('/data/t1.png',frame)
    #cv2.imwrite('/data/t2.png',f)
    print('finished')
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()

def test_02():
    path = 'C:\\Users\\Chau\\Downloads\\change_bg\\Photo10 (1).bmp'
    img = cv2.imread(path)
    result = remove(
    img,
    # alpha_matting=True,
    # alpha_matting_foreground_threshold=240,
    # alpha_matting_background_threshold=100,
    # alpha_matting_erode_structure_size=100,
    # alpha_matting_base_size=1000,
)
    # img = Image.open(io.BytesIO(result)).convert("RGBA")
    # img.save('bg.png')
    cv2.imwrite('bg.png',result)
def bgremove3(myimage):
    # BG Remover 3
    myimage_hsv = cv2.cvtColor(myimage, cv2.COLOR_BGR2HSV)
     
    #Take S and remove any value that is less than half
    s = myimage_hsv[:,:,1]
    s = np.where(s < 127, 0, 1) # Any value below 127 will be excluded
 
    # We increase the brightness of the image and then mod by 255
    v = (myimage_hsv[:,:,2] + 127) % 255
    v = np.where(v > 127, 1, 0)  # Any value above 127 will be part of our mask
 
    # Combine our two masks based on S and V into a single "Foreground"
    foreground = np.where(s+v > 0, 1, 0).astype(np.uint8)  #Casting back into 8bit integer
 
    background = np.where(foreground==0,255,0).astype(np.uint8) # Invert foreground to get background in uint8
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)  # Convert background back into BGR space
    foreground=cv2.bitwise_and(myimage,myimage,mask=foreground) # Apply our foreground map to original image
    finalimage = background+foreground # Combine foreground and background
 
    return finalimage
    
def test_03():
    
    path = 'bg.png'
    

    # load image
    img = cv2.imread(path)
    u_green = np.array([104, 153, 70])
    l_green = np.array([30, 30, 0])
  
    maskxx = cv2.inRange(img, l_green, u_green)

    # convert to graky
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold input image as mask
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # negate mask
    mask = 255 - mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # save resulting masked image
    cv2.imwrite('result.png', result)

    # display result, though it won't show transparency
    #cv2.imshow("INPUT", img)
    #cv2.imshow("GRAY", gray)
    #cv2.imshow("MASK", mask)
    #cv2.imshow("RESULT", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

from transparent_background import Remover
def transparent_background_photo():
    #path_img = 'C:\\Users\\Chau\\Downloads\\change_bg\\Photo11_rmbg_354_3_0_1000.png'
    path_img = 'C:\\Users\\Chau\\Downloads\\change_bg\\Photo10 (1).bmp'#Photo11.bmp'

    # Load model
    remover = Remover() # default setting
    #remover = Remover(fast=True, jit=True, device='cuda:0', ckpt='C:\\Users\\Chau\\.transparent-background\\ckpt_base.pth') # custom setting
    #remover = Remover(fast=True, jit=True, device='cpu', ckpt='C:\\Users\\Chau\\.transparent-background\\ckpt_base.pth') # custom setting

    # Usage for image
    img = Image.open(path_img).convert('RGB') # read image
    extract_folder = './data/transparent_bgs'
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    try:
        out = remover.process(img) # default setting - transparent background
        Image.fromarray(out).save(os.path.join(extract_folder,'output_default.png')) # save result
    except Exception as ex:
        print(f'-->mode default error:{ex}')

    try:
        out = remover.process(img, type='rgba') # same as above
        Image.fromarray(out).save(os.path.join(extract_folder,'output_rgba.png')) # save result
    except Exception as ex:
        print(f'-->mode rgba error:{ex}')

    try:
        out = remover.process(img, type='map') # object map only
        Image.fromarray(out).save(os.path.join(extract_folder,'output_map.png')) # save result
    except Exception as ex:
        print(f'-->mode map error:{ex}')
    try:
        out = remover.process(img, type='green') # image matting - green screen
        Image.fromarray(out).save(os.path.join(extract_folder,'output_green.png')) # save result
    except Exception as ex:
        print(f'-->mode green error:{ex}')
    try:
        out = remover.process(img, type='white') # change backround with white color -> [2023.05.24] Contributed by carpedm20
        Image.fromarray(out).save(os.path.join(extract_folder,'output_white.png')) # save result
    except Exception as ex:
        print(f'-->mode white error:{ex}')
    try:
        out = remover.process(img, type=[255, 0, 0]) # change background with color code [255, 0, 0] -> [2023.05.24] Contributed by carpedm20
        Image.fromarray(out).save(os.path.join(extract_folder,'output_255.png')) # save result
    except Exception as ex:
        print(f'-->mode 255 error:{ex}')
    try:
        out = remover.process(img, type='blur') # blur background
        Image.fromarray(out).save(os.path.join(extract_folder,'output_blur.png')) # save result
    except Exception as ex:
        print(f'-->mode blur error:{ex}')
    try:
        out = remover.process(img, type='overlay') # overlay object map onto the image
        Image.fromarray(out).save(os.path.join(extract_folder,'output_overlay.png')) # save result
    except Exception as ex:
        print(f'-->mode overlay error:{ex}')

    try:
        path_bg = 'E:\\KisData\\Database\Screens\\ChangeBackgroundColor\\bggradbrown_sample.png'
        out = remover.process(img, type=path_bg) # use another image as a background
        Image.fromarray(out).save(os.path.join(extract_folder,'output_bg.png')) # save result
    except Exception as ex:
        print(f'-->mode overlay error:{ex}')
    #Image.fromarray(out).save('output.png') # save result

    # Usage for video
    # cap = cv2.VideoCapture('samples/b5.mp4') # video reader for input
    # fps = cap.get(cv2.CAP_PROP_FPS)

    # writer = None

    # while cap.isOpened():
    #     ret, frame = cap.read() # read video

    #     if ret is False:
    #         break
            
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    #     img = Image.fromarray(frame).convert('RGB')

    #     if writer is None:
    #         writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, img.size) # video writer for output

    #     out = remover.process(img, type='map') # same as image, except for 'rgba' which is not for video.
    #     writer.write(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))

    # cap.release()
    # writer.release()
def test_trans_default():
    path_img = 'C:\\Users\\Chau\\Downloads\\change_bg\\Photo10 (1).bmp'
    remover = Remover(device='cpu') 

    frame = cv2.imread(path_img)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame).convert('RGB')
    out = remover.process(image)
    extract_folder = './data/transparent_bgs'
    new_path_img = os.path.join(extract_folder,'test_tp_grba_01.png')
    #Image.fromarray(out).save(new_path_img)
    out_default = Image.fromarray(out).convert('RGB')
    out = remover.process(out_default, type='rgba')
    Image.fromarray(out).save(new_path_img)
    out_default = Image.fromarray(out).convert('RGB')
    path_bg = 'E:\\KisData\\Database\Screens\\ChangeBackgroundColor\\bggradbrown_sample.png'
    #img = Image.open(new_path_img).convert('RGB') # read image
    #out = remover.process(img, type=path_bg) # use another image as a background
    out = remover.process(out_default, type=path_bg)
    Image.fromarray(out).save(os.path.join(extract_folder,'test_tp_addbg01.png')) # save result

def convert2png(paths):
    for path in paths:
        img = Image.open(path)
        name = os.path.splitext(path)[0]
        img.save(f'{name}.png')
if __name__=='__main__':
    print('hello')
    #test_02()
    #transparent_background_photo()
    # img = Image.open('./data/transparent_bgs/output_default.png')
    # new_img = remove(img)
    # new_img.save('./data/transparent_bgs/test.png')
    ##test_trans_default()
    convert2png(['C:\\Users\\Chau\\Downloads\\Photo10 (1).bmp','C:\\Users\\Chau\\Downloads\\Photo10.bmp'])