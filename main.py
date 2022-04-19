import numpy as np, cv2


# avval pastroqda ishlatadigan functionlarimizni ifodalab olamiz
# quyida 2ta funktion bor ularni biz pastroqda ishlatamiz
# birinchi functionni(process_click) biz boshqa funtionga argument sifatida bervoramiz
# u function bizni functionga turli xil argumentlarni beradi, biz buni oldindan bilishimiz
# va ularni ishlata olishimiz kerak. Aniqroq qilib aytadigan bo'lsak, aynan process_
# click nomli funtionni biz opencv-pythondan
# import qilib olib kelingan cv2 nomli packagedagi setMouseCallback nomli
# funtionni ishlatayotganda unga ikkinchi function argument
# sifatida pass qilamiz. birinchi argument esa window nomi bo'ladi. biz
# o'sha 2-argument qilib berib yuborgan funtionni, setMouseCallback
# funtioni qabul qilib oladi va o'z ichida qayerdadir chaqiradi.
# chaqirayotganda esa u o'zi ham turli xil argumentlarni pass qiladi.
# biz usha argumentlardan foydalanib o'zimizga kerka bo'lgan narsani
# qilishimiz kerak. u argumentlar: event, x, y, flags va params.
# biz bularni cv2 ni documentationslaridan ko'rib bilib olishimiz kerak


# 2-ifodalangan funtionimiz esa draw_histo funtioni
button = [100, 100, 250, 150]

# function that handles the mousclicks
def process_click(event, x, y, flags, params):
    # check if the click is within the dimensions of the button
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
            print('Clicked on Button!')


def draw_histo(hist, shape=(200, 475)):
    hist_img = np.full(shape, 255, np.uint8)
    cv2.normalize(hist, hist, 0, shape[0], cv2.NORM_MINMAX)
    gap = hist_img.shape[1] / hist.shape[0]  # 한 계급 너비

    for i, h in enumerate(hist):
        x = int(round(i * gap))  # 막대 사각형 시작 x 좌표
        w = int(round(gap))
        roi = (x, 0, w, int(h))
        cv2.rectangle(hist_img, roi, 0, cv2.FILLED)

    return cv2.flip(hist_img, 0)  # 영상 상하 뒤집기 후 반환


# image ni imread functioni orqali o'qiymiz
# va image variablega saqlab olamiz
# biz har qanday variableni print qilish imkoniyatiga
# egamiz! hattoki functionlarni ham
# TODO: function va variablelarni print qilib ko'ring!!!

image = cv2.imread("image2.jpeg", cv2.IMREAD_GRAYSCALE)

# agar yuqoridagi saqlab olish muvaffaqiyatli
# amalga oshmasa Exceptionni raise qilamiz
if image is None:
    raise Exception("영상 파일 읽기 오류")

hist = cv2.calcHist([image], [0], None, [32], [0, 256])
hist_img = draw_histo(hist)

# cv2.imshow("image", image)
# cv2.imshow("hist_img", hist_img)
# cv2.waitKey(0)

# ****************************************** BUTTON **************************************** #
# button dimensions (y1,y2,x1,x2)
button = [100, 100, 250, 150]
# create a window and attach a mouse-callback
cv2.namedWindow('hist_img')
cv2.setMouseCallback('hist_img', process_click)

# create button image
control_image = np.zeros((80, 300), np.uint8)
hist_img[button[0]:button[1], button[2]:button[3]] = 180
cv2.putText(hist_img, 'save', (400, 20), cv2.FONT_HERSHEY_PLAIN, 2, (128,128,0), 3,)

# cv2.imshow("image", image)
cv2.imshow("hist_img", hist_img)
# cv2.waitKey(0)


# show 'control panel'
cv2.imshow('button-window', control_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# **************************************************************************************
