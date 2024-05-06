import glob
import json

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

# 将 JSON 字符串写入 words.js 文件
with open('words.js', 'w', encoding='utf-8') as f:
    f.write('var words = ' + json_str + ';')