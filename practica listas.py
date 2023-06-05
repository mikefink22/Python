Lista1=["Lulu", "Jinx", "Sona", "Lee Sin"] * 2

Lista1.append("Ocho")
Lista1.insert(2,"Kai'Sa")

Lista2=[25, 43.2, True, False]

Lista3=Lista1+Lista2
Lista3.extend(["Bob Ross", "Steve", "borrar"])
Lista3.remove("Ocho")
Lista3.pop()



print(Lista1[:])

print(Lista3[:])

print(Lista3[-3])

print(Lista3.index("Sona"))











