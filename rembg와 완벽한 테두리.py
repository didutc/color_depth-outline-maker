# rembg module 사용 설명 github 참조 페이지
# https://github.com/danielgatis/rembg

# 이미지 경계에 stroke border 더하는 방법 참조 페이지
# https://stackoverflow.com/questions/61405583/how-can-i-add-an-outline-stroke-border-to-a-png-image-with-pillow-library-in-pyt

# Drop shadow 만드는 코드 참조 페이지
# https://stackoverflow.com/questions/74439028/wand-drop-shadow-on-image

# Code #1
# 개별 파일 열어 배경 제거하고 저장하기

import numpy as np
from rembg import remove
from PIL import Image, ImageFilter, ImageDraw
import random

def add_stroke(img, size=20, pos=(0,0), color='white'):
    X, Y = img.size
    
    edge = img.filter(ImageFilter.FIND_EDGES).load()
    print(edge)
    stroke = Image.new(img.mode, img.size, (0,0,0,0))
    draw = ImageDraw.Draw(stroke)

    for x in range(X):
        for y in range(Y):

            if edge[x,y][3] > 0:
                draw.ellipse((x-size,y-size,x+size,y+size), fill=color)

    stroke.paste(img, (pos[0], pos[1]), img)
    
    return stroke
def make_alpha_below_threshold_transparent(img, threshold=255):
    """
    알파 값이 threshold 이하인 픽셀을 모두 투명도로 만드는 함수.
    
    Parameters:
    img (PIL.Image.Image): 알파 채널이 포함된 이미지 (RGBA 모드)
    threshold (int): 알파 값의 임계값. 이 값 이하의 픽셀은 투명하게 변환됩니다. 기본값은 255 (완전히 불투명한 경우)
    
    Returns:
    PIL.Image.Image: 알파 값이 threshold 이하인 픽셀이 투명한 새로운 이미지
    """
    # 이미지의 RGBA 모드 확인
    if img.mode != 'RGBA':
        raise ValueError("이미지는 RGBA 모드여야 합니다.")
    
    # 이미지 배열 가져오기
    img_data = img.load()
    width, height = img.size
    
    # 알파 값을 기준으로 투명도 조절
    for x in range(width):
        for y in range(height):
            r, g, b, a = img_data[x, y]
            if a <= threshold:
                img_data[x, y] = (r, g, b, 0)  # 알파 값이 threshold 이하인 픽셀을 투명하게 설정
    
    return img

def main():
    # rembg 모듈 remove() 함수 활용 주변 배경 투명하게 만들기
    input_file = '20240313183519.jpg'
    output_file = 'output.png'
    input = Image.open(input_file)
    output = remove(input)
    output.save(output_file)


    img = Image.open(output_file).convert('RGBA')
    threshold = 200  # 이 값 이하의 알파 값을 투명도로 설정
    result_img = make_alpha_below_threshold_transparent(img, threshold)
    # 배경 투명 이미지 rgba (투명도 포함)로 읽기



    # 2번째 외곽 stroke 선 굵기 설정 (이미지 edge 경계점에 반지름 원 크기 활용
    # 3번째 stroke 외곽선 색 설정, default 'white'
    color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    stroke = add_stroke(result_img, 20, (0, 0), color)

##    # 추가 외곽선 설정시 활용
##    stroke = add_stroke(stroke, 4, (0, 0), 'black')    

    # 그림자 효과용으로도 활용
    stroke = add_stroke(stroke, 4, (-3, -2), 'black')    
    # stroke.show()
    
    stroke.save('output1_wbl.png')

    
### Code #2
### 폴더내 여러개 파일 모두 배경 투명하게 처리하기
##from pathlib import Path
##from rembg import remove, new_session
##
##def main():
##    session = new_session()
##
##    for file in Path('./image').glob('*.png'):
##        input_path = str(file)
##        output_path = str(file.parent / (file.stem + "_out.png"))
##
##        with open(input_path, 'rb') as i:
##            with open(output_path, 'wb') as o:
##                input = i.read()
##                output = remove(input, session=session)
##                o.write(output)


# main 함수 로딩부
if __name__ == '__main__':
    main()
