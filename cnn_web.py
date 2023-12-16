from PIL import Image, ImageFilter
import numpy as np


def imgProcessing(img_bytes):  #Processing images for loading in the CNN
  print('module imgProcessing is ok')

  #  data = []
  img_size = (256, 256)
  #         filepath = os.path.join(path, file)
  #          img = cv2.imread(filepath, 0)
  img1 = Image.open(img_bytes)
  img2 = img1.filter(ImageFilter.GaussianBlur(radius=5))
  img3 = img2.resize(img_size)  # resise images to size 256
  #img1.save('img1.png', 'png')
  #img2.save('img2.png', 'png')
  #img3.save('img3.png', 'png')
  X = []
  #y = []
  X.append(img3)
  print('will try to reshape')
  X = np.array(X).reshape(
      -1, img_size[0], img_size[1],
      1)  # from to list to array; from 2D array to 3D array;
  X = X / 255.0  # data normalization for CNN
  #y = np.array(y)
  print('array is ok')
  #return img1, img2,img3,
  #z = np.array(X).reshape()

  return X


from tensorflow.keras.models import load_model


def createCNN(X):  #
  print('module imgProcessing is ok')
  new_model = load_model('Gauss2dense3epoch.h5')  #. Check its architecture
  new_model.summary()
  y_pred = new_model.predict(X, verbose=0)
  y_pred_bool = np.argmax(y_pred, axis=1)
  y_pred_bool = np.argmax(
      y_pred, axis=1
  )  #function returns the index of the max value of predictions to show a case number
  print('prediction:', y_pred)
  print('!!!!!!!!!!!!!!!!!!!!!!!!!the result of prediction is:', y_pred_bool)
  return y_pred_bool
