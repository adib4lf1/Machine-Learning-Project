import asyncio
from TikTokApi import TikTokApi
from tiktok.helpers import logging

class Comment:
    def __init__(self) -> None:
        self.__result: dict = {}

    async def __get_comments(self, video_url: str, limit: int = 100):
        comments_data = []
        count = 0
        self.__result["video_id"] = "unknown"
        
        # headless=False artinya Browser MUNCUL
        async with TikTokApi() as api:
            await api.create_sessions(num_sessions=1, sleep_after=3, headless=False)
            
            try:
                video = api.video(url=video_url)
                
                logging.info("Browser terbuka. SAYA BERI WAKTU 60 DETIK UNTUK ANDA LOGIN.")
                logging.info(">>> SILAKAN LOGIN TIKTOK DI BROWSER ITU SEKARANG <<<")
                logging.info(">>> JIKA SUDAH LOGIN, TUNGGU SAJA SCRIPT LANJUT SENDIRI <<<")
                
                # --- WAKTU JEDA UNTUK LOGIN (60 DETIK) ---
                for i in range(60, 0, -1):
                    if i % 10 == 0:
                        print(f"\r[ Menunggu Anda Login... {i} detik lagi ]", end="", flush=True)
                    await asyncio.sleep(1)
                print("\n[ Waktu habis, mulai mengambil data... ]")
                
                # Coba ambil info video setelah login
                try:
                    video_info = await video.info()
                    self.__result["video_id"] = video_info.get('id', 'unknown')
                    self.__result["desc"] = video_info.get('desc', 'no desc')
                    self.__result["author"] = video_info.get('author', {}).get('uniqueId', 'unknown')
                except Exception:
                    logging.warning("Info video skip, lanjut komentar...")

                logging.info(f"Target: {limit} komentar.")

                # Loop pengambilan komentar
                async for comment in video.comments(count=limit):
                    try:
                        user_obj = comment.author
                        username = getattr(user_obj, 'unique_id', None) or getattr(user_obj, 'uniqueId', 'Hidden User')
                        likes = getattr(comment, 'likes_count', 0)
                        
                        comments_data.append({
                            "username": username,
                            "text": comment.text,
                            "likes": likes,
                            "time": comment.create_time
                        })
                        count += 1
                        
                        if count % 20 == 0:
                            print(f"\r[+] Berhasil mengambil {count} komentar...", end="", flush=True)
                            
                    except Exception:
                        continue

            except Exception as e:
                logging.error(f"\nStop/Error Utama: {e}")
                logging.info("Menyimpan data yang berhasil didapat sejauh ini...")
            
            finally:
                print("") 
                self.__result["total_scraped"] = count
                self.__result["comments"] = comments_data
                
        return self.__result

    def execute(self, video_url: str, limit: int):
        return asyncio.run(self.__get_comments(video_url, limit))