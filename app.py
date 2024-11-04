from flask import Flask, request, jsonify, render_template, redirect, url_for

from database import database
from routes import comment_create, comment_update, comment_read

app = Flask("automatic-core-review-report")


@app.route('/comment', methods=['POST'])
def create_comment():
    json_data = request.get_json()
    comment_create.create(json_data)
    return jsonify({'message': 'comment added'})


@app.route('/comment/update', methods=['GET'])
def update_comment():
    id_comment_internal = request.args.get('idCommentInternal', type=int)
    tp_status = request.args.get('tpStatus', type=int)

    if id_comment_internal is None or tp_status is None:
        return jsonify({'error': 'incorrect parameter'}), 400

    if not comment_update.update(tp_status, id_comment_internal):
        return jsonify({'error': 'comment not found'}), 404

    return jsonify({'message': 'comment status updated'})


@app.route('/comment', methods=['GET'])
def read_comment():
    page_size = request.args.get('pageSize', type=int)
    page_number = request.args.get('pageNumber', type=int)
    tp_status = request.args.get('tpStatus', type=int)

    return jsonify(comment_read.read(tp_status, page_size, page_number))


@app.route('/review')
def review():
    page_number = request.args.get('pageNumber', default=1, type=int)
    workspace_name = request.args.get('dsWorkspaceName', default="", type=str)
    data = comment_read.read(0, 1, page_number, workspace_name)

    qt_total = data['qtTotal']
    has_next = data['hasNext']

    if len(data['data']) == 0 and qt_total >= 1:
        return redirect(url_for(request.endpoint, pageNumber=qt_total))

    if len(data['data']) == 0:
        comment = {}
        page_number = 0
    else:
        comment = data['data'][0]

    return render_template('review.html', comment=comment, qtTotal=qt_total, nrPageNumber=page_number, hasNext=has_next)


@app.route('/health')
def health_check():
    if database.check_connection():
        return "OK", 200
    else:
        return "Error", 500


@app.route('/home')
def home():
    workspaces = comment_read.read_workspaces(0)
    return render_template('home.html', workspaces=workspaces)


@app.route('/')
def index():
    return redirect('/home')


if __name__ == '__main__':
    database.migration()
    app.run(host='0.0.0.0', port=8080)
