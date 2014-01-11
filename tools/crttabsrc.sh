if python ${AFAP_HOME}/tools/crttabsrc.py $1
then 
    if mv /tmp/rccpsDBT${1}.py ${AFAP_HOME}/application/rccps/library/db/rccpsDBT${1}.py
    then 
        echo 生成rccpsDBT${1}.py成功
    else
        echo 生成rccpsDBT${1}.py失败
    fi
fi
