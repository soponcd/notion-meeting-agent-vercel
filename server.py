# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/meetings.create', methods=['POST'])
def create_meeting():
    data = request.json or {}
    # Auto-normalize field names
    data['start_time'] = data.get('start_time') or data.get('start')
    data['end_time'] = data.get('end_time') or data.get('end')
    required = ['title', 'date', 'start_time', 'end_time']
    for f in required:
        if f not in data or not data[f]:
            return jsonify({'status': 'error', 'message': f'Missing required field: {f}'}), 400

    # Mock Notion record creation
    meeting = {
        'title': data['title'],
        'date': data['date'],
        'start': data['start_time'],
        'end': data['end_time']
    }
    return jsonify({
        'status': 'success',
        'message': 'Meeting record created successfully',
        'meeting': meeting
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
