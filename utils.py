def read_input(filename, project_line = None):

    if project_line == None:
        project_line = lambda x: x

    f = open(filename)
    
    lines = []

    for line in f.readlines():
        line = line.strip('\n')
        
        lines.append(project_line(line))
        
    return lines
