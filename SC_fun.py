from Compiler import floatingpoint
from Compiler import types
from Compiler import util
from .GC.types import sbit
from Compiler import library
from Compiler import rabbit

from Compiler.library import *

BIT_LENGTH = 64

def conv(x_2):
    """Converts a secret binary value x_2 to a secret arithmatic value x_p.

    This function implements a specific conversion algorithm that involves:
    1. Generating random bits r_p and r_2.
    2. XORing x_2 with r_2.
    3. Opening the result v.
    4. Calculating x_p based on v and r_p.

    Args:
        x_2: The secret value to convert.

    Returns:
        The public value x_p.
    """

    # Generate random bits r_p and r_2
    r_p, r_2 = types.sint.get_dabit()

    # XOR x_2 with r_2
    v_2 = x_2 + r_2

    # Open v_2 and convert to a Cint
    v = types.cint(v_2.reveal())

    # Calculate x_p
    x_p = v + r_p - 2 * v * r_p

    return x_p

def LTBits(R, x):
    """Computes the LTB of a secret value x, a public R.

    Args:
        R: A public value.
        x: A secret value, represented as a list of bits.

    Returns:
        R<?x
    """
    # Decompose R into individual bits
    R_bits = types.cint.bit_decompose(R, BIT_LENGTH)
    # XOR each bit of x with the corresponding bit of R
    y = [x[i].bit_xor(R_bits[i]) for i in range(BIT_LENGTH)]
    # Perform a prefix OR operation on y
    z = floatingpoint.PreOpL(floatingpoint.or_op, y[::-1])[::-1] + [0]
    # Calculate the difference between consecutive elements of z
    w = [z[i] - z[i + 1] for i in range(BIT_LENGTH)]
    # Sum the results for each bit where the corresponding R_bit is 0
    return sum((1 - R_bits[i]) & w[i] for i in range(BIT_LENGTH))

def LTS(a, b, k):
    """
    A protocol to compute the Least Than Secret (LTS) of two secret values.

    This protocol determines if secret value `a` is less than secret value `b`.

    Args:
        a: The first secret value.
        b: The second secret value.
        k: The bit length for secure computations.

    Returns:
        The LTS result, which is 1 if a < b, and 0 otherwise.
    """
    
    # Step 1: Generate a random k-bit value 'r' with the most significant bit set to 1
    r, rbits = types.sint.get_edabit(k, True)

    # Step 2: Compute 'c' as 2 * (a - b)
    c = 2 * (a - b)

    # Step 3: Compute 'eta' as 'c + r', open it, and add 1
    eta = (c + r).reveal() + 1

    # Decompose 'eta' into its bit representation
    eta_bits = sbit.bit_decompose_clear(eta, k)

    # Compute the number of bits set to 1 in 'eta' masked by 'r'
    h = LTBits(eta, rbits)

    # Calculate 'e0', the XOR of the most significant bits of 'eta_bits' and 'r_bits'
    e0 = util.bit_xor(eta_bits[k-1], rbits[k-1])

    # Compute the final result based on 'h' and 'e0'
    result = (1 - h) * e0 + h * (1 - e0)

    return result

def ReLU(a, k):
    """
    A protocol to compute the ReLU (Rectified Linear Unit) of a secret value.

    This protocol implements the ReLU function, which outputs the input if it's
    positive and 0 if it's negative.

    Args:
        a: The secret value.
        k: The bit length for secure computations.

    Returns:
        The ReLU result, which is a if a >= 0, and 0 otherwise.
    """
    
    # Step 1: Generate a random k-bit value 'r' with the most significant bit set to 1
    r, rbits = types.sint.get_edabit(k, True)

    # Step 2: Compute 'c' as 2 * a
    c = 2 * a

    # Step 3: Compute 'eta' as 'c + r', open it, and add 1
    eta = (c + r).reveal() + 1

    # Decompose 'eta' into its bit representation
    eta_bits = sbit.bit_decompose_clear(eta, k)

    # Compute the number of bits set to 1 in 'eta' masked by 'r'
    h = rabbit.LTBits(eta, rbits)

    # Calculate 'e0', the XOR of the most significant bits of 'eta_bits' and 'r_bits'
    e0 = util.bit_xor(eta_bits[k-1], rbits[k-1])

    # Compute the final result based on 'h' and 'e0'
    result = (1 - h) * e0 + h * (1 - e0)

    # Multiply the result by 'a' to get the ReLU output
    w_p = conv(1-result) * a

    return w_p