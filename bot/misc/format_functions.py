from database import Ad, Topic, User


def user_ad_preview(title: str, description: str):
    return (f"{title}\n\n"
            f"{description}")


def admin_ad_preview(ad: Ad, user: User):
    return (f"{ad.title}\n\n"
            f"{ad.description}\n\n"
            f"СЕРВИСНАЯ ИНФОРМАЦИЯ\n"
            f"Категория: {Topic.get_topic_by_id(ad.topic_id).title}\n"
            f"Пользователь: {user.first_name} - @{user.username}")
