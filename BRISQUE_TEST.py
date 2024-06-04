import cv2 as cv

img = cv.imread("04_AI_Upscale/HR_upscaling_all/08_HAT-L/achau-02_right/bbox_23/achau-02_right_23_4.png")
grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blurScore = cv.Laplacian(grey, cv.CV_64F).var()
score = cv.quality.QualityBRISQUE_compute(img, "tt/brisque_model_live.yml", "tt/brisque_range_live.yml")

print(f' >> Blur Score: {blurScore}')
print(f' >> BRISQUE Score: {score}')

cv.namedWindow("Output", cv.WINDOW_NORMAL)
cv.imshow("Output", img)
k = cv.waitKey(0)

