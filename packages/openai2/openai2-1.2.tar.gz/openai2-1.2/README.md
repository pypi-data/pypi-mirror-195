# 项目描述

根据openai官方接口‘openai’改造的‘openai2’，比官方接口更好用一点。

# 安装

安装：`pip install openai2`

# 获取api_key

[获取链接1](https://platform.openai.com/account/api-keys)

[获取链接2](https://www.baidu.com/s?wd=%E8%8E%B7%E5%8F%96%20openai%20api_key)

# 语法

导入：

```python
from openai2 import Chat
```

创建会话：

```python
api_key = 'api_key'  # 更换成自己的api_key

session_1 = Chat(api_key=api_key, model="gpt-3.5-turbo")

session_2 = Chat(api_key=api_key, model="gpt-3.5-turbo")
```

对话：

```python
session_1.request('数字1的后面是哪个数字?')
# >>> 2

session_2.request('数字101的后面是哪个数字?')
# >>> 102

session_1.request('再往后是哪个数字?')
# >>> 3

session_2.request('再往后是哪个数字?')
# >>> 103
```
