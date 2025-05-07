from z3 import *

pessoas = ["Ana","Nuno","Pedro","Maria"]
gabs = [1,2,3]


x = {}
for p in pessoas:
    x[p] = {}
    for g in gabs:
        x[p][g] = Bool("%s,%d" % (p,g))

s = Solver()



# Cada pessoa ocupa pelo menos um gabinete.
for p in pessoas:
    s.add(Or([x[p][g] for g in gabs]))
    
# Cada pessoa ocupa no máximo um gabinete.
for p in pessoas:
    for g in gabs:
        s.add(Implies(x[p][g], And([Not(x[p][n]) for n in gabs if n != g])))
    
# O Nuno e o Pedro não podem partilhar gabinete.
for g in gabs:
    s.add(Implies(x["Nuno"][g], And(Not(x["Pedro"][g]))))
    
# Se a Ana ficar sozinha num gabinete, então o Pedro também terá
# que ficar sozinho num gabinete.

anaSo = Or([And(x["Ana"][g], 
               Not(x["Nuno"][g]),
               Not(x["Pedro"][g]),
               Not(x["Maria"][g])) for g in gabs])

pedroSo = Or([And(x["Pedro"][g], 
               Not(x["Ana"][g]),
               Not(x["Nuno"][g]),
               Not(x["Maria"][g])) for g in gabs])

s.add(Implies(anaSo,pedroSo))
        
# Cada gabinete só pode acomodar, no máximo, 2 pessoas.
for g in gabs:
    s.add(And([Implies(And(x[p1][g],x[p2][g]),
            And(Not(x[p3][g]), Not(x[p4][g])))
    for p1 in pessoas for p2 in pessoas for p3 in pessoas for p4 in pessoas 
        if p1!=p2 and p1!=p3 and p1!=p4 and p2!=p3 and p2!=p4 and p3!=p4]))
    
    
#1. Se a Maria ocupar o gabinete um, então ela ficará sozinha nesse gabinete.
#for p in pessoas:
 #   if p != 'Maria':  
  #      s.add(And(x['Maria'][1], x[p][1]))
## Falso, a maria nao ficaria sozinha 

#----------------------------------
#2. Se a Ana e o Nuno ficarem no mesmo gabinete, então a Maria e o Pedro terão que partilhar também um outro gabinete.

for g in gabs:
    for f in gabs:
        if f != g:  
            s.add(And(And(x['Ana'][g], x['Nuno'][g])), Not(And(x['Maria'][f], x['Pedro'][f])))
  

## Falso, a maria e o pedro podem ficar em gabinetes separados

s.push()

if s.check() == sat:
    m = s.model()
    for p in pessoas:
        for g in gabs:
            if is_true(m[x[p][g]]):
                print("%s fica no gabinete %s" % (p,g))
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
            for g in gabs:
                # Impede que a mesma alocação seja repetida
                if is_true(modelo[x[p][g]]):
                    bloqueio.append(x[p][g])
                else:
                    bloqueio.append(Not(x[p][g]))
        
        # Adiciona a restrição que bloqueia a solução encontrada
        s.add(Not(And(bloqueio)))

    return contador

# Contando as soluções possíveis
total_solucoes = contar_solucoes()
print(f"Total de distribuições possíveis: {total_solucoes}")