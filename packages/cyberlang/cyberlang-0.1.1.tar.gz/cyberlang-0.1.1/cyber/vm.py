from ctypes import *
from pathlib import Path

lib = WinDLL((Path(__file__).parent / 'lib/cyber.dll').as_posix())

class UserVM(Structure):
    pass

vm_create = lib.cyVmCreate
vm_create.restype = c_void_p

vm_eval = lib.cyVmEval
vm_eval.restype = c_int
vm_eval.argtypes = [c_void_p, c_char_p, c_size_t, POINTER(c_uint64)]


class Cyber:
    def __init__(self) -> None:
        self.vm = vm_create()

    def eval(self, src:bytes):
        srcLen = c_size_t(len(src))

        out = c_uint64(0)
        outptr = pointer(out)

        result = vm_eval(self.vm, src, srcLen, outptr)

        return result