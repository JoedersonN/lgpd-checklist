#!/usr/bin/env python3
"""
LGPD Checklist Tool
Questionário interativo de conformidade com a Lei Geral de Proteção de Dados (Lei 13.709/2018).
Gera relatório com status, pontuação e recomendações priorizadas.
Autor: Joederson Neves | github.com/JoedersonN
"""

import sys
import json
import argparse
from datetime import datetime


# ─── Base de perguntas por categoria ─────────────────────────────────────────

CHECKLIST = [
    {
        "categoria": "Governança e Responsabilidade",
        "perguntas": [
            {
                "id": "GOV-01",
                "pergunta": "A empresa possui um Encarregado de Dados (DPO) designado?",
                "peso": 3,
                "recomendacao": "Indique um DPO (interno ou externo) responsável por garantir a conformidade com a LGPD. É obrigatório para empresas que tratam dados em larga escala. (Art. 41)",
            },
            {
                "id": "GOV-02",
                "pergunta": "Existe uma Política de Privacidade documentada e acessível aos titulares?",
                "peso": 3,
                "recomendacao": "Elabore e publique uma Política de Privacidade clara, indicando quais dados são coletados, por que e como são usados. (Art. 9)",
            },
            {
                "id": "GOV-03",
                "pergunta": "Os colaboradores receberam treinamento sobre proteção de dados?",
                "peso": 2,
                "recomendacao": "Implante treinamentos periódicos de conscientização sobre LGPD e boas práticas de segurança da informação para todos os colaboradores.",
            },
            {
                "id": "GOV-04",
                "pergunta": "Existe um processo formal de resposta a incidentes de segurança envolvendo dados pessoais?",
                "peso": 3,
                "recomendacao": "Crie um plano de resposta a incidentes que inclua notificação à ANPD e aos titulares afetados em até 72 horas. (Art. 48)",
            },
        ]
    },
    {
        "categoria": "Coleta e Base Legal",
        "perguntas": [
            {
                "id": "COL-01",
                "pergunta": "A empresa sabe quais dados pessoais coleta e para qual finalidade?",
                "peso": 3,
                "recomendacao": "Realize um mapeamento de dados (data mapping) para inventariar todos os dados pessoais tratados, suas finalidades e bases legais. (Art. 37)",
            },
            {
                "id": "COL-02",
                "pergunta": "Existe base legal definida para cada tipo de tratamento de dados realizado?",
                "peso": 3,
                "recomendacao": "Identifique a base legal adequada (consentimento, obrigação legal, legítimo interesse, etc.) para cada operação de tratamento. (Art. 7)",
            },
            {
                "id": "COL-03",
                "pergunta": "Quando o tratamento é baseado em consentimento, ele é coletado de forma clara, específica e registrada?",
                "peso": 3,
                "recomendacao": "O consentimento deve ser livre, informado e inequívoco. Mantenha registros de quando e como foi obtido e garanta fácil revogação. (Art. 8)",
            },
            {
                "id": "COL-04",
                "pergunta": "A empresa coleta apenas os dados estritamente necessários para a finalidade declarada?",
                "peso": 2,
                "recomendacao": "Aplique o princípio da minimização: colete apenas o mínimo necessário. Revise formulários e sistemas para eliminar campos desnecessários. (Art. 6, III)",
            },
        ]
    },
    {
        "categoria": "Direitos dos Titulares",
        "perguntas": [
            {
                "id": "DIR-01",
                "pergunta": "Existe canal para que titulares solicitem acesso, correção ou exclusão de seus dados?",
                "peso": 3,
                "recomendacao": "Implante um canal de atendimento (e-mail, formulário ou portal) para receber e responder solicitações de titulares em até 15 dias. (Art. 18)",
            },
            {
                "id": "DIR-02",
                "pergunta": "A empresa consegue atender uma solicitação de exclusão de dados (direito ao esquecimento)?",
                "peso": 2,
                "recomendacao": "Mapeie onde os dados estão armazenados (sistemas, backups, planilhas) e crie processo para exclusão segura mediante solicitação. (Art. 18, VI)",
            },
            {
                "id": "DIR-03",
                "pergunta": "A empresa consegue fornecer ao titular um relatório com todos os seus dados em formato portável?",
                "peso": 2,
                "recomendacao": "Implante mecanismo de exportação de dados do titular em formato estruturado (JSON, CSV) para atender o direito à portabilidade. (Art. 18, V)",
            },
        ]
    },
    {
        "categoria": "Segurança e Armazenamento",
        "perguntas": [
            {
                "id": "SEG-01",
                "pergunta": "Os dados pessoais são armazenados com criptografia?",
                "peso": 3,
                "recomendacao": "Implante criptografia em repouso para bases de dados com dados pessoais e em trânsito (HTTPS/TLS) para todas as transmissões. (Art. 46)",
            },
            {
                "id": "SEG-02",
                "pergunta": "O acesso aos dados pessoais é restrito apenas a quem precisa (princípio do menor privilégio)?",
                "peso": 3,
                "recomendacao": "Revise as permissões de acesso e implante controle baseado em função (RBAC). Ninguém deve ter acesso além do necessário para sua função. (Art. 46)",
            },
            {
                "id": "SEG-03",
                "pergunta": "Existe política de retenção de dados — os dados são descartados quando não mais necessários?",
                "peso": 2,
                "recomendacao": "Defina prazos de retenção para cada tipo de dado e implante rotina de descarte seguro (exclusão definitiva ou anonimização) ao fim do prazo. (Art. 15)",
            },
            {
                "id": "SEG-04",
                "pergunta": "Os sistemas que armazenam dados pessoais possuem logs de acesso e auditoria?",
                "peso": 2,
                "recomendacao": "Ative logs de acesso nos sistemas críticos para rastrear quem acessou quais dados e quando — essencial para resposta a incidentes. (Art. 37)",
            },
            {
                "id": "SEG-05",
                "pergunta": "Backups com dados pessoais são protegidos com o mesmo nível de segurança que os sistemas em produção?",
                "peso": 2,
                "recomendacao": "Garanta que backups sejam criptografados, com acesso restrito e testados periodicamente. Backups desprotegidos são alvo frequente de vazamentos.",
            },
        ]
    },
    {
        "categoria": "Terceiros e Fornecedores",
        "perguntas": [
            {
                "id": "TER-01",
                "pergunta": "Contratos com fornecedores que acessam dados pessoais incluem cláusulas de proteção de dados?",
                "peso": 3,
                "recomendacao": "Inclua cláusulas de proteção de dados (DPA — Data Processing Agreement) em todos os contratos com operadores que tratam dados em nome da empresa. (Art. 39)",
            },
            {
                "id": "TER-02",
                "pergunta": "A empresa sabe quais fornecedores têm acesso a dados pessoais dos seus clientes ou colaboradores?",
                "peso": 2,
                "recomendacao": "Mantenha inventário atualizado de todos os operadores (fornecedores, SaaS, parceiros) com acesso a dados pessoais e avalie periodicamente sua conformidade.",
            },
        ]
    },
]


