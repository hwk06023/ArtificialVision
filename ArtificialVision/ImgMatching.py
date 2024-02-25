import cv2
import numpy as np

'''
get_matching_result is finished, but it is not yet tested.
'''

def get_matching_result(img1, img2, type=0, threshold=0.5):
    # SIFT 검출기 초기화
    detector = cv2.SIFT_create()

    if type == 0:  # 이미지
        kp1, desc1 = detector.detectAndCompute(img1, None)
        kp2, desc2 = detector.detectAndCompute(img2, None)
        print('Image load Complete...\n\n')
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
            print('Matching Fail (False)')
        else:
            print('Matching Success (True)')
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

    elif type == 1:  # 비디오
        point_img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
        point_img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
        print('Image load Complete...\n\n')

        # If you want to resize frame size, change this value
        resize_frame_size = 1024
        query_img_width = 1024

        h, w = 1024, 1024
        point_img1 = cv2.resize(point_img1, (query_img_width, query_img_width * h // w))
        max_height = max(1024, query_img_width * h // w)
        point_img2 = cv2.resize(point_img2, (query_img_width, query_img_width * h // w))
        max_height = max(max_height, query_img_width * h // w)

        video_path = input('Enter the video path : ')
        video = cv2.VideoCapture()

        video_size = (max_height, resize_frame_size+query_img_width)

        fps = video.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_out = './' + str(resize_frame_size) + '_demo.mp4'
        out = cv2.VideoWriter(f'{video_out}', fourcc, fps, (video_size[1], video_size[0]))

        if not video.isOpened():
            print("Could not Open :")
            exit(0)

        detector = cv2.SIFT_create()

        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        count_frames = 0

        maching_frames = []

        print('Start Matching...')
        while True:
            print('frame :', count_frames, '/', total_frames)
            maching_frames.append(count_frames)
            count_frames += 1

            ret, frame = video.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (1024, 1024))

            kp, des = detector.detectAndCompute(frame, None)
            kp1, des1 = detector.detectAndCompute(point_img1, None)
            kp2, des2 = detector.detectAndCompute(point_img2, None)

            bf = cv2.BFMatcher()
            matches1 = bf.knnMatch(des, des1, k=2)
            matches2 = bf.knnMatch(des, des2, k=2)

            good_matches = []
            ratio = 0.5
            good_matches.append(list(first for first,second in matches1 \
                            if first.distance < second.distance * ratio))
            
            good_matches.append(list(first for first,second in matches2 \
                            if first.distance < second.distance * ratio))

            if len(good_matches[0]) <= 5 and len(good_matches[1]) <= 5: # len(good_matches[2]) <= 5:
                print('Matching Fail (False)')
                frame = np.pad(frame, [(0, video_size[0]-resize_frame_size), (0, video_size[1]-resize_frame_size)], mode='constant')
                frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
                out.write(np.array(frame).reshape(frame.shape[0], frame.shape[1] , 3))
                continue
            
            else:
                print('Matching Success (True)')

                print('-- good matches --')
                print('total matches :', len(matches1))

                # 4 -> point_num
                for i in range(2):
                    print(i,'- matches :',len(good_matches[i]))
                for i in range(2):
                    if len(good_matches[i]) > 5:
                        if i == 0:
                            kp_point = kp1
                            matches_point = matches1
                            good_matches_point = good_matches[0]
                            point = point_img1
                        elif i == 1 and len(good_matches[1]) > len(good_matches[0]):
                            kp_point = kp2
                            matches_point = matches2
                            good_matches_point = good_matches[1]
                            point = point_img2
                        
                        src_pts = np.float32([ kp[m.queryIdx].pt for m in good_matches[i] ])
                        dst_pts = np.float32([ kp_point[m.trainIdx].pt for m in good_matches[i] ])

                        break

                mtrx, mask = cv2.findHomography(src_pts, dst_pts)
                
                h,w = frame.shape[:2]

                pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
                dst = cv2.perspectiveTransform(pts,mtrx)

                point = cv2.polylines(point,[np.int32(dst)],True,255,3, cv2.LINE_AA)

                res = cv2.drawMatches(frame, kp, point, kp_point, good_matches_point, None, \
                                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
                
                h, w = res.shape[:2]
                if (video_size[0]-h) * (video_size[1]-w) != 0:
                    res = np.pad(res, [(0, video_size[0]-h), (0, video_size[1]-w)], mode='constant')
                out.write(np.array(res).reshape(res.shape[0], res.shape[1], 3))
        print('Matching Complete !\n')
        out.release()

