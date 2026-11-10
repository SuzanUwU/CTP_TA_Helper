"""Lab 8 behavioral grader; student programs are untrusted, run only in an isolated VM."""
from student_names import extract_student_name
import ast, json, shutil, tempfile, zipfile, io
from pathlib import Path
from grader import unpack_zip, find_script, run_python, normalize_output, canonical_script_name

QUESTIONS=['q1a','q1b','q2','q3a','q3b','q3c','q4','q5a','q5b','q5c','q6']
CIPHER={chr(97+i):chr(97+(i+13)%26) for i in range(26)}
CASES={
 'q1a':('encrypt',[(CIPHER,'i love python'),(CIPHER,'hello world'),(CIPHER,'abc xyz')]),
 'q1b':('decrypt',[(CIPHER,'v ybir clguba'),(CIPHER,'uryyb jbeyq'),(CIPHER,'nop klm')]),
 'q2':('create_prime_dict',[([2,3,5,10,20,23],),([4,5,6,8,11,12],),([13,17,21,25,29],)]),
 'q4':('get_students_by_school',[({'Joe Tan':'SIS','Alan Lee':'SOE','George Wong':'SOSS','Liu Chee Hwa':'SOL','Ng Yew Tung':'SIS','Wendy Li':'SIS','Jerry Lim':'SOSS'},),({'A':'X','B':'X','C':'Y'},)]),
 'q5a':('count_words_in_file',[('spam_sms.txt',)]),
 'q6':('create_employee_dictionary',[('employees.txt',)])
}
# Each input sequence exercises the official reference's interactive flow.
INPUTS={'q3a':'Y\nLKCSB\nSR1-1\nN\n','q3b':'Y\nSCIS\nN\n','q3c':'Y\nSCIS\n30\nN\n','q6':'999999\nN\n'}

def run(work,code,stdin=None):
    # Existing runner doesn't support stdin; patch interactive scripts via a supplied input iterator.
    if stdin is not None:
        prefix="import builtins\n_inputs=iter("+repr(stdin.splitlines())+")\nbuiltins.input=lambda prompt='': (print(prompt,end=''),next(_inputs))[1]\n"
        code=prefix+code
    return run_python(work,code,timeout=5)

def runner(q):
    if q in CASES:
        name,cases=CASES[q]
        # For q6, import only function definitions to avoid the reference's interactive main program.
        loader=("import ast\nsrc=open('q6.py',encoding='utf-8-sig').read()\ntree=ast.parse(src)\ntree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.Import,ast.ImportFrom,ast.ClassDef))]\nns={'__name__':'grading_module'}\nexec(compile(tree,'q6.py','exec'),ns)\nf=ns['create_employee_dictionary']\n" if q=='q6' else
                "import importlib.util,contextlib,io\ns=importlib.util.spec_from_file_location('grading_module',"+repr(q+'.py')+")\nm=importlib.util.module_from_spec(s)\nwith contextlib.redirect_stdout(io.StringIO()):s.loader.exec_module(m)\nf=getattr(m,"+repr(name)+")\n")
        return "import json,contextlib,io,sys\nsys.path.insert(0,'.')\n"+loader+"for args in "+repr(cases)+":\n b=io.StringIO()\n with contextlib.redirect_stdout(b): result=f(*args)\n print(json.dumps({'result':result,'printed':b.getvalue()},sort_keys=True,default=str))\n"
    return "import sys\nsys.path.insert(0,'.')\nfrom pathlib import Path\nexec(compile(Path("+repr(q+'.py')+").read_text(encoding='utf-8-sig'),"+repr(q+'.py')+",'exec'),{'__name__':'__main__','__file__':"+repr(q+'.py')+"})"

def normalized(q,s):
    if q in ('q5b',):return sorted(x.strip() for x in s.splitlines() if x.strip())
    if q=='q5c':
        try:
            obj=ast.literal_eval(s.strip());return sorted((str(k),int(v)) for k,v in obj)
        except Exception:return normalize_output(s)
    if q in CASES:
        try:return [json.loads(line) for line in s.splitlines() if line.strip()]
        except Exception:return normalize_output(s)
    return normalize_output(s)

def grade_question(root,q,starter,solutions):
    script=find_script(root,q)
    if not script:return {'status':'Missing','score':0,'detail':q+'.py not found'}
    with tempfile.TemporaryDirectory() as d:
        base=Path(d);student=base/'student';reference=base/'reference';student.mkdir();reference.mkdir()
        for work in (student,reference):
            for p in starter.iterdir():
                if p.is_file() and p.suffix=='.txt':shutil.copy2(p,work/p.name)
        for p in script.parent.iterdir():
            if p.is_file() and p.suffix.lower()=='.py' and p.stat().st_size<300000:
                shutil.copy2(p,student/canonical_script_name(p.name))
        shutil.copy2(script,student/(q+'.py'))
        for p in solutions.glob('*.py'):shutil.copy2(p,reference/p.name)
        code=runner(q)
        # q3a's facility lookup must use an existing key; reference output is authoritative.
        if q=='q3a':
            first=(starter/'facilities.txt').read_text().splitlines()[0].split('\t')
            inputs='Y\n'+first[0]+'\n'+first[1]+'\nN\n'
        else:inputs=INPUTS.get(q)
        if q in ('q3b','q3c'):
            school=(starter/'facilities.txt').read_text().splitlines()[0].split('\t')[0]
            inputs='Y\n'+school+'\n'+('30\n' if q=='q3c' else '')+'N\n'
        rc,expected,err=run(reference,code,inputs)
        if rc:return {'status':'Reference error','score':0,'detail':err[-500:] or 'Reference failed'}
        rc,actual,err=run(student,code,inputs)
        if rc:return {'status':'Error','score':0,'detail':err[-650:] or 'Student execution failed'}
        passed=normalized(q,expected)==normalized(q,actual)
        return {'status':'Passed' if passed else 'Failed','score':int(passed),'detail':'Behavior matched reference' if passed else 'Behavior differs from reference','expected':expected[:500],'actual':actual[:500]}

def grade_all(uploads,selected,starter,solutions):
    results=[]
    for filename,data in uploads:
        row={'student':extract_student_name(filename),'filename':filename,'questions':{},'total':0,'max':len(selected)}
        try:
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);unpack_zip(data,root)
                for q in selected:
                    item=grade_question(root,q,starter,solutions)
                    row['questions'][q]=item;row['total']+=item['score']
        except Exception as e:
            for q in selected:row['questions'][q]={'status':'Error','score':0,'detail':str(e)[:250]}
        results.append(row)
    return results
