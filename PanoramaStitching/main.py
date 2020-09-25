# -*- coding: utf-8 -*-

import cv2
import imutils
import numpy as np
import pandas as pd

class PanoramaManager:
    def __init__(self, left_img_fname, right_img_fname):
        self.left_coords  = []
        self.right_coords = []
        self.left_img_fname  = left_img_fname
        self.right_img_fname = right_img_fname
        self.is_left = True
        self.minimum_points = 10

    def main(self):
        self.select_points_in_left_img()
        self.select_points_in_right_img()

        print(f"left coordinates: {self.left_coords}\nright coordinates: {self.right_coords}")

        self.calc_homography_matrix()
        self.show_stitched_img()

    def select_points_in_left_img(self):
        self.left_img = cv2.imread(self.left_img_fname)
        cv2.namedWindow('left_img')

        cv2.setMouseCallback('left_img', self.mouse_callback)

        while len(self.left_coords) < self.minimum_points:
            cv2.imshow('left_img', self.left_img)
            k = cv2.waitKey(1) & 0xFF

            if k == ord('s'):
                print("S 키 눌러짐")
                break

        self.is_left = False
        cv2.destroyAllWindows()

    def select_points_in_right_img(self):
        self.right_img = cv2.imread(self.right_img_fname)
        cv2.namedWindow('right_img')

        cv2.setMouseCallback('right_img', self.mouse_callback)

        while len(self.right_coords) < self.minimum_points:
            cv2.imshow('right_img', self.right_img)
            k = cv2.waitKey(1) & 0xFF

            if k == ord('s'):
                print("S 키 눌러짐")
                break

        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"selected coordinates x: {x} / y: {y}")
            if self.is_left:
                self.left_coords.append([x, y])
                self.left_img = panorama.draw_circle(self.left_img, x, y)

                cv2.imshow('left_img', self.left_img)
            else:
                self.right_coords.append([x, y])
                self.right_img = panorama.draw_circle(self.right_img, x, y)

                cv2.imshow('right_img', self.right_img)

    @staticmethod
    def draw_circle(img, x, y):
        img = cv2.circle(img, (x, y), 4, (0, 0, 255), 2)
        return img

    def calc_homography_matrix(self):
        h, status = cv2.findHomography(np.array(self.left_coords), np.array(self.right_coords))
        self.final_img = cv2.warpPerspective(self.right_img, h, (self.left_img.shape[1] + self.right_img.shape[1], self.left_img.shape[0]))
        self.final_img[0:self.left_img.shape[0], 0:self.left_img.shape[1]] = self.left_img

    def show_stitched_img(self):
        cv2.imshow('final', self.final_img)
        cv2.waitKey(0)

if __name__ == "__main__":
    panorama = PanoramaManager(left_img_fname='yosemite1.jpg', right_img_fname='yosemite2.jpg')
    panorama.main()