# nginq-common 
quant/nginq 的公共模块整理出来，独立做个源码仓库  nginq-common 

后续  quant/nginq 拆分， 每个策略独立一个原编码仓库  strategy-18、strategy-6、strategy-b 等



## 项目打包

```


# pip install twine 

# 打包检查
# python setup.py check

# 打包
# python setup.py sdist build

# 上传
# twine upload dist/*

```

另， **不推荐的上传方式如下（密码容易被劫持）**
```

# 打包
# python setup.py sdist

# 上传
# python setup.py upload  
```

## 安装本项目的包（最好指定版本）

```
## 手工导入 
# pip install nginqcomm==0.2.2


## requirements.txt
# 

```