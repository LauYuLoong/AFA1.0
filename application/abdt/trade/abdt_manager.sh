#################################################################################
#	FILE:	   abdt_manager.sh			    			    					#
#	EDIT BY:   XZH																#
#	SYSTEM:    AIX & ORACLE & MAPS          									#
#	OVERVIEW:  �����������˵�	        			 				    		#
#	DATE:	   																	#
#################################################################################

#��ʾ���˵�����
dispmenu ()
{
	clear
	echo
	echo
	echo "                  ��������������������������������������������"
	echo "                  ��        ***** ��������˵� *****        ��"
	echo "                  ��              ( Ver 1.00 )              ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��    (1)�� У  ��  ��  ��  ��  ��  ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (2)�� ��  ��  ��  ��  ��  ��  ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (3)�� ��  ��  ��  ��  ��  ��  ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (4)�� ��  ��  ��  ��  ��  ��  ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (5)�� �� �� �� �� �� �� �� �� ��    ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��    (6)�� �� ʾ �� �� �� �� �� Ϣ ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (7)�� �� �� �� �� �� �� �� �� ��    ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��    (0)�� ��                   �� ��    ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��>>>��ѡ��:                              ��"
	echo "                  ��������������������������������������������"
	/usr/bin/tput cup 22 31                                                   
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

				python /home/maps/afa/application/abdt/trade/AbdtSq.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			2)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/abdt/trade/AbdtTj.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			3)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/abdt/trade/AbdtTh.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;
			4)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo

				python /home/maps/afa/application/abdt/trade/AbdtHp.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			5)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo

				python /home/maps/afa/application/abdt/trade/AbdtDeamon.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			6)
				clear
				more /home/maps/afa/conf/lapp.conf
				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			7)
				clear
				vi /home/maps/afa/conf/lapp.conf
		        ;;
 
        esac
done
