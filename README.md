# 日常物件 · 前端实战

商品搜索、分类筛选、价格排序、购物袋、数量调整、金额计算和本地订单。

## 在线访问
https://zhu-huiwen.github.io/daily-objects-demo/

## GitHub Pages 版本
- 原生 HTML / CSS / JavaScript，无构建依赖。
- 商品通过 fetch 请求 products.json，搜索筛选在浏览器执行。
- 购物袋、演示订单保存在当前浏览器 localStorage；创建订单没有 POST 请求，无支付、无发货、无服务端库存扣减。
- 订单不会跨设备同步，清理浏览器数据会删除本地记录。

## DevTools 查看位置
- Network：刷新或搜索时查看 products.json 的请求与响应。
- Console：商品查询、购物袋变化和本地订单日志。
- Sources：在 loadProducts、calculateCartTotal、submitOrder 设置断点，检查变量与计算过程。

## 完整本地接口版本
local-server/server.py 保留 Python 商品与订单接口，用于 GET 参数、POST 请求体和响应分析。将 local-server/shop.js 替换到项目根目录的副本，在该副本执行 python3 local-server/server.py，访问 http://127.0.0.1:8000。不要在 Pages 线上版本中替换。
