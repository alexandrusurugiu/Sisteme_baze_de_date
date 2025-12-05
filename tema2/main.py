# Exercitiile sunt rezolvate folosind NoSQLBooster pentru MongoDB.


# Exercitiul 1: Să se afișeze toți clienții care au leasing în EUR
db.clienti_leasing.find({ MONEDA: "EUR" })


# Exercitiul 2: Să se afișeze numele, profesia, varsta și suma din depozit pentru clienții care au în depozite mai mult de 10000 lei.
db.clienti_leasing.find(
    { SUMA_DEPOZIT: { $gt: 10000 } },
    { NUME_CLIENT: 1, PROFESIA: 1, VARSTA: 1, SUMA_DEPOZIT: 1, _id: 0 }
)


# Exercitiul 3: Afișați clienții (nume, varsta, suma credit, descriere) care au credite de tipul “DIVERS”.
db.clienti_leasing.find(
    { DESCRIERE: /DIVERS/ },
    { NUME_CLIENT: 1, VARSTA: 1, VAL_CREDITE_RON: 1, DESCRIERE: 1, _id: 0 }
)


# Exercitiul 4: Afișați clienții cu vârsta cuprinsă între 25 si 35 de ani care au credite mai mari decât 20.000 lei.
db.clienti_leasing.find({
    VARSTA: { $gte: 25, $lte: 35 },
    VAL_CREDITE_RON: { $gt: 20000 }
})


# Exercitiul 5: Să se afișeze numele, profesia, suma solicitată pentru clienții care au gradul de fidelitate =2. Ordonați crescător în funcție de vârstă.
db.clienti_leasing.find(
    { FIDELITATE: 2 },
    { NUME_CLIENT: 1, PROFESIA: 1, SUMA_SOLICITATA: 1, _id: 0 }
).sort({ VARSTA: 1 })


# Exercitiul 6: Afișați valoarea totală a creditelor pe fiecare profesie. Ordonați descrescător în funcție de valoarea totată a creditelor.
db.clienti_leasing.aggregate([
    {
        $group: {
            _id: "$PROFESIA",
            valoare_totala_credite: { $sum: "$VAL_CREDITE_RON" }
        }
    },
    {
        $sort: { valoare_totala_credite: -1 }
    }
])


# Exercitiul 7: Afișați numărul de clienți și valoarea medie solicitată în funcție de starea civilă pentru clienții cu vârsta între 30 – 40 de ani.
db.clienti_leasing.aggregate([
    {
        $match: {
            VARSTA: { $gte: 30, $lte: 40 }
        }
    },
    {
        $group: {
            _id: "$STARE_CIVILA",
            nr_clienti: { $sum: 1 },
            valoare_medie_solicitata: { $avg: "$SUMA_SOLICITATA" }
        }
    }
])