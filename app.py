from flask import Flask, request, send_file, render_template_string, send_from_directory
import img2pdf
from PIL import Image
import os
import io
import zipfile
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

@app.route('/convert/jpg2pdf', methods=['POST'])
def jpg2pdf():
    image_files = request.files.getlist('images')
    image_paths = []
    for img in image_files:
        filename = secure_filename(img.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        img.save(path)
        image_paths.append(path)
    output_pdf = os.path.join(UPLOAD_FOLDER, "output.pdf")
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    for path in image_paths:
        os.remove(path)
    return send_file(output_pdf, as_attachment=True, download_name="converted.pdf")

@app.route('/convert/png2jpg', methods=['POST'])
def png2jpg():
    image_files = request.files.getlist('images')
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename = secure_filename(os.path.splitext(img.filename)[0] + ".jpg")
            image = Image.open(img).convert("RGB")
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="converted_jpg.zip", mimetype='application/zip')

@app.route('/convert/compress', methods=['POST'])
def compress():
    image_files = request.files.getlist('images')
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename = secure_filename(img.filename)
            image = Image.open(img)
            img_bytes = io.BytesIO()
            if image.format == 'JPEG':
                image.save(img_bytes, format='JPEG', quality=50, optimize=True)
            else:
                image.save(img_bytes, format='PNG', optimize=True)
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="compressed.zip", mimetype='application/zip')

@app.route('/convert/resize', methods=['POST'])
def resize():
    image_files = request.files.getlist('images')
    width = int(request.form.get('width'))
    height = int(request.form.get('height'))
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename = secure_filename(img.filename)
            image = Image.open(img)
            resized = image.resize((width, height))
            img_bytes = io.BytesIO()
            if image.format == 'JPEG':
                resized.save(img_bytes, format='JPEG')
            else:
                resized.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="resized.zip", mimetype='application/zip')

@app.route('/convert/rotate', methods=['POST'])
def rotate():
    image_files = request.files.getlist('images')
    angle = int(request.form.get('angle', 90))
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename = secure_filename(img.filename)
            image = Image.open(img)
            rotated = image.rotate(-angle, expand=True)
            img_bytes = io.BytesIO()
            if image.format == 'JPEG':
                rotated.save(img_bytes, format='JPEG')
            else:
                rotated.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="rotated.zip", mimetype='application/zip')

@app.route('/convert/crop', methods=['POST'])
def crop():
    image_files = request.files.getlist('images')
    left = int(request.form.get('left', 0))
    upper = int(request.form.get('upper', 0))
    right = int(request.form.get('right', 100))
    lower = int(request.form.get('lower', 100))
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename = secure_filename(img.filename)
            image = Image.open(img)
            cropped = image.crop((left, upper, right, lower))
            img_bytes = io.BytesIO()
            if image.format == 'JPEG':
                cropped.save(img_bytes, format='JPEG')
            else:
                cropped.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="cropped.zip", mimetype='application/zip')

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
                img_bytes.seek(0)
                zf.writestr('animated.gif', img_bytes.read())
        else:
            for img in image_files:
                filename = secure_filename(os.path.splitext(img.filename)[0] + ".png")
                image = Image.open(img).convert("RGBA")
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name=f"converted_{fmt}.zip", mimetype='application/zip')

@app.route('/convert/watermark', methods=['POST'])
def watermark():
    image_files = request.files.getlist('images')
    text = request.form.get('text', 'PixelCraft')
    opacity = int(request.form.get('opacity', 50))
    mem_zip = io.BytesIO()
    from PIL import ImageDraw, ImageFont
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
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
            if image.mode == "RGBA":
                watermarked = watermarked.convert("RGB")
            watermarked.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="watermarked.zip", mimetype='application/zip')

@app.route('/convert/removebg', methods=['POST'])
def removebg():
    image_files = request.files.getlist('images')
    mem_zip = io.BytesIO()
    import numpy as np
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for img in image_files:
            filename = secure_filename(img.filename)
            image = Image.open(img).convert("RGBA")
            arr = np.array(image)
            r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
            mask = ((r > 240) & (g > 240) & (b > 240))
            arr[:,:,3][mask] = 0
            new_img = Image.fromarray(arr)
            img_bytes = io.BytesIO()
            new_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            zf.writestr(filename, img_bytes.read())
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name="nobg.zip", mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True)
