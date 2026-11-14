# Twitter推文获取CLI工具

基于Twitter GraphQL API的推文获取命令行工具。

## 快速开始

### 1. 配置认证

编辑 `auth.json`，填入你的认证信息：

```json
{
  "auth_token": "YOUR_AUTH_TOKEN",
  "ct0": "YOUR_CT0"
}
```

获取方法：
1. 登录 https://x.com
2. 打开浏览器开发者工具 (F12)
3. 切换到 Application → Cookies → x.com
4. 复制 `auth_token` 和 `ct0` 的值

### 2. 获取推文

```bash
# 获取单个用户推文
python main.py fetch PyTorch

# 获取多个用户推文
python main.py fetch PyTorch elonmusk

# 指定时间范围
python main.py fetch PyTorch --since 2026-04-01 --until 2026-04-05

# 指定输出文件和数量
python main.py fetch PyTorch --count 50 --output tweets.json
```

## 命令说明

| 命令 | 说明 |
|------|------|
| `fetch` | 获取推文 |
| `user` | 查看用户信息 |

## fetch 子命令

```bash
python main.py fetch USERNAME [USERNAME...] [选项]

可选参数:
  --since DATE          起始日期 (YYYY-MM-DD)
  --until DATE          结束日期 (YYYY-MM-DD)
  --count N             每次获取数量 (默认: 20)
  --output FILE         输出文件 (默认: result.json)
```

## user 子命令

```bash
python main.py user USERNAME
```

## 输出格式

结果保存为JSON格式：

```json
{
  "PyTorch": [
    {
      "id": "123456",
      "user": "PyTorch",
      "text": "推文内容...",
      "time": "2026-04-05 18:00:31",
      "url": "https://x.com/PyTorch/status/123456"
    }
  ]
}
```

## 注意事项

- 使用本地时间过滤（搜索API端点已过期）
- Cookie有效期有限，需定期更新
- 请遵守Twitter使用政策