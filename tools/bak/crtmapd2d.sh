if python ${AFAP_HOME}/tools/crtmapdict2dict.py $1 $2
then
    mv /tmp/rccpsMapD${1}2D${2}.py ${AFAP_HOME}/application/rccps/library/map/rccpsMapD${1}2D${2}.py
    echo ����rccpsMapD${1}2D${2}.py�ɹ�
else
    echo ����rccpsMapD${1}2D${2}.pyʧ��,���������ļ�
fi
