ptf ~
* parameter data
LdFConduct__=~LdFConduct__~
LdFbase_____=~LdFbase_____~
Kshallowclay=~Kshallowclay~
Klakes______=~Klakes______~
Recharge____=~Recharge____~
Cdrainage___=~Cdrainage___~
Cseepage____=~Cseepage____~
Cstream_____=~Cstream_____~
Cwetland____=~Cwetland____~
P-E_________=~P-E_________~
E-P_________ = ~P-E_________~ * -1
PminusE_____ = (~Recharge____~ + ~P-E_________~) * -1
Rlagoon_____ = (((~P-E_________~ * 1631383 + 16710.07) / 433152.2) + ~Recharge____~) * -1
* template files
SWlag_0_2x.tpl LF18LGbk.dat
