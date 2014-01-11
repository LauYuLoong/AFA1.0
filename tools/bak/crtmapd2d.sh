if python ${AFAP_HOME}/tools/crtmapdict2dict.py $1 $2
then
    mv /tmp/rccpsMapD${1}2D${2}.py ${AFAP_HOME}/application/rccps/library/map/rccpsMapD${1}2D${2}.py
    echo 生成rccpsMapD${1}2D${2}.py成功
else
    echo 生成rccpsMapD${1}2D${2}.py失败,请检查配置文件
fi
