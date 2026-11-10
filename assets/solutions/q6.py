# Q6 
# ########################################################################
# Solution 1 
# ########################################################################
with open('python_script.py','r') as in_file:
    with open('q6-output-1.txt','w') as out_file:
        count = 1
        inside_docstring = False
        
        for line in in_file:
            line = line.rstrip('\n')
            
            # remove the spaces in front and at the back
            line = line.strip(' ')
     
            # check whether this is a function header
            if (len(line) > 4 and line[0:4] == 'def '):
                
                # remove 'def ' in front and ':' at the back
                function_header = line[4:len(line) - 1]

                out_file.write(str(count) + '. ' + function_header + '\n')
                count += 1
            
            elif line == '"""':
                # This is either the beginning or the end of a docstring.
                if not inside_docstring:
                    inside_docstring = True
                else:
                    out_file.write('\n')
                    inside_docstring = False
            
            elif len(line) >= 6 and line[0:3] == '"""' and line[len(line) - 3:len(line)] == '"""':
                # This is the scenario when the docstring is in one line.
                line = line[3:len(line)-3]
                out_file.write('\t' + line + '\n')
                out_file.write('\n')
            
            elif len(line) >= 3 and line[0:3] == '"""':
                # This is the beginning of a docstring.
                inside_docstring = True
                line = line[3:len(line)]
                out_file.write('\t' + line + '\n')
            
            elif len(line) >=3 and line[len(line) - 3:len(line)] == '"""':
                # This is the end of a docstring.
                line = line[0:len(line) - 3]
                out_file.write('\t' + line + '\n')
                out_file.write('\n')
                inside_docstring = False
            
            elif inside_docstring:
                out_file.write('\t' + line + '\n')

# ########################################################################
# Solution 2
# ########################################################################
with open('python_script.py','r') as in_file:
    with open('q6-output.txt','w') as out_file:
        count = 1
        in_docstring = False
        for line in in_file:
            line = line.rstrip('\n')
            #detect start of function
            if 'def' in line:
                index1 = line.index(' ')
                index2 = line.index(':')
                funct_def = line[index1+1:index2]
                out_file.write(str(count) + '. ' + funct_def + '\n')
                count += 1
            # detect first line of docstring
            elif '"""' in line and not in_docstring:         
                in_docstring = True       # start of docstring
                line = line.lstrip(' "')  # clean start of line
                if len(line) > 0:         # if len(line) == 0 skip the line (line with only """)
                    if '"""' in line:
                        line = line.rstrip('"')
                        out_file.write('\t' + line + '\n\n')
                        in_docstring = False
                    else:
                        out_file.write('\t' + line + '\n')
            # detect last line in docstring
            elif '"""' in line and in_docstring:
                line = line.strip(' "')    # remove spaces on the left and """ on the right
                if len(line) > 0:
                    out_file.write('\t' + line + '\n\n')
                else:
                    out_file.write('\n')                
                in_docstring = False
            # detect lines in docstring
            elif in_docstring:
                out_file.write(line + '\n')
                            