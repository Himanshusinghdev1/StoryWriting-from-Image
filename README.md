# 🖼️➡️📝 Image to Story Generator

An AI-powered web application that transforms images into captivating stories using advanced machine learning models for image captioning and story generation.

[🚀 Demo Example](https://drive.google.com/file/d/1s3caQOkUvjP9RpHgNyUe7GDPfq1aOojy/view?usp=sharing) | [📖 Documentation](https://github.com/Himanshusinghdev1/StoryWriting-from-Image) | [🤝 Contributing](CONTRIBUTING.md)



***

## ✨ Features

- 🖼️ **Smart Image Processing** - Upload and automatically resize/validate images
- 🤖 **AI-Powered Captioning** - Generate detailed descriptions using BLIP/Florence-2 models
- 📚 **Story Generation** - Create themed stories with customizable word limits
- 🎨 **Multiple Themes** - Adventure, fantasy, mystery, romance, sci-fi, and more
- 🌐 **Dual Interface** - Both Flask web app and Streamlit interface
- ☁️ **API-Based Inference** - No local model loading required for deployment
- 🔄 **Modular Pipeline** - Clean MLOps architecture with separate stages
- 📱 **Responsive Design** - Works on desktop and mobile devices

***

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Himanshusinghdev1/StoryWriting-from-Image.git
cd StoryWriting-from-Image
```

### 2. Create Environment

```bash
# Create virtual environment
python -m venv story_env

# Activate environment
# On Windows:
story_env\Scripts\activate
# On macOS/Linux:
source story_env/bin/activate
```

### 3. Setup Project Structure

```bash
# Run template.py to create project structure automatically
python template.py
```

### 4. Install Dependencies

```bash
# Method 1: Using setup.py (Recommended)
python setup.py install

# Method 2: Using requirements.txt
pip install -r requirements.txt
```

### 5. Environment Configuration

Create `.env` file in project root:

```env
# Hugging Face API Token (Get from: https://huggingface.co/settings/tokens)
HF_API_KEY=hf_your_huggingface_token_here

# Together.ai API Key (Get from: https://api.together.xyz/settings/api-keys)
TOGETHER_API_KEY=your_together_api_key_here
```

***

## 🏃♂️ How to Run

### Option 1: Complete Pipeline (main.py)

```bash
# Run the full 3-stage pipeline
python main.py

# Follow prompts to:
# 1. Add image to data/raw/ folder
# 2. Enter story theme (adventure, fantasy, etc.)
# 3. Set word limit (100-1000 words)
```

### Option 2: Streamlit Web App

```bash
# Launch interactive web interface
streamlit run app.py

# Access at: http://localhost:8501
```

***

## 🔧 Project Workflow

### Stage 1: Data Ingestion Pipeline
```bash
# Automatically handles:
# - Image validation and format checking
# - Resizing and preprocessing
# - Directory structure creation
```

### Stage 2: Image Captioning Pipeline
```bash
# Process images using:
# - BLIP model via Hugging Face Inference API
# - Florence-2 for enhanced caption quality
# - Automatic caption saving and logging
```

### Stage 3: Story Generation Pipeline
```bash
# Generate stories with:
# - Together.ai Llama models
# - Customizable themes and word limits
# - Context-aware narrative generation
```

***

## 📁 Project Structure

```
StoryWriting-from-Image/
│
├── 📄 app.py                      # Streamlit web application
├── 📄 main.py                     # Complete pipeline execution
├── 📄 template.py                 # Auto-create project structure
├── 📄 setup.py                    # Package installation and setup
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env.example               # Environment variables template
├── 📄 render.yaml                # Render deployment configuration
│
├── 📁 src/Imagecaption/
│   ├── 📁 components/
│   │   ├── 📄 data_ingestion.py        # Stage 1: Image processing
│   │   ├── 📄 image_captioning.py      # Stage 2: AI captioning
│   │   └── 📄 story_generation.py      # Stage 3: Story creation
│   │
│   ├── 📁 pipeline/
│   │   ├── 📄 data_ingestion_pipeline.py
│   │   ├── 📄 image_captioning_pipeline.py
│   │   └── 📄 story_generation_pipeline.py
│   │
│   ├── 📁 config/
│   │   └── 📄 configuration.py          # Configuration management
│   │
│   ├── 📁 entity/
│   │   └── 📄 config_entity.py          # Data classes
│   │
│   └── 📁 utils/
│       └── 📄 common.py                 # Utility functions
│
├── 📁 config/
│   ├── 📄 config.yaml                   # Main configuration
│   └── 📄 params.yaml                   # Model parameters
│
├── 📁 data/
│   ├── 📁 raw/                          # Input images
│   ├── 📁 ingested/                     # Processed images
│   ├── 📁 captions/                     # Generated captions
│   └── 📁 stories/                      # Generated stories
│
├── 📁 templates/                        # Flask HTML templates
├── 📁 static/                           # CSS, JS, images
├── 📁 .streamlit/                       # Streamlit configuration
└── 📁 logs/                             # Application logs
```

***

## 🛠️ Development Workflow

### 1. Update Code Components

```bash
# Modify individual pipeline stages:
# - src/Imagecaption/components/data_ingestion.py
# - src/Imagecaption/components/image_captioning.py  
# - src/Imagecaption/components/story_generation.py
```

### 2. Update Configuration

```yaml
# config/config.yaml - Update model settings
image_captioning:
  florence2_model_name: "microsoft/Florence-2-large-ft"
  revision_id: "4a12a2b"

story_generation:
  together_model_name: "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
  max_tokens: 700
```

### 3. Test Pipeline Stages

```bash
# Test individual stages:
python -m src.Imagecaption.pipeline.data_ingestion_pipeline
python -m src.Imagecaption.pipeline.image_captioning_pipeline
python -m src.Imagecaption.pipeline.story_generation_pipeline
```

### 4. Run Complete Workflow

```bash
# Execute full pipeline
python main.py
```

***

## 📦 Requirements

### Core Dependencies

```txt
# Web Frameworks
streamlit>=1.25.0
flask>=2.3.0
gunicorn>=20.1.0

# AI/ML Libraries
requests>=2.28.0
pillow>=9.0.0
python-dotenv>=1.0.0

# Configuration & Utils
pyyaml>=6.0
ensure>=1.0.2
python-box[all]>=7.0.0
joblib>=1.3.0

# API Clients
together>=0.2.7
```

### Installation Methods

```bash
# Method 1: Development installation
pip install -e .

# Method 2: Production installation  
pip install -r requirements.txt

# Method 3: Setup script
python setup.py develop
```

***

***

## Way of Doing

### Basic Usage

```python
from src.Imagecaption.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.Imagecaption.pipeline.image_captioning_pipeline import ImageCaptioningPipeline
from src.Imagecaption.pipeline.story_generation_pipeline import StoryGenerationPipeline

# Stage 1: Process image
ingestion = DataIngestionPipeline()
processed_image = ingestion.main("path/to/image.jpg")

# Stage 2: Generate caption
captioning = ImageCaptioningPipeline()
caption = captioning.main(processed_image)

# Stage 3: Create story
story_gen = StoryGenerationPipeline()
story = story_gen.main(caption, theme="adventure", word_limit=400)
```

### Streamlit App Usage

1. 📤 **Upload Image**: Drag & drop or browse for image files
2. 🎨 **Choose Theme**: Select from adventure, fantasy, mystery, etc.
3. 📏 **Set Word Limit**: Choose between 100-1000 words
4. ✨ **Generate**: Click to create your story
5. 📖 **View Results**: Read generated caption and story

***

## 🔧 Configuration Options

### Model Configuration

```yaml
# config/config.yaml
image_captioning:
  ingested_data_dir: "data/ingested"
  captions_dir: "data/captions"
  florence2_model_name: "microsoft/Florence-2-large-ft"
  revision_id: "4a12a2b"

story_generation:
  captions_dir: "data/captions"
  stories_dir: "data/stories"
  together_model_name: "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
  max_tokens: 700
  temperature: 0.75
```

### Streamlit Configuration

```toml
# .streamlit/config.toml
[theme]
base = "auto"
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F7F7F7"
textColor = "#262730"
font = "sans serif"
```

***

## 📊 Performance & Optimization

### API vs Local Model Comparison

| Aspect | API Inference | Local Model |
|--------|---------------|-------------|
| **Memory Usage** | ✅ Low (~100MB) | ❌ High (~4-8GB) |
| **Deployment** | ✅ Easy | ❌ Complex |
| **Latency** | ⚠️ Network dependent | ✅ Fast |
| **Cost** | ⚠️ Per API call | ✅ One-time setup |
| **Scalability** | ✅ Auto-scaling | ❌ Limited |

### Optimization Tips

- 🚀 Use **API inference** for cloud deployment
- 💾 Implement **caching** for repeated images
- 🔄 Enable **async processing** for multiple requests
- 📊 Monitor **API usage** and rate limits

***

## 🤝 Contributing

### Development Setup

```bash
# 1. Fork the repository
git clone https://github.com/YOUR_USERNAME/StoryWriting-from-Image.git

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Install development dependencies
pip install -e ".[dev]"

# 4. Make changes and test
python -m pytest tests/

# 5. Submit pull request
git push origin feature/amazing-feature
```

### Code Standards

- ✅ Follow **PEP 8** style guidelines
- 📝 Add **docstrings** to all functions
- 🧪 Write **unit tests** for new features
- 📋 Update **documentation** for changes

***

## 📞 Support & Community



| Resource | Link |
|----------|------|
| 🐛 **Bug Reports** | [GitHub Issues](https://github.com/Himanshusinghdev1/StoryWriting-from-Image/issues) |
| 📧 **Email Support** | [your.email@example.com](mailto:singhhimanshu33456@gmail.com) |
| 💼 **LinkedIn** | [Your LinkedIn Profile](www.linkedin.com/in/himanshu-singh07) |



***

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

***

## 🙏 Acknowledgments

- 🤗 [Hugging Face](https://huggingface.co) - For providing excellent AI model APIs
- 🚀 [Together.ai](https://together.ai) - For powerful story generation capabilities
- 🎨 [Streamlit](https://streamlit.io) - For the amazing web framework
- 🖼️ [Florence-2](https://huggingface.co/models) - For state-of-the-art image captioning

***



**⭐ Star this repository if you found it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/Himanshusinghdev1/StoryWriting-from-Image.orks](https://img.shields.io/github/forks/Himanshusinghdev1/StoryWriting-from-Image.svg?github.com/Himanshusinghdev1/StoryWriting-from-Image/ by [Himanshu Singh](https://github.com/Himanshusinghdev1)**

