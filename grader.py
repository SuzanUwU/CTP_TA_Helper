"""Lab 7 behavior-based grader. Execute only trusted student submissions."""
from student_names import extract_student_name
import ast
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

QUESTIONS = ['q1a','q1b','q2a','q2b','q2c','q3','q4a','q4b','q5a','q5b','q6','q7']
FUNCTIONS = {
 'q1a': ('print_alternate_lines', [('q1-input-1.txt',), ('q1-input-2.txt',)]),
 'q1b': ('print_alternate_columns', [('q1-input-3.txt',), ('q1-input-4.txt',)]),
 'q2a': ('get_universities_founded_before', [('universities-1.txt',1905), ('universities-2.txt',1800)]),
 'q2b': ('get_average_num_students', [('universities-1.txt',), ('universities-2.txt',)]),
 'q2c': ('search_with_keyword', [('universities-1.txt','california'), ('universities-2.txt','university')]),
 'q5a': ('get_matrix', [('matrix.txt',)]),
 'q5b': ('get_matrix_transpose', [('matrix.txt',)]),
}
OUTPUT_FILES = {'q4a':'transactions-output-1.txt','q4b':'transactions-output-2.txt','q6':'q6-output-1.txt'}
MAX_ZIP_BYTES = 12*1024*1024
MAX_UNPACKED_BYTES = 35*1024*1024


def unpack_zip(data, destination):
    if len(data)>MAX_ZIP_BYTES: raise ValueError('ZIP exceeds 12 MB')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        total=0
        for entry in archive.infolist():
            path=Path(entry.filename)
            if path.is_absolute() or '..' in path.parts or entry.is_dir() and len(path.parts)>30:
                raise ValueError('Unsafe ZIP path')
            if entry.file_size > MAX_UNPACKED_BYTES: raise ValueError('Oversized file in ZIP')
            total += entry.file_size
            if total>MAX_UNPACKED_BYTES or len(path.parts)>30 or len(archive.infolist())>1500:
                raise ValueError('ZIP exceeds extraction limits')
            # Reject Unix symlinks
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('Symlinks are not supported')
        archive.extractall(destination)


def find_script(root, question):
    matches=[p for p in root.rglob('*.py')
             if p.name.lower().endswith(question.lower()+'.py')
             and (p.stem.lower()==question.lower() or p.stem[-len(question)-1] in ' _-')
             and '__MACOSX' not in p.parts
             and not any(x.startswith('.') for x in p.relative_to(root).parts)]
    if not matches:return None
    return sorted(matches,key=lambda p:(p.stem.lower()!=question.lower(),len(p.relative_to(root).parts),str(p).lower()))[0]


def canonical_script_name(filename):
    """Return the standard q*.py name for a prefixed LMS submission filename."""
    stem=Path(filename).stem
    match=re.search(r'(?:^|[\s_-])(q\d+[a-z]?)$',stem,re.IGNORECASE)
    return match.group(1).lower()+'.py' if match else filename


