from src.channel import Channel
import os
from googleapiclient.discovery import build


class Video:

    __API_KEY: str = os.getenv('API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__API_KEY)

    def __init__(self, video_id: str):
        self.__video_id = video_id
        if self.__verify_video_id(video_id) != 0:

            self.__video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=self.__video_id).execute()
            self.__title = self.__video_response['items'][0]['snippet']['title']
            self.__video_url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.__view_count = self.__video_response['items'][0]['statistics']['viewCount']
            self.__like_count = self.__video_response['items'][0]['statistics']['likeCount']
        else:
            self.__title = None
            self.__video_url = None
            self.__view_count = None
            self.__like_count = None

    def __str__(self) -> str:
        return self.__title

    def __verify_video_id(self, video_id):
        video_response = self.__youtube.videos().list(part='status', id=video_id).execute()
        search_count = video_response['pageInfo']['totalResults']
        return search_count

    @property
    def video_id(self) -> str:
        return self.__video_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def video_url(self) -> str:
        return self.__video_url

    @property
    def view_count(self) -> str:
        return self.__view_count

    @property
    def like_count(self) -> str:
        return self.__like_count


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                     maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        if video_id in video_ids:
            super().__init__(video_id)
            self.playlist_id = playlist_id
        else:
            raise ValueError(f"Видео {video_id} нету в плейлисте {playlist_id}")

    def __str__(self):
        return self.video_title
