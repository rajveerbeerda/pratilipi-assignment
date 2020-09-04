from flask import redirect, render_template, flash, Blueprint, request, url_for, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from src import db
from src.models import User, Stories

import os
import json

from datetime import datetime

main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')

# Routes

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
	stories = Stories.query.filter_by(category='story').limit(4)
	return render_template('dashboard.html', stories=stories)

@main_bp.route('/view-all-stories/', methods=['GET'])
@login_required
def view_all():
	stories = Stories.query.filter_by(category='story')
	return render_template('view_all.html', stories=stories)

@main_bp.route('/view-story/<story_id>', methods=['GET'])
@login_required
def view_story(story_id):
	story = Stories.query.filter_by(id=story_id).first()
	content = ''
	with open('./src/static/' + story.story_path, 'r') as f:
		content = str(f.read())
	return render_template('view_story.html', story=story, content=content)

@main_bp.route('/update-count', methods=["POST"])
def update_count():
    if request.method=="POST":
        data = dict(json.loads(request.get_data()))
        story_id = data['story_id']
        story = Stories.query.filter_by(id=story_id).first()

        if 'total_views' in data.keys():
        	story.seen_by += 1

        story.live_users += int(data['value'])
        db.session.commit()
        return json.dumps({"status":"ok"})

@main_bp.route('/live_data/<story_id>', methods=["GET"])
def live_data(story_id):
	story = Stories.query.filter_by(id=story_id).first()
	return jsonify(live_views=story.live_users, total_views=story.seen_by)

