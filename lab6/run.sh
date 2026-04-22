#!/bin/bash

cd "$(dirname "$0")"

if [ ! -f "build/zpadlab_6" ]; then
    echo "❌ Програма не зібрана. Запусти ./build.sh"
    exit 1
fi

./build/zpadlab_6
