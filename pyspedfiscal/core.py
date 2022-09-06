from pyspedfiscal.bloco_0 import *
from pyspedfiscal.bloco_c import *
from pyspedfiscal.bloco_9 import *

import re

from pyspedfiscal.exception import ArquivoInvalido


class SpedFiscal:
    def __init__(self) -> None:
        self._zerar_registros()

    def _zerar_registros(self):
        self._registro_0000: Registro0000 = None
        self._registro_c001: RegistroC001 = None
        self._registro_9001: Registro9001 = None
        self._registro_9999: Registro9999 = None

    @property
    def bloco_0(self):
        return self._registro_c001

    @property
    def abertura(self):
        return self._registro_0000

    def validar(self, arquivo: str):

        bloco_0000_pattern = r'^(\|0000\|)(\d){3,}\|[0,1]\|((\d){8,}\|){2}(.{0,100})\|(\d){,14}\|(\d){,11}\|.{2,}\|.{0,14}\|(\d){0,7}\|.*\|.{0,9}\|[a,b,c,A,B,C]\|[0,1]\|$'

        try:
            with open(arquivo, 'r', encoding='latin-1') as arq_sped:
                bloco_0000 = next(arq_sped)
        except OSError as e:
            raise OSError("Não foi possível ler o arquivo:\n", repr(e))
        except Exception as e:
            raise Exception(
                "Erro inesperado, entre em contato com o suporte:\n", repr(e))
        else:
            return bool(re.match(bloco_0000_pattern, bloco_0000))

    def importar_arquivo(self, arquivo: str):

        # Valida o arquivo
        if not self.validar(arquivo):
            raise ArquivoInvalido(arquivo)

        # Remove
        self._zerar_registros()

        with open(arquivo, 'r', encoding='latin-1') as arq_sped:
            for linha in arq_sped:
                tipo_registro = linha[1:5].upper()

                # Bloco 0
                if tipo_registro.startswith('0'):
                    # Nivel 0 - Abertura do arquivo
                    if tipo_registro == '0000':
                        self._registro_0000 = Registro0000.ler_registro(linha)

                # Bloco C
                elif tipo_registro.startswith('C'):
                    # Nivel 1 - Registro Pai
                    if tipo_registro == 'C001':
                        self._registro_c001 = RegistroC001.ler_registro(linha)

                    # Nivel 2 - Filho C001
                    elif tipo_registro == 'C100':
                        registro_c100 = RegistroC100.ler_registro(linha)
                        self._registro_c001.registros_c100.append(
                            registro_c100)

                    # Nivel 3 - Filho C100
                    elif tipo_registro == 'C170':
                        registro_c170 = RegistroC170.ler_registro(linha)
                        registro_c100.registros_c170.append(registro_c170)

                    # Nivel 3 - Filho C100
                    elif tipo_registro == 'C190':
                        registro_c190 = RegistroC190.ler_registro(linha)
                        registro_c100.registros_c190.append(registro_c190)

                    # Nivel 3 - Filho C100
                    elif tipo_registro == 'C195':
                        registro_c195 = RegistroC195.ler_registro(linha)
                        registro_c100.registros_c195.append(registro_c195)

                    # Nivel 4 - Filho C195
                    elif tipo_registro == 'C197':
                        registro_c197 = RegistroC197.ler_registro(linha)
                        registro_c195.registros_c197.append(registro_c197)

                # Bloco 9
                elif tipo_registro.startswith('9'):
                    # Nivel 1 - Registro Pai
                    if tipo_registro == '9001':
                        self._registro_9001 = Registro9001.ler_registro(linha)

                    # Nivel 0 - Encerramento do arquivo
                    # Ultimo Registro do arquivo
                    elif tipo_registro == '9999':
                        self._registro_9999 = Registro9999.ler_registro(linha)
                        break
