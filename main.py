"""
Twitter推文获取CLI工具

使用方法:
    python cli/main.py fetch USERNAME [USERNAME...] [--since DATE] [--until DATE] [--count N] [--output FILE]
    python cli/main.py user USERNAME
"""

import argparse
import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.fetcher import TweetFetcher

AUTH_FILE = os.path.join(os.path.dirname(__file__), "auth.json")


def load_auth():
    """加载认证信息"""
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_fetch(args):
    """获取推文命令"""
    auth = load_auth()
    auth_token = auth.get("auth_token")
    ct0 = auth.get("ct0")

    if not auth_token or not ct0:
        print("错误: 请在 cli/auth.json 中设置 auth_token 和 ct0!")
        return 1

    users = args.users
    if not users:
        print("错误: 请指定至少一个用户名!")
        return 1

    output = args.output or "result.json"

    fetcher = TweetFetcher(auth_token, ct0, args.count)
    fetcher.fetch(users, args.since or "", args.until or "", output)
    return 0


def cmd_user(args):
    """查看用户信息"""
    auth = load_auth()
    auth_token = auth.get("auth_token")
    ct0 = auth.get("ct0")

    if not auth_token or not ct0:
        print("错误: 请在 cli/auth.json 中设置 auth_token 和 ct0!")
        return 1

    fetcher = TweetFetcher(auth_token, ct0)
    user_id = fetcher.get_user_id(args.username)

    if user_id:
        print(f"用户: {args.username}")
        print(f"ID: {user_id}")
        return 0
    else:
        print(f"获取用户 {args.username} 信息失败")
        return 1


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="Twitter推文获取CLI工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  获取推文:
    python cli/main.py fetch PyTorch
    python cli/main.py fetch PyTorch elonmusk --since 2026-04-01 --until 2026-04-05
    python cli/main.py fetch PyTorch --count 50 --output tweets.json

  查看用户:
    python cli/main.py user PyTorch

  认证配置:
    编辑 cli/auth.json 设置 auth_token 和 ct0
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # fetch 子命令
    fetch_parser = subparsers.add_parser("fetch", help="获取推文")
    fetch_parser.add_argument("users", nargs="+", help="要获取的用户名列表")
    fetch_parser.add_argument("--since", help="起始日期 (YYYY-MM-DD)")
    fetch_parser.add_argument("--until", help="结束日期 (YYYY-MM-DD)")
    fetch_parser.add_argument(
        "--count", type=int, default=20, help="每次获取的推文数量 (默认: 20)"
    )
    fetch_parser.add_argument("--output", "-o", help="输出文件路径 (默认: result.json)")

    # user 子命令
    user_parser = subparsers.add_parser("user", help="查看用户信息")
    user_parser.add_argument("username", help="用户名")

    args = parser.parse_args()

    if args.command == "fetch":
        return cmd_fetch(args)
    elif args.command == "user":
        return cmd_user(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
