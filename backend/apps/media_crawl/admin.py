# -*- coding: utf-8 -*-
"""Admin configuration for media crawl models."""

from django.contrib import admin

from .models import (
    # Bilibili
    BilibiliVideo,
    BilibiliVideoComment,
    BilibiliUpInfo,
    BilibiliContactInfo,
    BilibiliUpDynamic,
    # Douyin
    DouyinAweme,
    DouyinAwemeComment,
    DyCreator,
    # Kuaishou
    KuaishouVideo,
    KuaishouVideoComment,
    # Weibo
    WeiboNote,
    WeiboNoteComment,
    WeiboCreator,
    # Xiaohongshu
    XhsCreator,
    XhsNote,
    XhsNoteComment,
    # Tieba
    TiebaNote,
    TiebaComment,
    TiebaCreator,
    # Zhihu
    ZhihuContent,
    ZhihuComment,
    ZhihuCreator,
)


class MultiDBModelAdmin(admin.ModelAdmin):
    """Base admin class that uses the mysql database."""

    using = "mysql"

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


# ============== Bilibili ==============
@admin.register(BilibiliVideo)
class BilibiliVideoAdmin(MultiDBModelAdmin):
    list_display = ["id", "video_id", "title", "user_id", "nickname", "create_time"]
    list_filter = ["video_type"]
    search_fields = ["video_id", "title", "nickname"]
    ordering = ["-create_time"]


@admin.register(BilibiliVideoComment)
class BilibiliVideoCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "video_id", "nickname", "create_time"]
    search_fields = ["comment_id", "nickname", "content"]
    ordering = ["-create_time"]


@admin.register(BilibiliUpInfo)
class BilibiliUpInfoAdmin(MultiDBModelAdmin):
    list_display = ["id", "user_id", "nickname", "total_fans", "total_liked"]
    search_fields = ["user_id", "nickname"]


@admin.register(BilibiliContactInfo)
class BilibiliContactInfoAdmin(MultiDBModelAdmin):
    list_display = ["id", "up_id", "fan_id", "up_name", "fan_name"]
    search_fields = ["up_name", "fan_name"]


@admin.register(BilibiliUpDynamic)
class BilibiliUpDynamicAdmin(MultiDBModelAdmin):
    list_display = ["id", "dynamic_id", "user_name", "type", "pub_ts"]
    search_fields = ["dynamic_id", "user_name", "text"]


# ============== Douyin ==============
@admin.register(DouyinAweme)
class DouyinAwemeAdmin(MultiDBModelAdmin):
    list_display = ["id", "aweme_id", "title", "nickname", "create_time"]
    list_filter = ["aweme_type"]
    search_fields = ["aweme_id", "title", "nickname"]
    ordering = ["-create_time"]


@admin.register(DouyinAwemeComment)
class DouyinAwemeCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "aweme_id", "nickname", "create_time"]
    search_fields = ["comment_id", "nickname", "content"]


@admin.register(DyCreator)
class DyCreatorAdmin(MultiDBModelAdmin):
    list_display = ["id", "user_id", "nickname", "fans", "videos_count"]
    search_fields = ["user_id", "nickname"]


# ============== Kuaishou ==============
@admin.register(KuaishouVideo)
class KuaishouVideoAdmin(MultiDBModelAdmin):
    list_display = ["id", "video_id", "title", "nickname", "create_time"]
    search_fields = ["video_id", "title", "nickname"]
    ordering = ["-create_time"]


@admin.register(KuaishouVideoComment)
class KuaishouVideoCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "video_id", "nickname", "create_time"]
    search_fields = ["comment_id", "nickname", "content"]


# ============== Weibo ==============
@admin.register(WeiboNote)
class WeiboNoteAdmin(MultiDBModelAdmin):
    list_display = ["id", "note_id", "nickname", "create_time"]
    search_fields = ["note_id", "nickname", "content"]
    ordering = ["-create_time"]


@admin.register(WeiboNoteComment)
class WeiboNoteCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "note_id", "nickname", "create_time"]
    search_fields = ["comment_id", "nickname", "content"]


@admin.register(WeiboCreator)
class WeiboCreatorAdmin(MultiDBModelAdmin):
    list_display = ["id", "user_id", "nickname", "fans"]
    search_fields = ["user_id", "nickname"]


# ============== Xiaohongshu ==============
@admin.register(XhsCreator)
class XhsCreatorAdmin(MultiDBModelAdmin):
    list_display = ["id", "user_id", "nickname", "fans", "interaction"]
    search_fields = ["user_id", "nickname"]


@admin.register(XhsNote)
class XhsNoteAdmin(MultiDBModelAdmin):
    list_display = ["id", "note_id", "title", "nickname", "time"]
    list_filter = ["type"]
    search_fields = ["note_id", "title", "nickname"]
    ordering = ["-time"]


@admin.register(XhsNoteComment)
class XhsNoteCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "note_id", "nickname", "create_time"]
    search_fields = ["comment_id", "nickname", "content"]


# ============== Tieba ==============
@admin.register(TiebaNote)
class TiebaNoteAdmin(MultiDBModelAdmin):
    list_display = ["id", "note_id", "title", "user_nickname", "tieba_name", "publish_time"]
    search_fields = ["note_id", "title", "user_nickname", "tieba_name"]


@admin.register(TiebaComment)
class TiebaCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "note_id", "user_nickname", "publish_time"]
    search_fields = ["comment_id", "user_nickname", "content"]


@admin.register(TiebaCreator)
class TiebaCreatorAdmin(MultiDBModelAdmin):
    list_display = ["id", "user_id", "nickname", "fans"]
    search_fields = ["user_id", "nickname"]


# ============== Zhihu ==============
@admin.register(ZhihuContent)
class ZhihuContentAdmin(MultiDBModelAdmin):
    list_display = ["id", "content_id", "title", "user_nickname", "content_type", "created_time"]
    list_filter = ["content_type"]
    search_fields = ["content_id", "title", "user_nickname"]


@admin.register(ZhihuComment)
class ZhihuCommentAdmin(MultiDBModelAdmin):
    list_display = ["id", "comment_id", "content_id", "user_nickname", "publish_time"]
    search_fields = ["comment_id", "user_nickname", "content"]


@admin.register(ZhihuCreator)
class ZhihuCreatorAdmin(MultiDBModelAdmin):
    list_display = ["id", "user_id", "user_nickname", "fans", "anwser_count"]
    search_fields = ["user_id", "user_nickname"]


# ============== Analysis Report ==============
from .models import AnalysisReport


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    """Admin for analysis reports - uses default PostgreSQL database."""

    list_display = ["id", "title", "platform", "source_keyword", "record_count", "created_at"]
    list_filter = ["platform"]
    search_fields = ["title", "source_keyword"]
    ordering = ["-created_at"]
    readonly_fields = ["id", "created_at"]

