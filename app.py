from pathlib import Path
import csv
import io
import json
import secrets
import tempfile
import zipfile
from flask import Flask, render_template, request, send_file, session, redirect, url_for, flash
import grader, grader8

app=Flask(__name__)
app.secret_key=secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH']=75*1024*1024
BASE=Path(__file__).parent
LABS={'7':(grader,BASE/'assets'/'starter',BASE/'assets'/'solutions'), '8':(grader8,BASE/'assets'/'lab8'/'starter',BASE/'assets'/'lab8'/'solutions')}
# Results stay in process memory only; restart clears them.
REPORTS={}

@app.get('/')
def index():
    report=REPORTS.get(session.get('report_id'))
    return render_template('index.html',labs={k:v[0].QUESTIONS for k,v in LABS.items()},report=report)

@app.post('/grade')
def grade():
    lab=request.form.get('lab','7')
    if lab not in LABS:
        flash('Invalid lab selected.');return redirect(url_for('index'))
    engine,STARTER,SOLUTIONS=LABS[lab]
    selected=[q for q in engine.QUESTIONS if q in request.form.getlist('questions')]
    uploads=[(f.filename,f.read()) for f in request.files.getlist('submissions') if f.filename.lower().endswith('.zip')]
    if not selected or not uploads:
        flash('Select at least one question and upload student ZIP files.');return redirect(url_for('index'))
    if len(uploads)>60:
        flash('Upload at most 60 ZIP files per batch.');return redirect(url_for('index'))
    if not STARTER.exists() or not SOLUTIONS.exists():
        flash('Starter and solution files are missing.');return redirect(url_for('index'))
    rows=engine.grade_all(uploads,selected,STARTER,SOLUTIONS)
    rows.sort(key=lambda row: (row['student'].casefold(), row['filename'].casefold()))
    key=secrets.token_urlsafe(16)
    REPORTS.clear();REPORTS[key]={'rows':rows,'selected':selected,'lab':lab}
    session['report_id']=key
    return redirect(url_for('index'))

@app.get('/export')
def export():
    report=REPORTS.get(session.get('report_id'))
    if not report:return redirect(url_for('index'))
    out=io.StringIO();writer=csv.writer(out)
    writer.writerow(['Student','ZIP filename']+[q.upper() for q in report['selected']]+['Total','Max','Details'])
    for r in report['rows']:
        writer.writerow([r['student'],r['filename']]+[r['questions'][q]['score'] for q in report['selected']]+[r['total'],r['max'],json.dumps({q:r['questions'][q]['status']+': '+r['questions'][q]['detail'] for q in report['selected']})])
    buffer=io.BytesIO(out.getvalue().encode('utf-8-sig'))
    return send_file(buffer,mimetype='text/csv',as_attachment=True,download_name='lab'+report['lab']+'_grades.csv')

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000,debug=False)
