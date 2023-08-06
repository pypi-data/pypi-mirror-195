import numpy
import zfit

from logzero import logger as log

#----------------------------------------------------
class model:
    def __init__(self, rk=1, preffix=''):
        self._obs    = zfit.Space('x', limits=(0, 100))
        self._rk     = rk
        self._preffix= preffix

        zfit.settings.changed_warnings.hesse_name = False

        self._d_mod = None
    #----------------------------------------------------
    def _get_data_simple(self, nentries):
        arr_sig = numpy.random.normal(size=nentries, loc=50, scale=3)
        arr_bkg = numpy.random.exponential(size=nentries, scale=100)
    
        arr_dat = numpy.concatenate([arr_sig, arr_bkg])
    
        return arr_dat
    #----------------------------------------------------
    def _get_gauss(self, preffix=''):
        preffix= f'{preffix}_{self._preffix}'

        mu     = zfit.Parameter(f'mu_{preffix}', 50., 40,  60)
        sg     = zfit.Parameter(f'sg_{preffix}', 2.0,  1,   5)
        gauss  = zfit.pdf.Gauss(obs=self._obs, mu=mu, sigma=sg)
        nsg    = zfit.Parameter(f'nsg_{preffix}', 10, 0, 100000)
        esig   = gauss.create_extended(nsg)
    
        lb     = zfit.Parameter(f'lb_{preffix}', -0.05,  -0.10, 0.00)
        exp    = zfit.pdf.Exponential(obs=self._obs, lam=lb)
        nbk    = zfit.Parameter(f'nbk_{preffix}', 10, 0, 100000)
        ebkg   = exp.create_extended(nbk)
    
        pdf    = zfit.pdf.SumPDF([esig, ebkg]) 
    
        return pdf 
    #----------------------------------------------------
    def _get_ds_model(self, ds):
        self._pdf_mm = self._get_gauss(preffix=f'mm_{ds}')
        self._pdf_ee = self._get_gauss(preffix=f'ee_{ds}')
    
        return self._pdf_mm, self._pdf_ee
    #----------------------------------------------------
    def _get_ds_data(self, nentries=20000, eff_ee=1.0, eff_mm=1.0):
        arr_mm = self._get_data_simple(self._rk * nentries)
        arr_ee = self._get_data_simple(           nentries)
    
        if eff_ee < 1.0:
            nev_ee = int(nentries * eff_ee)
            arr_ee = numpy.random.choice(arr_ee, size=nev_ee, replace=False)
    
        if eff_mm < 1.0:
            nev_mm = int(nentries * eff_mm)
            arr_mm = numpy.random.choice(arr_mm, size=nev_mm, replace=False)
    
        log.info(f'Electron data: {arr_ee.shape}')
        log.info(f'Muon data: {arr_mm.shape}')
    
        dst_mm = zfit.Data.from_numpy(obs=self._obs, array=arr_mm)
        dst_ee = zfit.Data.from_numpy(obs=self._obs, array=arr_ee)
    
        return dst_mm, dst_ee
    #----------------------------------------------------
    def get_data(self, nentries=20000, d_eff=None, rseed=3):
        numpy.random.seed(seed=rseed)

        d_data = {}
        for ds, (eff_mm, eff_ee) in d_eff.items():
            log.info(f'Dataset: {ds}')
            d_data[ds] = self._get_ds_data(nentries, eff_ee=eff_ee, eff_mm=eff_mm)
    
        return d_data
    #----------------------------------------------------
    def get_cov(self, kind='diag', c = 0.01):
        l_mat = []
        if kind == 'diag_eq':
            l_mat = [[ c, 0, 0, 0 ],
                     [ 0, c, 0, 0 ],
                     [ 0, 0, c, 0 ],
                     [ 0, 0, 0, c ]]
        else:
            log.error(f'Invalid kind: {kind}')
            raise
    
        return numpy.array(l_mat)
    #----------------------------------------------------
    def get_rjpsi(self, kind='one'):
        d_rjpsi = {}
    
        if   kind == 'one':
            d_rjpsi['d1'] = 1 
            d_rjpsi['d2'] = 1 
            d_rjpsi['d3'] = 1 
            d_rjpsi['d4'] = 1 
        elif kind == 'eff_bias':
            d_rjpsi['d1'] = 0.83333333 
            d_rjpsi['d2'] = 0.83333333 
            d_rjpsi['d3'] = 0.83333333 
            d_rjpsi['d4'] = 0.83333333 
        else:
            log.error(f'Wrong kind: {kind}')
            raise
    
        return d_rjpsi
    #----------------------------------------------------
    def get_model(self):
        if self._d_mod is not None:
            return self._d_mod
    
        d_mod       = {}
        d_mod['d1'] = self._get_ds_model('d1')
        d_mod['d2'] = self._get_ds_model('d2')
        d_mod['d3'] = self._get_ds_model('d3')
        d_mod['d4'] = self._get_ds_model('d4')
    
        self._d_mod = d_mod
    
        return self._d_mod
    #----------------------------------------------------
    def get_eff(self, kind='equal'):
        d_eff = {}
        if   kind == 'diff':
            d_eff['d1'] = (0.6, 0.3)
            d_eff['d2'] = (0.5, 0.2)
            d_eff['d3'] = (0.7, 0.3)
            d_eff['d4'] = (0.8, 0.4)
        elif kind == 'half':
            d_eff['d1'] = (0.6, 0.3)
            d_eff['d2'] = (0.6, 0.3)
            d_eff['d3'] = (0.6, 0.3)
            d_eff['d4'] = (0.6, 0.3)
        elif kind == 'equal':
            d_eff['d1'] = (0.3, 0.3)
            d_eff['d2'] = (0.3, 0.3)
            d_eff['d3'] = (0.3, 0.3)
            d_eff['d4'] = (0.3, 0.3)
        elif kind == 'bias':
            d_eff['d1'] = (0.6, 0.25)
            d_eff['d2'] = (0.6, 0.25)
            d_eff['d3'] = (0.6, 0.25)
            d_eff['d4'] = (0.6, 0.25)
        else:
            log.error(f'Invalid kind: {kind}')
            raise
    
        return d_eff
#----------------------------------------------------

