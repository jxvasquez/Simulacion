# ==============================================================================
# ARCHIVO : sir/dominio/estados.py
# CAPA    : Dominio
# OBJETIVO: definir los tres estados de salud posibles de una persona en el modelo SIR.
# ==============================================================================

# Estado S = Susceptible: la persona esta sana pero se puede contagiar.
ESTADO_SUSCEPTIBLE = "S"

# Estado I = Infectado: la persona tiene la enfermedad y puede contagiar a otras.
ESTADO_INFECTADO = "I"

# Estado R = Recuperado: la persona ya se curo y no vuelve a enfermar en este modelo.
ESTADO_RECUPERADO = "R"
