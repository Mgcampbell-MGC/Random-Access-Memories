"""Autoteste — proves, in about five minutes, that the O LANÇAMENTO tools work on this computer or sandbox.

Usage:
    python3 autoteste.py

It runs the whole still-and-film path on the fictional Climate Rescue pack (teste/EMBALAGEM_TESTE.png) and a test
scene with a blue stand-in (teste/CENA_TESTE.png), writes everything to ./autoteste_saida/, and prints one line per
check. The last check feeds the checker a piece with a deliberately WRONG label: the test passes only if that piece
is REJECTED, because a check that cannot fail proves nothing.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath("autoteste_saida")
results = []


def ok(name, passed, detail=""):
    results.append(passed)
    print(f"{'OK   ' if passed else 'FALHOU'}  {name}" + (f"  ({detail})" if detail else ""), flush=True)
    return passed


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    t0 = time.time()
    try:
        import cv2
        import imageio_ffmpeg
        import numpy as np
        import PIL
    except ImportError as e:
        ok("bibliotecas instaladas", False, f"{e}. Rode: python3 -m pip install opencv-python-headless numpy "
           "imageio-ffmpeg pillow")
        sys.exit(1)
    ok("bibliotecas instaladas", True, f"OpenCV {cv2.__version__}, Pillow {PIL.__version__}")

    test = next((d for d in (os.path.join(HERE, "teste"), os.path.join(HERE, "..", "teste")) if os.path.isdir(d)), None)
    if not test:
        ok("arquivos de teste", False, "pasta teste/ não encontrada ao lado das ferramentas")
        sys.exit(1)
    pack, scene = os.path.join(test, "EMBALAGEM_TESTE.png"), os.path.join(test, "CENA_TESTE.png")
    os.makedirs(OUT, exist_ok=True)
    o = lambda n: os.path.join(OUT, n)

    # 1. scene to delivery size, 2. composite, 3. crops, 4. text
    rc, msg = run("recortar.py", scene, o("cena_9x16.png"), "1080x1920")
    ok("cena no tamanho 1080x1920", rc == 0, msg.splitlines()[-1] if msg else "")
    rc, msg = run("compor.py", o("cena_9x16.png"), pack, o("kv_9x16.png"), "--sem-oclusao")
    ok("embalagem aplicada", rc == 0 and os.path.exists(o("kv_9x16.png")), msg.splitlines()[-1] if msg else "")
    rc1, _ = run("recortar.py", o("kv_9x16.png"), o("kv_4x5.png"), "1080x1350")
    rc2, _ = run("recortar.py", o("kv_9x16.png"), o("kv_1x1.png"), "1080x1080")
    sizes = [cv2.imread(o(n)).shape[:2] for n in ("kv_4x5.png", "kv_1x1.png")] if rc1 == rc2 == 0 else []
    ok("recortes 4:5 e 1:1", sizes == [(1350, 1080), (1080, 1080)], " e ".join(f"{w}x{h}" for h, w in sizes))
    rc, msg = run("texto.py", o("kv_4x5.png"), o("kv_4x5_texto.png"), "--linhas", "NOVO|Para dias de umidade")
    ok("texto ao lado da embalagem, embalagem intacta", rc == 0 and "intacta: sim" in msg, msg[-60:])

    # 5. the checker passes the exact pieces and catches its planted error on each
    pieces = [o(n) for n in ("kv_9x16.png", "kv_4x5_texto.png", "kv_1x1.png")]
    rc, msg = run("relatorio_fidelidade.py", pack, *pieces, "--json", o("relatorio_pecas.json"))
    ok("conferência: 3 peças exatas APROVADAS, erro plantado detectado", rc == 0 and msg.count("APROVADA") == 3
       and msg.count('"control_caught": true') == 3)

    # 6. film: size, colour tags, every frame checked
    film = o("corte_6s_9x16.mp4")
    rc, msg = run("filme.py", o("kv_9x16.png"), film, "--formato", "9:16", "--segundos", "6", "--fps", "30",
                  "--zoom", "0.04", "--pan", "0.02")
    info = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", film], capture_output=True, text=True).stderr
    ok("filme 1080x1920, 30 fps, cor BT.709", rc == 0 and "1080x1920" in info and "bt709" in info and "30 fps" in info)
    rc, msg = run("relatorio_fidelidade.py", pack, film, "--json", o("relatorio_filme.json"))
    ok("conferência do filme: todos os quadros APROVADOS", rc == 0 and "APROVADA" in msg)

    # 7. a wrong label must be rejected
    bad = cv2.imread(pack, cv2.IMREAD_UNCHANGED)
    g = cv2.cvtColor(bad[..., :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
    ink = np.abs(g - cv2.GaussianBlur(g, (0, 0), 3)) * (bad[..., 3] > 200)
    h, w = g.shape
    rows = ink[:, w // 5: 4 * w // 5].sum(1)
    y = int(np.argmax(np.convolve(rows, np.ones(h // 20), "same")))  # the line of lettering with the most ink
    x0, x1, y0, y1 = w // 5, 4 * w // 5, max(0, y - h // 40), min(h, y + h // 40)
    bad[y0:y1, x0:x1] = bad[y0:y1, x0:x1][:, ::-1]  # mirror that line: the letters are now wrong
    cv2.imwrite(o("embalagem_errada.png"), bad)
    run("compor.py", o("cena_9x16.png"), o("embalagem_errada.png"), o("peca_errada.png"), "--sem-oclusao")
    rc, msg = run("relatorio_fidelidade.py", pack, o("peca_errada.png"))
    ok("rótulo errado é REPROVADO", rc != 0 and "REPROVADA" in msg)

    n = len(results)
    print(f"\nAUTOTESTE: {sum(results)}/{n} OK em {time.time() - t0:.0f} s. Arquivos em {OUT}")
    if all(results):
        print("Tudo certo: as ferramentas funcionam aqui.")
    else:
        print("Algo falhou. Mande esta tela inteira para quem configurou o kit.")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
