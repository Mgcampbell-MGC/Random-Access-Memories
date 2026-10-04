"""Builds the Manus kit's three zips from the repo, so the tools inside them never drift from tools/.

Usage (from the repo root):
    python3 kit-manus/montar_kit.py

Writes kit-manus/dist/:
    o-lancamento-skill.zip   upload in Manus → Skills
    O_LANCAMENTO_pasta.zip   unzip into Sol's Documents
    KIT_MANUS_SOL.zip        everything, for sending
"""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, "kit-manus")
TOOLS = os.path.join(ROOT, "tools")
DIST = os.path.join(KIT, "dist")
SCRIPTS = ["recortar.py", "compor.py", "texto.py", "relatorio_fidelidade.py", "filme.py", "autoteste.py"]
TEST = ["teste/EMBALAGEM_TESTE.png", "teste/CENA_TESTE.png"]
WORK = ["00_recebido", "01_mundos", "02_cenas", "03_pecas", "04_filme", "05_entrega"]


def add(z, src, arc):
    z.write(src, arc)


def folder(z, arc):
    z.writestr(zipfile.ZipInfo(arc.rstrip("/") + "/"), "")


def main():
    os.makedirs(DIST, exist_ok=True)

    skill = os.path.join(DIST, "o-lancamento-skill.zip")
    with zipfile.ZipFile(skill, "w", zipfile.ZIP_DEFLATED) as z:
        add(z, os.path.join(KIT, "3_skill", "o-lancamento", "SKILL.md"), "o-lancamento/SKILL.md")
        for s in SCRIPTS + TEST:
            add(z, os.path.join(TOOLS, s), "o-lancamento/scripts/" + s)

    pasta = os.path.join(DIST, "O_LANCAMENTO_pasta.zip")
    base = "O LANCAMENTO/"
    with zipfile.ZipFile(pasta, "w", zipfile.ZIP_DEFLATED) as z:
        for s in SCRIPTS + TEST + ["LEIA-ME.md"]:
            add(z, os.path.join(TOOLS, s), base + "_ferramentas/" + s)
        z.writestr(base + "_biblioteca/mundos/LEIA-ME.txt",
                   "Cada mundo novo: o prompt que funcionou, a data e uma miniatura feita com a embalagem azul.\n")
        practice = base + "clientes/orvalha_PRATICA/"
        for w in WORK:
            folder(z, practice + w)
        src = os.path.join(KIT, "pratica_orvalha", "00_recebido")
        for f in sorted(os.listdir(src)):
            add(z, os.path.join(src, f), practice + "00_recebido/" + f)
        for f in ("GUIA_DA_SOL.md", "TESTE.md"):
            add(z, os.path.join(KIT, f), base + f)

    tudo = os.path.join(DIST, "KIT_MANUS_SOL.zip")
    with zipfile.ZipFile(tudo, "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("SETUP.md", "GUIA_DA_SOL.md", "TESTE.md", "1_instrucao_do_projeto.txt"):
            add(z, os.path.join(KIT, f), "KIT_MANUS_SOL/" + f)
        kb = os.path.join(KIT, "2_base_de_conhecimento")
        for f in sorted(os.listdir(kb)):
            add(z, os.path.join(kb, f), "KIT_MANUS_SOL/2_base_de_conhecimento/" + f)
        add(z, skill, "KIT_MANUS_SOL/o-lancamento-skill.zip")
        add(z, pasta, "KIT_MANUS_SOL/O_LANCAMENTO_pasta.zip")

    for p in (skill, pasta, tudo):
        print(f"{os.path.relpath(p, ROOT)}  {os.path.getsize(p) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
