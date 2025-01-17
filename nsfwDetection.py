import discord
import os
import predict
import urllib
from io import BytesIO
from PIL import Image
import requests
from dotenv import load_dotenv
import numpy as np
from keras.preprocessing import image

load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  activity = discord.Game(name="watching y'all")
  status = discord.Status.online

@client.event
async def on_message(message):
  print(message.attachments)
  try:
    for attachment in message.attachments:
      print(attachment.url)

      response = requests.get(attachment.url)
      images = Image.open(BytesIO(response.content))
      test_image = images.resize((64,64))
      test_image = image.img_to_array(test_image)
      test_image = np.expand_dims(test_image, axis = 0)
      CNN = predict.newCNN()
      checkpoint_path = "training_2/cp.ckpt"
      checkpoint_dir = os.path.dirname(checkpoint_path)
      CNN.load_weights(checkpoint_path).expect_partial()
      result = CNN.predict(test_image)
      if result[0][0] == 1:
          prediction = 'sfw'
          print('sfw')
      else:
          prediction = 'nsfw'
          print('nsfw')

      if prediction == 'nsfw':
        await message.delete()
        break
  except IndexError:
    pass


client.run(TOKEN)
