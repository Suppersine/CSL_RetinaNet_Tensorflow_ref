# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import numpy as np

from PIL import Image, ImageDraw, ImageFont
import cv2

from libs.configs import cfgs
from libs.label_name_dict.label_dict import LABEL_NAME_MAP
from help_utils.tools import get_dota_short_names

NOT_DRAW_BOXES = 0
ONLY_DRAW_BOXES = -1
ONLY_DRAW_BOXES_WITH_SCORES = -2

STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen', 'LightBlue', 'LightGreen'
]
FONT = ImageFont.load_default()


def draw_a_rectangel_in_img(draw_obj, box, color, width, method):
    '''
    use draw lines to draw rectangle. since the draw_rectangle func can not modify the width of rectangle
    :param draw_obj:
    :param box: [x1, y1, x2, y2]
    :return:
    '''

    # if cfgs.ANGLE_RANGE == 180:
    #     if box[2] < box[3]:
    #         angle = box[-1] + 90
    #     else:
    #         angle = box[-1]
    # else:
    #     angle = box[-1]
    #
    # if abs(angle-90) <= 1 or abs(angle+90) <= 1 or abs(angle-0) <= 1:
    #     color = (0, 0, 255)
    # else:
    #     color = (0, 255, 0)

    # color = (0, 255, 0)
    if method == 0:
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        top_left, top_right = (x1, y1), (x2, y1)
        bottom_left, bottom_right = (x1, y2), (x2, y2)

        draw_obj.line(xy=[top_left, top_right],
                      fill=color,
                      width=width)
        draw_obj.line(xy=[top_left, bottom_left],
                      fill=color,
                      width=width)
        draw_obj.line(xy=[bottom_left, bottom_right],
                      fill=color,
                      width=width)
        draw_obj.line(xy=[top_right, bottom_right],
                      fill=color,
                      width=width)
    else:
        x_c, y_c, w, h, theta = box[0], box[1], box[2], box[3], box[4]
        rect = ((x_c, y_c), (w, h), theta)
        rect = cv2.boxPoints(rect)
        rect = np.int0(rect)
        draw_obj.line(xy=[(rect[0][0], rect[0][1]), (rect[1][0], rect[1][1])],
                      fill=color,
                      width=width)
        draw_obj.line(xy=[(rect[1][0], rect[1][1]), (rect[2][0], rect[2][1])],
                      fill=color,
                      width=width)
        draw_obj.line(xy=[(rect[2][0], rect[2][1]), (rect[3][0], rect[3][1])],
                      fill=color,
                      width=width)
        draw_obj.line(xy=[(rect[3][0], rect[3][1]), (rect[0][0], rect[0][1])],
                      fill=color,
                      width=width)


def only_draw_scores(draw_obj, box, score, color):

    x, y = box[0], box[1]
    draw_obj.rectangle(xy=[x, y, x+60, y+10],
                       fill=color)
    draw_obj.text(xy=(x, y),
                  text="obj:" + str(round(score, 2)),
                  fill='black',
                  font=FONT)


def draw_label_with_scores(draw_obj, box, label, score, color):
    x, y = box[0], box[1]
    draw_obj.rectangle(xy=[x, y, x + 60, y + 20],
                       fill=color)

    if cfgs.DATASET_NAME == 'DOTA':
        label_name = get_dota_short_names(LABEL_NAME_MAP[label])
    else:
        label_name = LABEL_NAME_MAP[label]
    txt = label_name + ':' + str(round(score, 2))
    # txt = ' ' + label_name
    draw_obj.text(xy=(x, y),
                  text=txt,
                  fill='black',
                  font=FONT)
    if cfgs.ANGLE_RANGE == 180:
        if box[2] < box[3]:
            angle = box[-1] + 90
        else:
            angle = box[-1]
    else:
        angle = box[-1]
    txt_angle = 'angle:%.1f' % angle
    # txt_angle = ' %.1f' % angle
    draw_obj.text(xy=(x, y+10),
                  text=txt_angle,
                  fill='black',
                  font=FONT)


