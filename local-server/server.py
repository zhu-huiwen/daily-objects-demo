import json, secrets, threading
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
PRODUCTS=[{'id':'p101','name':'随行笔记本','category':'文具','price':38,'color':'#d5c3a6','shape':'notebook','description':'把灵感留在纸上。','stock':126},{'id':'p102','name':'机械键盘 K87','category':'数码','price':399,'color':'#becbc5','shape':'keyboard','description':'每一次敲击，都恰到好处。','stock':48},{'id':'p103','name':'桌面阅读灯','category':'生活','price':169,'color':'#dfc8a6','shape':'lamp','description':'给专注的夜晚，一束柔光。','stock':72},{'id':'p104','name':'无线耳机 Air','category':'数码','price':259,'color':'#c5cdd8','shape':'headphones','description':'让世界安静，让音乐靠近。','stock':35},{'id':'p105','name':'陶瓷马克杯','category':'生活','price':69,'color':'#d7bdb4','shape':'cup','description':'从一杯温热，开始新的一天。','stock':96},{'id':'p106','name':'中性笔套装','category':'文具','price':29,'color':'#c4cbb1','shape':'pens','description':'落笔流畅，记录日常。','stock':210}]
ORDERS=[]
LOCK=threading.Lock()
class Handler(SimpleHTTPRequestHandler):
 def respond(self,status,body):
  b=json.dumps(body,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  u=urlparse(self.path);q=parse_qs(u.query)
  if u.path=='/api/products':
   keyword=q.get('keyword',[''])[0].strip().lower();category=q.get('category',['全部'])[0]
   items=[p.copy() for p in PRODUCTS if keyword in (p['name']+p['id']+p['description']).lower() and (category=='全部' or category==p['category'])]
   sort=q.get('sort',['featured'])[0]
   if sort in ['price-asc','price-desc']:items.sort(key=lambda p:p['price'],reverse=sort=='price-desc')
   return self.respond(200,{'code':0,'data':{'items':items,'total':len(items)}})
  if u.path=='/api/orders':return self.respond(200,{'code':0,'data':{'items':list(reversed(ORDERS))}})
  if u.path.startswith('/api/'):return self.respond(404,{'code':404,'message':'接口不存在'})
  return super().do_GET()
 def do_POST(self):
  if urlparse(self.path).path!='/api/orders':return self.respond(404,{'code':404,'message':'接口不存在'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length>100000:return self.respond(413,{'code':413,'message':'请求内容过大'})
   body=json.loads(self.rfile.read(length));items=body.get('items',[])
   if not isinstance(items,list) or not items or len(items)>6:raise ValueError('请先添加商品')
   with LOCK:
    checked=[];seen=set()
    for line in items:
     product=next((p for p in PRODUCTS if p['id']==line.get('id')),None);qty=line.get('quantity')
     if not product or type(qty) is not int or qty<1 or qty>product['stock'] or product['id'] in seen:raise ValueError('商品数量不正确或库存不足，请刷新后重试')
     seen.add(product['id']);checked.append((product,qty))
    total=sum(p['price']*qty for p,qty in checked)
    order={'id':'DD'+datetime.now().strftime('%Y%m%d')+secrets.token_hex(3).upper(),'items':[{'id':p['id'],'name':p['name'],'price':p['price'],'quantity':qty} for p,qty in checked],'total':total,'status':'已创建','createdAt':datetime.now().strftime('%Y-%m-%d %H:%M')}
    for p,qty in checked:p['stock']-=qty
    ORDERS.append(order)
   return self.respond(201,{'code':0,'data':order})
  except (ValueError,TypeError,AttributeError):return self.respond(400,{'code':400,'message':'商品数量不正确或库存不足，请刷新后重试'})
print('Daily Objects → http://127.0.0.1:8000',flush=True)
ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
