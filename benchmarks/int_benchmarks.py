from RamseyQuantors.shortcuts import *
from RamseyQuantors.environment import push_ramsey

push_ramsey()
get_env().enable_infix_notation = True


def int_vector(name, dim):
    return [Symbol(f"{name}_{i}", INT) for i in range(dim)]

def benchmark_half_int(dim: int, bound: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    f = And([And(Times(Int(2), y[i]) <= x[i], x[i] >= Int(bound)) for i in range(dim)])
    return Ramsey(x, y, f)

def benchmark_equal_exists_int(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    z = int_vector("c", dim)

    f = And([And(x[i] < y[i], Equals(x[i], z[i])) for i in range(dim)])

    return Ramsey(x, y, Exists(z, f))

def benchmark_equal_exists_2_int(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    z = int_vector("c", dim)

    f = And([And(x[i] < y[i], And(x[i] <= z[i], x[i] >= z[i])) for i in range(dim)])

    return Ramsey(x, y, Exists(z, f))

def benchmark_equal_free_int(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    z = int_vector("c", dim)

    f = And([And(x[i] < y[i], Equals(x[i], z[i])) for i in range(dim)])

    return Ramsey(x, y, f)

def benchmark_equal_free_2_int(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    z = int_vector("c", dim)

    f = And([And(x[i] < y[i], And(x[i] >= z[i], x[i] <= z[i])) for i in range(dim)])

    return Ramsey(x, y, f)

def benchmark_dickson_int(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)

    f = And([x[i] >= 0 for i in range(dim)])
    g = And(Or([y[i] < x[i] for i in range(dim)]),And([y[i] <= x[i] for i in range(dim)]))
    g = Or(g,And(Or([y[i] < x[i] for i in range(dim)]),Or([x[i] < y[i] for i in range(dim)])))
    f = And(f,g)

    return Ramsey(x, y, f)


# These should all have an infinite clique:
def benchmark_congruence_mod_m(dim: int, m: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    k = [Symbol(f"k_{i}", INT) for i in range(dim)]
    f = And([Equals(x[i] - y[i] - m * k[i], Int(0)) for i in range(dim)])
    return Ramsey(x, y, Exists(k, f))

def benchmark_sum_even(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = [Symbol(f"t_{i}", INT) for i in range(dim)]
    f = And([And(Equals(x[i] + y[i] - Int(2) * t[i], Int(0)), NotEquals(x[i], y[i])) for i in range(dim)])
    return Ramsey(x, y, Exists(t, f))

def benchmark_diff_in_kZ(dim: int, k: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = Symbol("t", INT)
    f = Equals(x[0] - y[0] - k * t, Int(0))
    return Ramsey(x, y, Exists([t], f))

def benchmark_sum_eq_C(dim: int, C: int):
    assert dim == 2, "Dimension must be 2"
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    f = And(Equals(x[0] + x[1] - Int(C), Int(0)), Equals(y[0] + y[1] - C, Int(0)))
    return Ramsey(x, y, f)

def benchmark_dot_product_zero(dim: int, v_coeffs: list):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = Symbol("t", INT)
    dot_x = Plus(x[i] * v_coeffs[i] for i in range(dim))
    dot_y = Plus(y[i] * v_coeffs[i] for i in range(dim))
    f = And(Equals(dot_x - dot_y - t, Int(0)), Equals(t, Int(0)))
    return Ramsey(x, y, Exists([t], f))

def benchmark_sum_zero_hyperplane(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    delta = [Symbol(f"delta_{i}", INT) for i in range(1, dim)]
    eq1 = Equals(y[0] - x[0] - Plus(delta), Int(0))
    eqs = [Equals(y[i] - x[i] + delta[i-1], Int(0)) for i in range(1, dim)]
    f = And(eq1, *eqs)
    return Ramsey(x, y, Exists(delta, f))

def benchmark_diff_set(dim: int, D: list):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    or_terms = []
    for d in D:
        term1 = And([Equals(x[i] - y[i], Int(d_i)) for i, d_i in enumerate(d)])
        term2 = And([Equals(y[i] - x[i], Int(d_i)) for i, d_i in enumerate(d)])
        or_terms.append(Or(term1, term2))
    f = Or(or_terms)
    return Ramsey(x, y, f)

def benchmark_scheduling_overlap(dim: int):
    assert dim == 2, "Dimension must be 2"
    x = int_vector("a", dim)  # x = (s1, d1)
    y = int_vector("b", dim)  # y = (s2, d2)
    constraints = And(x[0] >= Int(0), x[1] >= Int(1), y[0] >= Int(0), y[1] >= Int(1))
    overlap = And(x[0] + x[1] > y[0], y[0] + y[1] > x[0])
    f = And(constraints, overlap)
    return Ramsey(x, y, f)

# def benchmark_multi_resource_scheduling(dim: int, n_resources: int):
#     assert dim == n_resources + Int(2), "dim must be n_resources + Int(2)"
#     x = int_vector("a", dim)  # (s1, d1, r1_1, ..., r1_{n_resources})
#     y = int_vector("b", dim)  # (s2, d2, r2_1, ..., r2_{n_resources})
#     constraints = And(
#         x[0] >= Int(0), x[1] >= Int(1), y[0] >= Int(0), y[1] >= Int(1),
#         And([x[i] >= Int(1) for i in range(Int(2), dim)]),
#         And([y[i] >= Int(1) for i in range(Int(2), dim)])
#     )
#     overlap = And(x[0] + x[1] > y[0], y[0] + y[1] > x[0])
#     resource_eq = Or([Exists([Symbol("t", INT)], 
#                      [x[i] - y[i] == Int(0)] for i in range(Int(2), dim)])
#     f = And(constraints, overlap, resource_eq)
#     return Ramsey(x, y, f))

def benchmark_divisibility_by_k(dim: int, k: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    f = And(
        Equals(Mod(x[0], Int(k)), Mod(Int(0), Int(k))),
        Equals(Mod(y[0], Int(k)), Mod(Int(0), Int(k)))
    )
    return Ramsey(x, y, f)

def benchmark_affine_progression(dim: int, v_coeffs: list):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = Symbol("t", INT)
    f = And([Equals(y[i] - x[i] - t * v_coeffs[i], Int(0)) for i in range(dim)])
    return Ramsey(x, y, Exists([t], f))

def benchmark_matrix_kernel(dim: int, A: list):
    n_rows = len(A)
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t_vec = [Symbol(f"t_{j}", INT) for j in range(n_rows)]
    eqs = []
    for j in range(n_rows):
        row_sum_x = Plus(A[j][i] * x[i] for i in range(dim))
        row_sum_y = Plus(A[j][i] * y[i] for i in range(dim))
        eqs.append(Equals(row_sum_y - row_sum_x - t_vec[j], Int(0)))
    f = And(And(*eqs), And([Equals(t, Int(0)) for t in t_vec]))
    return Ramsey(x, y, Exists(t_vec, f))

def benchmark_stabilizer(dim: int, M: list):
    assert len(M) == dim, f"Expected {dim} rows, got {len(M)}"
    assert all(len(row) == dim for row in M), "All rows must have length {dim}"
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t_vec = [Symbol(f"t_{i}", INT) for i in range(dim)]
    eqs = []
    for i in range(dim):
        Mx_i = Plus(M[i][j] * x[j] for j in range(dim))
        My_i = Plus(M[i][j] * y[j] for j in range(dim))
        eqs.append(Equals(Mx_i - My_i - t_vec[i], Int(0)))
    f = And(And(*eqs), And([Equals(t, Int(0)) for t in t_vec]))
    return Ramsey(x, y, Exists(t_vec, f))

def benchmark_weighted_sum_eq(dim: int, coeffs: list):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = Symbol("t", INT)
    sum_x = Plus(coeffs[i] * x[i] for i in range(dim))
    sum_y = Plus(coeffs[i] * y[i] for i in range(dim))
    f = And(Equals(sum_x - sum_y - t, Int(0)), Equals(t, Int(0)))
    return Ramsey(x, y, Exists([t], f))

def benchmark_equal_first_k(dim: int, k: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t_vec = [Symbol(f"t_{i}", INT) for i in range(k)]
    f = And([And(Equals(x[i] - y[i] - t_vec[i], Int(0)), Equals(t_vec[i], Int(0))) for i in range(k)])
    return Ramsey(x, y, Exists(t_vec, f))

def benchmark_sum_parity(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = Symbol("t", INT)
    sum_x = Plus(x[i] for i in range(dim))
    sum_y = Plus(y[i] for i in range(dim))
    f = Equals(sum_x - sum_y - Int(2) * t, Int(0))
    return Ramsey(x, y, Exists([t], f))

def benchmark_prefix_monotone(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t_vec = [Symbol(f"t_{i}", INT) for i in range(dim)]
    mono_x = And([x[i] <= x[i+1] for i in range(dim-1)])
    mono_y = And([y[i] <= y[i+1] for i in range(dim-1)])
    geq = And([And(Equals(y[i] - x[i] - t_vec[i], Int(0)), t_vec[i] >= Int(0)) for i in range(dim)])
    f = And(mono_x, mono_y, geq)
    return Ramsey(x, y, Exists(t_vec, f))

def benchmark_sum_zero_or_C(dim: int, C: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    s = Symbol("s", INT)
    sum_x = Plus(x[i] for i in range(dim))
    sum_y = Plus(y[i] for i in range(dim))
    f = And(Equals(sum_x - sum_y - s, Int(0)), Or(Equals(s, Int(0)), Equals(s, Int(C))))
    return Ramsey(x, y, Exists([s], f))

def benchmark_cross_coordinate_eq(dim: int):
    x = int_vector("a", dim)
    y = int_vector("b", dim)
    t = Symbol("t", INT)
    f = And([Equals(x[i] - y[i+1] - t, Int(0)) for i in range(dim-1)])
    return Ramsey(x, y, Exists([t], f))

def benchmark_mixed_sign_pair(dim: int):
    assert dim % 2 == 0, "dim must be even"
    n = dim // 2
    x = int_vector("a", dim)  # [x1,..,xn,y1,..,yn]
    y = int_vector("b", dim)  # [x1',..,xn',y1',..,yn']
    t_vec1 = [Symbol(f"t1_{i}", INT) for i in range(n)]
    t_vec2 = [Symbol(f"t2_{i}", INT) for i in range(n)]
    # For x: pairs (x_i, y_i) such that x_i + y_i = Int(0)
    f_x = And([And(Equals(x[i] + x[i+n] - t_vec1[i], Int(0)), Equals(t_vec1[i], Int(0))) for i in range(n)])
    f_y = And([And(Equals(y[i] + y[i+n] - t_vec2[i], Int(0)), Equals(t_vec2[i], Int(0))) for i in range(n)])
    f = And(f_x, f_y)
    return Ramsey(x, y, Exists(t_vec1 + t_vec2, f))
