from flask import Flask, request, send_file, render_template_string, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os, io, zipfile, numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

def process_images(save_func, download_name):
    image_files = request.files.getlist('images')
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename, data = save_func(img)
            zf.writestr(filename, data)
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name=download_name, mimetype='application/zip')

@app.route('/convert/png2jpg', methods=['POST'])
def png2jpg():
    def save_func(img):
        filename = secure_filename(os.path.splitext(img.filename)[0] + ".jpg")
        image = Image.open(img).convert("RGB")
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        return filename, img_bytes.getvalue()
    return process_images(save_func, "converted_jpg.zip")

@app.route('/convert/compress', methods=['POST'])
def compress():
    def save_func(img):
        filename = secure_filename(img.filename)
        image = Image.open(img)
        img_bytes = io.BytesIO()
        if image.format == 'JPEG':
            image.save(img_bytes, format='JPEG', quality=50, optimize=True)
        else:
            image.save(img_bytes, format='PNG', optimize=True)
        return filename, img_bytes.getvalue()
    return process_images(save_func, "compressed.zip")

@app.route('/convert/resize', methods=['POST'])
def resize():
    width = int(request.form.get('width'))
    height = int(request.form.get('height'))
    def save_func(img):
        filename = secure_filename(img.filename)
        image = Image.open(img)
        resized = image.resize((width, height))
        img_bytes = io.BytesIO()
        fmt = 'JPEG' if image.format == 'JPEG' else 'PNG'
        resized.save(img_bytes, format=fmt)
        return filename, img_bytes.getvalue()
    return process_images(save_func, "resized.zip")

@app.route('/convert/rotate', methods=['POST'])
def rotate():
    angle = int(request.form.get('angle', 90))
    def save_func(img):
        filename = secure_filename(img.filename)
        image = Image.open(img)
        rotated = image.rotate(-angle, expand=True)
        img_bytes = io.BytesIO()
        fmt = 'JPEG' if image.format == 'JPEG' else 'PNG'
        rotated.save(img_bytes, format=fmt)
        return filename, img_bytes.getvalue()
    return process_images(save_func, "rotated.zip")

@app.route('/convert/crop', methods=['POST'])
def crop():
    left = int(request.form.get('left', 0))
    upper = int(request.form.get('upper', 0))
    right = int(request.form.get('right', 100))
    lower = int(request.form.get('lower', 100))
    def save_func(img):
        filename = secure_filename(img.filename)
        image = Image.open(img)
        cropped = image.crop((left, upper, right, lower))
        img_bytes = io.BytesIO()
        fmt = 'JPEG' if image.format == 'JPEG' else 'PNG'
        cropped.save(img_bytes, format=fmt)
        return filename, img_bytes.getvalue()
    return process_images(save_func, "cropped.zip")

@app.route('/convert/jpg2pnggif', methods=['POST'])
def jpg2pnggif():
    image_files = request.files.getlist('images')
    fmt = request.form.get('format', 'png').lower()
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        if fmt == 'gif':
            images = [Image.open(img).convert("RGB") for img in image_files]
            if images:
                img_bytes = io.BytesIO()
                images[0].save(img_bytes, format='GIF', save_all=True, append_images=images[1:], loop=0)
                zf.writestr('animated.gif', img_bytes.getvalue())
        else:
            for img in image_files:
                filename = secure_filename(os.path.splitext(img.filename)[0] + ".png")
                image = Image.open(img).convert("RGBA")
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                zf.writestr(filename, img_bytes.getvalue())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name=f"converted_{fmt}.zip", mimetype='application/zip')

@app.route('/convert/watermark', methods=['POST'])
def watermark():
    text = request.form.get('text', 'PixelCraft')
    opacity = int(request.form.get('opacity', 50))
    def save_func(img):
        filename = secure_filename(img.filename)
        image = Image.open(img).convert("RGBA")
        watermark_layer = Image.new("RGBA", image.size, (255,255,255,0))
        draw = ImageDraw.Draw(watermark_layer)
        font_size = int(min(image.size) / 10)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        textwidth, textheight = draw.textsize(text, font=font)
        x = (image.width - textwidth) // 2
        y = (image.height - textheight) // 2
        draw.text((x, y), text, fill=(255,255,255,int(255*opacity/100)), font=font)
        watermarked = Image.alpha_composite(image, watermark_layer)
        img_bytes = io.BytesIO()
        watermarked = watermarked.convert("RGB")
        watermarked.save(img_bytes, format='JPEG')
        return filename, img_bytes.getvalue()
    return process_images(save_func, "watermarked.zip")

@app.route('/convert/removebg', methods=['POST'])
def removebg():
    def save_func(img):
        filename = secure_filename(img.filename)
        image = Image.open(img).convert("RGBA")
        arr = np.array(image)
        mask = ((arr[:,:,0] > 240) & (arr[:,:,1] > 240) & (arr[:,:,2] > 240))
        arr[:,:,3][mask] = 0
        new_img = Image.fromarray(arr)
        img_bytes = io.BytesIO()
        new_img.save(img_bytes, format='PNG')
        return filename, img_bytes.getvalue()
    return process_images(save_func, "nobg.zip")

if __name__ == '__main__':
    app.run(debug=True)
