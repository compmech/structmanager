class TopometryResults():
    """TODO add summary

    TODO add description

    """
    def __init__(self, path):
        self.maxgrad = 1.
        pchfile = open(path, 'r')
        lines = pchfile.readlines(1000000)
        self.elem_t = []
        for line in lines:
            if line.strip() == '' or line[:1] == '$':
                continue
            self.elem_t.append([  int(line.split()[0]) ,
                                   float(line.split()[1])  ])
        pchfile.close()
        self.elem_t.sort(key = i : i[1])














