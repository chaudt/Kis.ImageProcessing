
import uvicorn
import io
import PIL.Image as Image
import os
from starlette.responses import StreamingResponse
import cv2
from transparent_background import Remover
import numpy as np
import time



class ImageProcessingForKis:
    def __init__(self) -> None:
        pass

    def remove_background(self, contents):
        # download from endpoint: https://drive.google.com/uc?id=13oBl5MTVcWER3YU4fSxW3ATlVfueFQPY
        print('-->remove background called: hello world')
        try:
            t1 = time.time()
            remover = Remover(device='gpu',ckpt='./latest.pth')
            t2 = time.time(); 
            print('step1')
            nparr = np.fromstring(contents, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            t3 = time.time()
            print('step2')
            #frame = cv2.imread(data)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            t4 = time.time()
            print('step3')
            image = Image.fromarray(frame).convert('RGB')
            out = remover.process(image)
            t5 = time.time()
            print('step4')
            #extract_folder = './data/transparent_bgs'
            #new_path_img = os.path.join(extract_folder,'test_tp_grba_01.png')
            #Image.fromarray(out).save(new_path_img)
            out_default = Image.fromarray(out).convert('RGB')
            
            out = remover.process(out_default, type='rgba')
            print('step4')
            t7 = time.time()
            img_rgba = Image.fromarray(out)#.save(new_path_img)
            imgio = io.BytesIO()
            img_rgba.save(imgio, 'PNG')
            imgio.seek(0)
            t8 = time.time()
            print('step5')
            return imgio
        except Exception as ex:
            print(f'-->remove-background servce is failure. Details:{ex}')
        finally:
            print(f'step 1: init Remover: {t2-t1} seconds')
            print(f'step 2: decode: {t3-t2} seconds')
            print(f'step 3: convert to CORLOR-BGR2RGB:{t4-t3} seconds')
            print(f'step 4: change bg with RGB:{t5-t4} seconds')
            print(f'step 5: change bg with RGBA:{t7-t5} seconds')
            print(f'step 6: convert img to byte-io:{t8-t7} seconds')
            print(f'total time processing:{t8-t1} seconds')


if __name__=='__main__':
    remover = Remover()
    cap = cv2.VideoCapture('C:\\Users\\Chau\\Downloads\\video.mp4') # video reader for input
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = None
    number = 0
    root_bg = 'E:\\CHAU\\SOURCE-GIT\\RemoveBackground\\bgs'
    backgrounds = os.listdir(root_bg)
    len_bg = len(backgrounds)
    number_checkbg = 0
    index = 0 # so luong frame dung background

    while cap.isOpened():
        try:
            ret, frame = cap.read() # read video

            if ret is False:
                break
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            img = Image.fromarray(frame).convert('RGB')

            if writer is None:
                writer = cv2.VideoWriter('output2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height)) # video writer for output
                writer1 = cv2.VideoWriter('output_changebg.mp4', cv2.VideoWriter_fourcc(*'mp4v'),fps, (width, height)) # video writer for output
                print('create file mp4')

            out = remover.process(img) # same as image, except for 'rgba' which is not for video.
            writer.write(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
            Image.fromarray(out).save(f'E:\\CHAU\\SOURCE-GIT\\RemoveBackground\\files\\frame-{number}.png')
            img = Image.fromarray(out).convert('RGB')
            out = remover.process(img, type='rgba')
            img = Image.fromarray(out).convert('RGB')

            if number <100:
                index = 0
            elif number <200:
                index = 1
            elif number < 300:
                index = 2
            elif number <500:
                index = 3
            elif number <600:
                index = 4
            elif number < 800:
                index = 5
            else:
                index = 6
            print('background image:',backgrounds[index])
            out = remover.process(img, type=os.path.join(root_bg,backgrounds[index]) )
            img = Image.fromarray(out).convert('RGB') 
            img.save(f'E:\\CHAU\\SOURCE-GIT\\RemoveBackground\\files\\cbg-{number}.png')
            #writer1.write(img)
            writer1.write(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
            number +=1
            print(f'write frame:{number}')
        except Exception as ex:
            print('-->exception: ',ex)
    cap.release()
    writer.release()
    writer1.release()
    print('-->finished')