#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import os
import qeXml as xq
import qeXml.commands as cm


def setFields(fd):
    fd_opts = fd['options']

    nums = xq.Numerics()
    inout = xq.InputOutput()
    opts = xq.Options()
    fnums = nums.getField(fd['numerics'])
    fios = inout.getField(fd['inputoutput'])
    fopts = opts.getField(fd_opts)

    return (fios, fnums, fopts)

k_points = {'type': 'tpiba', 'npoints': 10, 'text': '''
0.1250000  0.1250000  0.1250000   1.00
0.1250000  0.1250000  0.3750000   3.00
0.1250000  0.1250000  0.6250000   3.00
0.1250000  0.1250000  0.8750000   3.00
0.1250000  0.3750000  0.3750000   3.00
0.1250000  0.3750000  0.6250000   6.00
0.1250000  0.3750000  0.8750000   6.00
0.1250000  0.6250000  0.6250000   3.00
0.3750000  0.3750000  0.3750000   1.00
0.3750000  0.3750000  0.6250000   3.00'''}


def example01(diag):


    BASE_DIR = '/opt/lmpizarro/python/'
    PSEUDODIR = BASE_DIR + 'espresso-5.3.0/pseudo/'
    HOME_CALCS = BASE_DIR +  'qeCalcs/'
    BIN_PATH = BASE_DIR +  'espresso-5.3.0/bin'
    # Number of processor for mpi calcs
    NP = 1

    PREFIX = 'silicon%s'%diag

    OUTDIR = os.path.abspath(HOME_CALCS + '/' + PREFIX + '/')

    # An object to generate commands to run qe
    rqe = cm.RunQe(BIN_PATH, NP, OUTDIR)


    inFileName = 'si.scf.%s.xml'%diag
    outFileName = 'si.scf.%s.out'%diag

    if os.path.isdir(OUTDIR) == False:
        os.makedirs(OUTDIR)

    fd = {'numerics': {
        'ecutWfc': 18.0,
        'diagonalization': diag,
        'mixing_mode': 'plain',
        'mixing_beta': 0.7,
        'convthreshold': 1.0E-8,
    },
        'inputoutput': {
        'restart_mode': 'from_scratch',
        'pseudodir': PSEUDODIR,
        'outdir': OUTDIR,
        'tstress': 'True',
        'tprnfor': 'True'},
        'options': {
        'occupations': 'smearing',
        'smearing': 'marzari-vanderbilt',
        'degauss': 0.05
    }}

    (inout, nums, opts) = setFields(fd)

    especies = [{'name': 'Si', 'pseudofile': 'Si.rel-pbe-rrkj.UPF', 'mass': 28.086}]

    ae_d = xq.setAtomicSpecies(especies)

    k_p_d = xq.setK_points(k_points)

    positions =[{'name':'Si', 'position':[0.0, 0.0, 0.0]},{'name':'Si', 'position':[0.25, 0.25, 0.25]}]
    pos_si1 = xq.setPosition(positions[0])
    pos_si2 = xq.setPosition(positions[1])

    al_d = xq.setAtomicList([pos_si1, pos_si2], 'alat')

    ce_d = xq.setCell(2, 10.2, [0.0, 0.0, 0.0, 0.0, 0.0, ])

    in_d = xq.setInput('scf', PREFIX, [
        ce_d, ae_d, al_d, inout, nums, opts, k_p_d])

    # Create the xml tree
    QExmlTree = xq.createXML(in_d)
    # Write the xml file
    xq.writeQe(QExmlTree, OUTDIR + '/' + inFileName)


    rqe.writeMpiScript(inFileName, outFileName)


if __name__ == '__main__':
    diago=['cg', 'david']

    for d in diago:
        example01(d)
