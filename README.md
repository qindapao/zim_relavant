# zim_relavant
some changes about zim,but they cannot be uploaded to the zim repository,for my personal use only

## zim中调用powershell脚本方式

```powershell
powershell.exe -ExecutionPolicy Bypass -File E:\code\zim_relavant\open_with_emacs.ps1 -filePath "E:\code\my_vim_config\complete_list_all.vim"
```
## zim中的快捷键绑定

首选项 -> 快捷键绑定

比如，我自己开发的插件中的动作绑定：

```txt
<Actions>/EmacsPageViewExtension/open_in_emacs Shift+Ctrl+O
```
## 配置文件中的一些注意点

在样式配置文件`style.conf`中，行内代码和跨行的代码只能指定字体，不应该指定字体大小。


