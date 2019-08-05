""" Version information. Based on ``_version_helper.py`` from PyCBC.
"""

import argparse
import distutils.version
import os
import re
import subprocess
import sys
import time

class Version(object):
    """ This class manages version information.

    Attributes
    ----------
    date
    githash
    branch
    tag
    author
    committer
    status
    builder
    build_date
    version
    release
    last_release
    """

    # list of attributes
    attrs = ["status", "tag", "version", "githash", "branch", "author",
             "committer", "date", "builder", "build_date", "release",
             "last_release"]

    def __init__(self):
        for attr in self.attrs:
            setattr(self, attr, None)

    def __repr__(self):
        out = ""
        for k in self.attrs:
            v = getattr(self, k)
            out += "{} = {}\n".format(k, v)
        return out[:-1]

    def as_dict(self):
        """ Returns a ``dict`` of attributes and values.
        """
        return {attr : getattr(self, attr) for attr in self.attrs}

    @staticmethod
    def get_build_name(git_path="git"):
        """ Return the username and user email of the current builder.
        """
        name, retcode = _external_call([git_path, "config", "user.name"])
        if retcode:
            name = "Unknown User"
        email, retcode = _external_call([git_path, "config", "user.email"])
        if retcode:
            email = ""
        return "{} <{}>".format(name, email)

    @staticmethod
    def get_build_date():
        """Returns the current datetime as the git build date.
        """
        return time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime())

    @staticmethod
    def get_last_commit(git_path="git"):
        """ Returns the details of the last Git commit as a tuple with values
        ``(hash, date, author name, author e-mail, committer name, committer e-mail)``.
        """
        result, _ = _external_call([git_path, "log", "-1",
                                    "--pretty=format:%H,%ct,%an,%ae,%cn,%ce"])
        githash, udate, aname, amail, cname, cmail = result.split(",")
        date = time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime(float(udate)))
        author = "{} <{}>".format(aname, amail)
        committer = "{} <{}>".format(cname, cmail)
        return githash, date, author, committer

    @staticmethod
    def get_branch(git_path="git"):
        """ Returns the name of the current Git branch.
        """
        branch_match, _ = _external_call([git_path, "rev-parse",
                                          "--symbolic-full-name", "HEAD"])
        if branch_match == "HEAD":
            return None
        else:
            return os.path.basename(branch_match)

    @staticmethod
    def get_tag(githash, git_path="git"):
        """ Returns the name of the current Git tag.
        """
        tag, retcode = _external_call([git_path, "describe", "--exact-match",
                                       "--tags", githash])
        if retcode == 0:
            return tag
        else:
            return None

    @staticmethod
    def get_status(git_path="git"):
        """ Returns the state of the git working copy.
        """
        status = subprocess.call([git_path, "diff-files", "--quiet"])
        if status != 0:
            return "UNCLEAN: Modified working tree"
        else:
            status = subprocess.call([git_path, "diff-index", "--cached",
                                     "--quiet", "HEAD"])
            if status != 0:
                return "UNCLEAN: Modified index"
            else:
                return "CLEAN: All modifications committed"

    @staticmethod
    def get_latest_release_version(git_path="git"):
        """ Query the Git repository for the last released version of the code.
        """

        # get all tags
        tag_list = _external_call([git_path, "tag"])[0].split("\n")
    
        # reduce to only versions
        tag_list = [t[1:] for t in tag_list if t.startswith("v")]
    
        # determine if indeed a tag and store largest
        latest_version = None
        latest_version_string = None
        re_magic = re.compile("\d+\.\d+\.\d+$")
        for tag in tag_list:

            # is this a version string
            if re_magic.match(tag):
                curr_version = distutils.version.StrictVersion(tag)
                if latest_version is None or curr_version > latest_version:
                    latest_version = curr_version
                    latest_version_string = tag
    
        return latest_version_string

    @classmethod
    def generate(cls):
        """ Return an instance of the class after querying the Git repository.
        """
    
        # create instance
        info = cls()
        git_path, _ = _external_call(["which", "git"])

        # get build info
        info.builder = cls.get_build_name()
        info.build_date = cls.get_build_date()

        # parse Git ID
        info.githash, info.date, info.author, info.committer = \
            cls.get_last_commit(git_path)
    
        # determine branch
        info.branch = cls.get_branch(git_path)
    
        # determine tag
        info.tag = cls.get_tag(info.githash, git_path)
    
        # determine version
        if info.tag:
            info.version = info.tag.strip("v")
            info.release = not re.search("[a-z]", info.version.lower())
        else:
            info.version = info.githash[:6]
            info.release = False
    
        # Determine last stable release
        info.last_release = cls.get_latest_release_version(git_path)
    
        # refresh index
        _external_call([git_path, "update-index", "-q", "--refresh"])
    
        # check working copy for changes
        info.status = cls.get_status(git_path)
    
        return info

class VersionAction(argparse.Action):
    """ This class manages version information for the command line.
    """

    # list of attributes
    attrs = Version.attrs

    def __init__(self, nargs=0, **kwargs):
        super(VersionAction, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        from spotlight import version
        info = Version()
        for attr in self.attrs:
            setattr(info, attr, getattr(version, attr))
        print(info)
        sys.exit(0)

def _external_call(cmd):
    """ This function makes external calls.
    """

    # start external command process
    p = subprocess.Popen(map(str, cmd), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    # get outputs
    out, _ = p.communicate()
    if p.returncode != 0:
        print("Failed to run {}".format(cmd))

    return out.strip(), p.returncode
