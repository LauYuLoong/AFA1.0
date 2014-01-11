if python ${AFAP_HOME}/tools/crtmaptable2table.py $1 $2
then
    mv /tmp/rccpsMapT${1}2T${2}.py ${AFAP_HOME}/application/rccps/library/map/rccpsMapT${1}2T${2}.py
    echo 生成rccpsMapT${1}2T${2}.py成功
fi
