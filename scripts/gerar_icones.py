"""
Gerador de ícones SVG para PWA.
Cria ícones em diferentes tamanhos para o app.
"""

import os
from pathlib import Path

def criar_icone_svg(tamanho=192):
    """
    Cria SVG de ícone do app.
    Retorna o conteúdo SVG como string.
    """
    return f'''<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Background gradient -->
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#d946ef;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#9333ea;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Circle background -->
  <circle cx="100" cy="100" r="95" fill="url(#grad)" stroke="#fff" stroke-width="2"/>
  
  <!-- Shield shape -->
  <g transform="translate(100, 100)">
    <!-- Shield outline -->
    <path d="M 0,-40 L 35,-20 L 35,20 Q 0,50 -35,20 L -35,-20 Z" 
          fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Checkmark inside shield -->
    <g transform="translate(0, 5)">
      <path d="M -12,0 L -5,7 L 15,-8" 
            fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>
</svg>'''

def criar_icone_panico_svg(tamanho=192):
    """
    Cria SVG de ícone para botão de pânico.
    """
    return f'''<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Red background -->
  <circle cx="100" cy="100" r="95" fill="#dc2626" stroke="#fff" stroke-width="2"/>
  
  <!-- SOS text -->
  <text x="100" y="110" font-size="60" font-weight="bold" fill="white" text-anchor="middle" font-family="Arial">
    SOS
  </text>
  
  <!-- Pulse rings -->
  <circle cx="100" cy="100" r="85" fill="none" stroke="#fca5a5" stroke-width="2" opacity="0.6"/>
  <circle cx="100" cy="100" r="75" fill="none" stroke="#fca5a5" stroke-width="1" opacity="0.4"/>
</svg>'''

def gerar_icones(diretorio_static='static'):
    """
    Gera todos os ícones necessários para o PWA.
    """
    icones_dir = Path(diretorio_static)
    
    # Cria ícones em diferentes tamanhos
    tamanhos = [192, 512]
    
    for tamanho in tamanhos:
        # Ícone principal do app
        icone_principal = criar_icone_svg(tamanho)
        caminho = icones_dir / f'icon-{tamanho}.png'
        
        # Para PNG real, usaria PIL, mas vou salvar como SVG primeiro
        caminho_svg = icones_dir / f'icon-{tamanho}.svg'
        with open(caminho_svg, 'w', encoding='utf-8') as f:
            f.write(icone_principal)
        
        print(f'✅ Ícone criado: {caminho_svg}')
    
    # Cria screenshot para PWA
    screenshot_svg = criar_icone_svg(540)
    screenshot_path = icones_dir / 'screenshot-540x720.svg'
    with open(screenshot_path, 'w', encoding='utf-8') as f:
        # Adiciona altura para screenshot
        conteudo = screenshot_svg.replace('svg width="540"', 'svg width="540" height="720"')
        f.write(conteudo)
    
    print(f'✅ Screenshot criado: {screenshot_path}')
    
    print('\n⚠️  Para converter SVG para PNG em produção, use:')
    print('   pip install pillow cairosvg')
    print('   ou use ferramentas online como: https://cloudconvert.com/')

if __name__ == '__main__':
    gerar_icones()
