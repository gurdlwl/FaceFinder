import dlib # face detection, face recognition
import cv2 # 영상처리
import numpy as np

img_path = {
  'Yu' : 'Images/Yu.jpg'
}

descs = {
  'Yu' : 'NONE'
}

detector = dlib.get_frontal_face_detector()
shapePredic = dlib.shape_predictor('Models/shape_predictor_68_face_landmarks.dat')
faceRecog = dlib.face_recognition_model_v1('Models/dlib_face_recognition_resnet_model_v1.dat')

# 얼굴 찾는 함수
def find_faces(img):
  dets = detector(img, 1)

  if len(dets) == 0:
    return np.empty(0), np.empty(0), np.empty(0)

  rects, shapes = [], []
  shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)

  for k, d in enumerate(dets):
    rect = ((d.left(), d.top()), (d.right(), d.bottom()))
    rects.append(rect)

    shape = shapePredic(img, d)

    for i in range(0, 68):
      shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)
    shapes.append(shape)

  return rects, shapes, shapes_np

# 얼굴 인코딩 하는 함수
def encode_face(img, shapes):
  face_descriptors = []
  for shape in shapes:
    face_descriptor = faceRecog.compute_face_descriptor(img, shape)
    face_descriptors.append(np.array(face_descriptor))

  return np.array(face_descriptors)

for name, img_path in img_path.items():
  img_bgr = cv2.imread(img_path)
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
  _,img_shapes,_ = find_faces(img_rgb)
  descs[name] = encode_face(img_rgb, img_shapes)[0]

np.save('Result/descs.npy', descs)
print(descs)