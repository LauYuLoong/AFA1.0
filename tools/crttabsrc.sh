if python ${AFAP_HOME}/tools/crttabsrc.py $1
then 
    if mv /tmp/rccpsDBT${1}.py ${AFAP_HOME}/application/rccps/library/db/rccpsDBT${1}.py
    then 
        echo ����rccpsDBT${1}.py�ɹ�
    else
        echo ����rccpsDBT${1}.pyʧ��
    fi
fi
