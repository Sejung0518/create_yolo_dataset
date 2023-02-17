"""
각 클래스에서 300개의 이미지 파일과 라벨 파일을 랜덤으로
"""
import os
import cv2
import numpy as np
import random
import xml.etree.ElementTree as ET
from PIL import Image
import xml_to_yolo_bndbox  # xml_to_yolo_bndbox 함수 저장

# 클래스 이름
class_name = ["A", "B", "C0", "C1", "C2", "D0", "D1", "E", "Z"]

# Plate 없는 라벨 파일들
no_plate_label = ["2-46-가-7907.jpg",
                  "2-46-마-4299.jpg",
                  "2-54-라-8772.jpg",
                  "2-93-모-5861.jpg",
                  "5-경기-32-바-6095.jpg",
                  "5-경기-40-바-2008.jpg",
                  "5-대구-31-바-2295.jpg",
                  "5-대구-32-바-1882.jpg",
                  "5-대구-36-바-1519.jpg",
                  "6-106-호-1014.jpg",
                  "6-127-호-1152.jpg",
                  "6-145-허-6077.jpg",
                  "6-159-너-3721.jpg",
                  "6-159-노-6027.jpg",
                  "6-162-하-8193.jpg",
                  "6-162-허-4162.jpg",
                  "6-165-너-3758.jpg",
                  "6-168-저-3682.jpg",
                  "6-246-소-7328.jpg",
                  "6-250-라-5308.jpg",
                  "7-146-나-9411.jpg",
                  "7-369-조-1820.jpg",
                  "7-382-모-7135.jpg",
                  "8-전남-04-나-4798.jpg",
                  "8-전남-04-나-4798-1.jpg",
                  "8-전북-06-아-8443.jpg",
                  "1_20210102_160951_986000.jpg",
                  "1_20210103_161155_775000.jpg",
                  "1_20210103_162257_677000.jpg",
                  "1_20210103_173943_404000.jpg",
                  "1_20210319_125400_982000.jpg",
                  "1_20210319_175808_576000.jpg",
                  "1_20210319_222311_866000.jpg",
                  "1_20210320_020734_305000.jpg",
                  "1_20210320_123126_013000.jpg",
                  "1_20210321_114630_022000.jpg",
                  "1_20210324_124908_991000.jpg",
                  "1_20210324_135106_130000.jpg",
                  "1_20210324_141124_233000.jpg",
                  "2_20210101_182123_447000.jpg",
                  "2_20210101_182552_897000.jpg",
                  "2_20210101_183815_157000.jpg",
                  "2_20210101_233641_025000.jpg",
                  "2_20210102_115853_920000.jpg",
                  "2_20210102_185056_730000.jpg",
                  "2_20210103_101906_867000.jpg",
                  "2_20210103_112205_644000.jpg",
                  "2_20210319_211944_151000.jpg"]

# 클래스 돌아가며 적용
for each_class in range(len(class_name)):
    # 원본 이미지, 라벨 파일의 폴더의 경로
    path_img = "C:/Users/rt_la/LPR_Region_1000X1000/Class_" + class_name[each_class] + "/images/src"
    path_lbl = "C:/Users/rt_la/LPR_Region_1000X1000/Class_" + class_name[each_class] + "/labels/src"
    files_img = os.listdir(path_img)
    if "desktop.ini" in files_img:
        files_img.remove("desktop.ini")
    files_lbl = os.listdir(path_lbl)
    if "desktop.ini" in files_lbl:
        files_lbl.remove("desktop.ini")
    print("Class" + class_name[each_class] + "\nimages:", len(files_img), "labels:", len(files_lbl))

    # 랜덤으로 추출할 300개의 이미지, 라벨의 인덱스 저장
    img_index_arr = []
    lbl_index_arr = []
    while (len(img_index_arr) < 300) and (len(lbl_index_arr) < 300):
        rand_num = random.randrange(0, len(files_img))
        img_lbl_filename = os.path.splitext(files_img[rand_num])[0] + '.xml'
        if files_img[rand_num] not in no_plate_label:

            if img_lbl_filename in files_lbl:  # 짝 맞는 게 있으면
                if rand_num not in img_index_arr:
                    img_index_arr.append(rand_num)
                    lbl_index_arr.append(files_lbl.index(img_lbl_filename))
    print("length of img index:", len(img_index_arr), "length of label index:", len(lbl_index_arr))

    # 이미지, 라벨 추출해서 저장할 새로운 폴더
    new_path_img = "C:/Users/rt_la/random/Class_" + class_name[each_class] + "/images"
    new_path_lbl = "C:/Users/rt_la/random/Class_" + class_name[each_class] + "/labels"
    os.makedirs(new_path_img)
    os.makedirs(new_path_lbl)

    # Class에서 인덱스에 따라 이미지, 라벨 파일 추출, 저장
    # 이미지 파일 저장
    for img_index in img_index_arr:
        full_img_path = path_img + '/' + files_img[img_index]  # 원본 이미지 파일의 경로
        # 왜인지 imread으로 이미지를 읽으면 에러가 나서 imdecode로 진행
        img_array = np.fromfile(full_img_path, np.uint8)
        curImg = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        new_dir_name = new_path_img + '/' + files_img[img_index]  # 추출한 이미지 파일 저장할 새로운 경로
        img_ext = os.path.splitext(files_img[img_index])[1]
        result, encoded_img = cv2.imencode(img_ext, curImg)
        # 새로운 경로에 이미지 파일 저장
        if result:
            with open(new_dir_name, mode='w+b') as f:
                encoded_img.tofile(f)
    # 라벨 파일 저장
    for lbl_index in lbl_index_arr:
        # "Plate"의 정보만 파싱해서 txt파일로 저장
        classes = []  # class의 name 저장
        result = []  # class의 index, xcenter, ycenter, width, height 저장

        # width, height, Plate 좌표 찾기
        try:
            tree = ET.parse(path_lbl + '/' + files_lbl[lbl_index], parser=ET.XMLParser(encoding='UTF-8'))
            root = tree.getroot()
            width = float(root.find("size").find("width").text)
            height = float(root.find("size").find("height").text)
            filename = os.path.splitext(files_lbl[lbl_index])[0]
            if width * height == 0:
                img = Image.open(path_img + '/' + filename + '.jpg')
                img_width, img_height = img.size
                width = img_width
                height = img_height
            # Plate의 정보 파싱
            plate_exist = False
            for obj in root.findall("object"):
                result = []
                label = obj.find("name").text
                if label == "Plate":
                    index = each_class  # class의 index
                    pil_bbox = [int(x.text) for x in obj.find("bndbox")]  # "Plate"의 bound box 좌표
                    yolo_bbox = xml_to_yolo_bndbox.xml_to_yolo_bndbox(pil_bbox, width, height)
                    bndbox_str = " ".join([str(x) for x in yolo_bbox])
                    result.append(f"{index} {bndbox_str}")
                    break
            # if not plate_exist:
            #     print("no plate:", files_lbl[lbl_index])
        except:
            print("예외:", files_lbl[lbl_index])
            print(result)
        finally:
            if result:
                # txt 파일로 저장
                filename = os.path.splitext(files_lbl[lbl_index])[0]
                with open(new_path_lbl + '/' + filename + '.txt', 'w', encoding='UTF-8') as f:
                    f.writelines(result)
            else:
                print("problem with result:", files_lbl[lbl_index])
                print(result)
