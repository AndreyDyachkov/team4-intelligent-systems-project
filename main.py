import os
from io import BytesIO

import requests
from PIL import Image
from replit import db
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from background import keep_alive
from cnn import callCNN, imgProcessing, getSummary
from knowledgeBase import perform_sparql_query

print("Script is starting...")
sparqlQuery: str = ''

async def start(update: Update, context):  #user pushed start button in menu
  user = update.effective_user
  if update.message:
    await update.message.reply_html(
        rf"Hi,  {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
  else:
    print("start(): update.message is None")
  await update.message.reply_text(
      "You can send your medical image of lungs to check it for diseases by our neural network."
  )

async def help_command(update: Update, context):  # send help message
  await update.message.reply_text(
    '''The output of this Convolutional neural network model represents the predicted probability for Pneumonia.\n 
    You can send your X-ray image of lungs to this telegram bot to predict the disease by the CNN. Then you get a reply with the result (NORMAL or PNEUMONIA) and estimation of cogency of the result.\n
The difference between the output of a sigmoid activation function in a binary classification model and the KPI can be referred to as the error or deviation. It represents the discrepancy or distance between the predicted probability for the positive class and the desired KPI value of 80%.''')

async def cnnInfo_command(update: Update, context):  # send info about CNN model
  inf = getSummary()
  await update.message.reply_text(inf )
    
def sendQuery():  # send prepared SPARQL-request  to the knowledgebase
  sparqlQueryAccuracy = """
  SELECT ?label ?threshold
  WHERE {ind:kpi3 rdfs:label ?label . 
  ind:kpi3 prop:hasMin ?threshold .}"""
  result = perform_sparql_query(sparqlQueryAccuracy)
  return result


async def accuracy_command(update: Update,context):  #Send query to tha knowledgebase
  print('accuracy command was recived')
  await update.message.reply_text(
      "A SPARKL query was sent  to get the Accuracy Score")
  result = sendQuery()
  await update.message.reply_text("The answer from the knowledgebase is: <<" +
                                  str(result) + ">>")

def accCheck(confidence: float):  # check if confidence is high enough
  '''The difference between the output value and the KPI can be referred to as the error or deviation. It represents the discrepancy or distance between the predicted probability for the positive class and the desired KPI value of 0.8.'''
  checkRes = ''
  currentAcc: int = confidence * 100
  treshold = sendQuery()
  intAcc = int(treshold['Accuracy score'])
  print('Value of treshold of confidense is:', treshold['Accuracy score'])
  print('Current CNN Model predicted value is:', currentAcc)
  if intAcc < currentAcc:
    checkRes = f'Note. The treshold {intAcc} is less than the current accuracy (cogency) {currentAcc}. The score of prediction by a sent photo is high'
    print(checkRes)
  else:
    checkRes = f'Attention! The treshold {intAcc} is more than the current accuracy (cogency) {currentAcc}!. The score of prediction by a sent photo is low!'
    print(checkRes)
  return checkRes

async def get_file(update, context: ContextTypes.DEFAULT_TYPE):
  print("Test - get_file()")
  #file = update.message.document.file_id
  #file_name = update.message.document.file_name
  #new_file = await context.bot.get_file(file)
  #new_file.download(file_name)
  #print("the file was recieved from telegram")

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):  #recivce photo from user
  print("def get_photo()")
  #print(update.message.photo)
  user_message = update.message.photo
  foto1 = await user_message[2].get_file(
  )  #the api send a massiv of the image with different resolution

  await update.message.reply_text("The file was got.") #processing of user messages
  print("\nPhoto file is:")
  file_url = foto1.file_path
  response = requests.get(file_url)  
  if response.status_code == 200:# Check if the request was successful
    file_bytes = response.content
    print(f"{len(file_bytes)} bytes are read")
    # TODO: this var (file_bytes) holds the bytes
    # of the user's message. These bytes are supposed to be sent
    # to the neural network
    # print_photo(file_bytes)
    image_bytes = BytesIO(file_bytes)  #reading the image bytes
    # with Image.open(image_bytes) as img:
    img = Image.open(image_bytes)
    width, height = img.size
    print(f"Width: {width}, Height: {height}")  #otput resolution of the image
    # Get dimensions
    #width, height = img.size
    print(f"Image size: {img.size}")
    #img.save('x-photo.png', 'png')
    #print("the photo was saved")
    #photo = open('x-photo.png', 'rb')
    # await update.message.reply_photo(photo=open('x-photo.png', 'rb')) #resend the image to user
    #await update.message.reply_text("Here is the recived photo for lungs diseases checking")
    await update.message.reply_text("Resolution of your file is " +
                                    str(width) + "x" + str(height))
    # await update.message.reply_text(file_url)
    # print("x-photo was sent in reply")
    #img1, img2,img3,
    X = imgProcessing(image_bytes)  #preparing  image for cnn
    print("Your image was processed for CNN")
    #photo = open('x-photo.png', 'rb')
    await update.message.reply_photo(photo=open('img3.png', 'rb'))
    await update.message.reply_text(
        "Here is the recived photo after processing for lungs diseases checking"
    )
    #pic = Image.open(imgOut)
    #await update.message.reply_photo(photo=open('img1.png', 'rb'))
    #await update.message.reply_photo(photo=open('img3.png', 'rb'))
    print('will try to get in module CNN')
    y, about, confidence = callCNN(X)  # loading CNN from the file
    #!!!!!!!print('about the CNN model:', about)  #output CNN model info to user
    #!!!!await update.message.reply_text(about)
    print(f"from function: {y}")
    await update.message.reply_text(f'The answer from CNN was got. {y}.')
    checkRes = accCheck(
        confidence)  # send comparacy of the accuracy and threshold to user
    await update.message.reply_text(checkRes)
  else:
    print(f"Response status: {response.status_code}")

