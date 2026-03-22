# File: src/llm_interpretation.py

# Funções para gerar interpretação por Linguagem Natural para saida do modelo usando OpenAI

# Imports

import os
import json
from datetime import datetime, UTC
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Environment load
def load_openai_client():   

    # Load variables from the .env file into the current environment
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. Check your .env file."
        )

    # Create OpenAI client using API key stored in the environment
    client = OpenAI(api_key=api_key)

    return client

# Prompt builder

def build_clinical_prompt(
    predicted_class: str,
    predicted_probability: float,
    recall: float,
    specificity: float,
    precision: float,
    fn: int,
    fp: int,
    case_features: dict | None = None,
    context_note: str = ""      # Previsto para entrada por frontend
) -> str:
    
    # Build prompt sent to LLM with prediction output and parameters and returns text

    formatted_features = format_case_features(case_features)
    
    prompt = f"""
    Você é um assistente de apoio à interpretação de resultados de triagem oncológica.

    Explique o resultado abaixo para um profissional de saúde, em linguagem técnica, breve, 
    responsável e sensível ao contexto clínico feminino.    

    Resultado do modelo:
    - Classe prevista: {predicted_class}
    - Probabilidade estimada para malignidade: {predicted_probability:.4f}

    Ao interpretar a probabilidade:
    - classifique qualitativamente o nível de risco (baixo, moderado, alto, muito alto)
    - comente o grau de confiança do modelo
    
    Desempenho global do modelo utilizado:
    - Recall: {recall:.4f}
    - Specificity: {specificity:.4f}
    - Precision: {precision:.4f}
    - Falsos negativos no teste: {fn}
    - Falsos positivos no teste: {fp}

    Características do caso analisado:
    {formatted_features}

    Ao relacionar as características do caso explique brevemente como essas características contribuem para a decisão do modelo

    Contexto adicional:
    {context_note if context_note else "Sem contexto adicional informado."}

    - Este caso deve ser interpretado no contexto da saúde da mulher
    - Use linguagem técnica, respeitosa, sensível e não alarmista
    - Não inferir identidade, histórico pessoal ou dados sensíveis não fornecidos
    - Não apresentar o resultado como diagnóstico definitivo
    - Considere que a saída deve ser útil para profissionais especializados no atendimento à mulher
    - Ao sugerir próximos passos, priorize encaminhamentos prudentes e contextualizados   

    Ao responder:
    - transforme os dados numéricos em insights acionáveis
    - indique se o caso parece exigir maior atenção clínica
    - explique como as características do caso ajudam a entender a decisão do modelo

"""
    return prompt.strip()


# Call to OpenAI LLM

def generate_llm_interpretation(
    predicted_class: str,
    predicted_probability: float,
    recall: float,
    specificity: float,
    precision: float,
    fn: int,
    fp: int,
    case_features: dict | None = None,
    context_note: str = "",
    model_name: str = None
) -> dict:    

    # Load authenticated client
    client = load_openai_client()

    # Allow the model name to come from the environment or from the function argument
    if model_name is None:
        load_dotenv()
        model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    # Build the final prompt text
    prompt = build_clinical_prompt(
        predicted_class=predicted_class,
        predicted_probability=predicted_probability,
        recall=recall,
        specificity=specificity,
        precision=precision,
        fn=fn,
        fp=fp,
        case_features=case_features,
        context_note=context_note
    )

    # Call the OpenAI Responses API
    response = client.responses.create(
        model=model_name,
        input=prompt
    )

    # Extract output text in a simple way
    output_text = response.output_text

    return {
        "model_name": model_name,
        "prompt": prompt,
        "response_text": output_text,
        "case_features": case_features,
        "created_at": datetime.now(UTC).isoformat()
    }


# Selected case features into readable text block to insert in LLM prompt
def format_case_features(case_features: dict | None) -> str:   

    if not case_features:
        return "Nenhuma característica do caso foi fornecida."

    lines = []

    for feature_name, feature_value in case_features.items():
        # If the value is numeric, format with limited decimals
        if isinstance(feature_value, (int, float)):
            lines.append(f"- {feature_name}: {feature_value:.4f}")
        else:
            lines.append(f"- {feature_name}: {feature_value}")

    return "\n".join(lines)



# Save response to JSON

def save_llm_response(result: dict, output_dir: str = "../outputs/") -> str:

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    file_path = Path(output_dir) / f"llm_response_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return str(file_path)

# Adiciona resposta em arquivo JSON

def append_llm_jsonl_record(
    input_payload: dict,
    prompt: str,
    output_text: str,
    model_name: str,
    output_path: str = "../outputs/llm_outputs.json"
) -> str:

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "input": input_payload,
        "prompt": prompt,
        "output": output_text,
        "model_name": model_name,
        "created_at": datetime.now(UTC).isoformat()
    }

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return str(output_file)
