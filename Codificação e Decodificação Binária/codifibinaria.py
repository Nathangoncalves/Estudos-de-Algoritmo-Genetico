def cod(pop, CromLim, Lbits):
    Nind = len(pop)
    Ncrom = len(CromLim)
    code = []

    for i in range(Nind):
        temp = ""
        for j in range(Ncrom):
            inf = CromLim[j][0]
            sup=CromLim[j][1]
            aux=((pop[i][j]-inf)/(sup-inf))*(2**Lbits[j]-1)
            aux = format(int(round(aux)), f'0{Lbits[j]}b')

            if j == 0:
                temp=aux
            else:
                temp+=aux

        code.append(temp)

    return code

def decode(binpop, CromLim, Lbits):
    Nind = len(binpop)
    Ncrom = len(CromLim)
    decode = []

    for i in range(Nind):
        temp = []
        start = 0  
        for j in range(Ncrom):
            end = start + Lbits[j]
            bin_cromossomo = binpop[i][start:end] 
            start = end 

            aux = int(bin_cromossomo, 2)
            inf = CromLim[j][0]
            sup = CromLim[j][1]
            aux = aux * (sup - inf) / (2 ** Lbits[j] - 1) + inf
            temp.append(aux)  

        decode.append(temp)  

    return decode

pop = [[0.15, 0.85], [0.05, 0.25], [0.45, 0.55]]
CromLim = [[0.0, 1.0],[0.0, 1.0]]
Lbits = [8, 8]  

populacao_codificada = cod(pop, CromLim, Lbits)
print("Codificação:", populacao_codificada)
populacao_decodificada = decode(populacao_codificada, CromLim, Lbits)
print("Decodificação:", populacao_decodificada)