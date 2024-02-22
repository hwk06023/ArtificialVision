import cv2
import numpy as np

def get_matching_score(img1, img2, type=0):
    if type == 0:
        img1 = cv2.cvtColor(img1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.cvtColor(img2, cv2.IMREAD_GRAYSCALE)

        img1 = cv2.resize(img1, (1024, 1024))
        img2 = cv2.resize(img2, (1024, 1024))
    else:
        # another type
        pass

    detector = cv2.SIFT_create()

    kp1, desc1 = detector.detectAndCompute(img1, None)
    kp2, desc2 = detector.detectAndCompute(img2, None)
    print('kp :', kp1[0])
    print('desc :', desc1[0])

    matcher = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
    matches = matcher.knnMatch(desc1, desc2, 2)
    print('matches :', list(matches[0]))

    ratio = 0.5
    good_matches = [first for first,second in matches \
                        if first.distance < second.distance * ratio]
    print('good matches:%d/%d' %(len(good_matches),len(matches)))

    if len(good_matches) <= 5:
        print('False')
    else:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ])
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ])

        mtrx, mask = cv2.findHomography(src_pts, dst_pts)
        h,w, = img1.shape[:2]
        pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
        dst = cv2.perspectiveTransform(pts,mtrx)
        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

        res = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, \
                            flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('Matching Homography', res)
        cv2.waitKey()
        cv2.destroyAllWindows()
