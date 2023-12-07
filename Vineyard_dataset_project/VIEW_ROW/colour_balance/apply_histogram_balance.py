import matplotlib.pyplot as plt

from skimage import data
from skimage import exposure
from skimage.exposure import match_histograms
import cv2 



reference =  cv2.cvtColor(cv2.imread('balanced_img_V1.png'), cv2.COLOR_BGR2RGB)
#reference = cv2.resize(reference, (1255, 945))
image = cv2.cvtColor(cv2.imread('IMG_0030.tif'), cv2.COLOR_BGR2RGB)
#image = cv2.cvtColor(cv2.imread('original_image.JPG'), cv2.COLOR_BGR2RGB)


print(image.shape)
print(reference.shape)

matched = match_histograms(image, reference, channel_axis=-1)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)
for aa in (ax1, ax2, ax3):
    aa.set_axis_off()

ax1.imshow(image)
ax1.set_title('Source')
ax2.imshow(reference)
ax2.set_title('Reference')
ax3.imshow(matched)
ax3.set_title('Matched')

plt.tight_layout()
plt.show()