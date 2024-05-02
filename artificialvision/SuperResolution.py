import cv2

# Load the low resolution image
lr_image = cv2.imread("path_to_lr_image.jpg")

hr_image = cv2.resize(lr_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Save the high resolution image
cv2.imwrite("path_to_hr_image.jpg", hr_image)
