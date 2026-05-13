import re
import logging
from collections import Counter

from qiskit.qasm3 import loads
from qiskit import transpile
from qiskit_aer import AerSimulator

from device_gateway.core.base_backend import SUCCESS_MESSAGE, BaseBackend

logger = logging.getLogger("device_gateway")


class AerBackend(BaseBackend):
    def __init__(self, config: dict):
        super().__init__(config)
        # qasm_simulator を使用
        self.simulator = AerSimulator(method="automatic")
    
    #baseが設定されているため形だけ作成
    def _get_circuit(self):
        return None
    
    #baseが設定されているため形だけ作成
    def _execute(self, qc, shots: int = 1024):
        backend = AerSimulator()
        tqc = transpile(qc, backend)
        result = backend.run(tqc, shots=shots).result()
        return result.get_counts()


    def execute(self, program: str, shots: int = 1024) -> tuple[dict, str]:
        """
        Execute the quantum program using Qiskit Aer.
        """
        logger.info("Executing on backend: Qiskit Aer")

        # OpenQASM 3 → Qiskit QuantumCircuit
        qc = loads(program)

        # Aer 用に transpile
        # tqc = transpile(qc, self.simulator)

        # 実行
        result = self.simulator.run(qc, shots=shots).result()

        # counts はすでに Qiskit 形式
        counts = result.get_counts()

        # zero count 除去（BaseBackend の仕様に合わせる）
        counts = self._remove_zero_values(counts)

        logger.info(f"counts={counts}")
        return counts, SUCCESS_MESSAGE
