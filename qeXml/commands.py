# -*- coding: utf-8 -*-

class Qsub(object):
    qsub = '''#PBS -N EquilNPT100
    #PBS -l nodes=8:ppn=2
    #PBS -S /bin/bash
    #PBS -q verylong
    #PBS -o nas-0-0.local:$PBS_O_WORKDIR/$PBS_JOBID.output                                                                   
    #PBS -e nas-0-0.local:$PBS_O_WORKDIR/$PBS_JOBID.error 
    cd $PBS_O_WORKDIR

    cat $PBS_NODEFILE > $PBS_O_WORKDIR/$PBS_JOBID.machines
    cat $PBS_NODEFILE | uniq > $PBS_O_WORKDIR/$PBS_JOBID.mpd.hosts

    NUM_PROCS=`cat $PBS_O_WORKDIR/$PBS_JOBID.machines|wc -l`
    NUM_NODES=`cat $PBS_O_WORKDIR/$PBS_JOBID.mpd.hosts|wc -l`

    echo NUM_PROCS = $NUM_PROCS
    echo NUM_NODES = $NUM_NODES

    export NUM_PROCS 
    export NUM_NODES

    BIN_EXE=''

    /home/pizarro/opt/openmpi-1.8.1-gcc/bin/mpirun -machinefile $PBS_O_WORKDIR/$PBS_JOBID.machines -np $NUM_PROCS $BIN_EXE'''

    def __init__(self, name, nodes, in_file, out_file, bin_exe, run_path):
        self.name = name
        self.nodes = nodes
        self.in_file = in_file
        self.run_path = run_path
        self.bin_exe = bin_exe
        self.out_file = out_file 

        self.qsub_split = self.qsub.split('\n')
        self.qsub_split[0] ="#PBS -N %s"%self.name  
        self.qsub_split[1] ="#PBS -l nodes=%d:ppn=2"%self.nodes  
        self.qsub_split[20] ='BIN_EXE="%s"'%self.bin_exe

    def gen_file(self):
        self.file_content = ""
        for e in self.qsub_split:
            self.file_content += e.strip() + "\n"
             

        fout = open(self.run_path + '/run.qsub','w')
        fout.write(self.file_content)

        fout.close()

class RunQe:

    def __init__(self, path, np, outdir, pbs=False):
        self.path_binaries = path
        self.NP = np
        self.PBS = pbs
        self.OUTDIR = outdir
    

    def getMpiCommandLine (self, inFileName, outFileName, pgm):
        pw_bin = self.path_binaries + '/' + pgm
        if self.NP > 1:
            return '%s -i %s  > %s'% (pw_bin, inFileName, outFileName)
        else:
            return '%s -i %s  > %s'% (pw_bin, inFileName, outFileName)


    def writeMpiScript(self, inFileName, outFileName, pgm='pw.x'):
        commandLine = self.getMpiCommandLine(inFileName, outFileName, pgm)

        f = open(self.OUTDIR + '/' + 'command.sh', 'w')

        f.writelines(commandLine)

        f.close()


        # name, nodes, in_file, out_file, bin_exe, run_path):
        qs = Qsub(inFileName, self.NP, inFileName, outFileName, commandLine, self.OUTDIR)
        qs.gen_file()
 
