if python ${AFAP_HOME}/tools/crtcopytable2table.py $1 $2
then 
    mv /tmp/rccpsCopyT${1}2T${2}.py ${AFAP_HOME}/application/rccps/library/copy/rccpsCopyT${1}2${2}.py
    echo ����rccpsCopyT${1}2T${2}.py�ɹ�
fi
