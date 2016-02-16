# -*- coding: utf-8 -*-


class RunQe:

    def __init__(self, path, np, outdir, pbs=False):
        self.path_binaries = path
        self.NP = np
        self.PBS = pbs
        self.OUTDIR = outdir
    

    def getMpiCommandLine (self, inFileName, outFileName):
        pw_bin = self.path_binaries + '/pw.x'
        if self.NP > 1:
            return 'mpirun -np %d %s -i %s  > %s'% (self.NP, pw_bin, inFileName, outFileName)
        else:
            return '%s -i %s  > %s'% (pw_bin, inFileName, outFileName)


    def writeMpiScript(self, inFileName, outFileName):
        commandLine = self.getMpiCommandLine(inFileName, outFileName)

        f = open(self.OUTDIR + '/' + 'command.sh', 'w')

        f.writelines(commandLine)

        f.close()
 
