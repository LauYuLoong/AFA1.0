if python ${AFAP_HOME}/tools/crtmap.py $1 $2 $3 $4 $5
then 
    case $1 in
        "dict") from_type="D";;
        "context") from_type="C";;
    esac

    case $3 in
        "dict") to_type="D";;
        "context") to_type="C";;
    esac

    mv /tmp/rccpsMap${5}${from_type}${2}2${to_type}${4}.py ${AFAP_HOME}/application/rccps/library/map/rccpsMap${5}${from_type}${2}2${to_type}${4}.py
    echo 生成rccpsMap${5}${from_type}${2}2${to_type}${4}.py成功
fi