def run_python(work, code, timeout=4):
    cmd=[sys.executable,'-I','-c',code]
    try:
        def limits():
            if os.name!='nt':
                import resource
                resource.setrlimit(resource.RLIMIT_CPU,(3,4))
                resource.setrlimit(resource.RLIMIT_AS,(384*1024*1024,384*1024*1024))
                resource.setrlimit(resource.RLIMIT_FSIZE,(2*1024*1024,2*1024*1024))
        proc=subprocess.run(cmd,cwd=work,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,preexec_fn=limits if os.name!='nt' else None,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        return proc.returncode,proc.stdout[-15000:],proc.stderr[-1500:]
    except subprocess.TimeoutExpired:
        return -1,'','Execution timed out'


def normalize_output(s):
    return '\n'.join(line.rstrip() for line in s.replace('\r\n','\n').strip().splitlines())


def normalize_transactions(text, grouped=False):
    if not grouped:return sorted(line.strip() for line in text.splitlines() if line.strip())
    groups={}; month=None
    for line in text.splitlines():
        if not line.strip():continue
        match=re.match(r'^\s*(\d\d-\d{4}):\s*total transaction amount is\s*\$([\d.]+)',line)
        if match:
            month=match.group(1);groups[month]={'total':float(match.group(2)),'items':[]}
        elif month:
            groups[month]['items'].append(tuple(x.strip() for x in line.split('\t') if x.strip()))
    return groups


def compare(question,expected,actual):
    if question=='q4a':return normalize_transactions(expected)==normalize_transactions(actual)
    if question=='q4b':
        a,b=normalize_transactions(expected,True),normalize_transactions(actual,True)
        return a.keys()==b.keys() and all(abs(a[k]['total']-b[k]['total'])<0.011 and Counter(a[k]['items'])==Counter(b[k]['items']) for k in a)
    if question=='q6':return normalize_output(expected)==normalize_output(actual)
    if question=='q3':
        # Reference solution prints three alternative implementations; accept any single correct block.
        lines=[x.strip() for x in normalize_output(expected).splitlines() if x.strip()]
        actual_lines=[x.strip() for x in normalize_output(actual).splitlines() if x.strip()]
        return actual_lines==lines or actual_lines==lines[:3] or actual_lines==lines[3:6] or actual_lines==lines[6:9]
    return normalize_output(expected)==normalize_output(actual)


def make_runner(question,solution=False):
    if question in FUNCTIONS:
        name,cases=FUNCTIONS[question]
        # Import from explicit file path to avoid ambiguous module search paths.
        return """import importlib.util,json,contextlib,io,sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path.cwd()))\np=Path(%r)\ns=importlib.util.spec_from_file_location('student_module',p)\nm=importlib.util.module_from_spec(s)\nwith contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m)\nf=getattr(m,%r)\nfor args in %r:\n buf=io.StringIO()\n with contextlib.redirect_stdout(buf): result=f(*args)\n print(json.dumps({'return':result,'printed':buf.getvalue()},sort_keys=True,default=str))\n""" % (question+'.py',name,cases)
    return "from pathlib import Path\nexec(compile(Path(%r).read_text(encoding='utf-8-sig'),%r,'exec'),{'__name__':'__main__','__file__':%r})" % (question+'.py',question+'.py',question+'.py')


def grade_question(root, question, starter, solutions):
    script=find_script(root,question)
    if not script:return {'status':'Missing','score':0,'detail':f'{question}.py not found'}
    with tempfile.TemporaryDirectory() as temp:
        base=Path(temp); student=base/'student'; reference=base/'reference';student.mkdir();reference.mkdir()
        for work in (student,reference):
            for p in starter.iterdir():
                if p.is_file() and (p.suffix=='.txt' or p.name=='python_script.py'):shutil.copy2(p,work/p.name)
        # Copy student's adjacent Python files for legitimate local imports (e.g. q5b imports q5a).
        for p in script.parent.iterdir():
            if p.is_file() and p.suffix.lower()=='.py' and p.stat().st_size<300000:
                shutil.copy2(p,student/canonical_script_name(p.name))
        shutil.copy2(script,student/(question+'.py'))
        for p in solutions.glob('*.py'):shutil.copy2(p,reference/p.name)
        # Some reference scripts rely on starter files.
        for work in (student,reference):
            for old in OUTPUT_FILES.values():
                (work/old).unlink(missing_ok=True)
        if question=='q6':
            # The provided reference Q6 is top-level code, despite the assignment requesting a function.
            # We test the documented output-file behavior, with a fallback to calling extract_functions.
            student_code="""from pathlib import Path\np=Path('q6.py'); ns={'__name__':'__main__'}\nexec(compile(p.read_text(encoding='utf-8-sig'),'q6.py','exec'),ns)\nif callable(ns.get('extract_functions')):ns['extract_functions']('python_script.py','q6-output-1.txt')"""
            reference_code=make_runner(question)
        else:
            student_code=make_runner(question);reference_code=make_runner(question)
        rcode,rout,rerr=run_python(reference,reference_code)
        if rcode:return {'status':'Reference error','score':0,'detail':rerr or 'Reference failed'}
        scode,sout,serr=run_python(student,student_code)
        if scode:return {'status':'Error','score':0,'detail':serr or 'Student program exited unsuccessfully'}
        if question in OUTPUT_FILES:
            filename=OUTPUT_FILES[question]
            expected=(reference/filename).read_text(errors='replace') if (reference/filename).exists() else None
            actual=(student/filename).read_text(errors='replace') if (student/filename).exists() else None
            if actual is None:return {'status':'Failed','score':0,'detail':f'Missing output file: {filename}'}
            if expected is None:return {'status':'Reference error','score':0,'detail':'Reference output not generated'}
        else:expected,actual=rout,sout
        if question=='q7':
            # Nondeterministic output: check word boundaries, punctuation and middle-letter multiset.
            source=(starter/'talk.txt').read_text(errors='replace').split()
            output=actual.split()
            def valid(a,b):
                punct=",'!."
                if a and a[-1] in punct:
                    return b.endswith(a[-1]) and valid(a[:-1],b[:-1])
                return len(a)==len(b) and (len(a)<2 or (a[0]==b[0] and a[-1]==b[-1])) and Counter(a[1:-1])==Counter(b[1:-1])
            passed=len(source)==len(output) and all(valid(a,b) for a,b in zip(source,output))
        else:passed=compare(question,expected,actual)
        return {'status':'Passed' if passed else 'Failed','score':1 if passed else 0,'detail':'Output matched' if passed else 'Output differs from reference','expected':str(expected)[:450],'actual':str(actual)[:450]}


def grade_all(uploads, selected, starter, solutions):
    results=[]
    for filename,data in uploads:
        student_name=extract_student_name(filename)
        row={'student':student_name,'filename':filename,'questions':{},'total':0,'max':len(selected)}
        try:
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                unpack_zip(data,root)
                for q in selected:
                    row['questions'][q]=grade_question(root,q,starter,solutions)
                    row['total']+=row['questions'][q]['score']
        except Exception as exc:
            for q in selected:row['questions'][q]={'status':'Error','score':0,'detail':str(exc)[:250]}
        results.append(row)
    return results
