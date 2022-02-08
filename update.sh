#!/bin/bash
# update the setup file with the correct information
read -p "Package name [mypkg]: " PKG_NAME
read -p "Author's full name [Omar Sosa Rodriguez]: " AUTHOR
read -p "Author's email [omarfsosa@gmailcom]: " EMAIL
read -p "Author's github username [omarfsosa]: " GITNAME
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

AUTHOR=${AUTHOR:-"Omar Sosa Rodriguez"}
EMAIL=${EMAIL:-"omarfsosa@gmail.com"}
GITNAME=${GITNAME:-"omarfsosa"}

if [[ -n "$PKG_NAME" ]]; then
    echo "Renaming package to '$PKG_NAME'"
    sed -i "" "s|<mypkg>|$PKG_NAME|" setup.cfg
    mv mypkg $PKG_NAME
fi

if [[ -n "$AUTHOR" ]]; then
    echo "Renaming author to '$AUTHOR'"
    sed -i "" "s|<author>|$AUTHOR|" setup.cfg
fi

if [[ -n "$EMAIL" ]]; then
    echo "Renaming email to '$EMAIL'"
    sed -i "" "s|<email>|$EMAIL|" setup.cfg
fi

if [[ -n "$GITNAME" ]]; then
    echo "Renaming git user to '$GITNAME'"
    sed -i "" "s|<github>|$GIT_NAME|" setup.cfg
fi