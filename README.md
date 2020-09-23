# Flyback
Todo o material usado para dimensionar o Flyback é contido aqui.

O **FlayBack** recebe 150 Vdc e deve entregar 5 V e 30 W na sáida com máxima variação de 50 mVpp.
Para tanto, o chaveamento pensado é de 50 kHz com ciclo ativo entre 0,25 e 0,4 (operando em modo descontínuo).
Admitiu-se que os indutores acoplados são ideais e não têm perdas na conversão da energia.


## Código
O código feito está na **linguagem Python** e utiliza de bibliotecas padrão. No _Linux_, Python já vem instalado. No _Windows_ pode ser necessário instalá-lo. Para fazer isso, instale o Anaconda pelo site
> ```https://www.anaconda.com/products/individual```

O código está comentado. Mas para seu funcionamento, são necessárias algumas informações. As especificações de projeto e valores comerciais de componentes.

## Referências e Datasheet
As referências usadas e os datasheets estão inclusos neste repositório. Nele estão contidas todas as informações e componentes usados.

## Componentes
Foram projetados: 1 capacitor, 1 indutor acoplado e 1 MOSFET.

### Capacitor
O capacitor de saída deve filtrar o sinal para que a oscilação seja de 50 mVpp. Logo, escolheu-se
> ```UUN1E102MNQ1ZD```
Cujas especificações são
* _Vdc_ = 20 V
* _C_ = 1000 µF ± 20%
* _Tmax_ = 105 °C
* Diametro = 18 mm

### Núcleo de Ferrite
O núcleo de ferrite deve conter uma área efetiva para transmitir eletromagneticamente a energia e área suficiente para suportar as espiras. Então
> ```NEE-30/15/14-100-IP12E```
* _Ae_ = 122
* _Al_ = 100
* Área para os enrolamentos = 119,31 (calculada)

### MOSFET
O MOSFET será a chave do circuito. Ele deve então suportar a corrente que passará pelo dreno (2 A) e ainda a potência no primário (30 W). Destarte,
> ```TK6A45DA```
* _VDSS_ = 450 V
* _Pd_ = 35 W
* _Id_ = 5,5 A
* Resistência térmica com dissipador = 3,57 °C/W

### Fios esmaltados
Para o primário a máxima corrente projetada _Iover_ foi de 2 Arms. Então
> Fio AWG 19
* _D_ = 0,9113 mm
* Corrente suportada = 2 A

Para o secundário a máxima corrente é de _ISrms_ 11,88 Arms. Então
> Fio AWG 10
* _D_ = 2,588 mm
* Corrente suportada = 15 A.
