import cv2
import numpy as np

def make_coordinates(image,line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])
def average_slop_intercept(image,lines):
    left_fit = []
    right_fit = []
    left_line = np.array([293,720,473,432])
    right_line = np.array([])
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slop = parameters[0]
        interccept = parameters[1]
        if slop < 0:
            try:
                slop,interccept = parameters
            except TypeError:
                slop,interccept = 0.001, 0
            left_fit.append((slop,interccept))
        else:
            right_fit.append((slop,interccept))
    if left_fit :
        left_fit_avarage = np.average(left_fit, axis=0)
        left_line = make_coordinates(image, left_fit_avarage)
    if right_fit:
        right_fit_avarage = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_avarage)
    return np.array([left_line,right_line])

def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    cany = cv2.Canny(blur,50,150)
    return cany

def area_of_interest(image):
    height = image.shape[0]
    polygon = np.array([
        [(200,height), (1100,height), (550,250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygon,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

def dis_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),8)
    return line_image


image = cv2.imread('D:/INTERN/Task1/test_image.jpg')
lane_image = np.copy(image)
cany = canny(lane_image)
cropped = area_of_interest(cany)
lines = cv2.HoughLinesP(cropped,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
averaged_lines = average_slop_intercept(lane_image,lines)
lined_image = dis_lines(lane_image,averaged_lines)
combo_image = cv2.addWeighted(lane_image,0.8,lined_image,1,1)
cv2.imshow('result',combo_image)
cv2.waitKey(0)

cap = cv2.VideoCapture("D:/INTERN/Task1/test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    cany = canny(frame)# Apply Canny edge detection
    cropped = area_of_interest(cany)
    lines = cv2.HoughLinesP(cropped, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slop_intercept(frame, lines)
    lined_image = dis_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, lined_image, 1, 1)
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
