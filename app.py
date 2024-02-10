
from flask import Flask, render_template_string, request
import os
import html
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/<file_name>', methods=['GET'])
def home(file_name='file1.txt'):
    # Dictionary to store file content
    file_content = {}
    
    # List of files to read
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
    
    # Check if the requested file exists
    if file_name not in files:
        return render_error_page('File not found!')
    
    # List of encodings to try
    encodings = ['utf-8', 'utf-16', 'gbk']
    
    # Attempt to read the file with different encodings
    for encoding in encodings:
        try:
            # Read content of the requested file
            with open(file_name, 'r', encoding=encoding) as f:
                file_content = f.read()
            break  # Stop trying encodings if successful
        except Exception as e:
            pass  # Try next encoding
    
    # Check if file content is empty
    if not file_content:
        return render_error_page('Error reading file: Unsupported encoding or file is empty.')
    
    # Get start and end line numbers from query parameters
    start_line = int(request.args.get('start', 1))
    end_line_param = request.args.get('end', None)
    
    if end_line_param is not None:
        end_line = int(end_line_param)
    else:
        end_line = None
    
    # Split the content into lines
    lines = file_content.split('\n')
    
    # Check if start line number is valid
    if start_line < 1 or start_line > len(lines):
        return render_error_page('Invalid start line number!')
    
    # Check if end line number is valid
    if end_line is not None and (end_line < 1 or end_line > len(lines) or end_line < start_line):
        return render_error_page('Invalid end line number!')
    
    # Extract lines between start and end line numbers
    selected_lines = lines[start_line - 1:end_line]
    
    # Escape HTML entities in the content segments of each line
    escaped_lines = []
    for line in selected_lines:
        segments = re.split(r'(<[^>]+>)', line)
        escaped_segments = [segment if segment.startswith('<') else html.escape(segment) for segment in segments]
        escaped_lines.append(''.join(escaped_segments))
    
    # Render HTML page with file content
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Content</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #add8e6;
                }
                h1 {
                    color: #333;
                }
                h2 {
                    color: #666;
                }
                pre {
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
            </style>
        </head>
        <body>
            <h1><i>File Content</i></h1>
            <h2>{{ file_name }}</h2>
            <pre>{{ escaped_lines | join('\n') | safe }}</pre>
        </body>
        </html>
    ''', file_name=file_name, escaped_lines=escaped_lines)

def render_error_page(error_message):
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: yellow;
                }
                h1 {
                    color: #900;
                }
                p {
                    color: #900;
                }
            </style>
        </head>
        <body>
            <h1>Error</h1>
            <p>{{ error_message }}</p>
        </body>
        </html>
    ''', error_message=error_message)

@app.errorhandler(500)
def internal_server_error(e):
    return render_error_page('Internal Server Error')

if __name__ == '__main__':
    app.run(debug=True)



