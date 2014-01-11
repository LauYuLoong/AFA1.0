#################################################################################
#	FILE:	   fsyw_manager.sh			    			    					#
#	EDIT BY:   XZH																#
#	SYSTEM:    AIX & ORACLE & MAPS          									#
#	OVERVIEW:  ��˰ҵ��˵�  	        			 				    		#
#	DATE:	   																	#
#################################################################################

#��ʾ���˵�����
dispmenu ()
{
	clear
	echo
	echo
	echo "                  ��������������������������������������������"
	echo "                  ��        ***** ��˰ҵ��˵� *****        ��"
	echo "                  ��              ( Ver 1.00 )              ��"
	echo "                  �ǩ�����������������������������������������"
	echo "                  ��    (1)�� ���ػ�����Ϣ            ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (2)�� ���ؽɿ�����Ϣ          ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (3)�� �����˸���Ϣ            ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (4)�� ʵʱ�ϴ������Ϣ        ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (5)�� �ϴ�������Ϣ            ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (6)�� ǩ��                    ��    ��"
	echo "                  ��                                        ��"
	echo "                  ��    (7)�� ǩ��                    ��    ��"
	echo "                  ��                                        ��"
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

				python /home/maps/afa/application/fsyw/trade/AHFS_JCSJSZ.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			2)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_JKSXZ.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			3)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_TF.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;
		        
			4)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo

				python /home/maps/afa/application/fsyw/trade/AHFS_SCFC60.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			5)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_SCSJ.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;
		        
			6)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo

				python /home/maps/afa/application/fsyw/trade/AHFS_LOGIN.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

			7)
				clear
				echo ">>>���ڴ���,���Ժ�..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_LOGOUT.py

				echo 
				echo ">>>�밴���������..."
				read aa
		        ;;

 
        esac
done
