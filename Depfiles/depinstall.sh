#!/bin/sh
while read p; do
pip3 install $p
done < ./Depfiles/dependencies.pip

while read p; do
composer require p
done < ./Depfiles/dependencies.comp
