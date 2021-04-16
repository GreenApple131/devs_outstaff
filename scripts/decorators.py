from datetime import datetime
import time


def timeit(arg):
    print(arg)

    def outer(func):
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            print(datetime.now() - start)
            return result
        return wrapper
    return outer


# @timeit('name')
def one(n):
    list = [x for x in range(n) if x % 2 == 0]
    return list

# l1 = one(10**4)


# l1 = one
# p = l1(10)
# print(p)


# l1 = timeit(one)
# # print(type(l1), l1.__name__)
# a = l1(10)


l1 = timeit('name')(one)(10)  # nested functions


# simple decorator

def benchmark(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
        return return_value
    return wrapper


@benchmark
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text


webpage = fetch_webpage('https://google.com')
print(webpage)


# decorator with args

def benchmark(iters):
    def actual_decorator(func):

        def wrapper(*args, **kwargs):
            total = 0
            for i in range(iters):
                start = time.time()
                return_value = func(*args, **kwargs)
                end = time.time()
                total = total + (end-start)
            print('[*] Среднее время выполнения: {} секунд.'.format(total/iters))
            return return_value

        return wrapper
    return actual_decorator


@benchmark(iters=10)
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text


webpage = fetch_webpage('https://google.com')
print(webpage)
