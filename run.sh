#!/usr/bin/env bash

IMG="tdc-stores:latest"

function run {
    case "$1" in
    version)
        echo ${IMG}
        echo ${IMG}|awk -F: '{print "base: "$1" . tag: "$2}'
        ;;
    build)
        docker build --rm -t ${IMG} . \
            && docker tag ${IMG} `echo ${IMG}|awk -F: '{print $1}'` \
            && docker images | grep "`echo ${IMG}|awk -F: '{print $1}'`"
        ;;
    api)
        docker run -it --rm --name tdc-stores-api \
            -p 5000:5000 \
            ${IMG}
        ;;
    cli)
        shift
        docker run -it --rm --name tdc-stores-cli \
            -v "$PWD"/output:/opt/tdc/output \
            -w /opt/tdc `echo ${IMG}|awk -F: '{print $1}'` cli/cli.py $@
        ;;
    test)
        docker run -it --rm --name tdc-stores-tests \
            -w /opt/tdc `echo ${IMG}|awk -F: '{print $1}'` python -m pytest -v
        ;;
    *)
        echo "# ---"
        echo "# version: Show Docker Image Version"
        echo "# build: Build Docker Image"
        echo "# api: Run API Server"
        echo "# cli: Run CLI"
        echo "# tests: Run tests"
        echo "# ---"
        ;;
    esac
}

run $@
exit $?
