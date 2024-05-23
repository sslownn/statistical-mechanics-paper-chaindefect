import random
import math
import re
from pathlib import Path

class Position:
    def __init__(self):
        self.DefectType = []  # define defect types
        self.Type = []  # define type value from 0 to 7 starting from 0 degree to 315 degree, spacing 45 degree
        self.FirstNeighbours = []  # save the index of first neighbours
        self.SecondNeighbours = []  # save the second neighbours
        self.X = []
        self.Y = []
        self.N = 0
        self.eij = 0
        self.eik = 0
        self.SweepsPerFrame = 0
        self.Frames = 0
        self.Energy = 0
        self.First_Neighbour_Corr = 0
        self.Second_Neighbour_Corr = 0
        self.count = True
        self.Fbond = False
        self.Sbond = False

FN = []
SN = []

def Init(P, sideN, FN, SN):
    sideN = 0
    P.SweepsPerFrame = 100
    P.Frames = 30000
    # 初始化其他属性的代码

    with open ("Input.txt", "r") as file:
        sideN, eij, eik, SweepsPerFrame, Frames = file.readline().split()
        sideN = int(sideN)
        P.eij = float(eij) / 1000  # 将读取的值除以1000，得到0.005
        P.eik = float(eik) / 1000  # 同样将读取的值除以1000，得到0.005
        P.SweepsPerFrame = int(SweepsPerFrame)
        P.Frames = int(Frames)

    print("The size of square lattice is", sideN)
    P.N = 2 * sideN * sideN

    for i in range(sideN):
        for j in range(sideN):
            P.X.append(i)
            P.Y.append(j)
            t = random.randint(0, 7)
            P.Type.append(t)
            P.DefectType.append(0)
            print(i, j, t)

            fn = [2 * (i * sideN + j) + 1, 2 * (((i - 1 + sideN) % sideN) * sideN + j) + 1,
                  2 * (((i - 1 + sideN) % sideN) * sideN + (j - 1 + sideN) % sideN) + 1,
                  2 * (i * sideN + (j - 1 + sideN) % sideN) + 1]
            P.FirstNeighbours.append(fn)

            sn = [2 * (((i + 1) % sideN) * sideN + j), 2 * (i * sideN + (j + 1) % sideN),
                  2 * (((i - 1 + sideN) % sideN) * sideN + j), 2 * (i * sideN + (j - 1 + sideN) % sideN)]
            P.SecondNeighbours.append(sn)

            P.X.append(i + 0.5)
            P.Y.append(j + 0.5)
            t = random.randint(0, 7)
            P.Type.append(t)
            P.DefectType.append(1)

            fn = [2 * (((i + 1) % sideN) * sideN + (j + 1) % sideN), 2 * (i * sideN + (j + 1) % sideN),
                  2 * (i * sideN + j), 2 * (((i + 1) % sideN) * sideN + j)]
            P.FirstNeighbours.append(fn)

            sn = [2 * (((i + 1) % sideN) * sideN + j) + 1, 2 * (i * sideN + (j + 1) % sideN) + 1,
                  2 * (((i - 1 + sideN) % sideN) * sideN + j) + 1, 2 * (i * sideN + (j - 1 + sideN) % sideN) + 1]
            P.SecondNeighbours.append(sn)

