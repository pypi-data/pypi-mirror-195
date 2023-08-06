def schedule_read(path):
    projects, layers, dates = [], [], []
    f = open(path, 'r').readlines()
    for line in f:
        if line[:8] == 'Schedule':
            s = line[9:-1].split(',')
            if s[1] != '':
                projects.append(s[0])
                layers.append(s[1])
                dates.append(s[-1])
            if s[3] != '':
                projects.append(s[0])
                layers.append(s[3])
                dates.append(s[-1])
    return projects, layers, dates