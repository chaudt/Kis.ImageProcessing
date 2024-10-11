#from fastapi  import FastAPI, File, UploadFile
import uvicorn
#from rembg import remove
#import io
import PIL.Image as Image
import os


#path = "C:\\Users\\Chau\\Downloads\\change_bg\\Photo11.bmp"

# name,ext = os.path.splitext(path)
# image = Image.open(path)
# if ext!='.png':
#     print(' khong phai file png')
#     with io.BytesIO() as f:
#         image.save(f, format='PNG')
#         f.seek(0)
#         ima_png = Image.open(f)
#         ima_png.load()
#         image = ima_png
#         print('-->cap nhat stream png')
                
#             #image.save(file.filename)
#         img_rm = remove(image,
#     alpha_matting=True,
#     alpha_matting_foreground_threshold=240,#240
#     alpha_matting_background_threshold=0,#10
#     alpha_matting_erode_structure_size=10,#10
#     alpha_matting_base_size=1000,)


# #Image.open(path).save( os.path.join(DATA_PATH,f'{name}.png'))
# path = os.path.join(DATA_PATH,f'{name}_rmbg_240_0_10_1000.png')
# img_rm.save(path)

# BLUR = 21
# CANNY_THRESH_1 = 10
# CANNY_THRESH_2 = 200
# MASK_DILATE_ITER = 10
# MASK_ERODE_ITER = 10
# MASK_COLOR = (0.0,0.0,1.0) # In BGR format

def test_loop(path_png:str):
    root = 'C:\\Users\\Chau\\Downloads\\change_bg\\logs\\'
    image = Image.open(path_png)
    for erode_structure_size in range(500):
        for background_threshold in range(500):
            for foreground_threshold in range(500):
                try:
                    print(f'erode_structure_size={erode_structure_size},background_threshold={background_threshold},foreground_threshold={foreground_threshold}')
        #             img_rm = remove(image,
        # alpha_matting=True,
        # alpha_matting_foreground_threshold=foreground_threshold,#240
        # alpha_matting_background_threshold=background_threshold,#10
        # alpha_matting_erode_structure_size=erode_structure_size,#10
        # alpha_matting_base_size=1000,)

                    img_rm = remove(image,
        alpha_matting=True,
        alpha_matting_foreground_threshold=foreground_threshold,#240
        alpha_matting_background_threshold=background_threshold,#10
        alpha_matting_erode_structure_size=erode_structure_size,#10
        alpha_matting_base_size=1000,)
                    
                    name,ext = os.path.splitext(path_png)
                    print(f'-->root={root}')
                    full_path = os.path.join(root,f'{name}_rmbg_{foreground_threshold}_{background_threshold}_{erode_structure_size}_1000.png')
                    img_rm.save(full_path)
                    print(f'save success file={full_path}')
                except Exception as ex:
                    print(f'loi ex={ex}::erode_structure_size={erode_structure_size},background_threshold={background_threshold},foreground_threshold={foreground_threshold}')
                    


if __name__=='__main__':
    #test_loop('C:\\Users\\Chau\\Downloads\\change_bg\\Photo11.bmp')
    from pathlib import Path
    import os
    import shutil
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR)
    l = BASE_DIR / "chau"
    print('location:',l)