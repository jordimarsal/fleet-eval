"""Simulacio del winner's curse per a l'article (angle B).

  python3 docs/winner_curse_sim.py

Pregunta: si la flota fos de 10 models IDENTICS (mateix recall real p) i cada
un avaluessim amb n=9 defectes, quina pinta tindria el 'lider' observat?

Resposta (exacta, binomial): E[max] ~ 0.51 a p=0.27 — el 0.56 observat de
minicpm a la primera onada ES el maxim esperat d'una flota igualada.
"""
from math import comb


def fleet_max_stats(p_true: float, n: int = 9, models: int = 10) -> dict:
    """Stats exactes del max/min observat de `models` binomials(n, p_true)."""
    pk = [comb(n, k) * p_true**k * (1 - p_true)**(n - k) for k in range(n + 1)]
    cdf = []
    acc = 0.0
    for k in range(n + 1):
        acc += pk[k]
        cdf.append(acc)
    emax = sum(k * (cdf[k]**models - (cdf[k - 1]**models if k else 0))
               for k in range(n + 1))
    # P(min = 0) = 1 - P(cap model encerta res) = 1 - (1-p0)^models
    p_min_zero = 1 - (1 - pk[0])**models
    return {
        "e_max": emax / n,
        "p_max_ge_5of9": 1 - cdf[4]**models,
        "p_min_zero": p_min_zero,
    }


def main() -> None:
    print("Flota de 10 models IDENTICS (recall real p), bateria de n=9 defectes:")
    print(f"{'p real':>7} {'E[max]':>8} {'P(max>=5/9)':>13} {'P(min=0/9)':>11}")
    for p in (0.20, 0.25, 0.27, 0.30):
        s = fleet_max_stats(p)
        print(f"{p:>7.2f} {s['e_max']:>8.2f} "
              f"{s['p_max_ge_5of9']:>12.0%} {s['p_min_zero']:>10.0%}")
    print("""
Llegit amb les dades reals de C2 (fleet-eval, 2026-11):
  - recall mig observat de la flota a n=33: ~0.24
  - lider de la primera onada (n=9): minicpm 0.56  <- E[max]=0.51 a p=0.27
  - cua de la primera onada: qwen36 i qwen4b 0/9   <- P(min=0)=45% a p=0.27
Conclusio: el rànquing sencer de la primera onada es compatible amb
10 models identics; el 'guanyador' era soroll de seleccio.
minicpm, mateix grading, corpus nou (24 defectes): 4/24 = 0.167.
""")


if __name__ == "__main__":
    main()
