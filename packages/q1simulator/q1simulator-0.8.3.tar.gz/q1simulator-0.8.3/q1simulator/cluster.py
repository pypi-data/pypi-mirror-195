from typing import Optional
import logging
import qcodes as qc

from qblox_instruments import (
        SystemStatus, SystemState, SystemStatusSlotFlags,
        InstrumentClass, InstrumentType,
        )

from .q1simulator import Q1Module

logger = logging.getLogger(__name__)


class ClusterModule(qc.InstrumentChannel, Q1Module):
    def __init__(self, root_instrument, name, slot, n_sequencers=6, sim_type=None):
        super().__init__(root_instrument, name)
        self._slot = slot
        super().init_module(n_sequencers, sim_type)

    def present(self):
        return True

    def slot_idx(self):
        return self._slot


class EmptySlot(qc.InstrumentChannel):
    def __init__(self, root_instrument, name):
        super().__init__(root_instrument, name)

    def present(self):
        return False


class Cluster(qc.Instrument):
    def __init__(self, name, modules={}):
        super().__init__(name)
        self._modules = {}
        for slot in range(1,21):
            name = f'module{slot}'
            if slot in modules:
                module = ClusterModule(self, name, slot, sim_type=modules[slot])
            else:
                module = EmptySlot(self, name)
            self.add_submodule(name, module)
            self._modules[slot] = module

    def get_idn(self):
        return dict(vendor='Q1Simulator', model='Cluster', serial='', firmware='')

    @property
    def instrument_class(self):
        return InstrumentClass.CLUSTER

    @property
    def instrument_type(self):
        return InstrumentType.MM

    def get_num_system_error(self):
        return 0

    def get_system_error(self):
        return '0,"No error"'

    def get_system_state(self):
        return SystemState(
            SystemStatus.OKAY,
            [],
            SystemStatusSlotFlags({}))

    def _check_module_present(self, slot):
        if not self._modules[slot].present():
            raise Exception(f'No module in slot {slot}')

    def arm_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        if slot is not None:
            self._check_module_present(slot)
            self._modules[slot].arm_sequencer(sequencer)
        else:
            for module in self._modules.values():
                if module.present():
                    module.arm_sequencer(sequencer)

    def start_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        if slot is not None:
            self._check_module_present(slot)
            self._modules[slot].start_sequencer(sequencer)
        else:
            for module in self._modules.values():
                if module.present():
                    module.start_sequencer(sequencer)

    def stop_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        if slot is not None:
            self._check_module_present(slot)
            self._modules[slot].stop_sequencer(sequencer)
        else:
            for module in self._modules.values():
                if module.present():
                    module.stop_sequencer(sequencer)

    @property
    def modules(self):
        return list(self.submodules.values())

    def reset(self):
        pass

