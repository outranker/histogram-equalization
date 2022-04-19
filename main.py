# import cv2
#
# image = cv2.imread("./image.webp")
#
# if image is None: raise Exception("no image")
# def back(*args):
#     pass
#
# cv2.imshow("screen", image)
# cv2.createButton("mybutton", back)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#
# import cv2
# import numpy as np
#



import numpy as np
import cv2
def draw_histo(hist, shape=(200, 256)):
    hist_img = np.full( shape, 255, np.uint8)
    cv2.normalize(hist, hist, 0, shape[0], cv2.NORM_MINMAX)
    gap = hist_img.shape[1]/hist.shape[0]             # 한 계급 너비

    for i, h in enumerate(hist):
        x = int(round(i * gap))                         # 막대 사각형 시작 x 좌표
        w = int(round(gap))
        roi = (x, 0, w, int(h))
        cv2.rectangle(hist_img, roi, 0, cv2.FILLED)
    return cv2.flip(hist_img, 0)                        # 영상 상하 뒤집기 후 반환


path = "./image2.jpeg"
img2 = cv2.imread(path)
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE) # 영상 읽기
if image is None: raise Exception("영상 파일 읽기 오류")

bins, ranges = [256], [0, 256]
hist = cv2.calcHist([image], [0], None, bins, ranges)    # 히스토그램 계산
print(hist)
# 히스토그램 누적합 계산
accum_hist = np.zeros(hist.shape[:2], np.float32)
accum_hist[0] = hist[0]
for i in range(1, hist.shape[0]):
    accum_hist[i] = accum_hist[i - 1] + hist[i]

accum_hist = (accum_hist / sum(hist)) * 255                 # 누적합의 정규화
dst1 = [[accum_hist[val] for val in row] for row in image] # 화소값 할당
dst1 = np.array(dst1, np.uint8)

# #numpy 함수 및 룩업 테이블 사용
accum_hist = np.cumsum(hist)                      # 누적합 계산
cv2.normalize(accum_hist, accum_hist, 0, 255, cv2.NORM_MINMAX)  # 정규화
dst1 = cv2.LUT(image, accum_hist.astype("uint8"))  #룩업 테이블로 화소값할당

dst2 = cv2.equalizeHist(image)                # OpenCV 히스토그램 평활화
hist1 = cv2.calcHist([dst1], [0], None, bins, ranges)   # 히스토그램 계산
hist2 = cv2.calcHist([dst2], [0], None, bins, ranges)   # 히스토그램 계산
hist_img = draw_histo(hist)
hist_img1 = draw_histo(hist1)
hist_img2 = draw_histo(hist2)

cv2.imshow("image", image);             cv2.imshow("hist_img", hist_img)
cv2.imshow("dst1_User", dst1);          cv2.imshow("User_hist", hist_img1)
cv2.imshow("dst2_OpenCV", dst2);        cv2.imshow("OpenCV_hist", hist_img2)
cv2.waitKey(0)

# ****************************************** BUTTON **************************************** #
# button dimensions (y1,y2,x1,x2)
button = [20,60,50,250]

# function that handles the mousclicks
def process_click(event, x, y,flags, params):
    # check if the click is within the dimensions of the button
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
            print('Clicked on Button!')


# create a window and attach a mousecallback and a trackbar
cv2.namedWindow('Control')
cv2.setMouseCallback('Control',process_click)

# create button image
control_image = np.zeros((80,300), np.uint8)
control_image[button[0]:button[1],button[2]:button[3]] = 180
cv2.putText(control_image, 'Button',(100,50),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)

#show 'control panel'
cv2.imshow('Control', control_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
