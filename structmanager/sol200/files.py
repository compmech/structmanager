def merge_temp_files(self):
    """Merge temporary files

    """
    #merging NASTRAN and GENESIS .dat files
    self.genesisfile.close()
    self.genesisfile = open(self.genesisfile.name, 'r')
    genfile = self.genesisfile
    genesislines = genfile.readlines(1000000000)
    if not genesislines:
        print 'GENESIS BULK DATA NOT FOUND!'
        raise
    genfile.close()
    #
    self.nastranfile.close()
    nastranfile = open(self.nastranfile.name, 'r')
    nastranlines = nastranfile.readlines(1000000000)
    if not nastranlines:
        print 'NASTRAN BULK DATA NOT FOUND!'
        raise
    nastranfile.close()
    #
    mergedfile = open(self.datname, 'w')
    #writing GENESIS card initial data
    mergedfile.write('$ Executive Control\n')
    mergedfile.write('$\n')
    mergedfile.write('POST = PUNCH\n')
    mergedfile.write('SOL COMPAT1\n')
    mergedfile.write('THREADS = 8\n')
    mergedfile.write('LENVEC=16000M\n')
    mergedfile.write('CEND\n')
    mergedfile.write('$\n')
    mergedfile.write('$ Solution Control\n')
    mergedfile.write('$\n')
    mergedfile.write('LINE = 64,80\n')
    mergedfile.write('ECHO = UNSORT(PARAM,DOPT)\n')
    mergedfile.write('APRINT = LAST\n')
    mergedfile.write('DPRINT = LAST\n')
    mergedfile.write('UPRINT = LAST\n')
    mergedfile.write('SIZING = POST\n')
    mergedfile.write('GRAPH = YES\n')
    mergedfile.write('$\n')
    mergedfile.write('$ Output options\n')
    mergedfile.write('$\n')
    mergedfile.write('DISP(PLOT) = ALL\n')
    mergedfile.write('FORCE(PLOT) = ALL\n')
    mergedfile.write('OLOAD(PLOT) = ALL\n')
    mergedfile.write('SPCFORCE(PLOT) = ALL\n')
    mergedfile.write('STRESS(PLOT) = ALL\n')
    mergedfile.write('$\n')
    mergedfile.write('$ Loadcase definitions\n')
    mergedfile.write('$\n')
    subcasecount=0
    for i in range(len(self.loads_list)):
        subcasecount += 1
        mergedfile.write('SUBCASE ' + str(subcasecount) + '\n')
        mergedfile.write('   LABEL = Loadcase ' + str(self.loads_list[i]) + '\n')
        mergedfile.write('   LOAD = ' + str(self.loads_list[i]) + '\n')
        mergedfile.write('   SPC = '  + str(self.spcs_list[i] ) + '\n')
    mergedfile.write('BEGIN BULK\n')
    mergedfile.write('DSCREEN,STRESS,-0.5,80\n')
    mergedfile.write('$\n')
    mergedfile.write('$ Parameters\n')
    mergedfile.write('$\n')
    mergedfile.write('PARAM    AUTOSPC     YES\n')
    mergedfile.write('PARAM     GRDPNT       0\n')
    mergedfile.write('PARAM   MAXRATIO1.0000+8\n')
    mergedfile.write('PARAM   POST    -1\n')
    mergedfile.write('$\n')
    mergedfile.write('$The following parameter activates BIGDOT\n')
    #mergedfile.write('DOPT,10\n')
    mergedfile.write('DOPT,' + str(self.num_cycles) + '\n')
    mergedfile.write('+,IREDCA,22222\n')
    mergedfile.write('+,OPTM,1\n')
    mergedfile.write('+,DELX,0.5\n')
    mergedfile.write('+,DXMIN,0.1\n')
    mergedfile.write('$\n')
    #copying GENESIS data
    mergedfile.write('$______________________________________________\n')
    mergedfile.write('$______________________________________________\n')
    mergedfile.write('$\n')
    mergedfile.write('$        BEGINNING GENESIS BULK DATA\n')
    mergedfile.write('$______________________________________________\n')
    mergedfile.write('$______________________________________________\n')
    for i in genesislines:
        mergedfile.write (i)
    startnext=False
    #copying NASTRAN data
    mergedfile.write('$______________________________________________\n')
    mergedfile.write('$______________________________________________\n')
    mergedfile.write('$\n')
    mergedfile.write('$        BEGINNING NASTRAN BULK DATA\n')
    mergedfile.write('$______________________________________________\n')
    mergedfile.write('$______________________________________________\n')
    skip_flag = False
    for i in nastranlines:
        if i[:5]=='PARAM': continue
        if startnext==True:
            if i.find(',') > -1:
                mergedfile.write(i)
            elif i.strip()[0:1] == '$':
                continue
            elif len(i.strip()) <= 1:
                continue
            elif i.find('ENDDATA') > -1:
                continue
            elif skip_flag:
                if i[:8].strip() == '+':
                    continue
                else:
                    skip_flag = False
            elif i[:4] == 'CBAR':
                mergedfile.write(i.strip()[:64] + '\n')
                continue
            if i[:8].strip() in self.newprops.keys():
                pcard = i[:8].strip()
                pid = int(i[8:16].strip())
                if pid in self.newprops[ pcard ].keys():
                    skip_flag = True
                    continue
            mergedfile.write(i.strip()[:72] + '\n')
        if i.find('BEGIN BULK')>-1 and startnext==False:
            startnext = True
    mergedfile.write('ENDDATA\n')
    mergedfile.close()
