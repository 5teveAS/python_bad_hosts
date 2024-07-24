from flask import Flask, request, Response, abort
import random

app = Flask(__name__)

def get_content(file_path, pages_count, is_random):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)

    # Validación y ajuste de pages_count
    if pages_count is None:
        pages_count = total_lines
    elif pages_count < 1 or pages_count > total_lines:
        abort(400, 'Número de líneas inválido')

    # Selección de líneas (secuenciales o aleatorias)
    if is_random.lower() == 'true':
        selected_lines = random.sample(lines, pages_count)
    else:
        selected_lines = lines[:pages_count]

    # Juntar las líneas seleccionadas en un solo bloque de texto
    content = ''.join(selected_lines)

    return content

@app.route('/api/dns-filter/bad-hosts', methods=['GET'])
def fishing_domains():
    try:
        pages_count = request.args.get('count', None)
        is_random = request.args.get('random', 'false').lower()
        if pages_count:
            pages_count = int(pages_count)
    except ValueError:
        abort(400, 'Parámetros inválidos')

    file_path = 'data/domains.txt'
    
    content = get_content(file_path, pages_count, is_random)

    return Response(content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)