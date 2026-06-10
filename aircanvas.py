import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Arrays to handle color points of different colors
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Indexes
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

paintWindow = np.zeros((471, 636, 3), dtype=np.uint8) + 255

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Initializing mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

quit_flag = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    x, y, c = frame.shape

    # Flip frame horizontally (mirror)
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw UI buttons on frame
    frame = cv2.rectangle(frame, (20, 1),  (115, 65), (0, 0, 0),       2)
    frame = cv2.rectangle(frame, (130, 1), (225, 65), (255, 0, 0),     2)
    frame = cv2.rectangle(frame, (240, 1), (335, 65), (0, 255, 0),     2)
    frame = cv2.rectangle(frame, (350, 1), (445, 65), (0, 0, 255),     2)
    frame = cv2.rectangle(frame, (460, 1), (555, 65), (0, 255, 255),   2)
    frame = cv2.rectangle(frame, (570, 1), (620, 65), (128, 0, 128),   2)

    cv2.putText(frame, "CLEAR",  (37,  33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE",   (150, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN",  (260, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED",    (380, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (480, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "QUIT",   (580, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    result = hands.process(framergb)

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)
                landmarks.append([lmx, lmy])

            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])
        cv2.circle(frame, center, 3, (0, 255, 0), -1)

        if (thumb[1] - center[1] < 40):
            # Fingers pinched — lift pen
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        elif center[1] <= 65:
            if 20 <= center[0] <= 115:       # CLEAR
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                blue_index = green_index = red_index = yellow_index = 0
                paintWindow[:, :, :] = 255

            elif 570 <= center[0] <= 620:    # QUIT
                quit_flag = True

            elif 130 <= center[0] <= 225:    # BLUE
                colorIndex = 0
            elif 240 <= center[0] <= 335:    # GREEN
                colorIndex = 1
            elif 350 <= center[0] <= 445:    # RED
                colorIndex = 2
            elif 460 <= center[0] <= 555:    # YELLOW
                colorIndex = 3

        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    else:
        # No hand detected — lift pen
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw all strokes on both frame and paintWindow
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame,       points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if quit_flag or cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()