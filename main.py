from fastapi  import FastAPI, File, UploadFile,HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery

import uvicorn
from rembg import remove
import io
import PIL.Image as Image
import os
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse
import cv2
import uuid
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


class ReadFileOperation:
    def get_data_from_file(file_path: str):
        with open(file=file_path, mode="rb") as file_like:
            yield file_like.read()

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
            name,ext = os.path.splitext(image_file.filename)
            print(f'name:{name} ext:{ext}')

            contents = image_file.file.read()
            image = Image.open(io.BytesIO(contents))
            if ext!='.png':
                print(' khong phai file png')
                with io.BytesIO() as f:
                    image.save(f, format='PNG')
                    f.seek(0)
                    ima_png = Image.open(f)
                    ima_png.load()
                    image = ima_png
                    print('-->cap nhat stream png')
                
            #image.save(file.filename)
            img_rm = remove(image)
            print('-->remove background ok')
            if not os.path.exists(DATA_PATH):
                print('-->duong dẫn khong ton tai')
                os.makedirs(DATA_PATH)
                print('-->make dir ok')
            path = os.path.join(DATA_PATH,f'{name}.png')
            img_rm.save(path)
            print('-->save image ok')
            image_file.file.close()
            print(f'current path ====:{path}')
            
            
            # img = Image.open(path).convert('RGBA')
            # img.save("data/file.png")
            img_rgba = Image.open(path).convert('RGBA')
            # save image to bytes
            imgio = io.BytesIO()
            img_rgba.save(imgio, 'PNG')
            imgio.seek(0)
            #img_rgba.save(path)
            return StreamingResponse(content=imgio, media_type="image/png")
            # path_res = os.path.join(DATA_PATH,f'{uuid.uuid4()}.png')
            # print('-->path-result:',path_res)
            # img_rgba.save(path_res)
            # print('convert 2 grba ok')

            # cv2img = cv2.imread(path_res)
            # print('-->cv2img read file: ',path_res)
            # cv2.imwrite('test.png',cv2img)
            # res, im_png = cv2.imencode(".png", cv2img)
            # return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
        except Exception as ex:
            print(f'Có lỗi trong quá trình xử lý-1:{ex}')
            return {"message": f"There was an error uploading the file: Details={ex}"}
        #finally:
        #    file.file.close()

        #return {"message": f"Successfully uploaded {os.path.join(DATA_PATH,file.filename)}"}
        #return StreamingResponse(content=image_stream, media_type="image/png")
   

if __name__=='__main__':
    print('remove backgound service - version 23.7.4.11.38')

    #uvicorn.run(app, host="0.0.0.0", port=3001)
    uvicorn.run(app, host="127.0.0.1", port=8001)