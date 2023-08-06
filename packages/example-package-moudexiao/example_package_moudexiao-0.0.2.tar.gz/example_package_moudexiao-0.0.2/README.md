# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

``` python
import gzip
def un_gz(file_name):
    #获取文件名，去掉后缀名
    f_name=filename.replace(".gz","")
    #开始解压
    g_file=gzip.GzipFile(file_name)
    #读取解压后的文件，并写入去掉后缀名的同名文件
    open(f_name,"wb+").write(g_file.read())
    g_file.close()
un_gz('D:\D盘\Desktop\cvyuan-0.1.tar.gz')#绝对路劲
```

``` bash
echo "# duoyuantongji" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/moudexiao/duoyuantongji.git
git push -u origin main


git remote add origin https://github.com/moudexiao/duoyuantongji.git
git branch -M main
git push -u origin main
```
