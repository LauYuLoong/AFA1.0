#################################################################################
#	FILE:	   abdt_manager.sh			    			    					#
#	EDIT BY:   XZH																#
#	SYSTEM:    AIX & ORACLE & MAPS          									#
#	OVERVIEW:  批量管理主菜单	        			 				    		#
#	DATE:	   																	#
#################################################################################

#显示主菜单函数
dispmenu ()
{
	clear
	echo
	echo
	echo "                  ┏━━━━━━━━━━━━━━━━━━━━┓"
	echo "                  ┃        ***** 批量管理菜单 *****        ┃"
	echo "                  ┃              ( Ver 1.00 )              ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃    (1)〖 校  验  批  量  文  件  〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (2)〖 提  交  批  量  文  件  〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (3)〖 提  回  批  量  文  件  〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (4)〖 生  成  回  盘  文  件  〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (5)〖 批 量 处 理 批 量 数 据 〗    ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃    (6)〖 显 示 批 量 配 置 信 息 〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (7)〖 编 辑 批 量 配 置 文 件 〗    ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃    (0)〖 退                   出 〗    ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃>>>请选择:                              ┃"
	echo "                  ┗━━━━━━━━━━━━━━━━━━━━┛"
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
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/abdt/trade/AbdtSq.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			2)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/abdt/trade/AbdtTj.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			3)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/abdt/trade/AbdtTh.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;
			4)
				clear
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/abdt/trade/AbdtHp.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			5)
				clear
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/abdt/trade/AbdtDeamon.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			6)
				clear
				more /home/maps/afa/conf/lapp.conf
				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			7)
				clear
				vi /home/maps/afa/conf/lapp.conf
		        ;;
 
        esac
done
