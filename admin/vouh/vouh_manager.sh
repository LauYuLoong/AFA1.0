#################################################################################
#	FILE:	   vouh_manager.sh			    			    					#
#	EDIT BY:   liyj																#
#	SYSTEM:    AIX & ORACLE & MAPS          									#
#	OVERVIEW:  ƾ֤����˵�  	        			 				    		#
#	DATE:	   																	#
#################################################################################

#��ʾ���˵�����
dispmenu ()
{
	clear
	echo
	echo
	echo "                  ��������������������������������������������"
	echo "                  ��        ***** ƾ֤����˵� *****        ��"
	echo "                  ��              ( Ver 1.00 )              ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��    (1)��       ǩ        ��      ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (2)��       ǩ        ��      ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (3)��       ƾ֤�������      ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (0)��       ��        ��      ��    ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��>>>��ѡ��:                              ��"
	echo "                  ��������������������������������������������"
	/usr/bin/tput cup 14 31                                                   
}

while [ 1 ]
do
        dispmenu
        read ans

        case $ans in
			0)
	            clear
	            exit
	            ;;

			1)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo

				python /home/maps/afa/application/vouh/template/Tvouh023.py 01

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			2)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/vouh/template/Tvouh023.py 02

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;
			3)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo

				python /home/maps/afa/application/vouh/template/Tvouh023.py 03

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;
 
        esac
done
