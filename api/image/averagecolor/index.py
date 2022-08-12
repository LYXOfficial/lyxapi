from http.server import BaseHTTPRequestHandler
import requests
from PIL import Image
from io import BytesIO
 
class handler(BaseHTTPRequestHandler):
    def getAverageColor(self,url):
        yzmdata = requests.get(url)
        tempIm = BytesIO(yzmdata.content)
        im = Image.open(tempIm)
        w,h=im.size #读取图片宽、高
        im = im.convert('RGB')#将im对象转换为RBG对象
        rtotal,gtotal,btotal=0,0,0
        array = []
        for x in range(w):#输出图片对象每个像素点的RBG值到array
            for y in range(h):
                r, g, b = im.getpixel((x,y))#获取当前像素点RGB值
                rtotal+=r
                gtotal+=g
                btotal+=b
        print(rtotal/w/h,gtotal/w/h,btotal/w/h)
    def do_GET(self):
        if not ("?" in self.path and "url" in self.path):
            self.send_response(400)
            self.wfile.write("Your request parameter must have \'URL\'")
            return
        p=self.path.split("?")[1].split("&")
        for i in p:
            if p[:2]=="url":
                url=p[3:]
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(self.getAverageColor(url).encode())
        return