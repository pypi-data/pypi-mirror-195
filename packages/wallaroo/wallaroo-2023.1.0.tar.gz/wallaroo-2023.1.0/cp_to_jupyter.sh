#!/bin/bash

usage="USAGE: $0 file"

podname=jupyter-

pod=$(kubectl get pods | grep $podname | awk '{print $1}')
kubectl cp ${1:?$usage} ${pod}:/home/jovyan

