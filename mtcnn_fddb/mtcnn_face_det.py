from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import argparse
import tensorflow as tf
import numpy as np
import src.align.detect_face
import src.align as align
import cv2

def detect_face(img, pnet, rnet, onet):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor
    regions = []

    bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    nrof_faces = bounding_boxes.shape[0]
    if nrof_faces > 0:
        det = bounding_boxes[:, 0:5]
        det_arr = []
        img_size = np.asarray(img.shape)[0:2]
        if nrof_faces > 1:
            for i in range(nrof_faces):
                det_arr.append(np.squeeze(det[i]))
        else:
            det_arr.append(np.squeeze(det))

        for i, det in enumerate(det_arr):
            det = np.squeeze(det)
            margin = 2

            bb = np.zeros(5, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2.0, 0.0)
            bb[1] = np.maximum(det[1] - margin / 2.0, 0.0)
            bb[2] = np.minimum(det[2] + margin / 2.0, img_size[1])
            bb[3] = np.minimum(det[3] + margin / 2.0, img_size[0])
            # conver to width and height
            bb[2] -= bb[0]
            bb[3] -= bb[1]
            bb[4] = det[4]*10000
            regions.append(bb)

    return regions, nrof_faces

def main(args):
    with tf.Graph().as_default():

        with tf.Session() as sess:
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
            print('Loading feature extraction model')

            result_file = open(args.output_file, 'w+')

            with open(args.fddb_file_folder_dir + 'FDDB-all.txt', 'r') as fddb_file_list:
                file_list = fddb_file_list.read().splitlines()

            image_count = 0
            fddb_image_dir = args.fddb_image_folder_dir
            for file_name in file_list:
                img_name = fddb_image_dir + file_name + ".jpg"
                img = cv2.imread(img_name, 1)
                regions, num_of_faces = detect_face(img, pnet, rnet, onet)

                # write result to output file in format
                # file_name
                # num_of_faces
                # bx0, by0, bw0, bh0, prob0
                # ...
                result_file.write(file_name)
                result_file.write("\n")
                result_file.write(str(num_of_faces) + "\n")

                for items in regions:
                    face_item = str(items).strip("[]").lstrip()+"\n"
                    result_file.write(face_item)

                image_count += 1
                print("Processed " + str(image_count) + " images")

            # For debug to show the image and rect
            #     bb = np.zeros(5, dtype=np.int32)
            #     bb[0] = regions[0][0]
            #     bb[1] = regions[0][1]
            #     bb[2] = regions[0][2]
            #     bb[3] = regions[0][3]
            #
            # print(img.shape)
            # print(bb[0], bb[1], bb[2], bb[3])
            # cv2.rectangle(img, (bb[0], bb[1]), (bb[2]+bb[0], bb[1]+ bb[3]),
            #               (255, 0, 0), 2)
            # cv2.imshow("face", img)
            # key = cv2.waitKey(0)
            # cv2.destroyAllWindows()

            result_file.close()

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('fddb_file_folder_dir', type=str,
                        help='Could be a directory containing fddb txt')
    parser.add_argument('fddb_image_folder_dir', type=str,
                        help='Could be a directory containing fddb image')
    parser.add_argument('output_file', type=str,
                        help='Could be the output file name including path')

    return parser.parse_args(argv)
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