# ─── Lógica do questionário ───────────────────────────────────────────────────

def run_checklist(modo_rapido: bool = False) -> list:
    respostas = []
    total = sum(len(cat["perguntas"]) for cat in CHECKLIST)
    atual = 0

    print("\n  Responda com S (sim) / N (não) / P (parcialmente)\n")

    for categoria in CHECKLIST:
        print(f"\n{'─'*60}")
        print(f"  {categoria['categoria'].upper()}")
        print(f"{'─'*60}")

        for pergunta in categoria["perguntas"]:
            atual += 1
            print(f"\n[{atual}/{total}] {pergunta['pergunta']}")

            while True:
                resp = input("  > ").strip().upper()
                if resp in ("S", "N", "P"):
                    break
                print("  Responda com S, N ou P.")

            respostas.append({
                "id":          pergunta["id"],
                "categoria":   categoria["categoria"],
                "pergunta":    pergunta["pergunta"],
                "resposta":    resp,
                "peso":        pergunta["peso"],
                "recomendacao": pergunta["recomendacao"],
            })

    return respostas


# ─── Cálculo de score ─────────────────────────────────────────────────────────

def calcular_score(respostas: list) -> dict:
    pontos_obtidos = 0
    pontos_totais  = 0
    nao_conformes  = []
    parciais       = []
    conformes      = []

    for r in respostas:
        peso = r["peso"]
        pontos_totais += peso * 2  # máximo = peso * 2

        if r["resposta"] == "S":
            pontos_obtidos += peso * 2
            conformes.append(r)
        elif r["resposta"] == "P":
            pontos_obtidos += peso      # metade dos pontos
            parciais.append(r)
        else:
            nao_conformes.append(r)

    percentual = (pontos_obtidos / pontos_totais * 100) if pontos_totais else 0

    if percentual >= 80:
        nivel = "BOM"
        descricao = "Conformidade satisfatória. Foque nos itens parciais para chegar na excelência."
    elif percentual >= 50:
        nivel = "ATENÇÃO"
        descricao = "Conformidade parcial. Existem lacunas relevantes que precisam ser endereçadas."
    else:
        nivel = "CRÍTICO"
        descricao = "Baixa conformidade. A empresa está exposta a riscos significativos e sanções da ANPD."

    return {
        "pontos_obtidos": pontos_obtidos,
        "pontos_totais":  pontos_totais,
        "percentual":     round(percentual, 1),
        "nivel":          nivel,
        "descricao":      descricao,
        "nao_conformes":  sorted(nao_conformes, key=lambda x: -x["peso"]),
        "parciais":       sorted(parciais, key=lambda x: -x["peso"]),
        "conformes":      conformes,
    }


