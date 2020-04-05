"""
An Iterative and recursive algorithm to solve the Towers of Hanoi Puzzle
Created by Nihad Kalathingal on 4/4/2020. Modified (04-04-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4306 Algorithm Ananlysis 04
    Programming Project: Algorithms, Implementation & Analysis
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
"""

# Modules used
import time  # used to time algorithms
import matplotlib.pyplot as plt  # Used to plot time taken
import sys  # used to retrieve CLI arguments
import pandas as pd  # Used to record data


def recursive_tower_of_hanoi(n: int, source_rod: list,
                             dest_rod: list, aux_rod: list) -> int:
    """Recursive solution to the Tower of Hanoi Puzzle. Based on an
    implementation from An Introduction to the Design and Analysis of
    Algorithms by Anany Levitin.
    Arguments:
        n {int} -- number of disks
        source_rod {list} -- source tower
        dest_rod {list} -- destination tower
        aux_rod {list} -- auxillary tower
    Returns:
        int -- count of moves
    """
    # if there is at least one disk to move
    if n > 0:
        # move n-1 disks from source to aux
        moves1 = recursive_tower_of_hanoi(n-1, source_rod, aux_rod, dest_rod)
        # move one disk from source disk to destination
        if source_rod:
            dest_rod.append(source_rod.pop())
            moves1 += 1
        # move disks from aux to dest
        moves2 = recursive_tower_of_hanoi(n-1, aux_rod, dest_rod, source_rod)
        # moves1 + moves2 were made
        return moves1+moves2
    # otherwise 0 moves are made
    return 0


def move_disk(source_rod: list, dest_rod: list) -> None:
    """ Helper function for the iterative solution to the TOH problem which
    implements the movement of disks between two rods/towers.
    Arguments:
        source_rod {list} -- source tower
        dest_rod {list} -- destination tower
    """
    # source is empty
    if len(source_rod) == 0:
        source_rod.append(dest_rod.pop())
    # destination is empty
    elif len(dest_rod) == 0:
        dest_rod.append(source_rod.pop())
    else:
        # both are non-empty
        # get elements on top of stack
        src_item = source_rod[-1]
        dest_item = dest_rod[-1]

        # source top is bigger than dest top
        if src_item > dest_item:
            source_rod.append(dest_rod.pop())
        # dest top is bigger than src top
        else:
            dest_rod.append(source_rod.pop())


def is_valid_rod(rod: list) -> bool:
    """Checks if a given tower is valid. As a tower is implemented as a list,
    the last element in the list is the top and each element below should be
    larger.
    Arguments:
        rod {list} -- a tower
    Returns:
        bool -- valid or not
    """
    if len(rod) == 0:
        return True
    previous = rod[0]
    for disk in rod[1:]:
        if disk > previous:
            return False
    return True


def iterative_tower_of_hanoi(n, source_rod: list,
                             dest_rod: list, aux_rod: list) -> int:
    """Iterative implementation a solution to TOH problem based on:
       @article{10.1145/948566.948573,
                author = {Mayer, Herbert and Perkins, Don},
                title = {Towers of Hanoi Revisited a Nonrecursive Surprise},
                year = {1984},
                issue_date = {February 1984},
                publisher = {Association for Computing Machinery},
                address = {New York, NY, USA},
                volume = {19},
                number = {2},
                issn = {0362-1340},
                url = {https://doi.org/10.1145/948566.948573},
                doi = {10.1145/948566.948573},
                journal = {SIGPLAN Not.},
                month = feb,
                pages = {80–84},
                numpages = {5}
            }
    Arguments:
        n {int} -- number of disks
        source_rod {list} -- source tower
        dest_rod {list} -- destination tower
        aux_rod {list} -- auxillary tower
    Returns:
        int -- count of moves
    """
    # number of moves to make
    total_moves = 2**n - 1
    # iterate through all moves
    for i in range(1, total_moves+1):
        # first move
        if i % 3 == 1:
            move_disk(source_rod, dest_rod)
        # second move
        elif i % 3 == 2:
            move_disk(source_rod, aux_rod)
        # third move
        elif i % 3 == 0:
            move_disk(aux_rod, dest_rod)
    # return total moves
    return total_moves


