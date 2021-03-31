import tweepy
import secrets
import os, random
import sched, time
import glob
from datetime import datetime
from PIL import Image

# Authenticate and create Tweepy instance 
auth=tweepy.OAuthHandler(secrets.API_KEY, secrets.API_KEY_SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
bot=tweepy.API(auth)

# Setup timer to tweet every {frequency} seconds
frequency=180
s=sched.scheduler(time.time, time.sleep)

# Pick 4 random images from faces folder and call tweet function
def pickImages(sc):
    age = str(random.randint(20,65))
    gender = str(random.randint(0,1))
    owd = os.getcwd()
    os.chdir("C:\\Users\\maxei\\Code\\EverythingIsABubble\\faces")
    whiteImages = glob.glob(age+"_"+gender+"_0*")
    nonWhiteImages = glob.glob(age+"_"+gender+"_[1-3]*")
    os.chdir(owd)
    whitePicks = random.sample(whiteImages, 2)
    nonWhitePicks = random.sample(nonWhiteImages, 2)
    (imageName, imagePath) = generateStitchedImage(whitePicks[0], whitePicks[1], nonWhitePicks[0], nonWhitePicks[1])
    tweetImage(imageName, imagePath, age, int(gender), sc)

# Generate stitched image of 4 inputted images
def generateStitchedImage(i1, i2, i3, i4):
    basePath = "C:\\Users\\maxei\\Code\\EverythingIsABubble\\faces\\"
    fileName = i1[0:6]+"-"+i2[0:6]+"-"+i3[0:6]+"-"+i4[0:6]+".jpeg"
    image1 = Image.open(basePath+i1)
    image2 = Image.open(basePath+i2)
    image3 = Image.open(basePath+i3)
    image4 = Image.open(basePath+i4)
    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size
    final_width = max(width1, width2, width3, width4)
    final_height = height1 + height2 + height3 + height4
    generatedImage = Image.new('RGB', (final_width, final_height))
    generatedImage.paste(im=image1, box=(0,0))
    generatedImage.paste(im=image2, box=(0,height1))
    generatedImage.paste(im=image3, box=(0,height1+height2))
    generatedImage.paste(im=image4, box=(0,height1+height2+height3))
    generatedImagePath = "C:\\Users\\maxei\\Code\\EverythingIsABubble\\tweetable\\"+fileName
    generatedImage.save(generatedImagePath)
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    print("\nGenerated "+fileName+" at "+currentTime)
    return (fileName, generatedImagePath)

# Tweet generated image and report to console
def tweetImage(imageName, imagePath, age, gender, sc):
    genders = ["male", "female"]
    status = imageName + " - four " + genders[gender] + " " + age + "-year-olds."
    bot.update_with_media(imagePath, status)
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    print("Tweeted at "+currentTime+": "+status)
    s.enter(frequency, 1, pickImages, (sc,))

pickImages(s)
s.run()