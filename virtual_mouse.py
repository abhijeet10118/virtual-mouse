
import cv2
import mediapipe as mp
import pyautogui
import math
import time


pyautogui.FAILSAFE = False

SMOOTHING = 0.2          # cursor smoothness (0.1–0.3)
LEFT_CLICK_DIST = 40     # index + thumb
RIGHT_CLICK_DIST = 30   # middle + thumb
DOWN_CLICK_DIST = 30
UP_CLICK_DIST = 30
CLICK_DELAY = 0.8        # seconds


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not accessible")
    exit()

mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

prev_x, prev_y = 0, 0
last_left_click = 0
last_right_click = 0
last_down_click=0
last_up_click=0


while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand_detector.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            drawing_utils.draw_landmarks(frame, hand)
            lm = hand.landmark

           
            ix, iy = int(lm[8].x * w), int(lm[8].y * h)     # index tip
            mx, my = int(lm[12].x * w), int(lm[12].y * h)   # middle tip
            tx, ty = int(lm[4].x * w), int(lm[4].y * h)     # thumb tip
            rx, ry = int(lm[16].x * w), int(lm[16].y*h)  # ring finger
            px, py = int(lm[20].x * w), int(lm[20].y*h)  # pinky finger

           
            target_x = screen_width * ix / w
            target_y = screen_height * iy / h

            raw_index_x = target_x
            raw_index_y = target_y
            curr_x = prev_x + (target_x - prev_x) * SMOOTHING
            curr_y = prev_y + (target_y - prev_y) * SMOOTHING

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            
            thumb_x = screen_width * tx / w
            thumb_y = screen_height * ty / h
            middle_x = screen_width * mx / w
            middle_y = screen_height * my / h
            ring_x = screen_width * rx / w
            ring_y = screen_height * ry / h
            pinky_x=screen_width * px / w
            pinky_y=screen_height * py / h

         
            index_thumb_dist = math.hypot(raw_index_x - thumb_x,
                                          raw_index_y - thumb_y)

            middle_thumb_dist = math.hypot(middle_x - thumb_x,
                                           middle_y - thumb_y)
            
            ring_thumb_dist = math.hypot(ring_x - thumb_x,
                                           ring_y - thumb_y)
            
            pinky_thumb_dist = math.hypot(pinky_x - thumb_x,
                                           pinky_y - thumb_y)

            now = time.time()

           
            if index_thumb_dist < LEFT_CLICK_DIST and now - last_left_click > CLICK_DELAY:
                pyautogui.click()
                last_left_click = now

       
            if middle_thumb_dist < RIGHT_CLICK_DIST and now - last_right_click > CLICK_DELAY:
                pyautogui.rightClick()
                last_right_click = now
                
            
            if ring_thumb_dist < DOWN_CLICK_DIST and now - last_down_click > CLICK_DELAY:
                pyautogui.press('down')
                last_down_click = now
                
          
            if pinky_thumb_dist < UP_CLICK_DIST and now - last_up_click > CLICK_DELAY:
                pyautogui.press('up')
                last_up_click = now
            
            cv2.putText(frame, f"L:{int(index_thumb_dist)} R:{int(middle_thumb_dist)}",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
