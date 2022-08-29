
from CSP.CSP_Agent import *


def makeOutputCsp(agent):
    result = agent.getSolution()
    root_chords = agent.getChordInformation()

    f = open("csp_result.txt", "w")
    if result is False:
        f.write("False")
        f.close()
        return

    bar_counter = 0
    for bar in result:
        bit_counter = 0
        for bit in bar:
            f.write(root_chords[bar_counter])
            f.write("/")
            f.write(bit)
            if bit_counter != 3:
                f.write(",")
            bit_counter += 1
        f.write("\n")
        bar_counter += 1
    f.close()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = input("type chord progressions\n")
    board = board(inputs)
    agent = CspAgent(board)
    makeOutputCsp(agent)