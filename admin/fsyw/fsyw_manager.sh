#################################################################################
#	FILE:	   fsyw_manager.sh			    			    					#
#	EDIT BY:   XZH																#
#	SYSTEM:    AIX & ORACLE & MAPS          									#
#	OVERVIEW:  非税业务菜单  	        			 				    		#
#	DATE:	   																	#
#################################################################################

#显示主菜单函数
dispmenu ()
{
	clear
	echo
	echo
	echo "                  ┏━━━━━━━━━━━━━━━━━━━━┓"
	echo "                  ┃        ***** 非税业务菜单 *****        ┃"
	echo "                  ┃              ( Ver 1.00 )              ┃"
	echo "                  ┣━━━━━━━━━━━━━━━━━━━━┫"
	echo "                  ┃    (1)〖 下载基础信息            〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (2)〖 下载缴款书信息          〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (3)〖 下载退付信息            〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (4)〖 实时上传余额信息        〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (5)〖 上传数据信息            〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (6)〖 签到                    〗    ┃"
	echo "                  ┃                                        ┃"
	echo "                  ┃    (7)〖 签退                    〗    ┃"
	echo "                  ┃                                        ┃"
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

				python /home/maps/afa/application/fsyw/trade/AHFS_JCSJSZ.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			2)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_JKSXZ.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			3)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_TF.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;
		        
			4)
				clear
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/fsyw/trade/AHFS_SCFC60.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			5)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_SCSJ.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;
		        
			6)
				clear
				echo ">>>正在处理,请稍候..."
				echo

				python /home/maps/afa/application/fsyw/trade/AHFS_LOGIN.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

			7)
				clear
				echo ">>>正在处理,请稍候..."
				echo
				
				python /home/maps/afa/application/fsyw/trade/AHFS_LOGOUT.py

				echo 
				echo ">>>请按任意键返回..."
				read aa
		        ;;

 
        esac
done
