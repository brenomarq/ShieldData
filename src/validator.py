import re
import signal
from contextlib import contextmanager
from types import FrameType
from re import Pattern


class Validator:
    """
    Detecta se um texto CONTÉM padrões comuns de:
    - CPF (com/sem pontuação)
    - CNPJ (com/sem pontuação)
    - E-mail
    - Telefone BR (com/sem DDD, com/sem +55)
    - RG (formatos comuns; heurístico)

    Timeout:
    - Cada busca por regex é protegida por timeout (default: 1s).
    - Implementação via signal (Unix/macOS/Linux) => funciona no *main thread*.
    """

    DEFAULT_TIMEOUT_S = 1.0

    _CPF_RE = re.compile(r"(?<!\d)(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?!\d)")
    _CNPJ_RE = re.compile(r"(?<!\d)(?:\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})(?!\d)")

    _EMAIL_RE = re.compile(
        r"(?i)\b[a-z0-9](?:[a-z0-9._%+-]{0,62}[a-z0-9])?"
        r"@"
        r"(?:[a-z0-9-]+\.)+[a-z]{2,63}\b"
    )

    _PHONE_BR_RE = re.compile(
        r"""
        (?<!\d)
        (?:\+?\s*55\s*)?
        (?:\(?\s*\d{2}\s*\)?\s*)?
        (?:9?\d{4}[\s.-]?\d{4})
        (?!\d)
        """,
        re.VERBOSE,
    )

    _RG_RE = re.compile(
        r"""
        (?<!\d)
        (?:\d{1,2}\.?\d{3}\.?\d{3})
        (?:-?[0-9Xx])?
        (?!\d)
        """,
        re.VERBOSE,
    )

    @staticmethod
    @contextmanager
    def _timeout(seconds: float):
        if not seconds or seconds <= 0:
            yield
            return
        def _handler(signum: int, frame: FrameType | None) -> None:
            raise TimeoutError("regex timeout")

        old_handler = signal.getsignal(signal.SIGALRM)
        try:
            signal.signal(signal.SIGALRM, _handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0.0)
            signal.signal(signal.SIGALRM, old_handler)

    @classmethod
    def _timed_search(cls, pattern: Pattern[str], text: str, timeout_s: float) -> bool:
        try:
            with cls._timeout(timeout_s):
                return bool(pattern.search(text))
        except TimeoutError:
            return False

    @classmethod
    def contains_cpf(cls, text: str, timeout_s: float | None = None) -> bool:
        return cls._timed_search(cls._CPF_RE, text or "", timeout_s or cls.DEFAULT_TIMEOUT_S)

    @classmethod
    def contains_cnpj(cls, text: str, timeout_s: float | None = None) -> bool:
        return cls._timed_search(cls._CNPJ_RE, text or "", timeout_s or cls.DEFAULT_TIMEOUT_S)

    @classmethod
    def contains_email(cls, text: str, timeout_s: float | None = None) -> bool:
        return cls._timed_search(cls._EMAIL_RE, text or "", timeout_s or cls.DEFAULT_TIMEOUT_S)

    @classmethod
    def contains_phone_br(cls, text: str, timeout_s: float | None = None) -> bool:
        return cls._timed_search(cls._PHONE_BR_RE, text or "", timeout_s or cls.DEFAULT_TIMEOUT_S)

    @classmethod
    def contains_rg(cls, text: str, timeout_s: float | None = None) -> bool:
        return cls._timed_search(cls._RG_RE, text or "", timeout_s or cls.DEFAULT_TIMEOUT_S)
    
    @classmethod
    def validate_all_types(cls, text: str, timeout_s: float | None = None) -> dict[str, bool]:
        """Retorna um dicionário com o status de cada validação."""
        return {
            "has_cpf": cls.contains_cpf(text, timeout_s),
            "has_cnpj": cls.contains_cnpj(text, timeout_s),
            "has_email": cls.contains_email(text, timeout_s),
            "has_phone": cls.contains_phone_br(text, timeout_s),
            "has_rg": cls.contains_rg(text, timeout_s)
        }