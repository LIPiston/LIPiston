---
title: Arch Linux 安装记录
date: 2022-06-05 23:56:49
---
    莫名其妙的就找到了一种奇快无比的安装方式
##  准备工作
- 4g+的u盘
- ArchLinux.iso
- Windows pe

##  安装
**放心这十分简单**

###  烧录
简单的使用 ecther 烧录就好  
~~如果你有别的能用也无所谓~~

###  安装Arch
进入 BIOS 选择烧录的u盘为启动项  
进入 Archiso-cdlive   
输入  `archinstall` 并回车  
按照你想要的意愿来设置  
`disks layout` 请选择 `wipe all`  
install 等待即可  
最后选 yes

###  分区
进入 Windows pe  
打开你的 dg  
查看安装 ArchLinux 的盘  
不出意外的话 `分区1>分区2`  
更改分区大小并扩展 分区1  
~~不然你随便滚几下系统就不够安装软件了~~

###  收尾
重启后更改 BIOS 中的启动项  
改为安装 Arch 的盘
即可进入系统