#! /bin/bash
#
# install_helper.sh
#
# Helps with WebRT installation steps.
#


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

function install_git() {

    debian_install_git

}

function debian_install_git() {

    apt-get install git-core

}

function check_RT4() {

    if [ -d /etc/request-tracker4 ]
    then
        echo 'RT4 OK'
        return 0
    else
        echo "You don't have RT4."
        return 1
    fi

}

function install_RT4() {

    debian_install_RT4

}

function debian_install_RT4() {

    apt-get install request-tracker4

}

function main() {

    check_git
    check_RT4
    #install_git
    #install_RT4

}


main
