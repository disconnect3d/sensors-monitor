import psutil


def combined():
    measures = cpu()
    measures.update(memory())
    return measures


def memory():
    memory_use = psutil.virtual_memory()
    total_memory = memory_use.total/1024/1024
    available_memory = memory_use.available/1024/1024
    used_memory_percent = memory_use.percent
    memory = {
        'Total memory [MB]': total_memory,
        'Available memory [MB]': available_memory,
        'Used memory [%]': used_memory_percent
    }
    return memory


def cpu():
    # cpu_percent = psutil.cpu_percent(percpu=True)
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return {
        'Core %d [%%]' % counter: cpu for counter, cpu in enumerate(cpu_percent)
    }
