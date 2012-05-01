# -*- coding: utf-8 -
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# Copyright 2011 Cloudant, Inc.

from bucky.metrics.metric import Metric, MetricValue as MV

class Counter(Metric):
    def __init__(self, name):
        self.name = name
        self.count = 0
    
    def update(self, value):
        self.value += value
    
    def clear(self):
        self.value = 0
    
    def metrics(self):
        return [MV(self.name, self.count)]