def draw_boxes_with_label_and_scores(img_array, boxes, labels, scores, method, in_graph=True):
    if in_graph:
        if cfgs.NET_NAME in ['resnet152_v1d', 'resnet101_v1d', 'resnet50_v1d']:
            img_array = (img_array * np.array(cfgs.PIXEL_STD) + np.array(cfgs.PIXEL_MEAN_)) * 255
        else:
            img_array = img_array + np.array(cfgs.PIXEL_MEAN)
    img_array.astype(np.float32)
    boxes = boxes.astype(np.int64)
    labels = labels.astype(np.int32)
    img_array = np.array(img_array * 255 / np.max(img_array), dtype=np.uint8)

    img_obj = Image.fromarray(img_array)
    raw_img_obj = img_obj.copy()

    draw_obj = ImageDraw.Draw(img_obj)
    num_of_objs = 0
    for box, a_label, a_score in zip(boxes, labels, scores):

        if a_label != NOT_DRAW_BOXES:
            num_of_objs += 1
            draw_a_rectangel_in_img(draw_obj, box, color=STANDARD_COLORS[a_label], width=3, method=method)
            if a_label == ONLY_DRAW_BOXES:  # -1
                continue
            elif a_label == ONLY_DRAW_BOXES_WITH_SCORES:  # -2
                only_draw_scores(draw_obj, box, a_score, color='White')
            else:
                draw_label_with_scores(draw_obj, box, a_label, a_score, color='White')

    out_img_obj = Image.blend(raw_img_obj, img_obj, alpha=0.7)

    return np.array(out_img_obj)


def draw_boxes(img_array, boxes, labels, scores, color, method, in_graph=True):
    if in_graph:
        if cfgs.NET_NAME in ['resnet152_v1d', 'resnet101_v1d', 'resnet50_v1d']:
            img_array = (img_array * np.array(cfgs.PIXEL_STD) + np.array(cfgs.PIXEL_MEAN_)) * 255
        else:
            img_array = img_array + np.array(cfgs.PIXEL_MEAN)
    img_array.astype(np.float32)
    boxes = boxes.astype(np.int64)
    labels = labels.astype(np.int32)
    img_array = np.array(img_array * 255 / np.max(img_array), dtype=np.uint8)

    img_obj = Image.fromarray(img_array)
    raw_img_obj = img_obj.copy()

    draw_obj = ImageDraw.Draw(img_obj)
    num_of_objs = 0
    for box, a_label, a_score in zip(boxes, labels, scores):

        if a_label != NOT_DRAW_BOXES:
            num_of_objs += 1
            draw_a_rectangel_in_img(draw_obj, box, color=color, width=3, method=method)
            # draw_a_rectangel_in_img(draw_obj, box, color=STANDARD_COLORS[1], width=3, method=method)
            if a_label == ONLY_DRAW_BOXES:  # -1
                continue
            elif a_label == ONLY_DRAW_BOXES_WITH_SCORES:  # -2
                 only_draw_scores(draw_obj, box, a_score, color='White')
            else:
                draw_label_with_scores(draw_obj, box, a_label, a_score, color='White')

    out_img_obj = Image.blend(raw_img_obj, img_obj, alpha=0.7)

    return np.array(out_img_obj)


if __name__ == '__main__':
    img_array = cv2.imread(r"C:\sjtu\codebase\IJCAI\RetinaNet_Tensorflow_Rotation\tools\test_dota\RetinaNet_DOTA_1x_20190527\dota_img_vis\P0006.png")
    boxes = np.array(
        [[200, 200, 100, 500, 0],
         [200, 200, 100, 500, -90]]
    )

    # test only draw boxes
    labes = np.ones(shape=[len(boxes), ], dtype=np.float32) * ONLY_DRAW_BOXES
    scores = np.zeros_like(labes)
    imm = draw_boxes_with_label_and_scores(img_array, boxes, labes, scores, method=1)
    # imm = np.array(imm)

    # cv2.imshow("te", imm)
    #
    # # test only draw scores
    # labes = np.ones(shape=[len(boxes), ], dtype=np.float32) * ONLY_DRAW_BOXES_WITH_SCORES
    # scores = np.random.rand((len(boxes))) * 10
    # imm2 = draw_boxes_with_label_and_scores(img_array, boxes, labes, scores)
    #
    # cv2.imshow("te2", imm2)
    # # test draw label and scores
    #
    # labels = np.arange(1, 4)
    # imm3 = draw_boxes_with_label_and_scores(img_array, boxes, labels, scores)
    cv2.imshow("te3", imm)

    cv2.waitKey(0)






