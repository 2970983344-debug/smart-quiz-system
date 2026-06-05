# Python 刷题题库系统

一个适合上传 GitHub 的命令行刷题系统，使用本地 JSON 文件保存题目、错题本、收藏题目和做题记录，不需要数据库。

## 项目结构

```text
quiz_system/
├── main.py
├── quiz.py
├── storage.py
├── statistics.py
├── data/
│   ├── questions.json
│   ├── wrong_questions.json
│   ├── favorites.json
│   └── records.json
├── README.md
└── requirements.txt
```

## 功能

- 开始刷题
- 随机练习
- 按分类练习
- 单选题、多选题、判断题
- 提交答案后自动判断对错
- 显示正确答案和解析
- 答错自动加入错题本
- 收藏题目
- 查看错题本
- 查看收藏题目
- 查看学习统计

## 题库分类

- Python基础
- 计算机网络
- 数据结构
- 操作系统
- 数据库

## 运行方式

```bash
python main.py
```

如果你的系统中 Python 命令是 `python3`：

```bash
python3 main.py
```

## 数据文件说明

`data/questions.json` 保存题库。每道题格式如下：

```json
{
  "id": "PY001",
  "category": "Python基础",
  "type": "single",
  "title": "Python 中用于定义函数的关键字是？",
  "options": {
    "A": "func",
    "B": "def",
    "C": "function",
    "D": "lambda"
  },
  "answer": "B",
  "explanation": "Python 使用 def 关键字定义普通函数。"
}
```

题型字段：

- `single`：单选题
- `multiple`：多选题，答案可写为 `["A", "B"]`
- `judge`：判断题，答案使用 `T` 或 `F`

其他数据文件：

- `data/wrong_questions.json`：保存错题 ID
- `data/favorites.json`：保存收藏题 ID
- `data/records.json`：保存每次做题记录

## 学习统计

统计内容包括：

- 总做题数
- 正确题数
- 错误题数
- 正确率
- 各分类正确率

## 说明

本项目不依赖第三方库，`requirements.txt` 仅作为 GitHub 项目规范文件保留。
