import os
import argparse
from json import dumps
from tiktok import Comment
from tiktok.helpers import logging

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument("--url", '-u', type=str, required=True, help="Link Video TikTok")
    # Hapus argument token
    argp.add_argument("--limit", '-l', type=int, default=100, help="Jumlah komentar")
    argp.add_argument("--output", '-o', type=str, default='data')
    args = argp.parse_args()

    # Inisialisasi Class (Tanpa Token)
    scraper = Comment()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    logging.info("Membuka browser otomatis...")
    
    data = scraper.execute(args.url, args.limit)

    file_name = data.get('video_id', 'tiktok_output')
    output_path = f'{args.output}/{file_name}.json'
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(dumps(data, ensure_ascii=False, indent=2))
        
    logging.info(f'Selesai! {data.get("total_scraped", 0)} komentar tersimpan di: {output_path}')