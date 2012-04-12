#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Łukasz Langa
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib import admin
from lck.django.common.admin import ModelAdmin
from lck.django.badges.models import BadgeType, BadgeIcon, BadgeGroup


class BadgeIconAdmin(ModelAdmin):
    list_display = ('title', 'image', 'created', 'width', 'height')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class BadgeTypeInline(admin.StackedInline):
    readonly_fields = ('created',)
    exclude = ('modified',)
    extra = 0
    model = BadgeType


class BadgeGroupAdmin(ModelAdmin):
    inlines = [BadgeTypeInline]
    list_display = ('key', 'name', 'created', 'callback')
    search_fields = ('key', 'name', 'description', 'callback')
    save_on_top = True


admin.site.register(BadgeIcon, BadgeIconAdmin)
admin.site.register(BadgeGroup, BadgeGroupAdmin)
