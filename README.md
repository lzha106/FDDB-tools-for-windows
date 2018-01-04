# FDDB-tools-for-windows
This is the repo for Face Detection Data Set and Benchmark(FDDB) tools and examples on windows

It includes the FDDB evaluation exe and ROC curve plot scripts on windows platform with mtcnn face detector as one example.

1. Preparation
(1) Download original unannotated set of images from http://vis-www.cs.umass.edu/fddb/
(2) Install gnuplot.exe for windows
(3) (Optional) setup facenet from https://github.com/davidsandberg/facenet, which has a tensorflow implemented mtcnn face detector.

2. How to generate FDDB format result file for your face detector?
Follow http://vis-www.cs.umass.edu/fddb/README.txt to generate the required format file with your face detector.
MTCNN as one example:
(1) Put ./mtcnn_fddb/mtcnn_face_det.py to your facenet environment and launch it.
(2) It will generate a mtcnn_fddb_result.txt file under the directory you assigned to above python scripts.
 
3. How to use fddb_evaluator.exe?
It is an cmd on windows to generate ROC curve data from your FDDB detection result file and save into two files named ContROC.txt and DiscROC.txt.
Launch the command from windows console
$ fddb_evaluator.exe -h

./evaluate [OPTIONS]
	-h              : print usage
	-a fileName     : file with face annotations (default: ellipseList.txt)
	-d fileName     : file with detections (default: faceList.txt)
	-f format       : representation of faces in the detection file (default: 0 
			: [ 0 (rectangle), 1 (ellipse) or  2 (pixels) ]
	-i dirName      : directory where the original images are stored (default: ~/scratch/Data/facesInTheWild/)
	-l fileName     : file with list of images to be evaluated (default: temp.txt)
	-r fileName     : prefix for files to store the ROC curves (default: temp)
	
E.X. Run command like below to generate the ROC curve file
$.\fddb_evaluator.exe -d "/PATH/TO/your_fddb_format_file.txt" -i "/PATH/TO/FDDB/UNANNOTATED_IMAGES" -r "/PATH/TO/YOUR_EVALUATION_OUTPUT" -l "/PATH/TO/FDDB-ANNOTATION/FDDB-all.txt" -a "/PATH/TO/FDDB/FDDB-ANNOTATION/FDDB-all-ellipseList.txt"

4. How to draw ROC curve?
Go to folder of FDDB-tools and run below command from console on windows to generate ROC curve image.
$ gnuplot.exe contROC.p

5. Reference
(1) https://github.com/davidsandberg/facenet
(2) http://vis-www.cs.umass.edu/fddb/
(3) http://vis-www.cs.umass.edu/fddb/results.html
