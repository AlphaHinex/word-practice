import glob
import json
import random
import string
import os

# 清理根路径下 words*.js 文件
files = glob.glob("words*.js")
for file in files:
    os.remove(file)

# 获取 words 目录下的所有 json 文件
files = glob.glob("words/**/*.json", recursive=True)
files.sort(key=lambda x: (os.path.dirname(x), os.path.basename(x)))

words = []

new_options = 'var newOptions = [];'
# 遍历每个文件
for file in files:
    # option 使用文件路径（不包括 words/），目录之间使用 - 分割
    option = os.path.dirname(file)[6:].replace('\\', '/') \
             + '/' + os.path.basename(file).replace('.json', '')
    new_options += f'''var option = document.createElement('option');
            option.value = '{option}';
            option.textContent = '{option}';
            newOptions.push(option);'''
    # Check if the file is empty
    if os.path.getsize(file) == 0:
        print(f"Skipping empty file: {file}")
        continue
    # 读取文件内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        # 解析 content 为 json 对象后，根据 option 修改 json 对象的 tag 属性
        json_arr = json.loads(content)
        for item in json_arr:
            item['tag'] = option
        # 添加到 words 列表
        words.extend(json_arr)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file}: {e}")

# 将 words 列表转换为 JSON 字符串
json_str = json.dumps(words, indent=4, ensure_ascii=False)

# Generate a random string of 5 characters
random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
words_file = f'words-{random_string}.js'

# 将 JSON 字符串写入 words.js 文件
with open(words_file, 'w', encoding='utf-8') as f:
    f.write('var words = ' + json_str + ';')
    f.write(new_options)

# 修改 index.html 文件中引用的 words-*.js 文件名
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    x = content.find('"words')
    y = content.find('.js"', x)
    old_words_file = content[x:y+4]
    content = content.replace(old_words_file, f'"{words_file}"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 生成音频教材索引 audio-books.js
# 扫描 words/**/audio/*.mp3，教材名称取同目录下 PDF 文件名（去掉 .pdf），无 PDF 则用目录名
audio_books = []
audio_dirs = sorted(glob.glob("words/**/audio", recursive=True))
for audio_dir in audio_dirs:
    book_dir = os.path.dirname(audio_dir)
    mp3_files = sorted(glob.glob(os.path.join(audio_dir, "*.mp3")))
    if not mp3_files:
        continue
    # 查找同目录下的 PDF 文件作为教材名称
    pdf_files = glob.glob(os.path.join(book_dir, "*.pdf"))
    if pdf_files:
        book_name = os.path.splitext(os.path.basename(pdf_files[0]))[0]
    else:
        book_name = os.path.basename(book_dir)
    rel_dir = book_dir[6:].replace('\\', '/')  # 去掉 words/ 前缀
    audio_books.append({
        "name": book_name,
        "dir": rel_dir,
        "files": [{"name": os.path.basename(f)} for f in mp3_files]
    })

audio_books_json = json.dumps(audio_books, indent=4, ensure_ascii=False)
with open('audio-books.js', 'w', encoding='utf-8') as f:
    f.write('var audioBooks = ' + audio_books_json + ';')
