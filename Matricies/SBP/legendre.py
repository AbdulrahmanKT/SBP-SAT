

import numpy as np 
import matplotlib.pyplot as plt 
import sympy as sp


def p_n(x,n): 
    """
     This is a function that returns the nth order legendre polynomial evaluated at the point x, with order n.

     x: is the point of evaluation 
     n: is the order of the Legendre polynomial

    """
    if n == 0:
        return 1
    
    if n == 1:
        return x
    
    p = np.zeros(n+1)
    p[0] = 1
    p[1] = x
    for i in range(2,n+1):
        p[i] = ((2*i-1)*x*p[i-1]-(i-1)*p[i-2])/i
        
    return p[-1]



def legplot(f,n,*args):
    
    """
    This is a function that uses the matplotlib library. Where f is a function 
    handle which should a Legndre Polynomial or a derivative of a polynomial, n is 
    the order of that polynomial. 
    The function will plot all polynomials up to n. 

    f: Function handle
    n: order of such polynomial
    args: the left and right bounds of the interval of evaluation

    ** Each function uses 5000 evaluations 
    """
    plt.figure
    print(args)
    if len(args)==0:
        points = np.linspace(-1,1,5000)
    else: 
        [left,right] = [*args[0]]
        points = np.linspace(left,right,5000)
    plt.plot(points,np.zeros(5000),".")
    for i in range(n): 
        poly = [f(c,i) for c in points]
        plt.plot(points,poly,label = "n = " + str(i))
    
    
    if len(args) > 1 and isinstance(args[1], str):
        title = args[1]
        plt.title("Plot of the " +title + " up to n")
    else: 
        plt.title("Plot of the polynomials up to n")

    plt.show()
    plt.legend()
    plt.grid()


    



def dp_n(x,n): 
    
    """ This is a function that returns the first derivative of the nth order 
    legendre polynomial evaluated at the point x. 

    x: point of evaluation 
    n: is the order of the polynomial 
    
    """
    if n == 0:
        return 0
    
    if n == 1:
        return 1
    else:
        p = np.zeros(n+1)
        p[0] = 0
        p[1] = 1
        for i in range(2,n+1):
            p[i] = i*(x*p_n(x,i)-p_n(x,i-1))/(x**2 -1) # From the Bonnet Formula 
    return p[-1]



def p_n_c(n): 
    """
    Generates the coefficients of the Legendre polynomial of degree n.
    Returns the coefficients as a list, from the highest degree to the lowest.
    """

    x = sp.symbols("x")  # Symbols are used to eventually extract the coefficients


    if n == 0: 
        return [1]
    
    if n == 1: 
        return [0, 1]
    if n < 0: 
        raise ValueError("n cannot be negative, it is a natural number!!!")
    else:
        size = n + 1
        p = sp.zeros(size,1)
        p[0] = 1
        p[1] = 1*x 

        for i in range(2,n+1):
            p[i] = sp.simplify((((2*i - 1)* x * p[i-1]) - (i-1)*p[i-2])/i)
        out = sp.Poly(p[-1], x)
        out = out.all_coeffs()


    return out


def dp_n_c(n):
    """
    Generates the coefficients of the derivative of the Legendre polynomial of degree n.
    """
    x = sp.symbols("x")

    if n == 0:
        return 0
    
    if n == 1:
        return [1, 0]
    else:
        size = n + 1
        p = sp.zeros(size,1)
        p_prime = sp.zeros(size,1)

        ## From Bonnet's formula, one requires the legendre polynomials in order to 
        ## calculate the derivative. 
        p[0] = 1
        p[1] = 1*x 
        for i in range(2,n+1):
            p[i] = (((2*i - 1)* x * p[i-1]) - (i-1)*p[i-2])/i




        p_prime[0] = 0
        p_prime[1] = 1
        for i in range(2,n+1):
            p_prime[i] = sp.simplify(i*(x*p[i]-p[i-1])/(x**2 -1)) # From the Bonnet Formula

        out = sp.Poly(p_prime[-1], x)
        out = out.all_coeffs()
        
    return out


