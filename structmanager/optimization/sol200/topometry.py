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

    def sxe_build_zones(self, sxe_model)
        import simx
        for elem_t in self.elem_t:
            elid = elem_t[0]
            self.elems = {}
            elobj = sxe_model.elementPtrFromAppid(elid)
            elobj = simx.SXEElement(elobj)
            elobj.edge_connected_elements(True, True, 4.)
            elobj.newt = elem_t[1]
            self.elems[elid] = elobj
            #
        eref = elem_t[0][0]
        tref = elem_t[0][1]
        npart = [refel]
        self.elems = {}
        for i in xrange(1 , len(elem_t)):
            e = elem_t[i][0]
            t = elem_t[i][1]
            if t - tref > self.maxgrad:
                npart.append(e)
                eref = e
                tref = t
            self.elems[e].newpart = eref
        for elem_t














