from z3 import *

Univ = DeclareSort('Univ')
x,y,z = Consts('x y z', Univ)

s = Solver()
s.set("timeout", 10000)

# Entities

User = Function('User', Univ, BoolSort())
Influencer = Function('Influencer', Univ, BoolSort())
Photo = Function('Photo', Univ, BoolSort())
Ad = Function('Ad', Univ, BoolSort())
Day = Function('Day', Univ, BoolSort())

# Associations

follows = Function('follows', Univ, Univ, BoolSort())
sees = Function('sees', Univ, Univ, BoolSort())
posts = Function('posts', Univ, Univ, BoolSort())
suggested = Function('suggested', Univ, Univ, BoolSort())
date = Function('date', Univ, Univ, BoolSort())

#
# 1. Specify the typing and multiplicity constraints that encode the semantics of the diagram
#
# FALL x nao(User(x) & Photo(x))  (um utilizador nao é uma photo)
# FALL x nao(User(x) & Day(x))
# FALL x nao(Photo(x) & Day(x))
# FALL x Influence(x) -> User(x)
# FALL x Ad(x) -> Photo(x)
# FALL x,y follows(x,y) -> User(x) & User(y)
# FALL x,y suggested(x,y) -> User(x) & User(y)
# FALL x,y sees(x,y) -> User(x) & Photo(y)
# FALL x,y posts(x,y) -> User(x) & Photo(y)
# FALL x,y date(x,y) -> Photo(x) & Day(y)
# FALL x Photo(x) -> Existe um y Day(y) & date(x,y)
# FALL x,y,z Photo(x) & Day(y) & Day(z) & date(x,y) & date(x,z) -> y = z

#
# 2. Specify the following requirements
#
# Every photo is posted by one user
# FALL x Photo(x) -> Existe um y posts(y,x)
# FALL x,y,z post(x,z) & posts(y,z) -> x = z

# Users cannot follow themselves
# FALL not(follows(x,x))

# Users can see ads posted by everyone, but only see non ads posted by followed users
# FALL x,y,z User(x) & User(y) & not(Ad(z)) & post(y,z) & sees(x,z) -> follows(x,y)

# If a user posts an ad then all its posts should be labeled as ads
# FALL x,y,z post(x,z) & Ad(z) & posts(x,y) -> Ad(y) 

# Influencers are followed by everyone else
#FALL y (Influencer(y) → FALL x (User(x) → follows(x, y)))

# Influencers post every day
#FALL x Influencer(x) -> FALL y Date(y) -> posts(x, y)

# Suggested are other users followed by followed users, but not yet followed
#FALL x,y (User(x) ∧ User(y) ∧ ∃z (User(z) ∧ follows(x, z) ∧ follows(z, y) ∧ not(follows(x, y))) → suggested(y, x))

# A user only sees ads from followed or suggested users
#FALL x,z (User(x) & Ad(z) -> E1 y (User(y) & (follows(x,y) or suggested(x,y)) & sees(x,z)))

#
# 3. How to check the consistency of these requirements?
#

if s.check() == sat:
    print("Valido")
else:
    print("Inválido")

#
# 4. How to check if, given these requirements, a scenario where some user sees an ad is possible?
#
s.push()
s.add(User(x))
s.add(Ad(z))
s.add(sees(x, z))

if s.check() == sat:
    print("Valido")
else:
    print("Inválido")

s.pop()

#
# 5. How to check the validity of the following assertions given these requirements?
#

# If there are no followers then there are no influencers
s.push()
s.add(User(x))
s.add(ForAll(y, Not(follows(y, x))))  # No followers for user x
s.add(Not(Influencer(x)))  # x is not an influencer


if s.check() == unsat:
    print("Valido")
else:
    print("Inválido")
    
s.pop()

# If there are no followers then there are no suggested users
s.push()
s.add(User(x))
s.add(ForAll(y, Not(follows(y, x))))  # No followers for user x
s.add(ForAll(y, Not(suggested(x,y)))) # No suggestes for user x


if s.check() == sat:
    print("Valido")
else:
    print("Inválido")
    
s.pop()