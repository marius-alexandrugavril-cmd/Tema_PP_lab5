import multiprocessing
from lab5.converter import text_to_html


def worker_process(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue):
    """
    Proces worker care ascultă pe o coadă de intrare,
    procesează textul și trimite HTML-ul pe coada de ieșire.
    """
    while True:
        data = input_queue.get()


        if data == "STOP":
            break


        text_content = data
        html_content = text_to_html(text_content)


        output_queue.put(html_content)