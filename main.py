import uasyncio as asyncio
from machine import Pin, PWM

def web_page(color: str) -> str:
    html = """
    <!doctype html>
    <html lang="fr">
        <head>
            
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="icon" href="data:,">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            <title>ESP Chouette</title>
        </head>
    <body>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <div class="text-center">
          <h1>Ma chouette chouette en couleurs</h1> 
          <form method="get">
              <div class="form-group">
                    <input class="form-control" type="color" id="owl" name="owl" value="""+ color +""" onchange="location.href='?owl='+value.replace('#', '%23')">
              </div>
          </form>
          
     
      </div>
      </body></html>
      """
    return html

def color_intensity_to_duty(c:int):
    return 1023 - int(c*1023/255)

def setcolor(color):
    rgb = [color_intensity_to_duty(c) for c in color]
    for c in range(3):
        rgbleb[c].duty(rgb[c])

def rgbtohexa(rgb):
    return '#%02x%02x%02x' % tuple(rgb)

def hexatorgb(hexa: str):
    print(hexa)
    hexa = hexa.lstrip('#')
    print("-",hexa,"-")
    lv = len(hexa)
    return list((int(hexa[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))

async def adjust_color():
    sign = lambda a: (a>0) - (a<0)
    global current_color_rgb
    global new_color_rgb
    while True:
        if new_color_rgb != current_color_rgb:
            current_color_rgb = [color + sign(new_color-color)
                              for color, new_color in zip(current_color_rgb, new_color_rgb)]
            setcolor(current_color_rgb)
        await  asyncio.sleep(0.01)

@asyncio.coroutine
def serve(reader, writer):
    try:
        request = str(await reader.read())
        colorfound = request.find('/?owl=')
        if colorfound == 6:
            global new_color
            new_color = str(request[15:21])
            global new_color_rgb
            new_color_rgb = hexatorgb(new_color)
            new_color = rgbtohexa(new_color_rgb)
        await writer.awrite("HTTP/1.0 200 OK\r\n\r\n"+web_page(new_color)+"\r\n")
    except OSError as e:
        pass
    finally:
        await writer.aclose()
        print("Finished processing request")



frequency = 1000
rgbpin  =[5, 4, 2]
rgbleb = [PWM(Pin(pin), frequency) for pin in rgbpin]

for led in rgbleb:
  led.duty(1023)

current_color_rgb = [0, 0, 0]
current_color = rgbtohexa(current_color_rgb)
new_color = "#FFFFFF"
new_color_rgb = hexatorgb(new_color)

loop = asyncio.get_event_loop()
loop.call_soon(asyncio.start_server(serve, station.ifconfig()[0], 80))
loop.create_task(adjust_color())
loop.run_forever()
loop.close()