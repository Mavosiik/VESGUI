from io import BytesIO
from flask import Flask, send_file, request, send_from_directory
from ves import render_ves
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def serve_pil_image(img):
  """
    Tato funkcia umozni obrazok z kniznice PIL ulozit do virtualneho suboru v pamati a ten subor potom vratit ako HTTP odpoved
  """
  img_io = BytesIO()
  img.save(img_io, 'PNG', quality=70)
  img_io.seek(0)
  return send_file(img_io, mimetype='image/png')



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  """
    Tato funkcia bude odpovedat na vsetky ostatne HTTP poziadavky, pre ktore nemame specialnu funkciu. Bude hladat subory v priecinku public.
  """
  if (len(path) == 0): # ak nezadany ziaden subor, teda cesta / chceme index.html
    return send_from_directory('public', 'index.html')

  return send_from_directory('public', path)


@app.route('/render', methods=['post'])
def render():
  """
    Tato funkcia dostane v HTTP poziadavke zdrojovy kod pre VES a pozadovanu sirku, vyrenderuje obrazok a vrati ho ako HTTP odpoved
  """
  ves = request.form.get('ves') # nacitanie hodnoty ktoru sme dostali v poziadavke
  width = request.form.get('width') # nacitanie hodnoty ktoru sme dostali v poziadavke
  print(ves)
  img = render_ves(ves, width) # tu posleme VES riadky do funkcie render_ves z projektu z prvého polroka
  return serve_pil_image(img) # vratime vyrenderovany obrazok ako jpg
