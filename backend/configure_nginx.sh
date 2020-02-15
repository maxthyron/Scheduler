#!/bin/zsh

RED='\033[0;31m'
NC='\033[0m'

CELLAR_PATH="/usr/local/Cellar"
TAP="denji/nginx"
OPTS=("--with-headers-more-module" "--with-http2" "--with-status")
NGINX_OPTS=("--add-module=/usr/local/share/headers-more-nginx-module" "--with-http_v2_module" "--with-http_stub_status_module")
CURRENT_NGINX="$(nginx -V 2>&1)"

if [[ ! $(brew tap | grep $TAP) ]]; then
  brew tap $TAP
else
  echo $TAP is already tapped!
fi

echo

# Chech for Nginx modules
MODULES_NOT_FOUND=0
for (( i=1; i<=${#NGINX_OPTS[*]}; i++ )); do
  if [[ $CURRENT_NGINX == *"${NGINX_OPTS[$i]}"* ]]; then
    echo Found: "${NGINX_OPTS[$i]}"
  else
    echo Not found: "${NGINX_OPTS[$i]}"
    ((MODULES_NOT_FOUND++))
  fi
done

echo


# Check for Nginx install
if [ $MODULES_NOT_FOUND -ne 0 ]; then
  echo Modules not found: $MODULES_NOT_FOUND
  echo
  if ! type nginx > /dev/null; then
    echo Nginx is not installed
    echo Installing with options: "${OPTS[*]}"
    COMMAND=install
  else
    echo Nginx is installed, but needs some modules
    echo Reinstalling with options: "${OPTS[*]}"
    COMMAND=reinstall
  fi
  brew $COMMAND nginx-full ${OPTS[*]}
  brew link nginx-full
else
  echo Nginx is installed and configured properly!
fi

echo

if [[ -z $1 ]]; then
  echo "${RED}Conf file or nginx directory is not passed!${NC}" 1>&2
  echo
  echo Usage: ./install-nginx.sh CONF CONF_PATH
  echo CONF - current nginx config file
  echo CONF_PATH - path to nginx install folder\(optional\)
  exit 1
else
  CONF=$1
  if [ ! -f "$(pwd)/$CONF" ]; then
    echo "${RED}File doesn't exist or represents directory!${NC}" 1>&2
    exit 2
  else
    if [ -z "$2" ]; then
      REG="\/usr\/local\/Cellar\/nginx-full\/[0-9\.]\+"
      VAR=$(brew ls nginx-full | head -n 1)
      CONF_PATH=$(echo $VAR | grep -o $REG)
    else
      CONF_PATH=$2
    fi
  fi
  echo Conf file: "$(pwd)/$CONF"
  echo Nginx folder: "$CELLAR_PATH/$CONF_PATH"
  echo
  echo Creating symlink to current nginx config file
  echo $CONF_PATH
  ln -s "$(pwd)/$CONF" "$CONF_PATH/$CONF"
fi