# -*- coding: utf-8 -*-
"""Analysis Report model for storing AI-generated reports."""

import uuid

from django.db import models


class AnalysisReport(models.Model):
    """分析报告模型 - 存储 AI 生成的分析报告。"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="报告标题")
    platform = models.CharField(max_length=50, db_index=True, help_text="平台名称")
    source_keyword = models.CharField(
        max_length=255, db_index=True, help_text="来源关键词"
    )
    time_from = models.BigIntegerField(null=True, blank=True, help_text="时间范围起始")
    time_to = models.BigIntegerField(null=True, blank=True, help_text="时间范围结束")
    content = models.TextField(help_text="报告内容 (Markdown)")
    record_count = models.IntegerField(default=0, help_text="分析的记录数量")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    class Meta:
        db_table = "analysis_report"
        verbose_name = "分析报告"
        verbose_name_plural = "分析报告"
        ordering = ["-created_at"]

    def __str__(self):
        return f"AnalysisReport({self.title})"

