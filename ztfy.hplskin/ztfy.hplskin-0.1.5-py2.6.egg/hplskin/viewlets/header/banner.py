### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2010 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

__docformat__ = "restructuredtext"

# import standard packages
import random

# import Zope3 interfaces
from z3c.language.switch.interfaces import II18n

# import local interfaces
from ztfy.blog.interfaces import IBaseContent
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.hplskin.interfaces import IBannerManager

# import Zope3 packages
from zope.component import queryAdapter

# import local packages
from ztfy.skin.viewlet import ViewletBase
from ztfy.utils.traversing import getParent


class BannerViewlet(ViewletBase):

    @property
    def langs(self):
        content = getParent(self.context, IBaseContent, allow_context=True)
        return II18n(content).getAvailableLanguages()

    @property
    def banner(self):
        site = getParent(self.context, ISiteManager)
        banner = queryAdapter(site, IBannerManager, 'top')
        if banner:
            return random.choice(banner.values())
        return None
