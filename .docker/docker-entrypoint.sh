#!/usr/bin/env bash

cd /app

if [[ "${1}" == "shell" ]]; then
    exec /bin/bash
fi