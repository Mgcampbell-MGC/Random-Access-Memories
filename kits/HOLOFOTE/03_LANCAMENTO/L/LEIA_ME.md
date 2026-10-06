# 03_LANCAMENTO/L · a loja (§E.3)

Fotos de catálogo 1200 × 1200, estado LOJA: luz principal de 30 × 30 cm a 45° à esquerda, rebatedor branco a 20 %,
fundo papel-cartaz `#FFF8EC` exato, preenchido por código por trás do render (o render sai transparente com a sombra
de contato num "shadow catcher"). Nenhum tipo, preço, estrela, selo ou "mais vendido" dentro da imagem.

| Arquivo | O que é |
|---|---|
| `L00_FRENTE.png` | AO VIVO 200 g de frente (0°), apagada, com a tampa: o painel da frente reto para a câmera (pedido do diretor para a linha "Frente 0°" do pacote). |
| `L01_FRENTE.png` | AO VIVO em ¾ (20°), apagada, a tampa-palco encostada no lado direito DELA (à esquerda de quem olha), mostrando o X e "ela fica aqui."; a tampa apoia de verdade no copo (posição resolvida por código). |
| `L02_VERSO.png` | O verso reto (180°), sem tampa: ELA ESTEVE EM TODAS. — o texto da página diz que o verso é o ponto. |
| `L03_A-BASE.png` | O copo deitado, base para a câmera, girado 15°, luz rasante pela esquerda: o relevo PRECISAVA. e a etiqueta de lote legíveis. |
| `L04_O-CASE-ABERTO.png` | O CASE aberto visto a 70° de cima: o espelho (só o teto e uma lâmpada), o copo na espuma, a setlist em leque mostrando os ingressos, a pulseira com o selo. |
| `L05_A-TAMPA-PALCO.png` | A vela ACESA em cima da própria tampa virada, ¾ de frente, 25° de cima; nada a menos de 30 cm. |
| `L06_A-TURNE.png` | A coleção em linha, apagada, com tampas: MAIS UM! · CAMARIM · AO VIVO · ACÚSTICO, O SINGLE (escala real) e uma cápsula NOVA TEMPORADA. A única foto em que as quatro cores se encontram. |
| `L07_NOVA-TEMPORADA.png` | O copo limpo e vazio, a cápsula de refil ao lado com a tampa de selar meio aberta. |

Os renders transparentes (com a sombra) estão em `02_PRODUTO/renders/L0n_*_alpha.png` (8 bits) e `_alpha_16bit.png`.
Fidelidade do rótulo: `06_PRODUCAO/fidelidade/L0n_*.json` (a verificação roda sobre a imagem final, já com o fundo).

Como refazer: `_build/shots/blender.sh _build/shots/campanha.py -- L00 L01 L02 L03 L04 L05 L06 L07`.
