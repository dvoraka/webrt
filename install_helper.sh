#! /bin/bash
#
# install_helper.sh
#
# Helps with WebRT installation steps.
#


WEBRT_GIT=https://github.com/dvoraka/webrt.git
PYRT_GIT=https://github.com/dvoraka/py-rt.git

SYSTEM=''

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

    if [ "$SYSTEM" == 'debian' ]
    then
        debian_install_git
    fi

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

    if [ "$SYSTEM" == 'debian' ]
    then
        debian_install_RT4
    fi

}

function debian_install_RT4() {

    apt-get install request-tracker4

}

function guess_system() {

    if [ -f /etc/debian_version ]
    then
        SYSTEM='debian'
    fi

}

function main() {

    check_git
    check_RT4
    guess_system
    echo $SYSTEM
    #install_git
    #install_RT4

}


main
