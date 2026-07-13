#!/bin/bash
# shellcheck disable=SC2035

OPENSHIFT_CLIENTS_URL=https://mirror.openshift.com/pub/openshift-v4/x86_64/clients

bin_check(){
  name=${1:-oc}

  BIN_PATH=${BIN_PATH:-scratch/bin}
  BASH_COMP=${BASH_COMP:-scratch/bash}

  OS="$(uname | tr '[:upper:]' '[:lower:]')"

  [ -d "${BIN_PATH}" ] || mkdir -p "${BIN_PATH}"
  [ -d "${BASH_COMP}" ] || mkdir -p "${BASH_COMP}"

  which "${name}" && return 0

  [ -e "${BIN_PATH}/${name}" ] || download_"${name}"

  case ${name} in
    oc)
      ${name} version --client 2>&1
      ;;
    *)
      ${name} --version 2>&1
      ;;
  esac
}

download_oc(){
  BIN_VERSION=stable-4.16
  DOWNLOAD_URL=${OPENSHIFT_CLIENTS_URL}/ocp/${BIN_VERSION}/openshift-client-${OS:-linux}.tar.gz
  curl "${DOWNLOAD_URL}" -sL | tar zx -C "${BIN_PATH}/" oc kubectl
}

download_jq(){
  BIN_VERSION=1.7.1
  DOWNLOAD_URL=https://github.com/jqlang/jq/releases/download/jq-${BIN_VERSION}/jq-linux-amd64
  curl "${DOWNLOAD_URL}" -sLo "${BIN_PATH}/jq"
  chmod +x "${BIN_PATH}/jq"
}
