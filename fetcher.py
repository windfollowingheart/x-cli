"""
Twitter推文获取核心模块
"""

import requests
import json
import time
import sys
from datetime import datetime

# Windows下设置UTF-8编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Twitter GraphQL API 相关常量
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
GRAPHQL_URL = "https://x.com/i/api/graphql/"

# GraphQL 端点
USER_BY_SCREEN_NAME = "-oaLodhGbbnzJBACb1kk2Q/UserByScreenName"
USER_TWEETS = "6QdSuZ5feXxOadEdXa4XZg/UserWithProfileTweetsQueryV2"

GQL_FEATURES = {
    "android_ad_formats_media_component_render_overlay_enabled": False,
    "android_graphql_skip_api_media_color_palette": False,
    "android_professional_link_spotlight_display_enabled": False,
    "articles_api_enabled": False,
    "articles_preview_enabled": True,
    "blue_business_profile_image_shape_enabled": False,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "commerce_android_shop_module_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "creator_subscriptions_quote_tweet_preview_enabled": False,
    "creator_subscriptions_subscription_count_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "grok_android_analyze_trend_fetch_enabled": False,
    "grok_translations_community_note_auto_translation_is_enabled": False,
    "grok_translations_community_note_translation_is_enabled": False,
    "grok_translations_post_auto_translation_is_enabled": False,
    "grok_translations_timeline_user_bio_auto_translation_is_enabled": False,
    "hidden_profile_likes_enabled": False,
    "highlights_tweets_tab_ui_enabled": False,
    "immersive_video_status_linkable_timestamps": False,
    "interactive_text_enabled": False,
    "longform_notetweets_consumption_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "longform_notetweets_richtext_consumption_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "mobile_app_spotlight_module_enabled": False,
    "payments_enabled": False,
    "post_ctas_fetch_enabled": True,
    "premium_content_api_read_enabled": False,
    "profile_label_improvements_pcf_label_in_post_enabled": True,
    "profile_label_improvements_pcf_label_in_profile_enabled": False,
    "responsive_web_edit_tweet_api_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_grok_analysis_button_from_backend": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
    "responsive_web_grok_analyze_post_followups_enabled": True,
    "responsive_web_grok_annotations_enabled": True,
    "responsive_web_grok_community_note_auto_translation_is_enabled": False,
    "responsive_web_grok_image_annotation_enabled": True,
    "responsive_web_grok_imagine_annotation_enabled": True,
    "responsive_web_grok_share_attachment_enabled": True,
    "responsive_web_grok_show_grok_translated_post": False,
    "responsive_web_jetfuel_frame": True,
    "responsive_web_media_download_video_enabled": False,
    "responsive_web_profile_redirect_enabled": False,
    "responsive_web_text_conversations_enabled": False,
    "responsive_web_twitter_article_notes_tab_enabled": False,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "responsive_web_twitter_blue_verified_badge_is_enabled": True,
    "rweb_lists_timeline_redesign_enabled": True,
    "rweb_tipjar_consumption_enabled": True,
    "rweb_video_screen_enabled": False,
    "rweb_video_timestamps_enabled": False,
    "spaces_2022_h2_clipping": True,
    "spaces_2022_h2_spaces_communities": True,
    "standardized_nudges_misinfo": True,
    "subscriptions_feature_can_gift_premium": False,
    "subscriptions_verification_info_enabled": True,
    "subscriptions_verification_info_is_identity_verified_enabled": False,
    "subscriptions_verification_info_reason_enabled": True,
    "subscriptions_verification_info_verified_since_enabled": True,
    "super_follow_badge_privacy_enabled": False,
    "super_follow_exclusive_tweet_notifications_enabled": False,
    "super_follow_tweet_api_enabled": False,
    "super_follow_user_api_enabled": False,
    "tweet_awards_web_tipping_enabled": False,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "tweetypie_unmention_optimization_enabled": False,
    "unified_cards_ad_metadata_container_dynamic_card_content_query_enabled": False,
    "unified_cards_destination_url_params_enabled": False,
    "verified_phone_label_enabled": False,
    "vibe_api_enabled": False,
    "view_counts_everywhere_api_enabled": True,
    "hidden_profile_subscriptions_enabled": False,
}


