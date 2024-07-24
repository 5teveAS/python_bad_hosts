from flask import Flask, request, Response, abort

app = Flask(__name__)

def get_paginated_content(file_path, pages):
    with open(file_path, 'r') as file:
        content = file.read()

    # Divide el contenido en el número de páginas especificado
    lines = content.splitlines()
    lines_per_page = len(lines) // pages
    if len(lines) % pages != 0:
        lines_per_page += 1  # Asegura que todas las líneas se incluyan
    
    paginated_content = []
    for i in range(pages):
        start = i * lines_per_page
        end = (i + 1) * lines_per_page
        paginated_content.append('\n'.join(lines[start:end]))

    return paginated_content

@app.route('/api/dns-filter/bad-hosts', methods=['GET'])
def fishing_domains():
    try:
        pages = int(request.args.get('pages', 1))
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(400, 'El parámetro de página debe ser un entero')

    if pages < 1 or page < 1 or page > pages:
        abort(400, 'Parámetros de página inválidos')

    file_path = 'data/domains.txt'
    
    paginated_content = get_paginated_content(file_path, pages)

    if page > len(paginated_content):
        abort(404, 'Página no encontrada')

    return Response(paginated_content[page - 1], mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)