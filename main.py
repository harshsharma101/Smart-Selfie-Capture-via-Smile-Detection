import cv2
import uuid
import time

face_cascade = cv2.CascadeClassifier('D:\SEM 6th\FDIP Lab\Mini Project\smart selfie\dataset\haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('D:\SEM 6th\FDIP Lab\Mini Project\smart selfie\dataset\haarcascade_smile.xml')

cap = cv2.VideoCapture(0)
count = 0 # Initialize image counter

while True:
    ret, frame = cap.read()
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Iterate through each face and detect smiles
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect smiles within the face region
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22, minSize=(155, 155))
        
        # Iterate through each smile and capture an image
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
            cv2.putText(roi_color, 'Smiling', (sx, sy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Check if maximum image count is reached
            if count < 5:
                filename = str(uuid.uuid1()) + '.jpg' # Generate a unique filename based on timestamp
                cv2.imwrite(filename, frame)
                print('Image captured:', filename)
                count += 1
            else:
                print('Maximum image count reached')
    
    # Display the frame
    cv2.imshow('Smile Detector', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
