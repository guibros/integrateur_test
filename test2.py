from profilAtlas import Profil



profil = Profil("Bill")

profilFetch = profil.fetch_profil()

profilPop = profil.pop_profil()

print(profilFetch)

print(profilPop)

print(profilFetch['Last_Name'])
print(profilFetch['First_Name'])
print(profilFetch['Personnel']['2'][-1])
print(profilFetch['Medicament'][-1])

