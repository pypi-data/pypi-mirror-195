# webz
```
简单的web服务器框架，实现的是配置文件的读取和调用，内部调用web.py

注：代码实现了url映射和查找，查找方式是for循环遍历列表，url映射配置多了的话循环显然不是好方法，相关代码在
configz.ConfigWeb.deal和config.ConfigWeb.deal
可以自行修改

demo在demo文件夹中，两种配置方式，分别运行：
python run.py
python runz.py
推荐runz.py的配置方式

为了本人自己使用方便以及利用浏览器缓存减少http请求，把bootstrap、jquery.js和vue.js放进文件夹了，可以不使用或者替换掉，另外有两脚本文件base.js和utils.js，分装了一些方法:
    json调用:
    $.json(url, data, success=(rst)=>{}, error=(rst)=>{})
    $.upload(...)
    $.submit(...) //这个没测试
    $.get(url, success=(rst)=>{}, error=(rst)=>{})
    页面跳转（带数据）
        _.jump(url, data)
    新页面通过以下方法获取数据：
        _.data()
    页面回跳（和左上角后退键一个功能，不过可以加回跳参数）:
        _.back(backData=null)
    原页面还是通过_.data()获取初始化时的原数据，也可以通过_.backData()获取回跳时设置的数据

    通过js代码引入js文件库:
        addScript(url)
    通过js代码引入css文件库:
        addStyle(url)

    vue相关：
    组件:
    component(url, id=null)
    实际是把url对应的页面嵌入当前页面

    页面vue创建：
    newVue({
        data(){return {...}},
        mounted(){...},
        methods:{...}
    })

    相关使用参考demo/test1.html

    要使用这个工具类，需要把/webz/js映射成webz.js，并在页面引入脚本:
        <script src="/webz/js/base.js"></script>
        <script src="/webz/js/packs.js"></script>
    或者
        <script src="/webz/js/base.js"></script>
        <script src="jquery路径"></script>
        <script src="vue路径"></script>
        <script src="/webz/js/utiils.js"></script>

任意一个运行后，尝试访问网址：
http://127.0.0.1:8080/page/test1.html
http://127.0.0.1:8080/func/abc?d=e&f=g

```
