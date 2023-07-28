# https://github.com/serengil/deepface
# pip install deepface
from deepface import DeepFace
import cv2
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]


# #face verification
# result = DeepFace.verify(img1_path = "img1.jpg", 
#       img2_path = "img2.jpg", 
#       model_name = models[0]
# )

# #face recognition
# dfs = DeepFace.find(img_path = "img1.jpg",
#       db_path = "C:/workspace/my_db", 
#       model_name = models[1]
# )

# #embeddings
# embedding_objs = DeepFace.represent(img_path = "img.jpg", 
#       model_name = models[2]
# )
image_path = 'C:\\Users\\Chau\\Downloads\\20230721_210845.jpg'

objs = DeepFace.analyze(img_path = image_path, 
        actions = ['age', 'gender', 'race', 'emotion']
)

print(objs)
img = cv2.imread(image_path)
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# fontScale
fontScale = 1
for item in objs:
    start_point = (item['region']['x'],item['region']['y'])
    end_point = (item['region']['x']+item['region']['w'], item['region']['y']+item['region']['h'])
    img = cv2.rectangle(img, start_point, end_point, color, thickness)
    
    img = cv2.putText(img, f'{item["age"]}t', start_point, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    
cv2.imwrite('export.jpg',img)

