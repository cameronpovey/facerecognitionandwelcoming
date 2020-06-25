import cv2
import time
import face_recognition
import shutil
import pyttsx3
import os.path
from datetime import datetime

true = True
engine = pyttsx3.init()
dir = os.listdir('pics/known')
num_people = len(dir)
number = 0
t=time.localtime()



# add people here:
person = ["Person 1", "Person 2"]
# then add picture which are known pics/known/(name).jpg
# then add folder pics/people/(name)

def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.imwrite('pics/captures/capture.jpg', frame) #Tempory folder
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    true = False


# speech module
engine.say("Program starting.")
engine.runAndWait()

# establish how many people are being search for
print(num_people, " people in database.")

while true == True:
    TakeSnapshotAndSave()

    image = face_recognition.load_image_file("pics/captures/capture.jpg")
    face_num = face_recognition.face_locations(image)
    faces = len(face_num)
    # check how many faces are in the capture

    if faces == 1:
        count = -1
        unknown_image = face_recognition.load_image_file("pics/captures/capture.jpg")
        un_en = face_recognition.face_encodings(unknown_image)[0]
        # set unknown face and encode set for comparison with known faces

        for i in range(num_people):
            count = count + 1
            known = face_recognition.load_image_file("pics/known/" + person[count] + ".jpg")
            # load known images for face_rec depending on count in the (person[array])

            encode = face_recognition.face_encodings(known)[0]
            rec = face_recognition.compare_faces([encode], un_en)
            # encode and compare to face capture

            if rec == [True]:
                # if face is found welcome and move
                os.system('clear')
                save_dir = os.listdir('pics/people/' + person[count])
                num_pics = len(save_dir) + 1
                print("Found: ", person[count])
                shutil.move("pics/captures/capture.jpg", "pics/people/" + person[count] + "/pic" + str(num_pics) + ".jpg")
                found = person[count]
                engine.say('Welcome ' + found)
                engine.say("Today's date is")

                now = datetime.now()  # get the current date and time
                engine.say(now.strftime("%A."))  # day
                engine.say(now.strftime("%B."))  # month
                engine.say(now.strftime("%d."))  # day (num)
                engine.say(now.strftime("%Y."))  # year
                engine.runAndWait()

                time.sleep(60*5)
                break
                # save found image with the name of the person (person[array]) and named pic(number of pics in dir +1)

            # if no faces found and if count is equal to the amount of people -1 (arrays start at 0)
            elif rec == [False] and count == (num_people - 1):
                save_dir = os.listdir('pics/unknown')
                num_pics = len(save_dir) + 1
                shutil.move("pics/captures/capture.jpg", "pics/unknown/capture" + str(num_pics) + ".jpg")
                break
                # move the unknown picture to a different dir then; name(num of pics in file + 1).jpg

    elif faces > 2:
        os.system('clear')
        print("Too many faces in frame.")
        print(faces, "found")

    else:
        os.system('clear')
        print("no faces found.")
