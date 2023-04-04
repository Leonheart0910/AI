from google_images_search import GoogleImagesSearch
from PIL import Image
import os
import requests
from io import BytesIO


# Google API 키 및 사용자 고유 식별자(CX)를 입력하세요.
api_key = "AIzaSyBLZj6H7iMsn4xA8g1HXihwktffEsDw8jc"
cx = "503bfa1d4b2b84f3c"

# 검색할 키워드 및 저장할 디렉토리 설정
search_term = "아디다스 신발"
save_directory = "C:\\Users\\halo0\\Desktop\\AI_test폴더"


# GoogleImagesSearch 객체 생성
gis = GoogleImagesSearch(api_key, cx)


# 검색 조건 설정
_search_params = {
    "q": search_term,
    "num": 50,  # 한 번에 다운로드 받을 이미지 개수
    "imgSize": "large",
    "fileType": "jpg"
}

# 검색 실행
gis.search(search_params=_search_params)

# 디렉토리가 없으면 생성
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 이미지 다운로드
for i, image in enumerate(gis.results()):
    try:
        # 이미지 데이터를 가져옵니다.
        response = requests.get(image.url)
        
        # 이미지 파일을 엽니다.
        img = Image.open(BytesIO(response.content))
        
        # 이미지 크기를 조정합니다 (선택 사항).
        img = img.resize((500, 500))
        
        # 이미지를 RGB 모드로 변환합니다.
        img = img.convert('RGB')
        
        # 이미지를 저장합니다.
        file_name = f"{search_term}_{i}.jpg"
        img.save(os.path.join(save_directory, file_name))
    except Exception as e:
        print(f"이미지 {i}를 저장하는 동안 오류 발생: {e}")


print("이미지 다운로드 완료")