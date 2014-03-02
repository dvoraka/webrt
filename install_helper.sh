#! /bin/bash
#
# install_helper.sh
#
# Helps with WebRT installation steps.
#


WEBRT_GIT=https://github.com/dvoraka/webrt.git
PYRT_GIT=https://github.com/dvoraka/py-rt.git

SYSTEM=''
DISTRIBUTION=''

function clone_repos() {

    E=0

    echo 'Cloning Webrt...'
    git clone $WEBRT_GIT
    if [ $? -eq 0 ]
    then
        echo 'Success.'
    else
        echo 'Webrt problem.'
        E=1
    fi
    echo ''

    echo 'Cloning py-rt...'
    git clone $PYRT_GIT
    if [ $? -eq 0 ]
    then
        echo 'Success.'
    else
        echo 'py-rt problem.'
        E=1
    fi
    echo ''

    return $E

}

function check_git() {

    if hash git 2>/dev/null
    then
        return 0
    else
        return 1
    fi

}

function install_git() {

    if [ "$DISTRIBUTION" == 'debian' ]
    then
        debian_install_git
        return 1
    elif [ "$DISTRIBUTION" == 'ubuntu' ]
    then
        ubuntu_install_git
        return 2
    fi

}

function debian_install_git() {

    su root -c 'apt-get install git-core'

}

function ubuntu_install_git() {

    sudo apt-get install git-core

}

function check_RT4() {

    # check config directory
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

    if [ "$DISTRIBUTION" == 'debian' ]
    then
        debian_install_RT4
        return 1
    elif [ "$DISTRIBUTION" == 'ubuntu' ]
    then
        ubuntu_install_RT4
        return 2
    fi

}

function debian_install_RT4() {

    su root -c 'apt-get install request-tracker4'

}

function ubuntu_install_RT4() {

    sudo apt-get install request-tracker4

}

function create_virtenv() {
    
    while true
    do
        if hash virtualenv 2>/dev/null
        then
            echo 'Creating new virtual environment...'
            mkdir virtenvs
            virtualenv virtenvs/webrt
            echo 'Done.'
            break
        else
            echo "You don't have virtualenv package."
            echo 'Do you want to install it?'
            read -p 'y/n: ' choice
            if [ "$choice" == 'y' ]
            then
                install_virtualenv
            else
                break
            fi
        fi
    done

}

function install_virtualenv() {

    debian_install_ve

}

function debian_install_ve() {

    su root -c 'apt-get install python-virtualenv'

}

function guess_system() {

    SYSTEM=`uname`
    # $OSTYPE can be used too

    DISTID=`lsb_release -s -i`

    if [ "$DISTID" == 'Debian' ]
    then
        DISTRIBUTION='debian'
    elif [ "$DISTID" == 'Ubuntu' ]
    then
        DISTRIBUTION='ubuntu'
    fi

}

function complete_install() {

    echo 'Complete install'
    echo '----'

    guess_system

    echo 'Checking Git...'
    if check_git
    then
        echo 'Git - OK'
    else
        echo "You don't have Git."
        echo 'Do you want to install it?'
        read -p 'y/n: ' choice
        if [ "$choice" == 'y' ]
        then
            install_git
        else
            exit 1
        fi
    fi

    echo ''

    echo 'Cloning repositories...'
    if clone_repos
    then
        echo 'Download - OK'
    else
        echo 'Repositories problem'
        exit 1
    fi

    echo ''

    create_virtenv

}

function update() {

    echo 'Update'

}

function show_menu() {

    echo '----'
    echo '  1) install'
    echo '  2) update'
    echo '  9) quit'
    echo ''

}

function proccess_input() {

    read -p 'Enter choice: ' choice
    #echo $choice

    echo ''
    case $choice in

        1)
            complete_install
        ;;
        2)
            update
        ;;
        9 | q)
            exit 0
        ;;

        *)
            echo 'Unknown choice'
        ;;
    esac

    echo ''

}

function main() {

    guess_system
    echo $DISTRIBUTION

    # show menu
    while true
    do
        show_menu
        proccess_input
    done

}


main
