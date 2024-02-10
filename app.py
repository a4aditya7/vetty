from flask import Flask, render_template_string, request
import os
import html
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/<file_name>', methods=['GET'])
def home(file_name='file1.txt'):
    try:
        file_content = {}
        files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
        if file_name not in files:
            raise FileNotFoundError('File not found!')
        encodings = ['utf-8', 'utf-16', 'gbk']
        for encoding in encodings:
            try:
                with open(file_name, 'r', encoding=encoding) as f:
                    file_content = f.read()
                break
            except Exception as e:
                pass
        if not file_content:
            raise Exception('Error reading file: Unsupported encoding or file is empty.')
        start_line = int(request.args.get('start', 1))
        end_line_param = request.args.get('end', None)
        if end_line_param is not None:
            end_line = int(end_line_param)
        else:
            end_line = None
        lines = file_content.split('\n')
        if start_line < 1 or start_line > len(lines):
            raise ValueError('Invalid start line number!')
        if end_line is not None and (end_line < 1 or end_line > len(lines) or end_line < start_line):
            raise ValueError('Invalid end line number!')
        selected_lines = lines[start_line - 1:end_line]
        escaped_lines = []
        for line in selected_lines:
            segments = re.split(r'(<[^>]+>)', line)
            escaped_segments = [segment if segment.startswith('<') else html.escape(segment) for segment in segments]
            escaped_lines.append(''.join(escaped_segments))
        return render_template_string('file_content.html', file_name=file_name, escaped_lines=escaped_lines)
    except Exception as e:
        return render_error_page(str(e))

def render_error_page(error_message):
    return render_template_string('error_page.html', error_message=error_message)

@app.errorhandler(500)
def internal_server_error(e):
    return render_error_page('Internal Server Error')

if __name__ == '__main__':
    app.run(debug=True)
