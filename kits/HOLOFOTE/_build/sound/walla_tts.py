#!/usr/bin/env python
"""HOLOFOTE · walla_tts.py — the raw voices for the pre-show murmur and the stadium roar.

Synthesises everyday theatre-foyer chatter (PT-BR) and open-vowel cheers with many Kokoro voices (Apache-2.0 model,
run locally). Nobody is imitated; at mix level the words are smeared below intelligibility on purpose.
Run with the Kokoro venv:

    /home/user/venvs/kokoro/bin/python -I walla_tts.py
Writes _tmp/walla/*.wav (24 kHz mono). Deterministic text/voice plan; the model itself is deterministic on CPU.
"""
import os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_tmp", "walla")
MODEL = "/home/user/maes_build/tts/kokoro-v1.0.onnx"
VOICES = "/home/user/maes_build/tts/voices-v1.0.bin"

LINES = [
    "Ai, que bom que a gente chegou cedo, olha esse lugar.",
    "Você trouxe o casaco? Aqui dentro faz um frio danado.",
    "Senta aqui do meu lado, guardei a cadeira pra você.",
    "Nossa, tá lotado, nunca vi tanta gente assim.",
    "Ela falou que ia começar às oito, mas sempre atrasa um pouquinho.",
    "Desliga o celular, senão depois toca no meio.",
    "Quer uma bala? Tenho de menta e de morango.",
    "Olha lá, já tão arrumando a luz no palco.",
    "Minha nossa, essa fila tava enorme lá fora.",
    "Depois a gente vai comer alguma coisa ali na esquina.",
    "Não, não, a fileira certa é essa aqui, a do meio.",
    "Será que dá pra ver bem daqui de trás?",
    "Fala baixo, já vai começar daqui a pouco.",
    "Comprei o ingresso faz três meses, acredita?",
    "Que cheiro bom, parece de baunilha.",
    "Você viu quem tava sentado na primeira fila?",
    "Tá todo mundo arrumado hoje, que chique.",
    "Eu adoro esse momento antes de começar, sabia?",
    "Passa a pipoca pra cá, por favor.",
    "A minha tia vinha sempre aqui quando era nova.",
]
CHEERS = ["Ééééééééé!", "Aaaaaaaaah!", "Uhuuuuuuuu!", "Ôôôôôôôô!", "Êêêêêêêê!", "Aêêêêêêêê!"]

# voice, lang, speed — PT-BR natives plus other voices made to speak Portuguese (accents vanish in a crowd)
CAST = [("pf_dora", "pt-br", 1.05), ("pm_alex", "pt-br", 1.0), ("pm_santa", "pt-br", 1.1), ("ef_dora", "pt-br", 1.0),
        ("em_alex", "pt-br", 1.05), ("if_sara", "pt-br", 1.0), ("im_nicola", "pt-br", 0.95), ("af_heart", "pt-br", 1.0),
        ("af_bella", "pt-br", 1.1), ("am_adam", "pt-br", 0.95), ("am_michael", "pt-br", 1.0), ("bf_emma", "pt-br", 1.05),
        ("bm_george", "pt-br", 0.95), ("af_sarah", "pt-br", 1.0), ("am_eric", "pt-br", 1.05), ("ff_siwis", "pt-br", 1.0)]


def main():
    os.makedirs(OUT, exist_ok=True)
    k = Kokoro(MODEL, VOICES)
    n = 0
    for vi, (v, lang, sp) in enumerate(CAST):
        # each voice says 3 different lines (rotating) and 2 cheers
        for j in range(3):
            line = LINES[(vi * 3 + j) % len(LINES)]
            fn = os.path.join(OUT, f"talk_{vi:02d}_{j}.wav")
            if not os.path.exists(fn):
                y, sr = k.create(line, voice=v, speed=sp, lang=lang)
                sf.write(fn, y, sr)
            n += 1
        for j in range(2):
            c = CHEERS[(vi * 2 + j) % len(CHEERS)]
            fn = os.path.join(OUT, f"cheer_{vi:02d}_{j}.wav")
            if not os.path.exists(fn):
                y, sr = k.create(c, voice=v, speed=0.8, lang=lang)
                sf.write(fn, y, sr)
            n += 1
        print(f"{v} done", flush=True)
    print("total", n)


if __name__ == "__main__":
    main()
