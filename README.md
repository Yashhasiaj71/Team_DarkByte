<div align="center">

  <h1>🛡️ Team DarkByte - Advanced Detection Engine</h1>
  
  <p>
    <strong>A powerful AI-driven platform for Text Analysis, Plagiarism Detection, and OCR Processing.</strong>
  </p>

  <p>
    <a href="#features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#getting-started">Getting Started</a>
  </p>

  <br />

</div>

<hr />

<h2 id="features">🚀 Features</h2>

<ul>
  <li><strong>🤖 AI Text Detection</strong>: Utilize machine learning models (Scikit-learn) to distinguish between human and AI-generated text.</li>
  <li><strong>📝 Plagiarism Checking</strong>: Advanced algorithms to detect copied content and ensure originality.</li>
  <li><strong>📷 OCR Engine</strong>: Integrated <strong>EasyOCR</strong> and <strong>OpenCV</strong> to extract text from images and scanned documents for analysis.</li>
  <li><strong>⚡ Asynchronous Processing</strong>: Powered by <strong>Celery</strong> and <strong>Redis</strong> for handling heavy validation tasks in the background.</li>
  <li><strong>📄 File Support</strong>: Analyze raw text, PDFs (via PyPDF2), and images.</li>
  <li><strong>🔒 Secure & Scalable</strong>: Built with <strong>Django 5</strong> and <strong>Django REST Framework</strong>.</li>
</ul>

<hr />

<h2 id="tech-stack">🛠️ Tech Stack</h2>

<table align="center">
  <tr>
    <td align="center"><strong>Backend</strong></td>
    <td align="center"><strong>Frontend</strong></td>
    <td align="center"><strong>AI & Data</strong></td>
    <td align="center"><strong>Infrastructure</strong></td>
  </tr>
  <tr>
    <td>
      <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
      <br />
      <img src="https://img.shields.io/badge/DRF-a30f2d?style=for-the-badge&logo=django&logoColor=white" />
    </td>
    <td>
      <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
      <br />
      <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
    </td>
    <td>
      <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
      <br />
      <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
    </td>
    <td>
      <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" />
      <br />
      <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
    </td>
  </tr>
</table>

<hr />

<h2 id="getting-started">🏁 Getting Started</h2>

<h3>🔹 Prerequisites</h3>
<ul>
  <li>Python 3.10+</li>
  <li>Node.js 18+</li>
  <li>Redis Server (running locally or via Docker)</li>
</ul>

<h3>⬇️ Installation</h3>

<h4>1. Clone the Repository</h4>
<pre>
git clone https://github.com/Yashhasiaj71/Team_DarkByte.git
cd Team_DarkByte
</pre>

<h4>2. Backend Setup</h4>
<pre>
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
</pre>

<h4>3. Start Celery Worker (for Async Tasks)</h4>
<pre>
# In a new terminal (backend directory)
celery -A config worker --loglevel=info
</pre>

<h4>4. Frontend Setup</h4>
<pre>
cd ../frontend
npm install
npm run dev
</pre>

<hr />

<p align="center">
  Developed with ❤️ by Team DarkByte
</p>

