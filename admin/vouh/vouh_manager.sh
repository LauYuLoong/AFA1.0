#################################################################################
#	FILE:	   vouh_manager.sh			    			    					#
#	EDIT BY:   liyj																#
#	SYSTEM:    AIX & ORACLE & MAPS          									#
#	OVERVIEW:  凭证管理菜单  	        			 				    		#
#	DATE:	   																	#
#################################################################################

#显示主菜单函数
dispmenu ()
{
	clear
	echo
	echo
	echo "                  ┏━━━━━━━━━━━━━━━━━━━━┓"
	echo "                  ┃        ***** 凭证管理菜单 *****        ┃"
	echo "                  ┃              ( Ver 1.00 )              ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃    (1)〖       签        到      〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (2)〖       签        退      〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (3)〖       凭证管理对帐      〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (0)〖       退        出      〗    ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃>>>请选择:                              ┃"
	echo "                  ┗━━━━━━━━━━━━━━━━━━━━┛"
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
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/vouh/template/Tvouh023.py 01

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			2)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/vouh/template/Tvouh023.py 02

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;
			3)
				clear
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/vouh/template/Tvouh023.py 03

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;
 
        esac
done
