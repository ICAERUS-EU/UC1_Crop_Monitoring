    
# import the necessary packages
import numpy as np
import cv2


HISTMATCH_EPSILON = 1e-6

# Compute histogram and CDF for an image with mask
def do1ChnHist(img, mask):
    h = np.zeros((1, 256), dtype=np.float64)
    cdf = np.zeros((1, 256), dtype=np.float64)

    for p in range(img.size):
        if mask.flat[p] > 0:
            c = img.flat[p]
            h[0, c] += 1.0

    h = cv2.normalize(h, None, 1, 0, cv2.NORM_MINMAX)
    
    cdf[0, 0] = h[0, 0]
    for j in range(1, 256):
        cdf[0, j] = cdf[0, j - 1] + h[0, j]

    cdf = cv2.normalize(cdf, None, 1, 0, cv2.NORM_MINMAX)

    return h, cdf

# Match histograms of 'src' to that of 'dst', according to both masks
def histMatchRGB(src, src_mask, dst, dst_mask):
    channels_src = cv2.split(src)
    channels_dst = cv2.split(dst)

    for i in range(3):
        src_hist, src_cdf = do1ChnHist(channels_src[i], src_mask)
        dst_hist, dst_cdf = do1ChnHist(channels_dst[i], dst_mask)

        last = 0
        lut = np.zeros((1, 256), dtype=np.uint8)

        for j in range(src_cdf.shape[1]):
            F1j = src_cdf[0, j]

            for k in range(last, dst_cdf.shape[1]):
                F2k = dst_cdf[0, k]
                if abs(F2k - F1j) < HISTMATCH_EPSILON or F2k > F1j:
                    lut[0, j] = k
                    last = k
                    break

        channels_src[i][:, :] = lut[0, channels_src[i]]

    res = cv2.merge(channels_src)
    return res

if __name__ == "__main__":
    dst = cv2.imread("balanced_img.png")
    src = cv2.imread("IMG_0133.tif")
    dst = cv2.resize(dst, (src.shape[1], src.shape[0]))

    mask = np.ones_like(src[:, :, 0], dtype=np.uint8) * 255

    matched_result = histMatchRGB(src, mask, dst, mask)

    cv2.imshow("original source", src)
    cv2.imshow("original query", dst)
    cv2.imshow("matched", matched_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