def lgl(n): 
    """
    This is a function that takes n as an argument. n is the polynomial order.
    It calculates the weights of the nth order Legendre-Gauss-Lobatto
    points (LGL) and the roots. Output = [roots_dp, weights] 
    """
    dp = dp_n_c(n) # generates the coefficients of the dp/dx polynomial. 
    roots_dp = np.array(np.roots(dp)) # solves for the roots of the dp/dx polynomial (the Absiccas)
    w = np.zeros(n+1)
    w[0] = 2/(n*(n+1))
    w[-1] = w[0]
    roots_dp = sorted(roots_dp)
    if n > 2: 
        for i in range(1,n):
            w[i] = w[0]*(1/(p_n(roots_dp[i-1],n))**2)
    out = np.zeros(n+1)
    out[0] = -1
    out[-1] = 1
    out[1:-1] = roots_dp
    
    return np.matrix([out,w])

def lagrange(n,x): 
    """
    This function creates a vector of lagrange polynomials that interpolate a unitary polynomial through the 
    Legendre-Gauss-Lobatto points. 
    n - order of the polynomial, which means n + 1 points. 
    The output will be a vector evaluated at the n LGL points. 
    """
    points = lgl(n) # uses the previous function to generate the roots and the weights
    roots = np.zeros(n+1)
    roots[:] = points[0,:]

    w = np.zeros(n+1)
    w[:] = points[1,:]

    l = np.ones(n+1) # initalization of the vector
    for i in range(n+1): 
        for j in range(n+1): 
            if j != i:
                l[i] = l[i]*(x-roots[j])/((roots[i]-roots[j]))
    return l


def dlagrange(n, *args): 
    """
    This function takes in the degree of the lagrange polynomial - n along with a collocation point - x. 
    The output is a matrix that satifies the SBP property for differentiation. 
    """
    points = lgl(n) # uses the previous function to generate the roots and the weights
    roots = np.zeros(n+1)
    roots[:] = points[0,:]


    if len(args) == 1: # This is to add a custom range of values (domain different than [-1,1]). Note: The negative number is because lgl(n) is defined from small to big. 
        jacob = args[0]
    else: 
        jacob = -1
    w = np.zeros(n+1)
    w[:] = points[1,:]
    dl = np.zeros((n+1,n+1))
    prod = 1 # Just to save the intermediate steps of multiplication 
    for i in range(n+1): # Note, since there are 2 exclusions (from the definition of the derivative of the lagrange polynomials)
        for k in range(n+1):
            if k != i: 
                prod = 1
                for j in range(n+1): 
                    if j!= i and j!= k: 
                        prod= prod*(roots[i]-roots[j])/((roots[k]-roots[j]))
                dl[i,k] = prod*(1/(roots[i] - roots[k]))
 
        
    for i in range(n+1):
        dl[i, i] = jacob*np.sum(dl[i, :])  # since off-diagonals sum to -D_ii
    return -1*dl



def Vmonde(n, *args):
    """
    This function generates a vandermonde matrix of order nxn. This matrix uses the monomials as its basis, 
    and they are evaluated at the LGL points.

    Note: NOT YET IMPLIMENTED!!
    There are different basis implimented: 
        - *args = none, this function will use the default monomial basis. 
        - *args = p, will use the Legendre Polynomials
        - *args = l, will use the Lagrange Interpolating Polynomials
    """
    
    x = np.zeros(n)
    out = lgl(n-1)
    x[:] = out[0,:]
    V = np.zeros((n,n))


    #if args == "l":
    #    raise ValueError("The Vandermonde with Lagrange Basis has not been implimented yet")
    #if args == "p":
    #    raise ValueError("The Vandermonde with Legendre Polynomial Basis has not been implimented yet")
    #else:
    for j in range(n):
        V[j,:] = [x[j]**i for i in range(n)]
    return V

def sbp_d(n): 

    """
    Generates the differentiation matrix D of size n + 1 by n + 1. Where n is the degree of the solution
    """
    D = dlagrange(n)
    return D 