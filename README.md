# U盘小偷（uThief）

免责说明：使用本软件从事违法违规行为导致的后果与本软件和本软件作者无关，下载原码或release视为已阅读本免责说明

## 有什么用

1.机智模式：只复制对应扩展名的文件，避免复制到大文件被发现

2.狂暴模式：全部复制U盘内所有文件

3.复制后的文件维持原目录结构

4.进程名伪装（取决于你打包时py的文件名），release在winXP下打的包(兼容winXP)

5.可以利用Windows的特性，将自己的u盘挂载到本地磁盘的一个文件夹，下课就关电脑的我一样拿的到文件（单独的程序）


## 怎么用

### FilesProtectService.py

主程序，依靠CONFIG.txt，请将FilesProtectService.py打包后再运行

将程序连同CONFIG.txt放到目标计算机内某个文件夹下，双击程序即可

文件会复制到这个文件夹下

### hideDiskCLI.py

用于帮助你隐藏盘符或盘符重映射到本地文件夹的工具，编译打包后，双击运行，根据提示进行操作

### CONFIG.txt

配置文件

写的很清楚了，真不懂请在issue提问，不要来QQ或者b站找我，一律不回

还有本人很讨厌伸手党，既然想要源码和release，请认真学认真对待我的源码
