import time
from rq import get_current_job

def example(seconds):
    job = get_current_job()
    print('Starting task example')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(i)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task example finished')

