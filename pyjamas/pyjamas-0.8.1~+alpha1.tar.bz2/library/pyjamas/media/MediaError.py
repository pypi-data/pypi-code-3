"""
* Copyright 2009 Mark Renouf
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http:#www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHDIR
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
"""



MEDIA_ERR_ABORTED = 1
MEDIA_ERR_NETWORK = 2
MEDIA_ERR_DECODE = 3
MEDIA_ERR_SRC_NOT_SUPPORTED = 4

class MediaError(object):
    
    def getCode(self):
        JS("""
        return this.code;
        """)
    


