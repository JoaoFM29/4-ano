from z3 import *

pessoas = ["Ana","Beatriz","Carlos"]
aulas = [1,2,3,4,5]
x = {}
for p in pessoas:
    x[p] = {}
    for a in aulas:
        x[p][a] = Bool("%s,%d" % (p,a))

s = Solver()

#O Carlos não pode dar a primeira aula.
s.add(Not(x['Carlos'][1]))

#Se a Beatriz der a primeira aula, não poderá dar a última.
s.add(Implies(x['Beatriz'][1], Not(x['Beatriz'][5])))
    
#Cada aula tem pelo menos um formador.
for a in aulas:
    s.add(Or(x['Ana'][a], x['Beatriz'][a], x['Carlos'][a]))

#As quatro primeiras aulas têm no máximo um formador.
for a in range(1,5):
    s.add(AtMost(x['Ana'][a], x['Beatriz'][a], x['Carlos'][a], 1))
    
#A última aula pode ter no máximo dois formadores.
s.add(AtMost(x['Ana'][5], x['Beatriz'][5], x['Carlos'][5], 2))

#Nenhum formador pode dar 4 aulas consecutivas.
for p in pessoas:
    for a in range(1,3):
        s.add(Not(And(x[p][a], x[p][a+1], x[p][a+2], x[p][a+3])))


s.push()

if s.check() == sat:
    m = s.model()
    for p in pessoas:
        for a in aulas:
            if is_true(m[x[p][a]]):
                print("%s dá a aula %s" % (p,a))
else:
  print("Não tem solução.")
  
  
# Função para contar todas as soluções
def contar_solucoes():
    contador = 0  # Contador de soluções

    while s.check() == sat:
        contador += 1
        modelo = s.model()
        
        # Cria uma restrição para bloquear a solução atual
        bloqueio = []
        for p in pessoas:
            for a in aulas:
                # Impede que a mesma alocação seja repetida
                if is_true(modelo[x[p][a]]):
                    bloqueio.append(x[p][a])
                else:
                    bloqueio.append(Not(x[p][a]))
        
        # Adiciona a restrição que bloqueia a solução encontrada
        s.add(Not(And(bloqueio)))

    return contador

# Contando as soluções possíveis
total_solucoes = contar_solucoes()
print(f"Total de distribuições possíveis: {total_solucoes}")