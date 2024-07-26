from PIL import Image, ImageEnhance

def adjust_saturation(img, factor):
    """
    이미지의 채도를 조정하는 함수.

    Parameters:
    img (PIL.Image.Image): RGBA 모드의 이미지
    factor (float): 채도 조정 비율 (1.0은 원래 채도, 0.0은 무채색)

    Returns:
    PIL.Image.Image: 채도 조정된 이미지
    """
    if img.mode != 'RGBA':
        raise ValueError("이미지는 RGBA 모드여야 합니다.")
    
    # 이미지의 채도 조정
    enhancer = ImageEnhance.Color(img)
    img_adjusted = enhancer.enhance(factor)
    
    return img_adjusted

def main():
    input_file = 'input.png'
    output_file = 'output.png'
    
    # 이미지 열기
    img = Image.open(input_file).convert('RGBA')
    
    # 채도 조정 비율 설정 (1.0은 원래 채도, 0.0은 무채색, 1.5는 50% 더 높은 채도 등)
    factor = 3  # 채도 비율 (1.0 = 원래 채도, 0.0 = 흑백, 1.5 = 50% 더 높은 채도)
    result_img = adjust_saturation(img, factor)
    
    # 결과 이미지 저장
    result_img.save(output_file)

if __name__ == '__main__':
    main()
