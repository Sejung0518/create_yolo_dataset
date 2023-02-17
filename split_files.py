import os
import shutil
from sklearn.model_selection import train_test_split

# 클래스 이름
class_name = ["A", "B", "C0", "C1", "C2", "D0", "D1", "E", "Z"]

# split할 이미지, 라벨 파일
image_files = []
label_files = []

# 파일 리스트에 저장
for each_class in class_name:
    path_img = "C:/Users/rt_la/random/Class_" + each_class + "/images"
    path_lbl = "C:/Users/rt_la/random/Class_" + each_class + "/labels"

    # split할 파일들의 리스트
    list_new_img = os.listdir(path_img)
    list_new_lbl = os.listdir(path_lbl)

    # images, labels 둘 다 300개씩 들어갔는지 확인
    comp_list_img = []
    for i in range(300):
        img_split = os.path.splitext(list_new_img[i])
        comp_list_img.append(img_split[0] + '.txt')
    print("Are images and labels same? ", (comp_list_img == list_new_lbl))
    print("length of random images:", len(list_new_img), "length of random labels:", len(list_new_lbl))

    # split 하기 위해 저장
    for i in range(300):
        image_files.append(list_new_img[i])
        label_files.append(list_new_lbl[i])

# 이미지와 라벨을 train, test, validation 7:2:1로 split
image_train, image_test, label_train, label_test = train_test_split(image_files, label_files, test_size=0.3)
image_val, image_test, label_val, label_test = train_test_split(image_test, label_test, test_size=2/3)
print("The number of image_train files(1890):", len(image_train), " & the number of label_train files(1890):", len(label_train))
print("The number of image_test files(540):", len(image_test), " & the number of label_test files(540):", len(label_test))
print("The number of image_val files(270):", len(image_val), " & the number of label_val files(270):", len(label_val))

# C:\Users\User\PycharmProjects\yolov5\data에 images, labels 폴더 만들고 각각 train, test, val 폴더 생성
new_dir = "C:/Users/rt_la/yolov5-master/data/"
dataset = ["images", "labels"]
split = ["train", "test", "val"]
for data in dataset:
    for folder in split:
        os.makedirs(new_dir + data + '/' + folder, exist_ok=True)

# train, test, val 폴더에 파일 저장
for each_class in class_name:
    new_path_img = "C:/Users/rt_la/random/Class_" + each_class + "/images"
    new_path_lbl = "C:/Users/rt_la/random/Class_" + each_class + "/labels"
    img_list = os.listdir(new_path_img)
    lbl_list = os.listdir(new_path_lbl)
    # train 폴더에 파일 복사
    for i in range(len(image_train)):
        if image_train[i] in img_list:
            original_img_path = new_path_img + '/' + image_train[i]
            yolo_img_path = new_dir + "images/train"
            shutil.copy(original_img_path, yolo_img_path)
        if label_train[i] in lbl_list:
            original_lbl_path = new_path_lbl + '/' + label_train[i]
            yolo_lbl_path = new_dir + "labels/train"
            shutil.copy(original_lbl_path, yolo_lbl_path)
    # test 폴더에 파일 복사
    for i in range(len(image_test)):
        if image_test[i] in img_list:
            original_img_path = new_path_img + '/' + image_test[i]
            yolo_img_path = new_dir + "images/test"
            shutil.copy(original_img_path, yolo_img_path)
        if label_test[i] in lbl_list:
            original_lbl_path = new_path_lbl + '/' + label_test[i]
            yolo_lbl_path = new_dir + "labels/test"
            shutil.copy(original_lbl_path, yolo_lbl_path)
    # val 폴더에 파일 복사
    for i in range(len(image_val)):
        if image_val[i] in img_list:
            original_img_path = new_path_img + '/' + image_val[i]
            yolo_img_path = new_dir + "images/val"
            shutil.copy(original_img_path, yolo_img_path)
        if label_val[i] in lbl_list:
            original_lbl_path = new_path_lbl + '/' + label_val[i]
            yolo_lbl_path = new_dir + "labels/val"
            shutil.copy(original_lbl_path, yolo_lbl_path)
