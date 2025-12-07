import os
import argparse
from json import dumps
from tiktok import Comment
from tiktok.helpers import logging

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    # Contoh URL Default
    argp.add_argument("--url", '-u', type=str, required=True, help="Masukkan Link Video TikTok")
    argp.add_argument("--token", '-t', type=str, default=None, help="ms_token (Optional)")
    argp.add_argument("--output", '-o', type=str, default='data')
    args = argp.parse_args()

    # Inisialisasi Class
    scraper = Comment(ms_token=args.token)

    # Buat folder output jika belum ada
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    logging.info("Memulai proses scraping...")
    
    # Jalankan Scraper
    data = scraper.execute(args.url)

    # Ambil ID video untuk nama file (jika gagal ambil ID, pakai 'output')
    file_name = data.get('video_id', 'tiktok_output')

    # Simpan ke JSON
    output_path = f'{args.output}/{file_name}.json'
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(dumps(data, ensure_ascii=False, indent=2))
        
    logging.info(f'Selesai! Data tersimpan di: {output_path}')