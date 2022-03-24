function dumpfunc()
{   
    IMAGE_FILE=Radar_S32R274_TEF810X_Z4/Debug/Radar_S32R274_TEF810X_Z4.elf
    OBJDUMP_CMD=arc-elf32-objdump

    while true; do
        arg=$1
        shift
        test -z "$arg" && break    
        case $arg in
            -i)
                IMAGE_FILE=$1
                shift
            ;; 
            
            -f)
                FUNCTION_NAME=$1
                shift
            ;;
            
            -c)
                OBJDUMP_CMD=$1
            ;;            
            ?) #当有不认识的选项的时候arg为?
              echo "unkonw argument"
              exit 
            ;;
        esac
    done    
    
    if [ "x$FUNCTION_NAME" == "x" ]; then
        echo "Please input function name as -ffunction_name"
        exit
    fi
    
    START_ADDRESS=`${OBJDUMP_CMD} -x ${IMAGE_FILE} | grep " $FUNCTION_NAME$" | awk '{ print $1 }'`
    FUNC_LEN=`${OBJDUMP_CMD} -x ${IMAGE_FILE} | grep " $FUNCTION_NAME$" | awk '{ print $5 }'`    
    END_ADDRESS=`printf "0x%x\n" $((16#${START_ADDRESS}+16#${FUNC_LEN}))`
    
    ${OBJDUMP_CMD} -d ${IMAGE_FILE} --start-address=0x${START_ADDRESS} --stop-address=${END_ADDRESS}
}


dumpfunc $@