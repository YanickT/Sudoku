import numpy as np
import functools


def mark(tensor, number, y, x):
    """
    Set a lattice place to 1 and all referring positions to 0
    :param tensor: np.array (3D) = sudoku-Tensor
    :param number: int = number to set
    :param y: int = vertical position to set on a 2D sudoku-field
    :param x:
    :return:
    """
    # close position for all numbers
    tensor[:, y, x] = 0
    # close all vertical positions for this number
    tensor[number, :, x] = 0
    # close all horizontal positions for this number
    tensor[number, y, :] = 0

    # close number for block
    y_block = (y // 3) * 3
    x_block = (x // 3) * 3
    tensor[number, y_block:y_block + 3, x_block:x_block + 3] = 0

    # set number to its place
    tensor[number, y, x] = 1


def to_array(sudoku):
    """
    Convert 2D sudoku into a 3D tensor containing {-1, 0, 1}.
    These states mean:
    0: Place is closed
    1: Place is set
    -1: Place is yet unknown
    :param sudoku: List[List[int]] = Sudoku-field
    :return: np.array (3d) = 3D tensor of the Sudoku-field
    """
    tensor = np.zeros([9, 9, 9], dtype=np.int8)
    tensor.fill(-1)
    for y, row in enumerate(sudoku):
        for x, slot in enumerate(row):
            if slot is not None:
                mark(tensor, slot - 1, y, x)
    return tensor


def grid_solve(tensor):
    """
    Try to solve the sudoku-tensor
    :param tensor: np.array (3D) = sudoku-tensor
    :return: np.array(3D) = solved sudoku-tensor
    """
    change = True
    while change:
        change = False
        spaces = np.where(tensor == -1)
        spaces = zip(*spaces)
        for space in spaces:
            if tensor[space] == -1:
                # set state to 0 to check other states without its influence
                tensor[space] = 0

                # check if space is needed to be 1 for horizontal line
                result_h = functools.reduce(lambda x, y: x | y, tensor[space[0], space[1], :])
                if result_h != -1:
                    change = True
                    mark(tensor, *space)
                    continue

                # check if space is needed to be 1 for vertical line
                result_v = functools.reduce(lambda x, y: x | y, tensor[space[0], :, space[2]])
                if result_v != -1:
                    change = True
                    mark(tensor, *space)
                    continue

                # check if space is needed to be 1 for block
                y_block = (space[1] // 3) * 3
                x_block = (space[2] // 3) * 3
                result_b = functools.reduce(lambda x, y: x | y,
                                            np.nditer(tensor[space[0], y_block:y_block + 3, x_block:x_block + 3]))
                if result_b != -1:
                    change = True
                    mark(tensor, *space)
                    continue

                # check if space is needed to be 1 for the space itself (only possible solution)
                result_d = functools.reduce(lambda x, y: x | y, tensor[:, space[1], space[2]])
                if result_d != -1:
                    change = True
                    mark(tensor, *space)
                    continue

                # if others do not need space to be 1 add its influence back to the tensor
                tensor[space] = -1
    return tensor


def check(tensor):
    """
    Checks if the given sudoku-tensor is a valid one.
    :param tensor: np.array (3d) = sudoku-tensor
    :return: bool = validity of the sudoku-tensor
    """
    for number in range(0, 9):
        for counter in range(0, 9):
            y_block = (counter // 3) * 3
            x_block = (counter % 3) * 3

            result_h = functools.reduce(lambda x, y: x | y, tensor[number, counter, :])
            result_v = functools.reduce(lambda x, y: x | y, tensor[number, :, counter])
            result_b = functools.reduce(lambda x, y: x | y,
                                        np.nditer(tensor[number, y_block:y_block + 3, x_block:x_block + 3]))

            if not all([result in [-1, 1] for result in [result_h, result_v, result_b]]):
                return False
    return True


def solve(tensor):
    """
    Solve the given sudoku
    :param tensor: np.array (3D) = sudoku-tensor
    :return: np.array (3D) = solved sudoku-tensor
    """
    # check if the tensor is valid
    if not check(tensor):
        return False

    # try to solve tensor
    grid_solve(tensor)

    # check if there are no positions left in the tensor
    if not -1 in tensor:
        return tensor

    # determine open positions
    spaces = np.where(tensor == -1)
    spaces = zip(*spaces)

    # try to close every possible space (hypothesis test)
    for space in spaces:
        cur_tensor = np.copy(tensor)
        mark(cur_tensor, *space)
        # recursive call of solve
        cur_tensor = solve(cur_tensor)
        if check(cur_tensor) is False:
            continue
        else:
            return cur_tensor

    raise Exception("Can´t solve Sudoku")


def translate(tensor):
    """
    Transform the given 3D sudoku-tensor back to a 2D sudoku-field
    :param tensor: np.array (3D) = sudoku-tensor
    :return: List[List[int]] = 2D sudoku-field
    """
    field = np.zeros([9, 9], dtype=np.int8)
    for number in range(0, 9):
        field += tensor[number] * (number + 1)
    field = field.tolist()
    return field


def run_solver(sudoku):
    """
    Prepare tensor to solve sudoku.
    :param sudoku: List[List[int]] = sudoku-field
    :return: List[List[int]] = solved sudoku-field
    """
    tensor = to_array(sudoku)
    solved = solve(tensor)
    return translate(solved)
