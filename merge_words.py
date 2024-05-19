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

words = []

# 遍历每个文件
for file in files:
    # 读取文件内容
    with open(file, 'r') as f:
        content = f.read()

    # 解析 JSON 并添加到 words 列表
    words.extend(json.loads(content))

# 将 words 列表转换为 JSON 字符串
json_str = json.dumps(words, indent=4, ensure_ascii=False)

# Generate a random string of 5 characters
random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
words_file = f'words-{random_string}.js'

# 将 JSON 字符串写入 words.js 文件
with open(words_file, 'w', encoding='utf-8') as f:
    f.write('var words = ' + json_str + ';')

# 修改 index.html 文件中应用的 words-*.js 文件名
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    x = content.find('"words')
    y = content.find('.js"', x)
    old_words_file = content[x:y+4]
    content = content.replace(old_words_file, f'"{words_file}"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
