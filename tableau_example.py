import polars as pl
import numpy as np
import opendp.prelude as dp

dp.enable_features("contrib")

# Étape 1 : Générer le dataset
np.random.seed(123)
sexe = np.random.choice(["Homme", "Femme"], size=50)
emploi = np.random.choice(["CDI", "CDD", "Chômage"], size=50)
logement = np.random.choice(["Appartement", "Maison"], size=50)
df = pl.DataFrame({"Sexe": sexe, "Emploi": emploi, "Logement": logement})

# Requête 1 : Taille du dataset (comptage total)
print("Taille réelle du dataset :", df.height)

# Requête 2 : Comptage par Sexe
print("Comptage par Sexe (non DP) :")
print(df.group_by("Sexe").len())

# Requête 3 : Comptage par Emploi
print("Comptage par Emploi (non DP) :")
print(df.group_by("Emploi").len())

# Requête 4 : Comptage croisé Sexe x Emploi
print("Comptage par Sexe et Emploi (non DP) :")
print(df.group_by(["Sexe", "Emploi"]).len())

# On ne peut pas set la seed en opendp ...
context = dp.Context.compositor(
    # Many columns contain mixtures of strings and numbers and cannot be parsed as floats,
    # so we'll set `ignore_errors` to true to avoid conversion errors.
    data=df.lazy(),
    privacy_unit=dp.unit_of(contributions=1),
    privacy_loss=dp.loss_of(rho=6/(2*25)),
    split_evenly_over=6,
    margins=[
        dp.polars.Margin(max_partition_length=1000),
        dp.polars.Margin(
            by=["Sexe", "Emploi", "Logement"],
            public_info="keys",
            max_partition_length=1000
        ),
    ],
)

taille_dataset = (
    context.query()
    .select(dp.len())
)

print(taille_dataset.release().collect())

comptage_par_sexe = (
    context.query()
    .group_by(pl.col.Sexe)
    .agg(dp.len())
)

print(comptage_par_sexe.release().collect())

comptage_par_emploi = (
    context.query()
    .group_by(pl.col.Emploi)
    .agg(dp.len())
)

print(comptage_par_emploi.release().collect())

comptage_par_emploi_et_sexe = (
    context.query()
    .group_by(pl.col.Sexe, pl.col.Emploi)
    .agg(dp.len())
)

print(comptage_par_emploi_et_sexe.release().collect())

comptage_par_logement = (
    context.query()
    .group_by(pl.col.Logement)
    .agg(dp.len())
)

print(comptage_par_logement.release().collect())

comptage_par_logement_et_sexe = (
    context.query()
    .group_by(pl.col.Sexe, pl.col.Logement)
    .agg(dp.len())
)

print(comptage_par_logement_et_sexe.release().collect())
