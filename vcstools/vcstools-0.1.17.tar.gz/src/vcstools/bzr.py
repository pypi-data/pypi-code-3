# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
"""
bzr vcs support.
"""

import os
import sys
import urllib


from vcs_base import VcsClientBase, VcsError, sanitized, normalized_rel_path, run_shell_command


def _get_bzr_version():
    """Looks up bzr version by calling bzr --version.
    :raises: VcsError if bzr is not installed"""
    try:
        value, output, _ = run_shell_command('bzr --version', shell=True, us_env = True)
        if value == 0 and output is not None and len(output.splitlines()) > 0:
            version = output.splitlines()[0]
        else:
            raise VcsError("bzr --version returned %s, maybe bzr is not installed"%value)
    except VcsError as e:
        raise VcsError("Coud not determine whether bzr is installed: %s"%e)
    return version


class BzrClient(VcsClientBase):
    def __init__(self, path):
        """
        :raises: VcsError if bzr not detected
        """
        VcsClientBase.__init__(self, 'bzr', path)
        _get_bzr_version()
        
    @staticmethod
    def get_environment_metadata():
        metadict = {}
        try:
            metadict["version"] = _get_bzr_version()
        except:
            metadict["version"] = "no bzr installed"
        return metadict
        
    def get_url(self):
        """
        :returns: BZR URL of the branch (output of bzr info command), or None if it cannot be determined
        """
        if self.detect_presence():
            cmd = 'bzr info %s'%self._path
            _, output, _ = run_shell_command(cmd, shell=True, us_env = True)
            matches = [l for l in output.splitlines() if l.startswith('  parent branch: ')]
            if matches:
                ppath = urllib.url2pathname(matches[0][len('  parent branch: '):])
                # when it can, bzr substitues absolute path for relative paths
                if (ppath is not None and os.path.isdir(ppath) and not os.path.isabs(ppath)):
                    return os.path.abspath(os.path.join(os.getcwd(), ppath))
                return ppath
        return None

    def detect_presence(self):
        return self.path_exists() and os.path.isdir(os.path.join(self._path, '.bzr'))

    def checkout(self, url, version=None, verbose = False):
        
        if version:
            cmd = "bzr branch -r %s %s %s"%(version, url, self._path)
        else:
            cmd = "bzr branch %s %s"%(url, self._path)
        value, _, _ = run_shell_command(cmd, shell=True, show_stdout = verbose, verbose = verbose)
        if value != 0:
            if self.path_exists():
                sys.stderr.write("Error: cannot checkout into existing directory\n")
            return False
        return True

    def update(self, version='', verbose = False):
        if not self.detect_presence():
            return False
        value, _, _ = run_shell_command("bzr pull", cwd=self._path, shell=True, show_stdout = True, verbose = verbose)
        if value != 0:
            return False
        # Ignore verbose param, bzr is pretty verbose on update anyway
        if version is not None and version != '':
            cmd = "bzr update -r %s"%(version)
        else:
            cmd = "bzr update"
        value, _, _ = run_shell_command(cmd, cwd=self._path, shell=True, show_stdout = True, verbose = verbose)
        if value == 0:
            return True
        return False

    def get_version(self, spec=None):
        """
        :param spec: (optional) revisionspec of desired version.  May
          be any revisionspec as returned by 'bzr help revisionspec',
          e.g. a tagname or 'revno:<number>'        
        :returns: the current revision number of the repository. Or if
          spec is provided, the number of a revision specified by some
          token. 
        """
        if self.detect_presence():
            if spec is not None:
                command = ['bzr log -r %s .'%sanitized(spec)]
                _, output, _ = run_shell_command(command, shell=True, cwd=self._path, us_env = True)
                if output is None or output.strip() == '' or output.startswith("bzr:"):
                    return None
                else:
                    matches = [l for l in output.split('\n') if l.startswith('revno: ')]
                    if len(matches) == 1:
                        return matches[0].split()[1]
            else:
                _, output, _ = run_shell_command('bzr revno --tree', shell=True, cwd=self._path, us_env = True)
                return output.strip()

    def get_diff(self, basepath=None):
        response = None
        if basepath == None:
            basepath = self._path
        if self.path_exists():
            rel_path = sanitized(normalized_rel_path(self._path, basepath))
            command = "bzr diff %s"%rel_path
            command += " -p1 --prefix %s/:%s/"%(rel_path, rel_path)
            _, response, _ = run_shell_command(command, shell=True, cwd=basepath)
        return response

    def get_status(self, basepath=None, untracked=False):
        response=None
        if basepath == None:
            basepath = self._path
        if self.path_exists():
            rel_path = normalized_rel_path(self._path, basepath)
            command = "bzr status %s -S"%sanitized(rel_path)
            if not untracked:
                command += " -V"
            _, response, _ = run_shell_command(command, shell=True, cwd=basepath)
            response_processed = ""
            for line in response.split('\n'):
                if len(line.strip()) > 0:
                    response_processed+=line[0:4]+rel_path+'/'+line[4:]+'\n'
            response = response_processed
        return response
    
BZRClient=BzrClient
