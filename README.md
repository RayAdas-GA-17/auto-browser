# Auto-browser

本项目是一个使用 Python 和 Selenium 实现的浏览器自动化操作工具.

## Auto-grab

定时填写腾讯文档, 将个人信息自动写入问卷中并提交. ~~适用于抢xxx, 请低调使用~~ :)

### 安装

1. 克隆仓库

    ```bash
    git clone https://github.com/RayAdas-GA-17/auto-browser.git
    ```

2. 安装 Python 3.x
3. 安装依赖包

   ```bash
   pip install selenium ntplib
   ```

4. 下载与当前浏览器版本一致的浏览器驱动
   1. 本项目默认使用 Edge 浏览器, 请下载对应版本的 [浏览器驱动](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH) 并放置于项目根目录下(或在 [`auto_grad.py`](./auto_grab.py#L120) 的`get_driver`中指定驱动的路径).
   2. 若使用其他浏览器, 请自行修改 [`auto_grad.py`](./auto_grab.py#L121) 的`get_driver`.
5. 在 [`auto_grad.py`](./auto_grab.py#L74) 中填写个人信息. `self_info` 中每个元素为 `["个人信息", "标签1|标签2"]`. 标签为问卷中需要填写的字段.

    ```python
    college_info = "某某学院"
    name_info = "某某某"
    ...
    self_info = [
        ...
        ["xxx@xx.com", "邮箱"],
        ...
    ]
   ```

### 运行

1. 在终端运行程序

   ```bash
   python auto_grab.py
   ```

2. 等待弹出的浏览器展示登录界面, 然后登录. (默认使用qq登录, 需要手动点击头像)
3. 在终端中输入问卷链接.
4. 输入设定时间, 格式为 `hh:mm:ss.f`. 例如 `17:00:01.5` 表示当天17点00分1.5秒后刷新页面并填写信息.
