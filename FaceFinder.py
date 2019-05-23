import dlib # face detection, face recognition
import cv2 # 영상처리
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

img_path = {
  'imjunhyuk':'Image/imjunhyuk.jpg'
}

descs = {
  'imjunhyuk':None
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

img_bgr = cv2.imread('Image/imjunhyuk.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

rects, shapes, _ = find_faces(img_rgb)
descriptors = encode_face(img_rgb, shapes)

fig, ax = plt.subplots(1, figsize=(20, 20))
ax.imshow(img_rgb)

for i, desc in enumerate(descriptors):
  found = False

  for name, saved_desc in descs.items():
    dist = np.linalg.norm([desc] - saved_desc, axis=1) # a, b 벡터 사이의 거리를 구함

    if dist < 0.6:
      found = True

      text = ax.text(rects[i][0][0], rects[i][0][1], name,
                     color='b', fontsize=20)
      text.set_path_effects([path_effects.Stroke(linewidth=10, foreground='white'), path_effects])
      rect = patches.Rectangle(rects[i][0],
                               rects[i][1][1] - rects[i][0][1],
                               rects[i][1][0] - rects[i][0][0],
                               linewidth=2, edgecolor='r', facecolor='none')
      ax.add_patch(rect)
      break

    if not found:
      ax.text(rects[i][0][0], rects[i][0][1], 'unknown',
              color='r', fontsize=20, fontweight='normal')
      rect = patches.Rectangle(rects[i][0],
                               rects[i][1][1] - rects[i][0][1],
                               rects[i][1][0] - rects[i][0][0],
                               linewidth=2, edgecolor='r', facecolor='none')
      ax.add_patch(rect)

plt.show()