f = 0.4

p = f
val = 0

for _i in range(1000):
    val += p
    p *= 1 - f

print(val)
print((1) / (f))
