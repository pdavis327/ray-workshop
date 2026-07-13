#!/bin/bash
# shellcheck disable=SC1091,SC2034

ORANGE='\033[0;33m'
NC='\033[0m' # No Color

check_shell(){
  [ -n "${BASH_VERSION}" ] && return
  echo -e "${ORANGE}WARNING: These scripts are ONLY tested in a bash shell${NC}"
  sleep "${SLEEP_SECONDS:-8}"
}

check_git_root(){
  [ -n "${GIT_ROOT}" ] && return

  if [ -d scripts ]; then
    GIT_ROOT=$(pwd)
    export GIT_ROOT
    echo "GIT_ROOT:   ${GIT_ROOT}"
    return
  else
    echo "Please run this script from the root of the workshop repo"
    exit 1
  fi
}

check_script_path(){
  [ -n "${SCRIPT_DIR}" ] && return

  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
  export SCRIPT_DIR
  echo "SCRIPT_DIR: ${SCRIPT_DIR}"
}

source_library(){
  for file in "${SCRIPT_DIR}/library/"*.sh
  do
    if [ -f "$file" ] ; then
      # shellcheck source=/dev/null
      . "$file"
    fi
  done
}

setup_bin_path(){
  [ -z ${GIT_ROOT+x} ] && return 1
  BIN_PATH="${GIT_ROOT}/scratch/bin"

  mkdir -p "${BIN_PATH}"
  echo "${PATH}" | grep -q "${BIN_PATH}" || \
    PATH="${BIN_PATH}:${PATH}"
    export PATH
}

is_sourced(){
  if [ -n "$ZSH_VERSION" ]; then
      case $ZSH_EVAL_CONTEXT in *:file:*) return 0;; esac
  else
      case ${0##*/} in dash|-dash|bash|-bash|ksh|-ksh|sh|-sh) return 0;; esac
  fi
  return 1
}

check_shell
check_git_root
check_script_path
source_library
setup_bin_path
