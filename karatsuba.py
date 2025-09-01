def karatsuba(x, y):
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    high1, low1 = divmod(x, 10**m)
    high2, low2 = divmod(y, 10**m)
    z0 = karatsuba(low1, low2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    z2 = karatsuba(high1, high2)
    ad_plus_bc = z1 - z2 - z0
    return (z2 * 10**(2*m)) + (ad_plus_bc * 10**m) + z0



def karatsuba_count(x, y):
    count = {}
    def inner_karatsuba(x, y):
        if x < 10 or y < 10:
            return x * y
        n = max(len(str(x)), len(str(y)))
        m = n // 2
        high1, low1 = divmod(x, 10**m)
        high2, low2 = divmod(y, 10**m)
        z0 = inner_karatsuba(low1, low2)
        z1 = inner_karatsuba((low1 + high1), (low2 + high2))
        z2 = inner_karatsuba(high1, high2)
        ad_plus_bc = z1 - z2 - z0
    # Підрахунок ad + bc
        if ad_plus_bc in count:
            count[ad_plus_bc] += 1
        else:
            count[ad_plus_bc] = 1
        return (z2 * 10**(2*m)) + (ad_plus_bc * 10**m) + z0
    result = inner_karatsuba(x, y)
    return result, count

# Приклад
x = 21625695688898558125310188636840316594920403182768
y = 13306827740879180856696800391510469038934180115260

result, count = karatsuba_count(x, y)
print("Результат множення:", result)
print("ad + bc:", count)
