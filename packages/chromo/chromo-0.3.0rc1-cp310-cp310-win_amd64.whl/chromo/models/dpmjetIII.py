from chromo.common import MCRun, MCEvent, CrossSectionData
from chromo.kinematics import EventFrame
from chromo.util import info, _cached_data_dir, fortran_chars, Nuclei
from chromo.constants import standard_projectiles, GeV


class DpmjetIIIEvent(MCEvent):
    """Wrapper class around DPMJET-III HEPEVT-style particle stack."""

    _hepevt = "dtevt1"
    _phep = "phkk"
    _vhep = "vhkk"
    _nevhep = "nevhkk"
    _nhep = "nhkk"
    _idhep = "idhkk"
    _isthep = "isthkk"
    _jmohep = "jmohkk"
    _jdahep = "jdahkk"

    def _charge_init(self, npart):
        return self._lib.dtpart.iich[self._lib.dtevt2.idbam[:npart] - 1]

    def _get_impact_parameter(self):
        return self._lib.dtglcp.bimpac

    def _get_n_wounded(self):
        return self._lib.dtglcp.nwasam, self._lib.dtglcp.nwbsam

    # Unfortunately not that simple since this is bounced through
    # entire code as argument not in COMMON
    # @property
    # def n_inel_NN_interactions(self):
    #     """Number of inelastic nucleon-nucleon interactions"""
    #     return self._lib.dtglcp.nwtsum


