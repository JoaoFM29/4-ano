from z3 import *

EShop,Catalogue,Payment,Security,GUI,Banners,Offers,Info,Image, Description, Price, Search, Basic, Advanced, BankDraft, CreditCard, Visa, AmericanExpress, High, Medium, PC, Mobile = Bools("EShop Catalogue Payment Security GUI Banners Offers Info Image Description Price Search Basic Advanced BankDraft CreditCard Visa AmericanExpress High Medium PC Mobile")
features = [EShop,Catalogue,Payment,Security,GUI,Banners,Offers,Info,Image,Description,Price,Search,Basic,Advanced,BankDraft,CreditCard,Visa,AmericanExpress,High,Medium,PC,Mobile]

s = Solver()

s.add(EShop)

#Obrigatorias nivel 1
s.add(Catalogue == EShop)
s.add(Payment == EShop)
s.add(GUI == EShop)

#Opcionais nivel 1
s.add(Implies(Security, EShop))
s.add(Implies(Banners, EShop))

#Obrigatorias nivel 2
s.add(Info == Catalogue)

#Opcionais nivel 2
s.add(Implies(Offers, Catalogue))
s.add(Implies(Search, Catalogue))

# Or sub-features de Info
s.add(Or(Image,Description, Price) == Info)

# Or sub-features de Search
s.add(Or(Basic,Advanced) == Search)

# Or sub-features de Payment
s.add(Or(BankDraft,CreditCard) == Payment)

# Or sub-features de CreditCard
s.add(Or(Visa,AmericanExpress) == CreditCard)

# Or sub-features de GUI
s.add(Or(PC,Mobile) == GUI)

# High, Medium are xor sub-features of Security
s.add(Or(High,Medium) == Security)
s.add(Not(And(High,Medium)))

# CreditCard requires High
s.add(Implies(CreditCard, High))

# Mobile excludes Banners
s.add(Not(And(Mobile,Banners)))

# Verificar modelo
if s.check() == sat:
    print("Modelo válido.")
    m = s.model()
else:
    print("Modelo inválido.")
    
# Qual o número máximo de dead features que poderia ter acrescentando uma restrição adicional do tipo requires a este feature model?
s.push()

max = 0
atual = 0

for f1 in features:
    for f2 in features:
      if f1.decl() != f2.decl():
        s.push()
        s.add(Implies(f1,f2))
        for f in features:
            s.push()
            s.add(f)
            if s.check() == unsat:
                atual += 1
            s.pop()
        if (atual > max):
          max = atual
        atual = 0
        s.pop()

print(str(max) + " dead features")
s.pop()

# Assumindo que a feature Banners é obrigatória quantas variantes existem? 504
s.push()
s.add(Banners == EShop) 

i = 0
while s.check() == sat:
  i += 1
  m = s.model()
  p = []
  for f in features:
    if is_true(m[f]):
      p.append(f)
    else:
      p.append(Not(f))
  s.add(Not(And(p)))
print("There are " + str(i) + " possible products!")

s.pop()