def CalculateEnergy(P, Index):
    TypeSelf = P.Type[Index]
    Energy = 0

    if TypeSelf % 2 == 1:
        if (TypeSelf + 4) % 8 == P.Type[P.FirstNeighbours[Index][TypeSelf // 2 - 1]]:
            P.Fbond = True
            Energy -= P.eij
        else:
            P.Fbond = False
    else:
        if (TypeSelf + 4) % 8 == P.Type[P.SecondNeighbours[Index][TypeSelf // 2 - 1]]:
            P.Sbond = True
            Energy -= P.eik
        else:
            P.Sbond = False

    P.First_Neighbour_Corr = 0
    for i in range(len(P.FirstNeighbours[Index])):
        sigma = math.cos(P.Type[P.FirstNeighbours[Index][i]] * math.pi / 4 - TypeSelf * math.pi / 4)
        P.First_Neighbour_Corr += sigma

    P.Second_Neighbour_Corr = 0
    for i in range(len(P.SecondNeighbours[Index])):
        sigma = math.cos(P.Type[P.SecondNeighbours[Index][i]] * math.pi / 4 - TypeSelf * math.pi / 4)
        P.Second_Neighbour_Corr += sigma

    return Energy

def Update(P, Index):
    Old_Type = P.Type[Index]
    Old_Energy = CalculateEnergy(P, Index)

    dType = random.randint(0, 1)
    P.Type[Index] = (P.Type[Index] + dType) % 8
    New_Energy = CalculateEnergy(P, Index)

    rand_num = random.random()
    if rand_num < math.exp(-(New_Energy - Old_Energy)):
        P.Energy += (New_Energy - Old_Energy)
        P.count = True
    else:
        P.Type[Index] = Old_Type
        P.count = False


if __name__ == "__main__":
    P = Position()
    sideN = 16
    Init(P, sideN, FN, SN)

    Energy = 0
    for i in range(len(P.Type)):
        Energy += CalculateEnergy(P, i)
    P.Energy = Energy / 2

    with open("Output.xyz", "w") as Pointer, open("Fraction.txt", "w") as Pointer1, open("AutoCorrelation.txt", "w") as Pointer2, open("EnergyIteration.txt","w")as Pointer3:
        Pointer.write(f"{P.N}\nAtoms. Timestep = 0. Energy = {P.Energy}\n")
        for i in range(P.N):
            Pointer.write(f"{P.DefectType[i]}  {P.X[i]}  {P.Y[i]}  {math.cos(P.Type[i] * math.pi / 4)}  {math.sin(P.Type[i] * math.pi / 4)}\n")

        print(f"Initial energy is {Energy}")

        for i in range(P.Frames):
            count = 0
            for j in range(P.SweepsPerFrame):
                for k in range(P.N):
                    Index = random.randint(0, P.N - 1)
                    Update(P, Index)
                    if P.count:
                        count += 1

            print(f"Acceptance rate is {count / P.N / P.SweepsPerFrame}")
            print(f"Energy is {P.Energy}")
            Pointer3.write(f"{P.Energy}\t{count / P.N / P.SweepsPerFrame}\n")
            Pointer.write(f"{P.N}\nAtoms. Timestep = {i + 1}. Energy = {P.Energy}\n")
            count_ij = count_ik = count_vacancy = 0
            First_Neighbour_Corr = Second_Neighbour_Corr = 0
            vx = []
            vy = []
            for j in range(P.N):
                Pointer.write(f"{P.DefectType[j]}  {P.X[j]}  {P.Y[j]}  {math.cos(P.Type[j] * math.pi / 4)}  {math.sin(P.Type[j] * math.pi / 4)}\n")
                dE = CalculateEnergy(P, j)
                First_Neighbour_Corr += P.First_Neighbour_Corr
                Second_Neighbour_Corr += P.Second_Neighbour_Corr
                vx.append(math.cos(P.Type[j] * math.pi / 4))
                vy.append(math.sin(P.Type[j] * math.pi / 4))

                if P.Fbond:
                    count_ij += 1
                if P.Sbond:
                    count_ik += 1
                if not P.Sbond and not P.Fbond:
                    count_vacancy += 1
                P.Fbond = False
                P.Sbond = False

            Pointer1.write(f"{count_ij / 2}  {count_ik / 2}  {count_vacancy}  {-First_Neighbour_Corr / P.N}  {-Second_Neighbour_Corr / P.N}\n")
            Pointer.flush()
            Pointer3.flush()
            Pointer1.flush()

        for i in range(P.Frames // 3):
            auto_corr = 0
            for j in range(P.Frames // 3, 2 * (P.Frames // 3)):
                for k in range(P.N):
                    auto_corr += vx[j][k] * vx[j + i][k] + vy[j][k] * vy[j + i][k]
            Pointer2.write(f"{auto_corr / (P.N * (P.Frames // 3) + 1)}\n")
    Pionter2.close()