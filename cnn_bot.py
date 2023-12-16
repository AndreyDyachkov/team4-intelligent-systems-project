import io

import numpy as np
from PIL import Image, ImageFilter
#from tensorflow.keras import backend
from tensorflow.keras.models import load_model


def imgProcessing(img_bytes):   #Processing images for loading in the CNN
  print('module imgProcessing is ok')
  #  data = []
  img_size = (256,256)
  #         filepath = os.path.join(path, file)
  #          img = cv2.imread(filepath, 0)
  img1 = Image.open(img_bytes).convert('L')  #open as GRAYSCALE
  img2 = img1.filter(ImageFilter.GaussianBlur(radius = 2)) #Apply Blur filter to reduce noise
  img3 = img2.resize(img_size)# resise images to size 256 
  print('измерения файла',np.array(img3).shape)
  #img1.save('img1.png', 'png')
  #img2.save('img2.png', 'png')
  img3.save('img3.png', 'png')
  X = [img3]
  #X.append(img3)
  print('измерения массива с файлом',np.array(X).shape)
  print('will try to reshape')
  X = np.array(X).reshape(-1, img_size[0], img_size[1], 1) # from to list to array; from 2D array to 3D array; 
  X = X / 255.0   # data normalization for CNN
  # y = np.array(y)
  print('измерения массива с файлом после решейпа',X.shape)
  print('array is ok')
  #return img1, img2,img3,
  #z=np.array(X).reshape()  
  return X #, imgOut

def getSummary():   #Get info about the CNN model
  new_model = load_model('Gauss1dense1epoch.h5') #. Check its architecture 
  new_model.summary()
  buf = io.StringIO()
  new_model.summary(print_fn=lambda x: buf.write(x + '\n'))
  summary_string = buf.getvalue()
  buf.close()
  print(summary_string)
  del new_model
  return summary_string

def callCNN(X): # processing user data to get predicton
  new_model = load_model('Gauss1dense1epoch.h5') #. Check its architecture 
  #new_model.summary()
  #!!!!about = getSummary(new_model)
  about:str = ''# type(new_model.summary())
  #print('Created model:', about)
  #single_image_batch = np.expand_dims(X, axis=0)
  y_pred = new_model.predict(X, verbose=0)
  
  confidence = y_pred[0] if y_pred[0] > 0.5 else 1 - y_pred[0]
  # good confidence > 0.8
  is_sick = y_pred[0] > 0.5
  # are_we_sure = confidence > 0.8
  # you might call the "confidence" "kpi"
  result = "PNEUMONIA" if is_sick else "NORMAL"
  result = f"Result of prediction: {result} ({y_pred[0]})"
  #backend.clear_session() #clear memory after useing cnn
  del new_model
  return result, about, confidence
   
  """ For CNN model with 2 output neurons
  #y_pred = new_model.predict(X, verbose=0)
  y_pred_bool = np.argmax(y_pred, axis=1) 
  y_pred_bool = np.argmax(y_pred, axis=1) #function returns the index of the max value of predictions to show a case number
  #print('prediction:', y_pred)
  print('!!!!!!!!!!!!!!!!!!!!!!!!!the result of prediction is:', int(y_pred_bool))
  classNumber = int(y_pred_bool)
  classes = ['NORMAL', 'PNEUMONIA']
  #result:str = "Result of prediction:"+str(classes[int(у_pred)])
  #print(result)
  #print("Result of prediction:", classes[classNumber])
  result:str = f"Result of prediction: {classes[classNumber]}"
  print(result)
  return  result, about
  """