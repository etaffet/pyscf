#!/usr/bin/env python

import unittest
import numpy
import scipy.linalg
from pyscf import gto
from pyscf import scf
from pyscf import df
from pyscf import ao2mo
from pyscf import mcscf

b = 1.4
mol = gto.M(
verbose = 5,
output = '/dev/null',
atom = [
    ['N',(  0.000000,  0.000000, -b/2)],
    ['N',(  0.000000,  0.000000,  b/2)], ],
basis = {'N': 'ccpvdz', },
max_memory = 1,
)
m = scf.RHF(mol)
m.conv_tol = 1e-9
m.scf()

molsym = gto.M(
verbose = 5,
output = '/dev/null',
atom = [
    ['N',(  0.000000,  0.000000, -b/2)],
    ['N',(  0.000000,  0.000000,  b/2)], ],
basis = {'N': 'ccpvdz', },
max_memory = 1,
symmetry = True,
)
msym = scf.RHF(molsym)
msym.conv_tol = 1e-9
msym.scf()


class KnowValues(unittest.TestCase):
    def test_mc1step_4o4e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(m, 4, 4), auxbasis='weigend')
        emc = mc.mc1step()[0]
        self.assertAlmostEqual(emc, -108.913786407955, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()),
                               2.7015375913946591, 4)

    def test_mc2step_4o4e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(m, 4, 4), auxbasis='weigend')
        emc = mc.mc2step()[0]
        self.assertAlmostEqual(emc, -108.913786407955, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()),
                               2.7015375913946591, 4)

    def test_mc1step_4o4e_df(self):
        mc = mcscf.density_fit(mcscf.CASSCF(m, 4, 4), auxbasis='weigend')
        emc = mc.mc1step()[0]
        self.assertAlmostEqual(emc, -108.9105231091045, 7)

    def test_mc2step_4o4e_df(self):
        mc = mcscf.density_fit(mcscf.CASSCF(m, 4, 4), auxbasis='weigend')
        emc = mc.mc2step()[0]
        self.assertAlmostEqual(emc, -108.91052310869014, 7)

    def test_mc1step_6o6e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(m, 6, 6), auxbasis='weigend')
        emc = mc.mc1step()[0]
        self.assertAlmostEqual(emc, -108.980105451388, 7)

    def test_mc2step_6o6e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(m, 6, 6), auxbasis='weigend')
        emc = mc.mc2step()[0]
        self.assertAlmostEqual(emc, -108.980105451388, 7)

    def test_mc1step_symm_4o4e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(msym, 4, 4), auxbasis='weigend')
        emc = mc.mc1step()[0]
        self.assertAlmostEqual(emc, -108.913786407955, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()),
                               2.7015375913946591, 4)

    def test_mc2step_symm_4o4e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(msym, 4, 4), auxbasis='weigend')
        emc = mc.mc2step()[0]
        self.assertAlmostEqual(emc, -108.913786407955, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()),
                               2.7015375913946591, 4)

    def test_mc1step_symm_6o6e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(msym, 6, 6), auxbasis='weigend')
        emc = mc.mc1step()[0]
        self.assertAlmostEqual(emc, -108.980105451388, 7)

    def test_mc2step_symm_6o6e(self):
        mc = mcscf.approx_hessian(mcscf.CASSCF(msym, 6, 6), auxbasis='weigend')
        emc = mc.mc2step()[0]
        self.assertAlmostEqual(emc, -108.980105451388, 7)

    def test_casci_4o4e(self):
        mc = mcscf.CASCI(m.density_fit(), 4, 4)
        emc = mc.casci()[0]
        self.assertAlmostEqual(emc, -108.8896744464714, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()),
                               2.6910276344981119, 4)

    def test_casci_symm_4o4e(self):
        mc = mcscf.CASCI(msym.density_fit(), 4, 4)
        emc = mc.casci()[0]
        self.assertAlmostEqual(emc, -108.8896744464714, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()),
                               2.6910276344981119, 4)

    def test_casci_4o4e(self):
        mc = mcscf.DFCASCI(m.density_fit('weigend'), 4, 4)
        emc = mc.casci()[0]
        self.assertAlmostEqual(emc, -108.88669369639578, 7)

    def test_casci_symm_4o4e(self):
        mc = mcscf.DFCASCI(msym.density_fit('weigend'), 4, 4)
        emc = mc.casci()[0]
        self.assertAlmostEqual(emc, -108.88669369639578, 7)

    def test_casci_uhf(self):
        mf = scf.UHF(mol)
        mf.scf()
        mc = mcscf.CASCI(mf, 4, 4)
        emc = mc.casci()[0]
        self.assertAlmostEqual(emc, -108.8896744464714, 7)
        self.assertAlmostEqual(numpy.linalg.norm(mc.analyze()), 0, 7)

    def test_casci_uhf(self):
        mf = scf.UHF(mol)
        mf.scf()
        mc = mcscf.approx_hessian(mcscf.CASSCF(mf, 4, 4))
        emc = mc.mc1step()[0]
        self.assertAlmostEqual(emc, -108.913786407955, 7)
        emc = mc.mc2step()[0]
        self.assertAlmostEqual(emc, -108.913786407955, 7)

    def test_df_ao2mo(self):
        mf = scf.density_fit(msym, auxbasis='weigend')
        mf.max_memory = 100
        mf.kernel()
        mc = mcscf.DFCASSCF(mf, 4, 4)
        with df.load(mf._cderi) as feri:
            cderi = numpy.asarray(feri)
        eri0 = numpy.dot(cderi.T, cderi)
        nmo = mc.mo_coeff.shape[1]
        ncore = mc.ncore
        nocc = ncore + mc.ncas
        eri0 = ao2mo.restore(1, ao2mo.kernel(eri0, mc.mo_coeff), nmo)
        eris = mc.ao2mo(mc.mo_coeff)
        self.assertTrue(numpy.allclose(eri0[:,:,ncore:nocc,ncore:nocc], eris.ppaa))
        self.assertTrue(numpy.allclose(eri0[:,ncore:nocc,:,ncore:nocc], eris.papa))

    def test_assign_cderi(self):
        nao = molsym.nao_nr()
        w, u = scipy.linalg.eigh(mol.intor('int2e_sph', aosym='s4'))
        idx = w > 1e-9

        mf = scf.density_fit(scf.RHF(molsym))
        mf._cderi = (u[:,idx] * numpy.sqrt(w[idx])).T.copy()
        mf.kernel()

        mc = mcscf.DFCASSCF(mf, 6, 6)
        mc.kernel()
        self.assertAlmostEqual(mc.e_tot, -108.98010545803884, 7)

    def test_init(self):
        from pyscf.mcscf import df
        mf = scf.RHF(mol)
        self.assertTrue(isinstance(mcscf.CASCI(mf, 2, 2), mcscf.casci.CASCI))
        self.assertTrue(isinstance(mcscf.CASCI(mf.density_fit(), 2, 2), df._DFCASSCF))
        self.assertTrue(isinstance(mcscf.CASCI(mf.newton(), 2, 2), mcscf.casci.CASCI))
        self.assertTrue(isinstance(mcscf.CASCI(mf.density_fit().newton(), 2, 2), df._DFCASSCF))
        self.assertTrue(isinstance(mcscf.CASCI(mf.newton().density_fit(), 2, 2), mcscf.casci.CASCI))
        self.assertTrue(isinstance(mcscf.CASCI(mf.density_fit().newton().density_fit(), 2, 2), df._DFCASSCF))


if __name__ == "__main__":
    print("Full Tests for density fitting N2")
    unittest.main()

