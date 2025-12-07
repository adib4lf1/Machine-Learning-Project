import asyncio
import os
from TikTokApi import TikTokApi
from tiktok.helpers import logging

class Comment:
    def __init__(self, ms_token: str = None) -> None:
        # ms_token adalah cookie opsional untuk stabilitas
        self.ms_token = ms_token
        self.__result: dict = {}

    async def __get_comments(self, video_url: str):
        comments_data = []
        
        # Menggunakan Context Manager untuk TikTokApi
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[self.ms_token], num_sessions=1, sleep_after=3)
            
            try:
                video = api.video(url=video_url)
                
                # Mengambil info video dasar
                video_info = await video.info()
                self.__result["video_id"] = video_info['id']
                self.__result["desc"] = video_info['desc']
                self.__result["author"] = video_info['author']['uniqueId']
                self.__result["post_url"] = video_url
                
                logging.info(f"Mengambil komentar untuk video: {self.__result['desc'][:30]}...")

                # Loop komentar (ambil 50 komentar pertama sebagai contoh agar tidak terlalu lama)
                count = 0
                async for comment in video.comments(count=50):
                    comments_data.append({
                        "username": comment.author.uniqueId,
                        "text": comment.text,
                        "likes": comment.likes_count,
                        "time": comment.create_time
                    })
                    count += 1
                
                self.__result["total_scraped"] = count
                self.__result["comments"] = comments_data
                
            except Exception as e:
                logging.error(f"Error scraping TikTok: {e}")
                
        return self.__result

    def execute(self, video_url: str):
        # Membungkus fungsi async agar bisa dipanggil secara sync di main.py
        return asyncio.run(self.__get_comments(video_url))