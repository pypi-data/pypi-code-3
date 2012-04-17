# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## AlliedTelesis.AT9400.get_config
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.sa.script import Script as NOCScript
from noc.sa.interfaces import IGetConfig


class Script(NOCScript):
    name = "AlliedTelesis.AT9400.get_config"
    implements = [IGetConfig]

    def execute(self):
        config = self.cli("show config dynamic")
        return self.cleaned_config(config)
