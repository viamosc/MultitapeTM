class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}  #Key: symbol tuple, Value: (next, write_symbols, direction)

    def set_next(self, symbols, next, write_symbols, direction):
        self.transitions[symbols] = (next, write_symbols, direction)

    def delta(self, symbols):
        return self.transitions.get(symbols, None)


class MultiTapeTM:
    def __init__(self, q, f, sigma=None, blankSymbol='B', initialTapes=None, initialHeads=None):
        self.q = {state.name: state for state in q}     #name of state: state object
        self.f = f
        self.sigma = sigma or ['0', '1']
        self.blankSymbol = blankSymbol
        self.tape = initialTapes or [
            [self.blankSymbol] * 2 + list("101+001=") + [self.blankSymbol] * 2,  #tape 1
            [self.blankSymbol] * 10,  #tape 2
            [self.blankSymbol] * 10   #tape 3
        ]
        self.tapeHead = initialHeads or [2, 0, 0]  #head positions
        self.current_state = self.q['q0']

    def transition(self):
        #read current symbols from the tape
        # print("states", self.q)
        current_symbols = tuple(self.tape[i][self.tapeHead[i]] for i in range(len(self.tape)))

        #transition logic
        transition = self.current_state.delta(current_symbols)
        if not transition:
            print(f"No valid transition from state {self.current_state.name} with symbols {current_symbols}. Halting...")
            return False

        next, write_symbols, direction = transition

        #write new symbols
        for i in range(len(self.tape)):
            self.tape[i][self.tapeHead[i]] = write_symbols[i]

        #move head
        for i in range(len(self.tape)):
            if direction[i] == 'R':
                self.tapeHead[i] += 1
                if self.tapeHead[i] == len(self.tape[i]):
                    self.tape[i].append(self.blankSymbol)
            elif direction[i] == 'L':
                if self.tapeHead[i] == 0:
                    self.tape[i].insert(0, self.blankSymbol)
                else:
                    self.tapeHead[i] -= 1

        #update current state
        self.current_state = self.q[next]
        return True

    def run(self):
        while self.current_state.name not in self.f:
            print(f"At state {self.current_state.name}, read: {tuple(self.tape[i][self.tapeHead[i]] for i in range(len(self.tape)))}")

            #for each iteration, print the contents of the tape   
            for i, tape in enumerate(self.tape):
                print(f"Tape {i + 1}: {'   |   '.join(tape)}")
            print("\n")

            #run until there is no valid transition
            if not self.transition():      
                break

        print(f"Halting in state {self.current_state.name}.")
        if (self.current_state.name == 'qf'):
            print("Halting in final state")
        else:
            print("Invalid input")
        print("\n")
        
        print("Final tape contents:")
        for i, tape in enumerate(self.tape):
            print(f"Tape {i + 1}: {'   |   '.join(tape)}")


# Create q
q0 = State('q0')
q1 = State('q1')
q2 = State('q2')
q3_0 = State('[q3,0]')
q3_1 = State('[q3,1]')
qf = State('qf')

# Define transitions
q0.set_next(('0', 'B', 'B'), 'q0', ('0', 'B', 'B'), ('R', 'S', 'S'))
q0.set_next(('1', 'B', 'B'), 'q0', ('1', 'B', 'B'), ('R', 'S', 'S'))
q0.set_next(('+', 'B', 'B'), 'q1', ('+', 'B', 'B'), ('R', 'S', 'S'))

q1.set_next(('0', 'B', 'B'), 'q1', ('B', '0', 'B'), ('R', 'R', 'S'))
q1.set_next(('1', 'B', 'B'), 'q1', ('B', '1', 'B'), ('R', 'R', 'S'))
q1.set_next(('=', 'B', 'B'), 'q2', ('B', 'B', 'B'), ('L', 'L', 'S'))

q2.set_next(('B', '0', 'B'), 'q2', ('B', '0', 'B'), ('L', 'S', 'S'))
q2.set_next(('B', '1', 'B'), 'q2', ('B', '1', 'B'), ('L', 'S', 'S'))
q2.set_next(('+', '0', 'B'), '[q3,0]', ('B', '0', 'B'), ('L', 'S', 'S'))
q2.set_next(('+', '1', 'B'), '[q3,0]', ('B', '1', 'B'), ('L', 'S', 'S'))

q3_0.set_next(('0', '0', 'B'), '[q3,0]', ('0', '0', '0'), ('L', 'L', 'L'))
q3_0.set_next(('0', '1', 'B'), '[q3,0]', ('0', '1', '1'), ('L', 'L', 'L'))
q3_0.set_next(('1', '0', 'B'), '[q3,0]', ('1', '0', '1'), ('L', 'L', 'L'))
q3_0.set_next(('1', '1', 'B'), '[q3,1]', ('1', '1', '0'), ('L', 'L', 'L'))

q3_1.set_next(('0', '0', 'B'), '[q3,0]', ('0', '0', '1'), ('L', 'L', 'L'))
q3_1.set_next(('0', '1', 'B'), '[q3,1]', ('0', '1', '0'), ('L', 'L', 'L'))
q3_1.set_next(('1', '0', 'B'), '[q3,1]', ('1', '0', '0'), ('L', 'L', 'L'))
q3_1.set_next(('1', '1', 'B'), '[q3,1]', ('1', '1', '1'), ('L', 'L', 'L'))

q3_0.set_next(('B', 'B', 'B'), 'qf', ('B', 'B', 'B'), ('R', 'R', 'R'))
q3_1.set_next(('B', 'B', 'B'), 'qf', ('B', 'B', 'B'), ('R', 'R', 'R'))

# Add q
q = [q0, q1, q2, q3_0, q3_1, qf]

# Create and run Turing machine
tm = MultiTapeTM(q, f={'qf'})
tm.run()