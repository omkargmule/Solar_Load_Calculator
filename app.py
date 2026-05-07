import os
import subprocess
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
UPLOAD_DIR = "bill_repository"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-extraction', methods=['POST'])
def trigger_engine():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return "No file uploaded", 400

    # Save the file
    save_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
    uploaded_file.save(save_path)

    output_xlsx = "Solar_Load_Result.xlsx"
    template_xlsx = "Solar_Load_Template.xlsx"

    # This calls your logic_processor.py script
    try:
        subprocess.run([
            "python", "logic_processor.py",
            save_path,
            "--template", template_xlsx,
            "--output", output_xlsx
        ], check=True)
        
        return send_file(output_xlsx, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(port=5050)