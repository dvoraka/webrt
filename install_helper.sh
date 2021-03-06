#! /bin/bash
#
# install_helper.sh
#
# Helps with WebRT installation steps.
#
# Compatibility (tested):
#   Debian: Wheezy
#   Ubuntu
#


WEBRT_GIT=https://github.com/dvoraka/webrt.git
PYRT_GIT=https://github.com/dvoraka/py-rt.git

SYSTEM=''
DISTRIBUTION=''

DEBIAN_PKGS='python-dev libsasl2-dev libldap2-dev'
UBUNTU_PKGS='python-dev libsasl2-dev libldap2-dev'


function clone_repos() {

    E=0

    echo 'Cloning Webrt...'
    git clone "$WEBRT_GIT"
    if [ "$?" -eq 0 ]
    then
        echo 'Success.'
    else
        echo 'Webrt problem.'
        E=1
    fi
    echo ''

    echo 'Cloning py-rt...'
    git clone "$PYRT_GIT"
    if [ "$?" -eq 0 ]
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
    elif [ "$DISTRIBUTION" == 'ubuntu' ]
    then
        ubuntu_install_RT4
    fi

}

function debian_install_RT4() {

    su root -c 'aptitude install request-tracker4'

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
            return 0
        else
            echo "You don't have virtualenv package."
            echo 'Do you want to install it?'
            read -p 'y/n: ' choice
            if [ "$choice" == 'y' ]
            then
                install_virtualenv
            else
                return 1
            fi
        fi
    done

}

function activate_ve() {

    source virtenvs/webrt/bin/activate

}

function deactivate_ve() {

    deactivate

}

function install_dependencies() {

    REPOS='py-rt webrt'
    for REPO in $REPOS
    do
        if [ -d "$REPO" ]
        then
            cd "$REPO"
            if [ -f requirements.txt ]
            then
                pip install -r requirements.txt
            else
                'requirements.txt not found'
            fi
            cd ..
        fi
    done

}

function install_virtualenv() {

    if [ "$DISTRIBUTION" == 'debian' ]
    then
        debian_install_ve
    elif [ "$DISTRIBUTION" == 'ubuntu' ]
    then
        ubuntu_install_ve
    fi

}

function install_pkgs() {

    if [ "$DISTRIBUTION" == 'debian' ]
    then
        debian_install_pkgs
    elif [ "$DISTRIBUTION" == 'ubuntu' ]
    then
        ubuntu_install_pkgs
    fi

}

function debian_install_pkgs() {

    su root -c "aptitude install $DEBIAN_PKGS"

}

function ubuntu_install_pkgs() {

    sudo apt-get install $UBUNTU_PKGS

}

function debian_install_ve() {

    su root -c 'aptitude install python-virtualenv'

}

function ubuntu_install_ve() {

    sudo apt-get install python-virtualenv

}

function update_repositories() {

    REPOS='py-rt webrt'
    BRANCH='master'
    for REPO in $REPOS
    do
        if [ -d "$REPO" ]
        then
            cd "$REPO"
            echo 'Updating...'
            git checkout $BRANCH
            git pull
            echo 'Done.'
            cd ..
        fi
    done

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

    echo 'Installing packages...'
    install_pkgs
    echo 'Done.'
    echo ''

    if create_virtenv
    then
        activate_ve

        install_dependencies

        deactivate_ve
    fi

    echo 'Checking RT4...'
    if check_RT4
    then
        echo 'Request tracker 4 installed.'
    else
        echo "You don't have RT4 locally."
        echo 'Do you want to install it?'
        read -p 'y/n: ' choice
        if [ "$choice" == 'y' ]
        then
            if install_RT4
            then
                echo 'RT install OK'
            else
                echo 'RT install problem!'
            fi
        else
            echo 'No RT4 locally.'
        fi
    fi

    echo ''
    echo 'Install complete.'
    echo ''

}

function update() {

    echo 'Update:'
    update_repositories
    echo 'Update complete.'

}

function debug() {

    echo 'Debug:'
    echo 'Debug end!'

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
        d)
            debug
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
    echo "Distribution: $DISTRIBUTION"
    echo ''

    # show menu
    while true
    do
        show_menu
        proccess_input
    done

}


main
