
from CSP.CSP_Agent import *
import Parse
from QLearningAgent import chord
from QLearningAgent import musicGUI
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
    cspAgent = CspAgent(board)
    makeOutputCsp(cspAgent)
    parser = Parse.parse_notes('csp_result.txt')
    G_chord = chord.Chord('G', 'B', 'D', 'G')
    C_chord = chord.Chord('C', 'E', 'G', 'C')
    D_chord =chord.Chord('D', 'A', 'g', 'D')
    EM_chord = chord.Chord('E', 'B', 'G', 'Em')
    chord_progression = [G_chord, C_chord, D_chord, EM_chord]
    player = musicGUI.musicPlayer(chord_progression, 1, 0.9, 0.2)
    player.runTraining(10000)
    player.run()
    Parse.parse_notes('rr')