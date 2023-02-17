# xml 파일의 Plate의 정보를 yolo txt 파일에 저장할 형식으로 변환할 때 사용하는 함수
def xml_to_yolo_bndbox(pil_bbox, width, height):
    xcenter = ((pil_bbox[0] + pil_bbox[2]) / 2) / width
    ycenter = ((pil_bbox[1] + pil_bbox[3]) / 2) / height
    w = (pil_bbox[2] - pil_bbox[0]) / width
    h = (pil_bbox[3] - pil_bbox[1]) / height
    return [xcenter, ycenter, w, h]