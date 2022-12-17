class Foo():
    def initial_value():
        print("generating initial value") 
        return 42

    # initialize class variable
    shared_count = initial_value() 
    
    def inc(self):
        Foo.shared_count += 1

print("creating a and b")
a = Foo()
b = Foo()
a.inc()
print(a.shared_count)
print(b.shared_count)