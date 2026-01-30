import torch
from piiclassifier import PIIClassifier
from validator import Validator
from ner_detector import NamedEntityDetector
from utils import get_best_device
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constantes para thresholds de decisão
BERT_HIGH_CONFIDENCE_THRESHOLD = 0.8  # Confiança alta do BERT
BERT_MODERATE_THRESHOLD = 0.4          # Confiança moderada do BERT
BERT_PHONE_MIN_THRESHOLD = 0.3         # Confiança mínima para telefone
DEFAULT_THRESHOLD = 0.5                # Threshold padrão
PHONE_CONFIDENCE = 0.85                # Confiança para padrão de telefone

class HybridClassifier:
    """
    Classificador Híbrido que combina:
    1. BERT (Deep Learning - Contexto)
    2. Regex (Padrões Fixos - Alta Precisão)
    3. SpaCy/NER (Entidades Nomeadas - Semântica)
    
    Objetivo: Maximizar o F1-Score e garantir que dados sensíveis óbvios (CPF, Email)
    nunca passem despercebidos, mesmo que o BERT falhe.
    """
    def __init__(self, model_path: str = "models/best_model", device: str = None):
        self.device = device if device else str(get_best_device())
        
        # 1. Carregar BERT
        logger.info(f"Carregando modelo BERT de {model_path} no dispositivo {self.device}...")
        try:
            self.bert_model = PIIClassifier.load(model_path)
            self.bert_model.to(self.device)
            self.bert_model.eval()  # Modo de avaliação (desliga dropout)
        except Exception as e:
            logger.error(f"Erro ao carregar modelo BERT: {e}")
            raise e

        # 2. Inicializar NER
        logger.info("Inicializando Detector de Entidades (SpaCy)...")
        self.ner_detector = NamedEntityDetector()
        
        # 3. Validadores Regex são estáticos, não precisam de inicialização

    def predict(self, text: str, threshold: float = 0.5) -> dict:
        """
        Realiza a predição híbrida.
        
        Retorna:
            dict: {
                "is_pii": bool,        # Decisão final
                "confidence": float,   # Confiança estimada (0-1)
                "details": dict        # Detalhes de cada validador
            }
        """
        # --- PASSO 1: REGEX (O mais rápido e confiável para padrões) ---
        # Se tem CPF, CNPJ ou Email válido, É DADO PESSOAL. Sem discussão.
        regex_results = Validator.validate_all_types(text)
        has_strong_regex = (
            regex_results["has_cpf"] or 
            regex_results["has_cnpj"] or 
            regex_results["has_email"] or 
            regex_results["has_rg"]
        )
        
        if has_strong_regex:
            return {
                "is_pii": True,
                "confidence": 1.0,
                "reason": "Correspondência forte de Regex",
                "details": {"regex": regex_results}
            }

        # --- PASSO 2: BERT (Inteligência Contextual) ---
        bert_prob = self._get_bert_probability(text)
        
        # --- LÓGICA DE DECISÃO HÍBRIDA (ENSEMBLE) ---
        
        # Regra A: BERT está muito confiante (> 0.8)
        # Confiamos no BERT
        if bert_prob > BERT_HIGH_CONFIDENCE_THRESHOLD:
            return {
                "is_pii": True,
                "confidence": float(bert_prob),
                "reason": "Alta confiança do BERT",
                "details": {"bert": bert_prob, "regex": regex_results}
            }
        
        # Regra B: BERT está moderado (0.4 a 0.8) E NER encontrou Pessoa/Local
        # O contexto é meio suspeito e tem um nome de pessoa -> Classificamos como PII (Boost no Recall)
        # Executa NER apenas se necessário (otimização de performance)
        if bert_prob > BERT_MODERATE_THRESHOLD:
            ner_results = self.ner_detector.extract_signals(text)
            has_person_or_loc = ner_results["has_person_entity"] or ner_results["has_location_entity"]
            
            if has_person_or_loc:
                return {
                    "is_pii": True,
                    "confidence": float(bert_prob + 0.1),  # Boost artificial na confiança
                    "reason": "BERT moderado + suporte NER",
                    "details": {"bert": bert_prob, "regex": regex_results, "ner": ner_results}
                }

        # Regra C: Padrão de Telefone (Regex fraco) + BERT mínimo
        # Telefone às vezes confunde com data, então pedimos um apoio mínimo do BERT (> 0.3)
        if regex_results["has_phone"] and bert_prob > BERT_PHONE_MIN_THRESHOLD:
             return {
                "is_pii": True,
                "confidence": PHONE_CONFIDENCE, 
                "reason": "Regex de telefone + contexto BERT fraco",
                "details": {"bert": bert_prob, "regex": regex_results}
            }

        # Decisão Padrão (Fallback para o Threshold)
        is_pii = bert_prob >= threshold
        return {
            "is_pii": is_pii,
            "confidence": float(bert_prob),
            "reason": "Threshold do BERT",
            "details": {"bert": bert_prob, "regex": regex_results}
        }

    def _get_bert_probability(self, text: str) -> float:
        # Preparar dados para o BERT
        encoding = self.bert_model.tokenizer(
            text,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = encoding['input_ids'].flatten().unsqueeze(0).to(self.device)
        attention_mask = encoding['attention_mask'].flatten().unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.bert_model(input_ids, attention_mask)
            # Aplicar Softmax para ter probabilidades (0 a 1)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            # Probabilidade da classe 1 (Tem PII)
            pii_prob = probs[0][1].item()
            
        return pii_prob
