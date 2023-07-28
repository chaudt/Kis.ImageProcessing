from fastapi  import FastAPI, File, UploadFile,HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery

import uvicorn
import io
import PIL.Image as Image
import os
from starlette.responses import StreamingResponse
import cv2
from transparent_background import Remover
import numpy as np
import time
DATA_PATH = os.environ.get('DATA_PATH', 'data')

API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


app = FastAPI()


class ImageProcessingForKis:
    def __init__(self) -> None:
        pass

    def remove_background(self, contents):
        # download from endpoint: https://drive.google.com/uc?id=13oBl5MTVcWER3YU4fSxW3ATlVfueFQPY
        print('-->remove background called: hello world')
        try:
            t1 = time.time()
            remover = Remover(device='cpu',ckpt='./latest.pth')
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

@app.get("/api/removebackgrounds/")
def hello():
    return "Remove background hello world"

@app.post("/api/removebackgrounds/")
def remove_background(image_file: UploadFile = File(...),api_key: str = Security(get_api_key)):
    print('root current:',DATA_PATH)
    
    if not image_file:
        return {'message':"No upload file sent"}
    else:
        print('filename=',os.path.join(DATA_PATH,image_file.filename))
        
        try:
            contents = image_file.file.read()
            
            # save image to bytes
            kis = ImageProcessingForKis()
            imgio = kis.remove_background(contents)
            return StreamingResponse(content=imgio, media_type="image/png")
        except Exception as ex:
            print(f'Có lỗi trong quá trình xử lý:{ex}')
            return {"message": f"There was an error uploading the file: Details={ex}"}
   

if __name__=='__main__':
    print('remove backgound service - new version')

    uvicorn.run(app, host="0.0.0.0", port=3001)
    #uvicorn.run(app, host="127.0.0.1", port=8001)