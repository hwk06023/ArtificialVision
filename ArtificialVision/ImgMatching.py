import cv2
import numpy as np

class ImgMatching:
    @staticmethod
    def get_matching_score(source, target, type=0, threshold=0.5):
        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        if type == 0:  # Image
            # Find keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(source, None)
            kp2, des2 = sift.detectAndCompute(target, None)

        elif type == 1:  # Video
            # Process the first frame of each video
            ret1, frame1 = source.read()
            ret2, frame2 = target.read()
            if not ret1 or not ret2:
                return None  # Error reading frames
            kp1, des1 = sift.detectAndCompute(frame1, None)
            kp2, des2 = sift.detectAndCompute(frame2, None)

        # Initialize BFMatcher
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test to find good matches
        good_matches = []
        for m, n in matches:
            if m.distance < threshold * n.distance:
                good_matches.append([m])

        # Matching score based on the number of good matches
        matching_score = len(good_matches) / max(len(des1), len(des2))
        return matching_score

    @staticmethod
    def get_matching_result(source, target, type=0, threshold=0.5):
        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        if type == 0:  # Image
            # Find keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(source, None)
            kp2, des2 = sift.detectAndCompute(target, None)
            img_matches = np.empty((max(source.shape[0], target.shape[0]), source.shape[1]+target.shape[1], 3), dtype=np.uint8)

        elif type == 1:  # Video
            # Process the first frame of each video
            ret1, frame1 = source.read()
            ret2, frame2 = target.read()
            if not ret1 or not ret2:
                return None  # Error reading frames
            kp1, des1 = sift.detectAndCompute(frame1, None)
            kp2, des2 = sift.detectAndCompute(frame2, None)
            img_matches = np.empty((max(frame1.shape[0], frame2.shape[0]), frame1.shape[1]+frame2.shape[1], 3), dtype=np.uint8)

        # Initialize BFMatcher
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test to find good matches
        good_matches = []
        for m, n in matches:
            if m.distance < threshold * n.distance:
                good_matches.append([m])

        # Draw matches
        cv2.drawMatchesKnn(source, kp1, target, kp2, good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        return img_matches
