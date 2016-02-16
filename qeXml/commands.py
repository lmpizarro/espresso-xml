# -*- coding: utf-8 -*-


def mpiCommand(NP, inFileName, outFileName, outDir):
    commandLine = 'mpirun -np %d pw.x -i %s  > %s'% (NP, inFileName, outFileName)

    f = open(outDir + '/' + 'command.sh', 'w')

    f.writelines(commandLine)

    f.close()
 
