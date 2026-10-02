import os
import sys
import re
import django

# Setup Django environment
sys.path.append('/app')
sys.path.append('/app/apps')
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend/apps'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sepbot.settings')
django.setup()

from knowledge.models import KnowledgeArticle, Image

EBOOK_DIR = '/app/media/knowledge/Ebook'
if not os.path.exists(EBOOK_DIR):
    EBOOK_DIR = os.path.join(os.path.dirname(__file__), '../backend/media/knowledge/Ebook')

def run():
    print(f"Scanning Ebook directory: {EBOOK_DIR}")
    if not os.path.exists(EBOOK_DIR):
        print("Ebook directory not found!")
        return

    articles = list(KnowledgeArticle.objects.order_by('id'))
    if not articles:
        print("No articles found in DB!")
        return

    # Map chapter number (1 to 8) to Article instance
    chapter_map = {}
    for art in articles:
        if 'บทที่ 1' in art.title:
            chapter_map[1] = art
        elif 'บทที่ 2' in art.title:
            chapter_map[2] = art
        elif 'บทที่ 3' in art.title:
            chapter_map[3] = art
        elif 'บทที่ 4' in art.title:
            chapter_map[4] = art
        elif 'บทที่ 5' in art.title:
            chapter_map[5] = art
        elif 'บทที่ 6' in art.title:
            chapter_map[6] = art
        elif 'บทที่ 7' in art.title:
            chapter_map[7] = art
        elif 'บทที่ 8' in art.title:
            chapter_map[8] = art

    files = sorted(os.listdir(EBOOK_DIR))
    linked_count = 0

    for fname in files:
        if not fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Extract sequence number and chapter number
        # e.g., "1.1.1.png" -> page 1, chapter 1
        # "10.4.2.png" -> page 10, chapter 4
        # "40.png" -> page 40
        match = re.search(r'^(\d+)(?:\.(\d+))?', fname)
        if not match:
            continue

        seq_num = int(match.group(1))
        chap_num = int(match.group(2)) if match.group(2) else None

        # Fallback chapter detection based on page range if chap_num is None
        if chap_num is None:
            if seq_num in [1, 2, 3, 4]:
                chap_num = 1
            elif seq_num == 5:
                chap_num = 2
            elif seq_num in [6, 7, 8]:
                chap_num = 3
            elif 9 <= seq_num <= 14:
                chap_num = 4
            elif 15 <= seq_num <= 17:
                chap_num = 5
            elif 18 <= seq_num <= 22:
                chap_num = 6
            elif 23 <= seq_num <= 34:
                chap_num = 7
            elif 35 <= seq_num <= 39:
                chap_num = 8
            else: # 40, 41, 42, 43, 44
                chap_num = 8

        target_article = chapter_map.get(chap_num, articles[0])
        rel_path = f"knowledge/Ebook/{fname}"

        img_obj, created = Image.objects.update_or_create(
            article=target_article,
            image=rel_path,
            defaults={
                "caption": f"หน้า {seq_num} - ภาพอินโฟกราฟิกคู่มือจุฬาฯ ({fname})",
                "order": seq_num
            }
        )
        linked_count += 1
        print(f"Linked [{fname}] -> Article: '{target_article.title[:30]}...' (Page #{seq_num})")

    print(f"\nSuccessfully linked {linked_count} infographic images to Knowledge Articles!")

if __name__ == '__main__':
    run()
