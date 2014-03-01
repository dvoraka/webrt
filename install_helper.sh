#! /bin/bash
#
# install_helper.sh
#
# Helps with WebRT installation steps.


WEBRT_GIT=https://github.com/dvoraka/webrt.git
PYRT_GIT=https://github.com/dvoraka/py-rt.git

function clone_repos() {

    git clone $WEBRT_GIT
    git clone $PYRT_GIT

}

function check_git() {

    if [ -x /usr/bin/git ]
    then
        echo 'Git OK'
        return 0
    else
        echo 'You need Git installed.'
        return 1
    fi

}

check_git
