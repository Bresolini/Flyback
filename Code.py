#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 18:18:07 2020

@author: Bernardo Bresolini
@email:  berbresolini14@gmail.com

O código abaixo executa uma rotina de cálculos a fim de dimensionar os componentes de um FlyBack sem Snubber.
Para tanto, pode ser necessário alterar alguns dados dos componentes usados se for usar especificações/componentes diferentes. 
"""
from math import sqrt, ceil, pi
#import numpy as np


# Passo 1: definiçao das especificaçoes do sistema

Vdc    = 150    # (V)     Tensao de entrada
Vo     = 5      # (V)     Tensao da saida
Po     = 30     # (W)     Potencia de saida
fs     = 50e3   # (V)     Frequencia da rede
Vrp    = 0.05   # (Vpp)   Tensao de ripple maxima na saida
Vf     = 0.6    # (V)     Tensao no diodo da saida
Dmax   = 0.4    # (%/100) Ciclo ativo maximo
Dmin   = 0.25   # (%/100) Ciclo ativo minimo
k      = 1      # (%?100) Eficiencia do transformador


# Estimar a corrente media do primario
"""

        |
        |
        |
     ΔI |--------.                       .
        |       /|                      /|
        |      / |                     / |
        |     /  |                    /  |
   Imed |----/---|-------------------/---|
        |   /    |                  /    |
        |  /     |                 /     |
        | /      |                /      |
        |/_______|_______________/_______|__________>
        |<------>|<------------->|<----->|
           ton          toff       ton

           T = ton + toff

           O valor medio e dado por

            Imed = ΔI/2 = Imax/2

"""

# Da conservaçao da energia no transformador segue
Pi   = Po/k            # (W) Potencia de saida do trafo
Imed = Pi/(Dmax*Vdc)   # (A) Corrente media no primario

# A indutancia do transformador deve ser tal que
Lm = (Vdc*Dmax)**2/(2*fs*Pi)   # (H) Indutancia do trafo
print('Indutancia projetada: %0.4f mH' %(Lm*1000))

# Resolvendo a equaçao da corrente media
Imax = 2*Imed   # (A) Corrente maxima no primario

# Corrente do Dreno-Source rms
IDSrms = sqrt( ( 3*Imed**2 + Imax**2/4 )*Dmax/3 )

# Escolha da corrente maxima da chave
Iover = 2   # (A)

# Sabendo Imax e Vdc, pode-se escolher uma chave: MOSFET ou BJT
Vsat = 450             # (V) Tensao maxima que a chave suporta
Vro = (Vsat - Vdc)/2   # (V) Tensao refletida


# Dimensionamento do indutor
Ae = 0.2*sqrt(Pi)/fs   # (m²) Area efetiva do nucleo
print('A area projetado eh: %d mm²' %(Ae*1e6))
Ae = 85.97   # (mm²) Area efetiva do nucleo
print('A area comercial eh: %d mm²' %(Ae))

"""
    O nucleo E tem as medidas
                                       ct - tol
            |            |<-------------------------------->|
            |            |                                  |
            |            |                 cc               |
            |            |           |<---------->|         |
             _____________           _____________          _____________ _________
            |            |          |            |          |           |     |
            |            |          |            |          |           |     |
            |            |          |            |          |           |     |
            |            |          |            |          |           |     | hs
            |            |          |            |          |           |     |
            |            |          |            |          |           |     |
            |            |__________|            |__________|           | ____|____
            |                                                           |
            |                                                           |
            |                                                           |
            |                                                           |
            |___________________________________________________________|
"""

hs = 6.3         # (mm)  Altura
cc = 7.5 + 0     # (mm)  Comprimento central
ct = 18.6 - 0    # (mm)  Comprimento total
A = hs*(ct-cc)   # (mm²) Area disponivel no nucleo

Al = 75   # (nH/volta²) Vallor AL sem GAP

Bsat = 0.3   # (T) Quando nao ha dados, admitir que seja entre 0,3 a 0,35

# Numero de espiras no primario
Np = ceil( Lm*Iover/(Bsat*Ae)*1e6 ) # (Espiras) Arredondado para cima
print('O numero de espiras no primario eh: %d espiras' %(Np) )

# Numero de espiras no secundario
Ns = ceil( Np*(Vo+Vf)/Vro )   # (Espiras) Arredondado para cima
print('O numero de espiras no secundario eh: %d espiras' %(Ns) )

G = 40*pi*Ae/1e6*( Np/(1000*Lm) - 1/Al )   # (mm) GAP
G = ceil(G*1e2)/1e2                        # (mm) GAP arredondado
print('o GAP deve ser de: %0.2f' %(G))


# Diametro do fio
ISrms = IDSrms*sqrt( (1-Dmax)/Dmax )*Vro/(Vo+Vf)   # (Arms) Corrente rms no secundario
ISrms = ceil( ISrms*1e2 )/1e2
print('Corrente rms no secundario: %0.2f A' %(ISrms))

# O fio escolhido no secundario eh AWG 10, D = 2,588 mm
Af = 2.588**2*pi/4   # (mm²) Area do fio
Sf = Af*Ns           # (mm²) Area ocupada pelas espiras

print('Area disponivel no nucleo: %d mm²' %(A))
print('Area ocupada pelos fios do secundario: %d mm²' %(Sf))

# Verifica se a area do nucleo eh necessaria
if (0.4*A > Ns*Af):
    print('Os fios do secundario NAO OCUPAM 40% do espaço!')
else:
    print('DEVE-SE AUMENTAR O NUCLEO! AREA INSUFICIENTE PARA OS FIOS!')

# Dimensoes do diodo SCHOTTKY
"""
    Segundo FAIRCHILD  a tensao tipica e corrente de margem do retificador sao

                     Vrrm > 1.3*Vd
                     If   > 1.5*IDrms
"""
Vd    = Vo + Vdc*(Vo+Vf)/Vro               # (V)    Tensao reversa
IDrms = IDSrms*sqrt(Vdc/Vro)*Vro/(Vd+Vf)   # (Arms) Corrente rms direta

Vrrm = ceil( 1.3*Vd*1e2)/1e2
If   = ceil( 1.5*IDrms*1e2)/1e2

print('Maxima tensao reversa: %0.2f V' %(Vrrm))
print('Corrente rms direta: %0.2f A' %(If))

# Capacitor de saida

Io = Po/Vo
Rc = Vo**2/Po
Co = Io*Dmax/(Vrp*fs )
Co = ceil( Co*1e6 )   # (μF) Arredondando

print('Capacitor da saida: %d μF' %(Co) )