class TweetFetcher:
    """推文获取器"""

    def __init__(self, auth_token, ct0, count=20):
        self.auth_token = auth_token
        self.ct0 = ct0
        self.count = count

    def get_headers(self):
        """构建请求头"""
        return {
            "accept": "*/*",
            "accept-encoding": "gzip",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {BEARER_TOKEN}",
            "content-type": "application/json",
            "cookie": f"auth_token={self.auth_token}; ct0={self.ct0}",
            "x-csrf-token": self.ct0,
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en",
            "x-twitter-active-user": "yes",
            "origin": "https://x.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }

    def get_user_id(self, username):
        """获取用户ID"""
        variables = {"screen_name": username, "withGrokTranslatedBio": False}
        url = f"{GRAPHQL_URL}{USER_BY_SCREEN_NAME}"
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(GQL_FEATURES),
            "fieldToggles": json.dumps({
                "withArticleRichContentState": True,
                "withArticlePlainText": False,
                "withGrokAnalyze": False,
                "withDisallowedReplyControls": False,
            }),
        }

        try:
            resp = requests.get(url, headers=self.get_headers(), params=params)
            if resp.status_code != 200:
                print(f"[{username}] 获取用户ID失败: {resp.status_code}")
                return None
            data = resp.json()
            user_result = data.get("data", {}).get("user", {}).get("result", {})
            user_id = user_result.get("rest_id")
            if user_id:
                print(f"[{username}] 用户ID: {user_id}")
                return user_id
            else:
                print(f"[{username}] 解析用户ID失败")
                return None
        except Exception as e:
            print(f"[{username}] 获取用户ID出错: {e}")
            return None

    def get_user_tweets(self, user_id, username):
        """获取用户推文"""
        variables = {"rest_id": user_id, "count": self.count}
        url = f"{GRAPHQL_URL}{USER_TWEETS}"
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(GQL_FEATURES),
        }

        try:
            resp = requests.get(url, headers=self.get_headers(), params=params)
            if resp.status_code != 200:
                print(f"[{username}] 获取推文失败: {resp.status_code}")
                return []
            data = resp.json()

            # 解析推文timeline
            timeline_data = (
                data.get("data", {})
                .get("user_result", {})
                .get("result", {})
                .get("timeline_response", {})
                .get("timeline", {})
            )
            if not timeline_data:
                print(f"[{username}] 解析推文timeline失败")
                return []

            instructions = timeline_data.get("instructions", [])
            tweets = []

            for instruction in instructions:
                instr_type = instruction.get("__typename") or instruction.get("type")
                if instr_type == "TimelineAddEntries":
                    entries = instruction.get("entries", [])
                    for entry in entries:
                        content = entry.get("content", {})
                        content_type = content.get("__typename")

                        if content_type == "TimelineTimelineItem":
                            inner_content = content.get("content", {})
                            tweet_data = inner_content.get("tweet_results", {}).get("result", {})

                            if tweet_data and tweet_data.get("__typename") != "TweetTombstone":
                                tweet_info = self.parse_tweet(tweet_data, username)
                                if tweet_info:
                                    tweets.append(tweet_info)

            return tweets
        except Exception as e:
            print(f"[{username}] 获取推文出错: {e}")
            return []

    def parse_tweet(self, tweet_data, username):
        """解析推文内容"""
        try:
            tweet_id = tweet_data.get("rest_id")
            legacy = tweet_data.get("legacy", {})
            details = tweet_data.get("details", {})

            text = legacy.get("full_text", "") or details.get("full_text", "")

            if not text:
                note_tweet = tweet_data.get("note_tweet", {})
                if note_tweet:
                    text = (
                        note_tweet.get("note_tweet_results", {})
                        .get("result", {})
                        .get("text", "")
                    )

            created_at_ms = legacy.get("created_at_ms") or details.get("created_at_ms", 0)
            if created_at_ms:
                formatted_time = datetime.fromtimestamp(created_at_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
            else:
                created_at = legacy.get("created_at", "")
                try:
                    dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = created_at

            return {
                "id": tweet_id,
                "user": username,
                "text": text,
                "time": formatted_time,
                "url": f"https://x.com/{username}/status/{tweet_id}",
            }
        except Exception as e:
            print(f"解析推文出错: {e}")
            return None

    def filter_tweets_by_time(self, tweets, since, until):
        """按时间范围过滤推文"""
        filtered = []
        for tweet in tweets:
            tweet_time = tweet.get("time", "")
            if not tweet_time:
                continue
            tweet_date = tweet_time.split(" ")[0]
            if since and tweet_date < since:
                continue
            if until and tweet_date > until:
                continue
            filtered.append(tweet)
        return filtered

    def fetch(self, users, since="", until="", output="result.json"):
        """获取指定用户的推文"""
        print("=" * 50)
        print("开始获取推文...")

        if since or until:
            print(f"时间范围: {since or '不限制'} ~ {until or '不限制'}")
            print("使用本地时间过滤")

        print("=" * 50)

        all_results = {}

        # 获取用户ID
        user_ids = {}
        for username in users:
            user_id = self.get_user_id(username)
            if user_id:
                user_ids[username] = user_id
            time.sleep(1)

        print(f"\n成功获取 {len(user_ids)} 个用户ID")
        print("-" * 50)

        # 获取推文
        for username, user_id in user_ids.items():
            print(f"\n[{username}] 获取推文...")
            tweets = self.get_user_tweets(user_id, username)
            print(f"[{username}] 获取到 {len(tweets)} 条推文")

            # 时间过滤
            if (since or until) and tweets:
                tweets = self.filter_tweets_by_time(tweets, since, until)
                print(f"[{username}] 过滤后保留 {len(tweets)} 条推文")

            if tweets:
                tweets.sort(key=lambda x: x["time"], reverse=True)
                print(f"[{username}] 最新推文:")
                for tweet in tweets[:3]:
                    print(f"  [{tweet['time']}]")
                    print(f"  {tweet['text'][:80]}{'...' if len(tweet['text']) > 80 else ''}")
                    print(f"  链接: {tweet['url']}")
                    print()
                all_results[username] = tweets
            else:
                print(f"[{username}] 未获取到推文")
                all_results[username] = []

            time.sleep(2)

        # 保存结果
        with open(output, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到 {output}")

        return all_results