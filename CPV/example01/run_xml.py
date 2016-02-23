#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import os
import sys
import qeXml as xq
import qeXml.commands as cm

def example01(nstep):

    BASE_DIR = '/opt/lmpizarro/python/'
    PSEUDODIR = BASE_DIR + 'espresso-5.3.0/pseudo/'
    HOME_CALCS = BASE_DIR +  'qeCalcs/'
    BIN_PATH = BASE_DIR +  'espresso-5.3.0/bin'
    # Number of processor for mpi calcs
    NP = 1

    PREFIX = 'sio2cp'

    OUTDIR = os.path.abspath(HOME_CALCS + '/' + PREFIX + '/')


    # An object to generate commands to run qe
    rqe = cm.RunQe(BIN_PATH, NP, OUTDIR)


    inFileName = 'si.cp.xml'
    outFileName = 'si.cp.out'

    if os.path.isdir(OUTDIR) == False:
        os.makedirs(OUTDIR)



    fd = {'numerics': {
        'ecutWfc': 20.0,
        'ecutrho': 150.0,
    },
        'inputoutput': {
        'restart_mode': 'from_scratch',
        'pseudodir': PSEUDODIR,
        'outdir': OUTDIR,
        'iprint': 20,
        'startingwfc': 'random'
    },
        'options': {
        'nbnd': 48,
        'qcutz': 150,
        'q2sigma': 2.05,
        'ecfixed': 16.0
    },
        'fields': {
        'nspin': 1
    },
        'cp': {
        'nstep': nstep,
        'dt': 5.0,
        'ion_dynamics': 'none',
        'isave': 20,
        'nr1b': 16,
        'nr2b': 16,
        'nr3b': 16,
        'electron_dynamics': 'damp',
        'electron_damping': 0.2,
        'emass': 700.0,
        'emass_cutoff': 3.0,
        'ndr': 90,
        'ndw': 91,
        'ampre': 0.01
    }
    }

    cp = xq.CP()
    nums = xq.Numerics()
    ios = xq.InputOutput()
    opts = xq.Options()
    fields = xq.Fields()

    cp_params = fd['cp']
    num_params = fd['numerics']
    ios_params = fd['inputoutput']
    opts_params = fd['options']
    fields_params = fd['fields']

    inout_d = ios.getField(ios_params)
    nums_d = nums.getField(num_params)
    opts_d = opts.getField(opts_params)
    field_d = fields.getField(fields_params)
    cp_d = cp.getField(cp_params)

    especies = [{'name': 'O', 'pseudofile': 'O.pz-rrkjus.UPF', 'mass': 16.086},
                {'name': 'Si', 'pseudofile': 'Si.pz-vbc.UPF', 'mass': 28.086},
                ]

    ae_d = xq.setAtomicSpecies(especies)

    positions = xq.readPositions('cpsio2pos.txt')
    al_d = xq.setAtomicList(positions, 'bohr')

    ce_d = xq.setCell(8, 9.28, [1.73206, 1.09955, 0.0, 0.0, 0.0, ])

    in_d = xq.setInput('cp', PREFIX, [
                    ce_d, ae_d, al_d, inout_d, nums_d, opts_d, field_d, cp_d])

    # Create the xml tree
    QExmlTree = xq.createXML(in_d)
    # Write the xml file
    xq.writeQe(QExmlTree, OUTDIR + '/' + inFileName)


    rqe.writeMpiScript(inFileName, outFileName, 'cp.x')


if __name__ == '__main__':
    example01(200)

