import spacy
from spacy.util import is_package
from typing import Dict, List, Iterable


class NamedEntityDetector:
    """
    Extrator de sinais semânticos baseados em Entidades Nomeadas (NER).

    Esta classe utiliza o modelo de NLP do spaCy para identificar entidades
    nomeadas em textos em português e extrair atributos quantitativos
    e booleanos que indicam a possível presença de dados pessoais.

    O objetivo NÃO é classificar textos como públicos ou não públicos,
    mas sim gerar sinais explicáveis que possam ser utilizados como
    features em modelos de aprendizado supervisionado.

    Entidades de interesse:
    - PERSON: nomes de pessoas físicas
    - LOC / GPE: localizações que podem indicar endereço
    - ORG: organizações (menos sensível, mas contextual)
    """

    def __init__(self, model_name: str = "pt_core_news_lg"):
        """
        Inicializa o extrator carregando o modelo spaCy.

        Parameters
        ----------
        model_name : str
            Nome do modelo spaCy em português a ser utilizado.
            Exemplo: 'pt_core_news_sm' ou 'pt_core_news_md ou 'pt_core_news_lg'
        """

        if not is_package(model_name):
            raise ImportError(
                f"O modelo '{model_name}' não foi encontrado. "
                f"Por favor, execute: python -m spacy download {model_name}"
            )
        
        self.nlp = spacy.load(model_name)

    def _process_doc(self, doc) -> Dict[str, int]:
        """
        Processa um documento spaCy e retorna os sinais extraídos.
        """
        # Filtra entidades de pessoas (PER) que possuem pelo menos 2 palavras (ex: Nome Sobrenome)
        # Isso ajuda a reduzir falsos positivos com palavras isoladas que o modelo confunde com nomes.
        persons = [ent for ent in doc.ents if ent.label_ == "PER" and len(ent.text.strip().split()) >= 2]
        locations = [ent for ent in doc.ents if ent.label_ in ("LOC", "GPE")]
        organizations = [ent for ent in doc.ents if ent.label_ == "ORG"]

        return {
            "has_person_entity": int(len(persons) > 0),
            "has_location_entity": int(len(locations) > 0),
            "has_organization_entity": int(len(organizations) > 0),
            "person_entity_count": len(persons),
            "location_entity_count": len(locations),
            "organization_entity_count": len(organizations),
            "total_named_entities": len(doc.ents),
        }

    def extract_signals(self, text: str) -> Dict[str, int]:
        """
        Analisa o texto e retorna sinais baseados em entidades nomeadas.

        Parameters
        ----------
        text : str
            Texto a ser analisado.

        Returns
        -------
        Dict[str, int]
            Dicionário contendo sinais binários e contagens de entidades.
        """
        doc = self.nlp(text)
        return self._process_doc(doc)

    def extract_signals_batch(self, texts: Iterable[str]) -> List[Dict[str, int]]:
        """
        Analisa uma lista de textos e retorna sinais baseados em entidades nomeadas usando nlp.pipe para eficiência.

        Parameters
        ----------
        texts : Iterable[str]
            Lista de textos a serem analisados.

        Returns
        -------
        List[Dict[str, int]]
            Lista de dicionários contendo sinais binários e contagens de entidades.
        """
        docs = self.nlp.pipe(texts)
        return [self._process_doc(doc) for doc in docs]

    def contains_potential_pii(self, text: str) -> bool:
        """
        Verifica se o texto contém entidades que podem indicar
        a presença de dados pessoais.

        Este método é útil para análises exploratórias ou geração
        de rótulos auxiliares, mas não deve ser usado como decisão final.

        Parameters
        ----------
        text : str
            Texto a ser analisado.

        Returns
        -------
        bool
            True se houver indícios de dados pessoais, False caso contrário.
        """
        signals = self.extract_signals(text)
        return (
            signals["has_person_entity"] == 1
            or signals["has_location_entity"] == 1
        )
