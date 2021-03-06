#!/bin/sh

if [ ! -d "Ultros" ]
then
    echo "** Creating virtualenv.. **"
    pip install virtualenv
    virtualenv Ultros

    echo "** Activating virtualenv.. **"
    #source Ultros/bin/activate

    echo "** Installing dependencies.. **"
    python packages.py setup

    echo "** Renstalling packages.. **"
    python packages.py update all
else
    echo "** Activating virtualenv.. **"
    #source Ultros/bin/activate
fi

while [ 1 ]
do
    echo "** Starting Ultros.. **"

    if [ $# -eq 0 ]
    then
        python run.py
    else
        python run.py $@
    fi

    echo "** Updating.. **"
    python run.py --update

    echo "** Updating plugins.. **"
    python packages.py update all --overwrite
done

echo "** Deactivating virtualenv.. **"
deactivate