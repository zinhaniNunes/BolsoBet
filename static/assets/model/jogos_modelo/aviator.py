import random
import time
import os

saldo = 1000

while saldo > 0:

    os.system("clear")  # use "cls" no Windows

    print("=" * 35)
    print(f"Saldo: R${saldo:.2f}")

    try:
        aposta = float(input("Aposta: R$"))
    except:
        continue

    if aposta <= 0 or aposta > saldo:
        input("Aposta inválida.")
        continue

    saldo -= aposta

    # Gera o multiplicador onde o avião irá cair
    crash = max(1.00, round(random.expovariate(0.55), 2))

    multiplicador = 1.00

    while True:

        os.system("clear")
        print(f"Saldo: R${saldo:.2f}")
        print()
        print("✈️", end=" ")
        print(f"{multiplicador:.2f}x")
        print()

        if multiplicador >= crash:
            print("💥 O avião caiu!")
            input()
            break

        escolha = input("[ENTER] continuar | [s] sacar: ").lower()

        if escolha == "s":
            premio = aposta * multiplicador
            saldo += premio

            print(f"\nVocê sacou em {multiplicador:.2f}x")
            print(f"Prêmio: R${premio:.2f}")
            input()
            break

        multiplicador += 0.10
        time.sleep(0.05)

print("Game Over!")