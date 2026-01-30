import re
from re import Pattern


class Validator:
    """
    Detecta se um texto CONTÉM padrões comuns de dados sensíveis:
    - CPF
    - CNPJ
    - E-mail
    - Telefone brasileiro
    - RG (heurístico)

    Observações importantes:
    - Regex são determinísticos (sem risco de ReDoS)
    - Não usa signal / timeout por SO (cross-platform)
    - Proteção feita via:
        • limite de tamanho do texto
        • captura de exceções do re
    """

    # Limite defensivo: evita analisar textos absurdamente grandes
    MAX_TEXT_LENGTH = 50_000

    # =========================
    # REGEX DEFINITIONS
    # =========================

    _CPF_RE = re.compile(
        r"(?<!\d)(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?!\d)"
    )

    _CNPJ_RE = re.compile(
        r"(?<!\d)(?:\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})(?!\d)"
    )

    _EMAIL_RE = re.compile(
        r"(?i)\b[a-z0-9](?:[a-z0-9._%+-]{0,62}[a-z0-9])?"
        r"@"
        r"(?:[a-z0-9-]+\.)+[a-z]{2,63}\b"
    )

    _PHONE_BR_RE = re.compile(
        r"""
        (?<!\d)
        (?:
            # CASO 1 — Com DDD (fixo ou celular)
            (?:(?:\+?55\s?)?\(?\d{2}\)?[\s.-]?)
            (
                # Celular: 9XXXX-XXXX
                9\d{4}[-.\s]?\d{4}
                |
                # Fixo: XXXX-XXXX (somente com DDD)
                \d{4}[-.]\d{4}
            )
            |
            # CASO 2 — Sem DDD (somente celular)
            9\d{4}[-.\s]?\d{4}
        )
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

    # =========================
    # CORE SEARCH LOGIC
    # =========================

    @classmethod
    def _safe_search(cls, pattern: Pattern[str], text: str) -> bool:
        """
        Executa uma busca regex de forma segura:
        - Limita tamanho do texto
        - Trata exceções do re
        """
        if not text:
            return False

        if len(text) > cls.MAX_TEXT_LENGTH:
            text = text[:cls.MAX_TEXT_LENGTH]

        try:
            return bool(pattern.search(text))
        except re.error:
            # Falha defensiva: se regex quebrar, assume que não encontrou
            return False

    # =========================
    # PUBLIC API
    # =========================

    @classmethod
    def contains_cpf(cls, text: str) -> bool:
        """Verifica se o texto contém um CPF."""
        return cls._safe_search(cls._CPF_RE, text)

    @classmethod
    def contains_cnpj(cls, text: str) -> bool:
        """Verifica se o texto contém um CNPJ."""
        return cls._safe_search(cls._CNPJ_RE, text)

    @classmethod
    def contains_email(cls, text: str) -> bool:
        """Verifica se o texto contém um e-mail."""
        return cls._safe_search(cls._EMAIL_RE, text)

    @classmethod
    def contains_phone_br(cls, text: str) -> bool:
        """Verifica se o texto contém um telefone brasileiro."""
        return cls._safe_search(cls._PHONE_BR_RE, text)

    @classmethod
    def contains_rg(cls, text: str) -> bool:
        """Verifica se o texto contém um RG (heurístico)."""
        return cls._safe_search(cls._RG_RE, text)

    @classmethod
    def validate_all_types(cls, text: str) -> dict[str, bool]:
        """
        Executa todas as validações disponíveis e retorna um dicionário
        com os resultados.
        """
        return {
            "has_cpf": cls.contains_cpf(text),
            "has_cnpj": cls.contains_cnpj(text),
            "has_email": cls.contains_email(text),
            "has_phone": cls.contains_phone_br(text),
            "has_rg": cls.contains_rg(text),
        }
