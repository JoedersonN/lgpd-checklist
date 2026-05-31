# lgpd-checklist

Ferramenta de linha de comando para avaliação de conformidade com a **Lei Geral de Proteção de Dados (Lei 13.709/2018)**.

Gera relatório com score, não conformidades priorizadas e recomendações práticas — desenvolvida para uso em diagnósticos de segurança em pequenas e médias empresas.

---

## O que faz

Conduz um questionário interativo de **19 perguntas** organizadas em 5 categorias e gera relatório com:

- Score de conformidade (0–100%)
- Classificação: **BOM / ATENÇÃO / CRÍTICO**
- Não conformidades priorizadas por criticidade
- Recomendação prática para cada item com referência ao artigo da lei
- Resumo por categoria
- Exportação em `.txt` ou `.json`

### Categorias avaliadas

| Categoria | Itens |
|---|---|
| Governança e Responsabilidade | DPO, Política de Privacidade, Treinamentos, Resposta a Incidentes |
| Coleta e Base Legal | Mapeamento de dados, Bases legais, Consentimento, Minimização |
| Direitos dos Titulares | Canal de atendimento, Exclusão, Portabilidade |
| Segurança e Armazenamento | Criptografia, Controle de acesso, Retenção, Logs, Backup |
| Terceiros e Fornecedores | Contratos (DPA), Inventário de operadores |

---

## Instalação

```bash
git clone https://github.com/JoedersonN/lgpd-checklist
cd lgpd-checklist
```

Sem dependências externas — usa apenas a biblioteca padrão do Python 3.

---

## Uso

```bash
# Avaliação básica
python3 lgpd_checklist.py

# Informar nome da empresa
python3 lgpd_checklist.py -e "Nome da Empresa"

# Salvar relatório em .txt
python3 lgpd_checklist.py -e "Nome da Empresa" -o relatorio.txt

# Salvar em JSON (para integração com outros sistemas)
python3 lgpd_checklist.py -e "Nome da Empresa" --json resultado.json

# Tudo junto
python3 lgpd_checklist.py -e "Clínica Exemplo" -o relatorio.txt --json resultado.json
```

### Respostas aceitas

| Entrada | Significado | Pontuação |
|---|---|---|
| `S` | Sim — totalmente conforme | 100% do peso |
| `P` | Parcialmente conforme | 50% do peso |
| `N` | Não conforme | 0% |

---

## Exemplo de output

```
============================================================
  LGPD CHECKLIST — RELATÓRIO DE CONFORMIDADE
============================================================
  Empresa  : Clínica Exemplo
  Data     : 2025-06-10 16:20:44
  Score    : 28/60 pontos  (46.7%)
  Status   : [CRÍTICO] Baixa conformidade. A empresa está exposta
             a riscos significativos e sanções da ANPD.
============================================================

[NÃO CONFORMIDADES — 8 item(ns) — PRIORIDADE ALTA]
------------------------------------------------------------

  [GOV-01] A empresa possui um Encarregado de Dados (DPO) designado?
  → Indique um DPO responsável por garantir a conformidade com a LGPD.
    É obrigatório para empresas que tratam dados em larga escala. (Art. 41)

  [SEG-01] Os dados pessoais são armazenados com criptografia?
  → Implante criptografia em repouso para bases de dados com dados
    pessoais e em trânsito (HTTPS/TLS) para todas as transmissões. (Art. 46)
  ...
```

---

## Caso de uso

Ideal para:
- Diagnóstico inicial de conformidade LGPD em pequenas e médias empresas
- Parte de um serviço de consultoria de segurança
- Auditoria interna rápida antes de contratar consultoria especializada
- Conscientização de gestores sobre obrigações legais

> **Nota:** Esta ferramenta não substitui assessoria jurídica especializada. Os resultados devem ser interpretados como diagnóstico técnico preliminar.

---

## Estrutura

```
lgpd-checklist/
├── lgpd_checklist.py    # Script principal com todas as regras
└── README.md
```

---

## Tecnologias

- Python 3.8+ (sem dependências externas)
- Biblioteca padrão: `json`, `argparse`, `datetime`

---

## Autor

**Joederson Neves** — Blue Team | SOC | Segurança da Informação  
[GitHub](https://github.com/JoedersonN) · [LinkedIn](https://linkedin.com/in/joederson-neves-araujo) · [TryHackMe](https://tryhackme.com/p/Joe.Sk)
