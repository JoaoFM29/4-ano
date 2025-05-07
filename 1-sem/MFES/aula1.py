from z3 import *

Survey,License,ABtesting,Statistics,QA,Advancedlicense,Basiclicense,BasicQA,MultimediaQA = Bools("Survey License ABtesting Statistics QA Advancedlicense Basiclicense BasicQA MultimediaQA")
features = [Survey,License,ABtesting,Statistics,QA,Advancedlicense,Basiclicense,BasicQA,MultimediaQA]

s = Solver()

# Survey is a root reature
s.add(Survey)
# Calls is a mandatory sub-feature of Survey
s.add(License == Survey)
# GPS is an optional sub-feature of Survey
s.add(Implies(ABtesting,Survey))
# GPS is an optional sub-feature of Survey
s.add(Implies(Statistics,Survey))
# Screen is a mandatory sub-feature of Survey
s.add(QA == Survey)
# Basic, Colour, and Highres are xor sub-features of Screen
s.add(Or(Advancedlicense,Basiclicense) == License)
s.add(Not(And(Advancedlicense,Basiclicense)))
# Camera and MP3 are or sub-features of Media
s.add(Or(BasicQA,MultimediaQA) == QA)
# Basiclicense excludes MultimediaQA
s.add(Not(And(Basiclicense,MultimediaQA)))
# Basiclicense excludes ABtesting
s.add(Not(And(Basiclicense,ABtesting)))
# ABtesting requires Statistics
s.add(Implies(ABtesting, Statistics))

if s.check() == sat:
  print("Feature model is non void")
else:
  print("Feature model is void")

s.push()
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

s.add(ABtesting == Survey)

if s.check() == sat:
  print("Feature model is non void")
else:
  print("Feature model is void")
  
s.push()
s.add(Implies(BasicQA,ABtesting))
for f in features:
  s.push()
  s.add(f)
  if s.check() == unsat:
    print("Feature " + f.decl().name() + " is dead!")
  s.pop()
s.pop()