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
# files.sort(key=os.path.basename, reverse=True)

words = []

new_options = '<!-- Add your tags here -->'
# 遍历每个文件
for file in files:
    # option 使用文件路径（不包括 words/），目录之间使用 - 分割
    option = os.path.dirname(file)[6:].replace('\\', '-').replace('/', '-') \
             + '-' + os.path.basename(file).replace('.json', '')
    new_options += f'<option value="{option}">{option}</option>'
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
new_options += '<!-- tag end -->'

# 将 words 列表转换为 JSON 字符串
json_str = json.dumps(words, indent=4, ensure_ascii=False)

# Generate a random string of 5 characters
random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
words_file = f'words-{random_string}.js'

# 将 JSON 字符串写入 words.js 文件
with open(words_file, 'w', encoding='utf-8') as f:
    f.write('var words = ' + json_str + ';')

# 修改 index.html 文件中引用的 words-*.js 文件名
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    x = content.find('"words')
    y = content.find('.js"', x)
    old_words_file = content[x:y+4]
    content = content.replace(old_words_file, f'"{words_file}"')

    x = content.find('<!-- Add your tags here -->')
    y = content.find('<!-- tag end -->', x)
    old_options = content[x:y+16]
    content = content.replace(old_options, new_options)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
