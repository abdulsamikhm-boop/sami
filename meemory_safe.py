import time

def samikhan(func):
    def stramline(*sam,**sami):
        print('the words are going to be proceeded')
        remember_time = time.time()
        stream_lite = func(*sam,**sami)
        for token in stream_lite:
            yield token
        print(f'\ntotal time taken to print words is {time.time() - remember_time:.2f}')
    return stramline


@samikhan
def defining():
    tokens = ['sami',' khan',' is', ' currently', ' studying',' something',' difficult',' than',' your',' ex']
    for token in tokens:
        time.sleep(0.2)
        yield token

for word in defining():
    print(word, end='', flush=True)