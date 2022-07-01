---
title: aria2-conf
layout: post
author: LIPiston
date: 2022-06-09
tags: 笔记
---

aria2 是一個__多線程不限速__的下載器  
官方開源 [前往](https://github.com/aria2/aria2)

## 安裝

下載 aria2 的最新壓縮包並解壓
下載一個 aria2.conf

```sh
wget https://github.com/P3TERX/aria2.conf/blob/master/aria2.conf
```

在文件夾內新建一個 `aria2.session`
__完事__

## 使用方法

### for Windows

根據注釋更改 aria2.conf  
__必須打開 PRC__ _密鑰可選_

我們需要一個簡單的瀏覽器插件來讓我們懶  
[for edge](https://microsoftedge.microsoft.com/addons/detail/aria2-for-edge/jjfgljkjddpcpfapejfkelkbjbehagbh)  
[for chrome](https://chrome.google.com/webstore/detail/aria2-for-chrome/mpkodccbngfoacfalldjimigbofkhgjn)  
[github](https://github.com/alexhua/Aria2-for-chrome)  
[crx](http://www.crx4.com/9813.html)  
安裝后如圖設置

![设置](./images/aria2/1647893816-244595-1.png)  
__拦截文件大小为 0 时全部使用 aria2 进行下载__

回到 aria2 文件夾  
新建一個 start.vbs 並寫入以下內容

```sh
CreateObject("WScript.Shell").Run "aria2c.exe --conf-path=aria2.conf",0
```

保存后運行即可使用  
win + R 輸入 `shell:startup` 並放入快捷方式即可開機自啟

### for linux & OSX

同樣安裝瀏覽器插件  
start.vbs 改為 start.sh  
内容更换为

```sh
screen aria2c --conf-path=aria2.conf
```

保存即可使用

## 下载连接设置

```sh
# 设置代理服务器
# 默认：无
all-proxy=http://127.0.0.1:7890/

# 为all-proxy选项配置的代理服务器设置密码
# 默认：无
# all-proxy-passwd=""

# 为all-proxy选项配置的代理服务器设置用户名
# 默认：无
# all-proxy-user=""
```

## 油猴获取度盘直链下载

[油小猴](https://www.baiduyun.wiki/zh-cn/)  
__速度由账号决定，可多选下载文件，不需要多次验证__

-----
[简易下载助手](https://greasyfork.org/zh-CN/scripts/418182-%E7%99%BE%E5%BA%A6%E7%BD%91%E7%9B%98%E7%AE%80%E6%98%93%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B-%E7%9B%B4%E9%93%BE%E4%B8%8B%E8%BD%BD%E5%A4%8D%E6%B4%BB%E7%89%88)  
__速度快，不可多选，需要多次验证__
