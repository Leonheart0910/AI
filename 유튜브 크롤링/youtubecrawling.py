import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# API 키 설정
api_key = 'AIzaSyA0OQvWjCvO0MPosjbuhDHn0I03Hc5ofRg'

# YouTube API 클라이언트 빌드
youtube = build('youtube', 'v3', developerKey=api_key)

# 원하는 영상 링크를 가져오는 함수
def get_video_links(query, min_views, days_ago):
    # 한 달 전 날짜 계산 및 문자열 형태로 변환
    published_after = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # 유튜브 검색 요청 설정
    request = youtube.search().list(
            part="snippet",
            type="video",
            q=query,
            videoDefinition="high",
            maxResults=50,
            fields="items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description)),nextPageToken",
            publishedAfter=published_after,
            order='viewCount',
        )

    # 요청 실행 및 결과 저장
    response = request.execute()
    video_links = []

    # 검색 결과 순회
    for item in response['items']:
        video_id = item['id']['videoId']

        # 영상 정보 요청 설정
        request = youtube.videos().list(
            part="statistics",
            id=video_id,
            fields="items(id,statistics(viewCount))"
        )

        # 요청 실행 및 조회수 저장
        video_response = request.execute()
        video_views = int(video_response['items'][0]['statistics']['viewCount'])

        # 조회수 기준 필터링
        if video_views >= min_views:
            video_links.append(f'https://www.youtube.com/watch?v={video_id}')
        else:
            break

    return video_links

# 검색어, 조회수, 기간 설정
query = "나이키 신발"
min_views = 100000
days_ago = 30

# 영상 링크 가져오기
video_links = get_video_links(query, min_views, days_ago)

# 링크 출력
for link in video_links:
    print(link)
