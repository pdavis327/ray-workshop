#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "--- Ray Workshop Sanity Check ---"

if command -v oc &> /dev/null; then
    echo -e "[${GREEN}OK${NC}] oc CLI is installed."
else
    echo -e "[${RED}FAIL${NC}] oc CLI is NOT installed."
fi

if oc whoami &> /dev/null; then
    echo -e "[${GREEN}OK${NC}] Logged into cluster as: $(oc whoami)"
else
    echo -e "[${RED}FAIL${NC}] Not logged into OpenShift. Run 'oc login'."
fi

if oc api-resources 2>/dev/null | grep -q rayjobs; then
    echo -e "[${GREEN}OK${NC}] KubeRay RayJob CRD is available."
else
    echo -e "[${RED}FAIL${NC}] RayJob CRD not found. Enable the ray component in DataScienceCluster."
fi

if oc api-resources 2>/dev/null | grep -q rayclusters; then
    echo -e "[${GREEN}OK${NC}] KubeRay RayCluster CRD is available."
else
    echo -e "[${RED}FAIL${NC}] RayCluster CRD not found."
fi

if oc get project ray-workshop &> /dev/null; then
    echo -e "[${GREEN}OK${NC}] Project ray-workshop exists."
else
    echo -e "[${YELLOW}WARN${NC}] Project ray-workshop not found. Run: bash scripts/setup.sh -s 1"
fi

if oc get hardwareprofile -n redhat-ods-applications cpu-local-queue &> /dev/null; then
    echo -e "[${GREEN}OK${NC}] HardwareProfile cpu-local-queue exists."
else
    echo -e "[${YELLOW}WARN${NC}] HardwareProfile cpu-local-queue not found. Run: bash scripts/setup.sh -s 1"
fi

if oc get localqueue -n ray-workshop ray-workshop-queue &> /dev/null; then
    echo -e "[${GREEN}OK${NC}] LocalQueue ray-workshop-queue exists."
else
    echo -e "[${YELLOW}WARN${NC}] LocalQueue ray-workshop-queue not found. Run: bash scripts/setup.sh -s 1"
fi

if oc get localqueue -n ray-workshop default &> /dev/null; then
    echo -e "[${GREEN}OK${NC}] LocalQueue default exists in ray-workshop."
else
    echo -e "[${YELLOW}WARN${NC}] LocalQueue default not found in ray-workshop."
fi

echo "--- Sanity Check Complete ---"
