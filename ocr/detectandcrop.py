# -*- coding: utf-8 -*-
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import sys

import time
import argparse #ipynb에서는 easydict로 활용
import easydict

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image, ImageDraw

import cv2
from skimage import io
import numpy as np
import craft_utils
import imgproc
import file_utils
import json
import zipfile

from craft import CRAFT


from collections import OrderedDict

#copyStateDict 함수는 PyTorch 모델의 state_dict에서 불필요한 prefix (예: "module.")를 제거하는 역할
def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

#str2bool 함수는 문자열을 boolean 값으로 변환해주는 함수입니다. 대소문자를 구분하지 않으며, "yes", "y", "true", "t", "1" 중 하나가 입력되면 True를 반환합니다. 
#그 외에는 False를 반환합니다. 이 함수는 일반적으로 argparse 모듈과 함께 사용되어, 스크립트 실행 시 입력되는 인자값을 boolean 형태로 변환해주는데 사용

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")

#craft text detect model 경로
trained_model = './craft_mlt_25k.pth'
#ocr 대상 이미지 경로 /image 폴더 내 이미지
test_folder = './image' 

#argparse를 easydict로 대체(py에서는 argparse로 사용 가능)
#argparse 사용 시 용이하도록 args로 필요한 요소들 저장
args = easydict.EasyDict({
    #"trained_model": "weights/craft_mlt_25k.pth",
    "text_threshold": 0.7,
    "low_text": 0.4,
    "link_threshold": 0.4,
    "cuda": True,
    "canvas_size": 1280,
    "mag_ratio": 1.5,
    "poly": False,
    "show_time": False,
    #"test_folder": "/data/",
    "refine": False,
    "refiner_model": "weights/craft_refiner_CTW1500.pth"
})


""" For test images in a folder """
#test_folder = './test'로 설정해두었음
image_list, _, _ = file_utils.get_files(test_folder)

#craft 결과 이미지, 텍스트 좌표 등의 결과 파일은 result라는 폴더에 저장하겠음
result_folder = './result/'
if not os.path.isdir(result_folder):
    os.mkdir(result_folder)

def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly, refine_net=None):
    t0 = time.time()

    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, args.canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio=args.mag_ratio)
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0,:,:,0].cpu().data.numpy()
    score_link = y[0,:,:,1].cpu().data.numpy()

    # refine link
    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0,:,:,0].cpu().data.numpy()

    t0 = time.time() - t0
    t1 = time.time()

    # Post-processing
    boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None: polys[k] = boxes[k]

    t1 = time.time() - t1

    # render results (optional)
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = imgproc.cvt2HeatmapImg(render_img)

    if args.show_time : print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

    return boxes, polys, ret_score_text


#if __name__ == '__main__': 이거 치면 이하의 내용 tap 해야함.
# load net
net = CRAFT()     # initialize

print('Loading weights from checkpoint (' + trained_model + ')')
if args.cuda:
    net.load_state_dict(copyStateDict(torch.load(trained_model)))
else:
    net.load_state_dict(copyStateDict(torch.load(trained_model, map_location='cpu')))

if args.cuda:
    net = net.cuda()
    net = torch.nn.DataParallel(net)
    cudnn.benchmark = False

net.eval()

# LinkRefiner
refine_net = None
if args.refine:
    from refinenet import RefineNet
    refine_net = RefineNet()
    print('Loading weights of refiner from checkpoint (' + args.refiner_model + ')')
    if args.cuda:
        refine_net.load_state_dict(copyStateDict(torch.load(args.refiner_model)))
        refine_net = refine_net.cuda()
        refine_net = torch.nn.DataParallel(refine_net)
    else:
        refine_net.load_state_dict(copyStateDict(torch.load(args.refiner_model, map_location='cpu')))

    refine_net.eval()
    args.poly = True

t = time.time()

## load data
for k, image_path in enumerate(image_list):
    print("Test image {:d}/{:d}: {:s}".format(k+1, len(image_list), image_path), end='\r')
    image = imgproc.loadImage(image_path)

    bboxes, polys, score_text = test_net(net, image, args.text_threshold, args.link_threshold, args.low_text, args.cuda, args.poly, refine_net)

    #print(bboxes, polys, score_text) #bboxes, polys, score_text 출력
    # save score text
    filename, file_ext = os.path.splitext(os.path.basename(image_path))
    mask_file = result_folder + "/res_" + filename + '_mask.jpg'
    cv2.imwrite(mask_file, score_text)

    file_utils.saveResult(image_path, image[:,:,::-1], polys, dirname=result_folder)
#시간 출력
#print("elapsed time : {}s".format(time.time() - t))


#여기서부터 bboxes의 좌표대로 Image를 crop합니다
bboxes = bboxes.astype(int) #bboxes 정수화
#bbox를 왼쪽 위 x,y랑 오른쪽아래 x,y로 나타내기
bbox_list = []
for bbox in bboxes:
    x_min, y_min = bbox.min(axis=0)
    x_max, y_max = bbox.max(axis=0)
    bbox_list.append([x_min, y_min, x_max, y_max])

#비슷한 높이에 있는 bbox 하나의 bbox로 묶어주기
merged_bboxes = []

# 두 번째 요소를 기준으로 정렬
sorted_bboxes = sorted(bbox_list, key=lambda bbox: bbox[1])

for bbox in sorted_bboxes:
    if len(merged_bboxes) == 0:
        # merged_bboxes가 비어있을 경우, 새로운 바운딩 박스 추가
        merged_bboxes.append(bbox)
    else:
        # 새로운 바운딩 박스와 기존 바운딩 박스의 왼쪽 위의 y좌표가 조정범위 내에 들어오는 경우, 합치기
        bbox_height = bbox[3] - bbox[1] # 바운딩 박스 높이 계산
        adjust_range = int(bbox_height * 0.3) # 높이의 0.3를 조정 범위로 설정
        if bbox[1] <= merged_bboxes[-1][1] + adjust_range:
            merged_bboxes[-1] = [min(merged_bboxes[-1][0], bbox[0]), 
                                 min(merged_bboxes[-1][1], bbox[1]), 
                                 max(merged_bboxes[-1][2], bbox[2]), 
                                 max(merged_bboxes[-1][3], bbox[3])]
        else:
            # 겹치지 않는 경우, 새로운 바운딩 박스 추가
            merged_bboxes.append(bbox)


# test_folder 내의 이미지 파일명을 읽어옵니다.
img_filename = [f for f in os.listdir(test_folder) if f.endswith('.jpg') or f.endswith('.png')][0]

# img를 지정합니다.
img = Image.open(os.path.join(test_folder, img_filename))

# bbox를 순회하며 crop 및 저장
for i, bbox in enumerate(merged_bboxes):
    # bbox 좌표를 정수형으로 변환

    # bbox 내부를 crop하여 저장
    x1, y1, x2, y2 = bbox
    img_cropped = img.crop((x1,y1,x2,y2))
    img_cropped.save(f'crop/cropped_{i}.png')   
