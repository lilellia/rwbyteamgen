from flask import Flask, render_template, url_for, request, flash
import os

import teamgen

app = Flask(__name__)
app.config['SECRET_KEY'] = '...'

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.form

        c1 = {f['char1_first'][:1].upper(), f['char1_last'][:1].upper()} - {''}
        c2 = {f['char2_first'][:1].upper(), f['char2_last'][:1].upper()} - {''}
        c3 = {f['char3_first'][:1].upper(), f['char3_last'][:1].upper()} - {''}
        c4 = {f['char4_first'][:1].upper(), f['char4_last'][:1].upper()} - {''}
        fix_leader = f.get('fix_leader')

        if len(c1 | c2 | c3 | c4) == 0:
            # simply return a few random choices
            options_nosub = set(teamgen.get_random_teams(10))

            options_nosub_dict = [
                {'team': t, 'name': n, 'hexstring': h.upper()}
                for t, n, h in options_nosub
            ]

            return render_template(
                'index.html',
                options_nosub=sorted(options_nosub_dict, key=lambda t: (t['team'], t['name']))
            )
        else:
            options_nosub = set(teamgen.teamgen(c1, c2, c3, c4, False, fix_leader))
            options_withsub = set(teamgen.teamgen(c1, c2, c3, c4, True, fix_leader)) - options_nosub

            options_nosub_dict = [
                {'team': t, 'name': n, 'hexstring': h.upper()}
                for t, n, h in options_nosub
            ]
            options_withsub_dict = [
                {'team': t, 'name': n, 'hexstring': h.upper()}
                for t, n, h in options_withsub
            ]

            allowed_subs = ', '.join(f'{k}\u2192{v}' for k, v in teamgen.SUBS.items())

            return render_template(
                'index.html',
                options_nosub=sorted(options_nosub_dict, key=lambda t: (t['team'], t['name'])),
                options_withsub=sorted(options_withsub_dict, key=lambda t: (t['team'], t['name'])),
                allowed_subs=allowed_subs
            )
    else:
        return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='127.0.0.1', port=5000)      # localhost
    app.run(host='0.0.0.0', port=port)          # server
