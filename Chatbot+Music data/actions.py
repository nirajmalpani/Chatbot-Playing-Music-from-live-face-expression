# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from twilio.rest import Client
import random
from tensorflow.keras.models import load_model
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import cv2
import numpy as np
from pygame import mixer
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
from scipy import misc
import imageio
from tensorflow import keras
import joblib
import numpy as np
class Song(Action):
     def name(self) -> Text:
         return "play_oldsong"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         conn = sqlite3.connect('data.db')
         emotion_dict={0:"Angry",1:"Happy",2:"Sad",3:"Shocking"}
         classifier=load_model("full_model.h5")

         image = imageio.imread("saved_img-final.jpg")
         resiz=resize(image, (1,48, 48,1))
         prediction=classifier.predict(resiz)
         maxindex = int(np.argmax(prediction))
         print(maxindex)
         mixer.init()
         tr= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Old Song' and MOOD is '{0}'".format(emotion_dict[maxindex])
         content = conn.execute(tr)
         song=content.fetchone()[0]
         mixer.music.load(r"{0}".format(song))

         mixer.music.set_volume(0.7)

# Start playing the song
         mixer.music.play()

         content_text="Enjoy your Music"
         dispatcher.utter_message(text=content_text)
         return []

class ActionClickPhoto(Action):
     def name(self) -> Text:
         return "action_click_photo"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        key=cv2.waitKey(1)
        cam=cv2.VideoCapture(0)
        print("read")
        try:
            ret, frame = cam.read() # prints true as long as the webcam is running
            print(frame)  # prints matrix values of each framecd
            cv2.imshow("Capturing", frame)
            print("passed")
            key = cv2.waitKey(1)
            cv2.imwrite(filename='saved_img.jpg,%Y-%b-%d_%H-%M-%S', img=frame)
            #print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

            # webcam.release()
            img_new = cv2.imread('saved_img.jpg,%Y-%b-%d_%H-%M-%S', cv2.IMREAD_GRAYSCALE)
            # cv2.imshow("Captured Image", img_new)
            # cv2.waitKey(1925)
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg,%Y-%b-%d_%H-%M-%S', cv2.IMREAD_ANYCOLOR)
            print("Converting RGB image to grayscale...")
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            print("Converted RGB image to grayscale...")
            print("Resizing image to 28x28 scale...")
            img_ = cv2.resize(gray, (28, 28))
            print("Resized...")
            img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            print("Image saved!")
            content_text="Image Successfully Captured"
            
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            camera.release()
            content_text="error in saving picture"
        dispatcher.utter_message(text=content_text)
        return []
class MusicOptions(Action):

    def name(self) -> Text:

        return "music_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = str((tracker.latest_message)['text']).lower()
        if user_message == 'p':
             mixer.music.pause()
             content_text="Song has been paused To resume write r or to stop write e"
             dispatcher.utter_message(text=content_text)
        elif user_message == 'r':
             mixer.music.unpause()
             content_text="Song has been Resumed To pause write p or to stop write e"
             dispatcher.utter_message(text=content_text)
        elif user_message == 'e':
             mixer.music.stop()
             content_text="Thanks for listening the music"
             dispatcher.utter_message(text=content_text)
        return []


class NewSong(Action):
     def name(self) -> Text:
         return "play_newsong"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         conn = sqlite3.connect('data.db')
         user_message = str((tracker.latest_message)['text'])
         emotion_dict={0:"Angry",1:"Happy",2:"Sad",3:"Shocking"}
         classifier=load_model("full_model.h5")

         image = imageio.imread("saved_img-final.jpg")
         resiz=resize(image, (1,48, 48,1))
         prediction=classifier.predict(resiz)
         maxindex = int(np.argmax(prediction))
         print(maxindex)

         if "Amit" in user_message:
             train= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Amit Trivedi' and MOOD is '{0}'".format(emotion_dict[maxindex])
         elif "Honey" in user_message:
             train= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Honey Singh' and MOOD is '{0}'".format(emotion_dict[maxindex])
         elif "Shreya" in user_message:
             train= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Shreya Goshal' and MOOD is '{0}'".format(emotion_dict[maxindex])
         elif "Neeti" in user_message:
             train= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Neeti Mohan' and MOOD is '{0}'".format(emotion_dict[maxindex])
         elif "Aayushman" in user_message:
             train= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Aayushman' and MOOD is '{0}'".format(emotion_dict[maxindex])
         elif "Vishal" in user_message:
             train= "SELECT LOCATION FROM 'Music - Sheet1' where ARTIST is 'Vishal Dadlani' and MOOD is '{0}'".format(emotion_dict[maxindex])
         mixer.init()
         content = conn.execute(train)
         song=content.fetchone()[0]
         mixer.music.load(r"{0}".format(song))

         mixer.music.set_volume(0.7)

# Start playing the song
         mixer.music.play()

         content_text="Enjoy your Music"
         dispatcher.utter_message(text=content_text)
         return []
