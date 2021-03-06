#!/bin/bash
###############################################################################
# Django Set Env v1
# by kbruder Tech
###############################################################################
# Set user environment variables expected by lookaway/settings.py
# This script is written for Ubuntu 20 LTS and should work on
# Most Debian-like OSes. 
# It will check your environment_var_file (see below) to see 
# if the variables already exist before appending them.

# Set which file will read the variable assignments
# This will be overwritten when pulling from the master repo
environment_var_file="~/.bashrc"

# Do NOT edit below this line! #
###############################################################################
t1="is already present in"
t2="is now assigned in"
t3="You must edit the file to change it."
t4="--------------------------------------------------------------------------"

# Settings Paths
pro_template="settings/production.py"
dev_template="settings/development.py"
django_config="lookaway/settings.py"

copy_settings_template () {
    echo "Copy the ${2} settings template to \"$django_config\"? (yes, no)"
    read;
    if [ ${REPLY} == "yes" ]; then
        if [ -f ${1} ]; then
            cp ${1} $django_config
            if [ ! $? ]; then
                echo "copy failed!"
            else
                echo "copy successful"
            fi
        else
            echo "No ${2} settings template was found at \"${1}\". Aborting!"
        fi
    else
        echo "No settings template was copied to \"$django_config\"/"
    fi
}

insert_env () {
    if  ! egrep "^${1}=" $environment_var_file > /dev/null; then
        echo "Enter ${2}: ";
        read;
        echo "${1}=\"${REPLY}\"" >> $environment_var_file
        if [ $? ]; then
            echo "${1} $t2 \"$environment_var_file\"."
        fi
    else
        echo "${1} $t1 \"$environment_var_file\"."
        echo $t3
    fi
    echo $t4
}

# Help Text
h1="This script will add environmental variables to the file \"$environment_var_file\". If you do not want this file to change, enter \"12\" to exit. If you would like to change the file in which to assign the environmental variables needed by \"lookaway/settings.py\", then edit this script and change \"\$environment_var_file\", then run it again."
h2="You can always change these settings directly in the \"lookaway/settings.py\" file itself once one of the settings templates from the \"settings/\" has been copied to the aforementioned path. However, keeping sensitive data in the evironment rather than the settings file is more secure."

# Ensure files exist

if [ ! -f $environtment_var_file ]; then
    echo "\"$environmental_var_file\" does not exist! Please set the \"\$environment_var_file\" in this script to a file that is sourced when the shell process starts then run it again."
fi
if [ ! -f $django_config ]; then
    echo "\"$django_config\" does not exist! Would you like to copy a template to that location now? (yes, no)"
    read;
    if [ ${REPLY} == "yes" ]; then
        templates=("Production" "Development")
        select template in "${templates[@]}"; do
            case $template in
                "Production")
                    copy_settings_template $pro_template "Production"
                    break
                    ;;
                "Development")
                    copy_settings_template $dev_template "Development"
                    break
                    ;;
            esac
        done
    else
        echo ""
        echo "I did not read \"yes\" so nothing was copied!"
    fi
fi
echo $t4
# Menu
echo $h1
echo ""
django_vars=("Django Secret Key (autogenerated)" "PostgreSQL Database Name" "PostgreSQL Database User" "PostgreSQL Database Password" "PostgreSQL Database Host" "PostgreSQL Database Port Number" "Email \"from\" Name" "Email Server User" "Email Server Password" "Email Server Host" "Email Server Port" "Exit")
select var in "${django_vars[@]}"; do
    case $var in
        "Django Secret Key (autogenerated)")
            # Django Secret Key
            if ! egrep "^DJANGO_SECRET_KEY=" $environment_var_file > /dev/null ; then
                echo "DJANGO_SECRET_KEY=\"$(./make_key.py)\"" >> $environment_var_file
            if [ $? ]; then
                echo "DJANGO_SECRET_KEY $t2 \"$environment_var_file\"."
            fi
        else
            echo "DJANGO_SECRET_KEY $t1 \"$environment_var_file\"."
            echo $t3
        fi
        echo $t4
        ;;
        # PostgreSQL Database
        "PostgreSQL Database Name")
            ## Database Name
            insert_env "DJANGO_DATABASE_NAME" "the name of the PostgreSQL database"
            ;;
        "PostgreSQL Database User")
            ## Database User
            insert_env "DJANGO_DATABASE_USER" "the name of the PostgreSQL user"
            ;;
        "PostgreSQL Database Password")
            ## Database Password
            insert_env "DJANGO_DATABASE_PASSWORD" "the PostgreSQL user password"
            ;;
        "PostgreSQL Database Host")
            ## Database Host
            insert_env "DJANGO_DATABASE_HOST" "the PostgreSQL host"
            ;;
        "PostgreSQL Database Port Number")
            ## Database Port
            insert_env "DJANGO_DATABASE_PORT" "the PostgreSQL host port number"
            ;;
        # Email
        "Email \"from\" Name")
            ## Email From
            insert_env "ES_FROM" "the name of the sender for the automated password recovery service"
            ;;
        "Email Server User")
            ## Email Host
            insert_env "ES_HOST" "the Email Server host"
            ;;
        "Email Server Port")
            ## Email Port
            insert_env "ES_PORT" "the Email Server port"
            ;;
        "Email Server Host")
            ## Email User
            insert_env "ES_USER" "the name of the Email Server user"
            ;;
        "Email Server Password")
            ## Email Password
            insert_env "ES_PASS" "the Email Server user password"
            ;;
        "Exit")
            echo "Bye!"
            exit
            ;;
        *)
            echo "Invalid option, \"$REPLY\"."
            break
            ;;
    esac
done