def test_iterative(n_max: int) -> None:
    """Tests the iterative TOH algorithm with upto n_max disks. Outputs a csv
    file and a graph of the input size vs the time elapsed in seconds.
    Arguments:
        n_max {int} -- max number of disks to run algorithm on
    """
    # all ns to test disk for
    n_disks = range(1, n_max+1)
    # n_disks = [6, 10, 20, 50, 100]

    # dataframe for storing values
    df = pd.DataFrame(columns=["Number of Disk(s)",
                               "Time Elapsed (s)",
                               "Move(s)"])
    # x and y labels for the plot
    plt.title("Iterative Towers of Hanoi Algorithm")
    plt.ylabel('Time taken (s)')
    plt.xlabel("Number of disks")

    # do all Ns in n-disks
    for i, n in enumerate(n_disks):
        src = list(reversed(range(1, n+1)))
        dest = []
        aux = []
        assert is_valid_rod(src) and is_valid_rod(dest) and is_valid_rod(aux)
        # time it
        start = time.time()
        moves = iterative_tower_of_hanoi(n, src, dest, aux)
        time_taken = time.time() - start
        assert is_valid_rod(src) and is_valid_rod(dest) and is_valid_rod(aux)
        time_taken = round(time_taken, 5)
        df.loc[i] = [n, time_taken, moves]
        df.to_csv("iterative_toh.csv")
        print(df)
        # print("{0} disks took {1} (s) and {2} moves".format(n,
        #                                                     time_taken,
        #                                                     moves))
        plt.plot(df["Number of Disk(s)"], df["Time Elapsed (s)"])
        plt.pause(0.05)
        plt.savefig("iterative_toh.png")
    plt.show()


def test_recursive(n_max: int) -> None:
    """Tests the recursive TOH algorithm with upto n_max disks. Outputs a csv
    file and a graph of the input size vs the time elapsed in seconds.
    Arguments:
        n_max {int} -- max number of disks to run algorithm on
    """
    # all ns to test disk for
    n_disks = range(1, n_max+1)
    # n_disks = [6, 10, 20, 50, 100]

    # dataframe for storing values
    df = pd.DataFrame(columns=["Number of Disk(s)",
                               "Time Elapsed (s)",
                               "Move(s)"])
    # x and y labels for the plot
    plt.title("Recursive Towers of Hanoi Algorithm")
    plt.ylabel('Time taken (s)')
    plt.xlabel("Number of disks")

    # do all Ns in n-disks
    for i, n in enumerate(n_disks):
        src = list(reversed(range(1, n+1)))
        dest = []
        aux = []
        # check if all rods are valid per TOH rules
        assert is_valid_rod(src) and is_valid_rod(dest) and is_valid_rod(aux)
        # time it
        start = time.time()
        moves = recursive_tower_of_hanoi(n, src, dest, aux)
        time_taken = time.time() - start
        assert is_valid_rod(src) and is_valid_rod(dest) and is_valid_rod(aux)
        time_taken = round(time_taken, 5)
        df.loc[i] = [n, time_taken, moves]
        df.to_csv("recursive_toh.csv")
        print(df)
        # print("{0} disks took {1} (s) and {2} moves".format(n,
        #                                                     time_taken,
        #                                                     moves))
        plt.plot(df["Number of Disk(s)"], df["Time Elapsed (s)"])
        plt.pause(0.05)
        plt.savefig("recursive_toh.png")
    plt.show()


def main():
    """Main function that runs both tests with n_max equal to the first CLI
    argument (defualts to 6 if none provided). To run the script with the
    python interpreter:

        python3 hanoi.py <num_max>

    For example:

        python3 hanoi.py 25
    """
    # parse the first CLI arguments
    try:
        n_max = int(sys.argv[1])
    except IndexError:
        # if none set defualt
        n_max = 6
    # test the recursive implementation
    test_recursive(n_max)
    # test the iterative implementation
    test_iterative(n_max)


if __name__ == "__main__":
    main()
