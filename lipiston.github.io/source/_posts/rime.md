---
title: 逃离个性化推荐的最后一步：rime
categories: 好玩的
tags:
  - 记录
date: 2024-10-27 00:05:49
---

# 起因

国内的个性化推荐都做得让人一言难尽，有一种同一盆盆栽放到你面前让你辨认的美感。  
包括国内输入法的数据采集问题，也让我使用了很久的Gboard。
但最后Windows端的微软拼音成功劝退我了，所以找到了被我尘封多年的rime。

## Windows

2024-11-07，有时间了，现在写写。  

### 安装

前往[rime.im](https://rime.im/)下载 Windows 平台安装包  

打开照常安装。

### 配置

前往[rime-ice](https://github.com/iDvel/rime-ice)，下载整个zip  

解压到用户文件夹  

在输入法设定中选择`雾凇拼音`即可使用

<img title="" src="https://ghp.ci/https://github.com/LIPiston/picx-images-hosting/raw/master/20241107/QQ20241107-181618.60u9bvvftc.webp" alt="截图" style="zoom:50%;" width="458">

### 同步

Windows端推荐使用坚果云将这个目录进行同步

> C:\Users\Administrator\AppData\Roaming\Rime\sync

其他设备使用WebDAV进行同步就好了

## Android

Android端我是不推荐使用trime的，因为Fcitx5-Android的多次更新已经很完善了，包括现在这篇文章的整个Android篇章都是用的Fcitx5-Android搭配rime-plugin。

<img title="" src="https://jsd.cdn.zzko.cn/gh/LIPiston/picx-images-hosting@master/Screenshot_20241026-235509_Markor.5mnt47fxt0.png" alt="" style="zoom:50%;" width="441">

### 安装

回归正题，安装部分很简单，在[Fcitx5-Android的官方文档](https://fcitx5-android.github.io/installation/)就可以找到安装Fcitx5-Android的方式。  
在[GitHub就可以安装rime-plugin](https://github.com/fcitx5-android/fcitx5-android)

### 配置

两者安装好后就到配置输入法  
一开始的向导叫你干啥就干啥，然后到[rime-ice](https://github.com/iDvel/rime-ice)下载整个zip，解压到rime用户目录

> /storage/emulated/0/Android/data/org.fcitx.fcitx5.android/files/data/rime/

至此，你已经完成Android端的安装与配置。
可以开始使用rime了

### 词库同步

推荐使用 [folder sync](https://foldersync.io/) 或者 [autosync](https://play.google.com/store/apps/details?id=com.ttxapps.autosync)  

然后进入到autosync中添加一个云储存账号方便同步词库，然后创建文件夹对，将远程文件夹与本地文件夹进行同步，然后就能使用了。  
<img title="" src="https://ghp.ci/https://github.com/LIPiston/picx-images-hosting/raw/master/ae25378a-019b-4924-aa93-c23f1fdd0df4.1zicvbujso.webp" alt="" style="zoom:50%;" width="441">
<img title="" src="https://ghp.ci/https://github.com/LIPiston/picx-images-hosting/raw/master/image.45s2pjolj.webp" alt="" style="zoom:50%;" width="441">

注意：fcitx5-Android自带了定时保存用户数据的设置，则rime会自动同步数据而Windows的自动同步只需要将开始菜单中的用户资料同步做到计划任务即可
---


## Linux

Linux机子没啦后面再写