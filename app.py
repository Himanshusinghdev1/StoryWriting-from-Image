import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from src.Imagecaption.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.Imagecaption.pipeline.image_captioning_pipeline import ImageCaptioningPipeline
from src.Imagecaption.pipeline.story_generation_pipeline import StoryGenerationPipeline

UPLOAD_FOLDER = "data/raw"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key_here'  # needed for flash messages

# Ensure upload and output folders exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/ingested", exist_ok=True)
os.makedirs("data/captions", exist_ok=True)
os.makedirs("data/stories", exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Validate and save file
        if 'image' not in request.files or request.files['image'].filename == '':
            flash('No file selected!')
            return redirect(request.url)
        file = request.files['image']

        if not allowed_file(file.filename):
            flash('Unsupported file type!')
            return redirect(request.url)

        # Get theme and word limit
        theme = request.form.get('theme', 'adventure')
        try:
            word_limit = int(request.form.get('word_limit', 400))
        except ValueError:
            word_limit = 400

        filename = file.filename
        upload_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(str(upload_path))

        # Run pipeline stages
        # 1. Data Ingestion
        data_pipeline = DataIngestionPipeline()
        ingested_path = data_pipeline.main(upload_path)

        # 2. Image Captioning
        caption_pipeline = ImageCaptioningPipeline()
        caption = caption_pipeline.main(ingested_path)

        # 3. Story Generation (accepts theme and word limit)
        caption_file = Path("data/captions") / f"{ingested_path.stem}_caption.txt"
        story_pipeline = StoryGenerationPipeline()
        story = story_pipeline.main(caption_file, theme, word_limit)

        # Show results
        return render_template('result.html',
                               filename=filename,
                               caption=caption,
                               story=story,
                               theme=theme,
                               word_limit=word_limit)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f"File uploaded: {filename}"

if __name__ == "__main__":
    app.run(debug=True)
