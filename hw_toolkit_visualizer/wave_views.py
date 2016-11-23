from flask.blueprints import Blueprint
from flask.templating import render_template


waveBp = Blueprint('wave', __name__,
                          template_folder='templates/wave/')


@waveBp.route('/wave-test/')
def connections_test():
    return render_template('wave_test.html')