# ─── Relatório ────────────────────────────────────────────────────────────────

def print_report(respostas: list, empresa: str = "Empresa"):
    score = calcular_score(respostas)
    sep   = "=" * 60
    sep2  = "-" * 60
    ts    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{sep}")
    print("  LGPD CHECKLIST — RELATÓRIO DE CONFORMIDADE")
    print(sep)
    print(f"  Empresa  : {empresa}")
    print(f"  Data     : {ts}")
    print(f"  Score    : {score['pontos_obtidos']}/{score['pontos_totais']} pontos  ({score['percentual']}%)")
    print(f"  Status   : [{score['nivel']}] {score['descricao']}")
    print(sep)

    # Resumo por categoria
    print("\n[RESUMO POR CATEGORIA]")
    print(sep2)
    categorias = {}
    for r in respostas:
        cat = r["categoria"]
        if cat not in categorias:
            categorias[cat] = {"S": 0, "P": 0, "N": 0}
        categorias[cat][r["resposta"]] += 1

    for cat, contagem in categorias.items():
        total_cat = sum(contagem.values())
        print(f"\n  {cat}")
        print(f"  ✔ Conforme: {contagem['S']}  ◑ Parcial: {contagem['P']}  ✗ Não conforme: {contagem['N']}")

    # Não conformes (prioridade)
    if score["nao_conformes"]:
        print(f"\n[NÃO CONFORMIDADES — {len(score['nao_conformes'])} item(ns) — PRIORIDADE ALTA]")
        print(sep2)
        for r in score["nao_conformes"]:
            print(f"\n  [{r['id']}] {r['pergunta']}")
            print(f"  → {r['recomendacao']}")

    # Parciais
    if score["parciais"]:
        print(f"\n[PARCIALMENTE CONFORMES — {len(score['parciais'])} item(ns)]")
        print(sep2)
        for r in score["parciais"]:
            print(f"\n  [{r['id']}] {r['pergunta']}")
            print(f"  → {r['recomendacao']}")

    # Conformes
    if score["conformes"]:
        print(f"\n[CONFORMES — {len(score['conformes'])} item(ns)]")
        print(sep2)
        for r in score["conformes"]:
            print(f"  ✔ [{r['id']}] {r['pergunta']}")

    print(f"\n{sep}")
    print("  Relatório gerado por LGPD Checklist Tool")
    print(f"  github.com/JoedersonN/lgpd-checklist")
    print(sep)

    return score


def save_report(respostas: list, empresa: str, output_path: str):
    import io, contextlib
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print_report(respostas, empresa)
    with open(output_path, "w") as f:
        f.write(buffer.getvalue())
    print(f"\n[*] Relatório salvo em: {output_path}")


def save_json(respostas: list, empresa: str, output_path: str):
    score = calcular_score(respostas)
    data = {
        "empresa":   empresa,
        "data":      datetime.now().isoformat(),
        "score":     score["percentual"],
        "nivel":     score["nivel"],
        "respostas": respostas,
    }
    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[*] JSON salvo em: {output_path}")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Questionário interativo de conformidade LGPD com geração de relatório."
    )
    parser.add_argument(
        "-e", "--empresa",
        default="Empresa",
        help="Nome da empresa avaliada (padrão: Empresa)"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Salvar relatório em arquivo .txt"
    )
    parser.add_argument(
        "--json",
        default=None,
        help="Salvar resultado em arquivo .json"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  LGPD CHECKLIST TOOL")
    print("  Avaliação de conformidade — Lei 13.709/2018")
    print("=" * 60)
    print(f"\n  Empresa: {args.empresa}")
    print(f"  Total de perguntas: {sum(len(c['perguntas']) for c in CHECKLIST)}")

    respostas = run_checklist()
    score = print_report(respostas, args.empresa)

    if args.output:
        save_report(respostas, args.empresa, args.output)

    if args.json:
        save_json(respostas, args.empresa, args.json)


if __name__ == "__main__":
    main()