def print_photo(file_bytes):    #send user`s image back
  print("print_photo was called")
  #img = Image.open(file_bytes)только для файла
  imgSize = 1
  img = Image.fromstring('L', imgSize, file_bytes, 'raw', 'F;16')
  print("file_bytes was delivered")
  img.save('x-photo.png', 'png')
  print("the photo was saved")
  photo = open('x-photo.png', 'rb')
  update.message.reply_photo(photo=photo)
  print("x-photo was sent in reply")

def send_photo_file(chat_id, img):
  files = {'photo': open(img, 'rb')}
  requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}', files=files)

async def echo(update: Update, context):  #send user`s text back 
  await update.message.reply_text(update.message.text + " It is a wrong command!")

async def check_message(update: Update, context): # handling cases of user text messages
  print("def check_message()")
  user_message = update.message.text
  if user_message.lower() in ['привет', 'hello', 'hi']:
    await update.message.reply_text("Welcome!")
  elif user_message.lower() in ['фото', 'photo', 'foto']:
    await update.message.reply_text("Please send an image to check.")
  else:
    if 'SPARQL:' in user_message: # if there is the prefix SPARQL then make the query for request 
      await update.message.reply_text("SPARQL is detected in the message.")
      sparqlQuery2 = user_message[
          7:]  # Extract the SPARQL query from the request
      await update.message.reply_text("You have sent <<" + sparqlQuery2 +
                                      ">> query to the knowledgebase ")
      result = perform_sparql_query(sparqlQuery2)
      await update.message.reply_text("The answer is: <<" + str(result) + ">>")
    else:
      await update.message.reply_text(
          "The command <<" + update.message.text +
          ">> is wrong. Please, send a medical image of lungs to check for diseases"
      )
def doc_hook(update, context):# if user sent another file
  try:
    print("_msg_hook(): Document")
  except Exception as e:
    print(f"Error: {e}")

def main():
  my_bot_token = os.environ['TOKEN']
  # Create the Application and pass it your bot's token.
  application = Application.builder().token(my_bot_token).build()
  # on different commands - answer in Telegram
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(CommandHandler("kpi", accuracy_command))
  application.add_handler(CommandHandler("cnn", cnnInfo_command))
  # on non command i.e message - echo the message on Telegram
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))  #echo))stylize))
  application.add_handler(MessageHandler(filters.PHOTO, get_photo))
  #application.add_handler(MessageHandler(filters.Document, get_file))
  application.add_handler(MessageHandler(filters.Document, doc_hook))
  # Run the bot until the user presses Ctrl-C
  keep_alive()  #keep bot service alive by Flask web server  application.run_polling(allowed_updates=Update.ALL_TYPES)  #listening telegram
  application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
  main()
