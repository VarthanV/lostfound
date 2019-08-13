# USAGE
# python align_faces.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg

# import the necessary packages
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2
import uuid
import os


def align_face(path):
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(os.path.join(os.getcwd(),"lostfoundapp","shape_predictor_68_face_landmarks.dat"))
	fa = FaceAligner(predictor, desiredFaceWidth=256)
	image = cv2.imread(path)
	image = imutils.resize(image, width=800)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	try:
		rects = detector(gray, 2)

		(x, y, w, h) = rect_to_bb(rects[0])
		faceAligned = fa.align(image, gray, rects[0])

		f = str(uuid.uuid4())
		cv2.imwrite(path,faceAligned)
	except:
		cv2.imwrite(path,image)