# =========================================================================
# DpmjetIIIMCRun
# =========================================================================
class DpmjetIIIRun(MCRun):
    """Implements all abstract attributes of MCRun for the
    DPMJET-III series of event generators.

    It should work identically for the new 'dpmjet3' module and the legacy
    dpmjet306. No special constructor is necessary and everything is
    handled by the default constructor of the base class.
    """

    _name = "DPMJET-III"
    _event_class = DpmjetIIIEvent
    _frame = None
    # DPMJet is supposed to support photons as projectiles, but fails
    _projectiles = standard_projectiles | Nuclei()
    _targets = _projectiles
    _param_file_name = "dpmjpar.dat"
    _evap_file_name = "dpmjet.dat"
    _data_url = (
        "https://github.com/impy-project/chromo"
        + "/releases/download/zipped_data_v1.0/dpm3191_v001.zip"
    )
    _ecm_min = 1 * GeV
    _max_A1 = 0
    _max_A2 = 0

    def __init__(self, evt_kin, *, seed=None):
        import chromo

        super().__init__(seed)

        data_dir = _cached_data_dir(self._data_url)
        # Set the dpmjpar.dat file
        if hasattr(self._lib, "pomdls") and hasattr(self._lib.pomdls, "parfn"):
            pfile = data_dir + self._param_file_name
            info(3, "DPMJET parameter file at", pfile)
            self._lib.pomdls.parfn = fortran_chars(self._lib.pomdls.parfn, pfile)

        # Set the data directory for the other files
        if hasattr(self._lib, "poinou") and hasattr(self._lib.poinou, "datdir"):
            pfile = data_dir
            info(3, "DPMJET data dir is at", pfile)
            self._lib.poinou.datdir = fortran_chars(self._lib.poinou.datdir, pfile)
            self._lib.poinou.lendir = len(pfile)
        # TODO: Rename the common block to chromo
        if hasattr(self._lib, "dtchro"):
            evap_file = data_dir + self._evap_file_name
            info(3, "DPMJET evap file at", evap_file)
            self._lib.dtchro.fnevap = fortran_chars(self._lib.dtchro.fnevap, evap_file)

        # Setup logging
        lun = 6  # stdout
        if hasattr(self._lib, "dtflka"):
            self._lib.dtflka.lout = lun
            self._lib.dtflka.lpri = 5 if chromo.debug_level else 1
        elif hasattr(self._lib, "dtiont"):
            self._lib.dtiont.lout = lun
        else:
            assert False, "Unknown DPMJET version, IO common block not detected"
        self._lib.pydat1.mstu[10] = lun

        self.kinematics = evt_kin

        # Relax momentum and energy conservation checks at very high energies
        if evt_kin.ecm > 5e4:
            # Relative allowed deviation
            self._lib.pomdls.parmdl[74] = 0.05
            # Absolute allowed deviation
            self._lib.pomdls.parmdl[75] = 0.05

        # Prevent DPMJET from overwriting decay settings
        # self._lib.dtfrpa.ovwtdc = False
        # Set PYTHIA decay flags to follow all changes to MDCY
        self._lib.pydat1.mstj[21 - 1] = 1
        self._lib.pydat1.mstj[22 - 1] = 2
        self._set_final_state_particles()

    def _cross_section(self, kin=None):
        kin = self.kinematics if kin is None else kin
        # we override to set precision
        if (kin.p1.A and kin.p1.A > 1) or kin.p2.A > 1:
            assert kin.p2.A >= 1, "DPMJET requires nucleons or nuclei on side 2."
            self._lib.dt_xsglau(
                kin.p1.A or 1,
                kin.p2.A or 1,
                self._lib.idt_icihad(2212)
                if (kin.p1.A and kin.p1.A > 1)
                else self._lib.idt_icihad(kin.p1),
                0,
                0,
                kin.ecm,
                1,
                1,
                1,
            )
            return CrossSectionData(inelastic=self._lib.dtglxs.xspro[0, 0, 0])
        else:
            stot, sela = self._lib.dt_xshn(
                self._lib.idt_icihad(kin.p1), self._lib.idt_icihad(kin.p2), 0.0, kin.ecm
            )
            return CrossSectionData(total=stot, elastic=sela, inelastic=stot - sela)

        # TODO set more cross-sections

    @property
    def glauber_trials(self):
        """Number of trials for Glauber model integration

        Default is 1000 (set at model initialisation).
        Larger number of `ntrials` reduces the fluctuations in the cross section,
        thus, making it more smooth. Smaller number of `ntrials` makes calculations of
        cross section faster.
        """
        return self._lib.dtglgp.jstatb

    @glauber_trials.setter
    def glauber_trials(self, ntrials):
        self._lib.dtglgp.jstatb = ntrials

    def _set_kinematics(self, kin):
        # Save maximal mass that has been initialized
        # (DPMJET sometimes crashes if higher mass requested than initialized)
        if not self._max_A1:
            # only do this once
            if kin.frame == EventFrame.FIXED_TARGET:
                self._lib.dtflg1.iframe = 1
                self._frame = EventFrame.FIXED_TARGET
            else:
                self._lib.dtflg1.iframe = 2
                self._frame = EventFrame.CENTER_OF_MASS
            self._max_A1 = kin.p1.A or 1
            self._max_A2 = kin.p2.A or 1
            self._lib.dt_init(
                -1,
                max(kin.plab, 100.0),
                kin.p1.A or 1,
                kin.p1.Z or 0,
                kin.p2.A or 1,
                kin.p2.Z or 0,
                kin.p1,
                iglau=0,
            )

        if (kin.p1.A or 1) > self._max_A1 or (kin.p2.A or 1) > self._max_A2:
            raise ValueError(
                "Maximal initialization mass exceeded "
                f"{kin.p1.A}/{self._max_A1}, {kin.p2.A}/{self._max_A2}"
            )

        # AF: No idea yet, but apparently this functionality was around?!
        # if hasattr(k, 'beam') and hasattr(self._lib, 'init'):
        #     self._lib.dt_setbm(k.A1, k.Z1, k.A2, k.Z2, k.beam[0], k.beam[1])
        #     print 'OK'

    def _set_stable(self, pdgid, stable):
        kc = self._lib.pycomp(pdgid)
        self._lib.pydat3.mdcy[kc - 1, 0] = not stable

    def _generate(self):
        k = self.kinematics
        reject = self._lib.dt_kkinc(
            k.p1.A or 1,
            k.p1.Z or 0,
            k.p2.A or 1,
            k.p2.Z or 0,
            self._lib.idt_icihad(2212)
            if (k.p1.A and k.p1.A > 1)
            else self._lib.idt_icihad(k.p1),
            k.elab,
            kkmat=-1,
        )
        self._lib.dtevno.nevent += 1
        return not reject


class DpmjetIII191(DpmjetIIIRun):
    _version = "19.1"
    _library_name = "_dpmjetIII191"


class DpmjetIII193(DpmjetIIIRun):
    _version = "19.3"
    _library_name = "_dpmjetIII193"


class DpmjetIII306(DpmjetIIIRun):
    _version = "3.0-6"
    _library_name = "_dpmjet306"
    _param_file_name = "fitpar.dat"
    _data_url = (
        "https://github.com/impy-project/chromo"
        + "/releases/download/zipped_data_v1.0/dpm3_v001.zip"
    )


class DpmjetIII193_DEV(DpmjetIIIRun):
    _version = "19.3-dev"
    _library_name = "_dev_dpmjetIII193"
