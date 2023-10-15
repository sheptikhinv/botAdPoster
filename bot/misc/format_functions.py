from database import Ad, Topic


def user_ad_preview(title: str, description: str):
    return (f"{title}\n\n"
            f"{description}")


def admin_ad_preview(ad: Ad):
    return (f"{ad.title}\n\n"
            f"{ad.description}\n\n"
            f"СЕРВИСНАЯ ИНФОРМАЦИЯ\n"
            f"Категория: {Topic.get_topic_by_id(ad.topic_id).title}")
