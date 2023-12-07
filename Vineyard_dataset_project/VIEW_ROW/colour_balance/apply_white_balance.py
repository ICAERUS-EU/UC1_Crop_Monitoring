
import cv2 
import numpy as np
import matplotlib.pyplot as plt 
from skimage import img_as_ubyte


def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
 
    # checking for right mouse clicks    
    if event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)


# reading the image
img = cv2.cvtColor(cv2.imread('IMG_0133.tif', 1), cv2.COLOR_BGR2RGB)
img_res = cv2.resize(img, None, fx=0.5,fy=0.5)
#img_res_copy = img_res.copy()
print(img.shape)


'''
cv2.imshow('image', img)
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

'''
h_start, w_start, h_width, w_width = 857, 2077, 30, 30 #For lake.png 174, 502, 10, 10 
h_start, w_start, h_width, w_width = 285, 407, 10, 10
h_start, w_start, h_width, w_width = 590, 928, 10, 10


#image_patch = img_res_copy[h_start:h_start+h_width, 
#                    w_start:w_start+w_width]
image_patch = img[h_start:h_start+h_width, 
                    w_start:w_start+w_width]


image_normalized = img / np.max(image_patch)
image_balanced = image_normalized.clip(0,1)
image_balanced = (image_balanced*255).astype(np.uint8)
'''


img_mean = (img*1.0 / img.mean(axis=(0,1)))

'''
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                    sharex=True, sharey=True)
for aa in (ax1, ax2):
    aa.set_axis_off()


ax1.imshow(img)
ax1.set_title('Source')
ax2.imshow(img_mean)
ax2.set_title('balanced')
plt.tight_layout()
plt.show()'''


percentile_value = 99

print(img)


fig, ax = plt.subplots(1,2, figsize=(12,6))
for channel, color in enumerate('rgb'):
    channel_values = img[:,:,channel]
    value = np.percentile(channel_values, percentile_value)
    ax[0].step(np.arange(256), 
            np.bincount(channel_values.flatten(), 
            minlength=256)*1.0 / channel_values.size, 
            c=color)
    ax[0].set_xlim(0, 255)
    ax[0].axvline(value, ls='--', c=color)
    ax[0].text(value-70, .01+.012*channel, 
            "{}_max_value = {}".format(color, value), 
                weight='bold', fontsize=10)
    ax[0].set_xlabel('channel value')
    ax[0].set_ylabel('fraction of pixels');
    ax[0].set_title('Histogram of colors in RGB channels')    
    whitebalanced = img_as_ubyte((img*1.0 / np.percentile(img,percentile_value, axis=(0, 1))).clip(0, 1))
    ax[1].imshow(whitebalanced);
    ax[1].set_title('Whitebalanced Image')

plt.tight_layout()
plt.show()

'''
are_equal = np.array_equal(image_balanced, img)
print(image_balanced)
print(img)

if are_equal:
    print("All elements are equal.")
else:
    print("Not all elements are equal.")


cv2.imwrite("balanced_img_V1.png", image_balanced)

cv2.imshow('image', img)
cv2.imshow('image_balanced', image_balanced)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
