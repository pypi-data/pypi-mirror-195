from multiprocessing import connection, Pipe
from threading import Thread
import numpy as np
from cczero.model_helper import load_best_model_weight, need_to_reload_best_model_weight
from time import time


class CChessModelAPI:

    def __init__(self, config, agent_model):
        self.agent_model = agent_model  # CChessModel
        self.pipes = []  # use for communication between processes/threads
        self.config = config
        self.need_reload = True
        self.done = False

    def start(self, need_reload=True):
        self.need_reload = need_reload
        prediction_worker = Thread(target=self.predict_batch_worker, name="prediction_worker")
        prediction_worker.daemon = True
        prediction_worker.start()

    def get_pipe(self, need_reload=True):
        me, you = Pipe()
        self.pipes.append(me)
        self.need_reload = need_reload
        return you

    def predict_batch_worker(self):
        last_model_check_time = time()
        while not self.done:
            if last_model_check_time + 600 < time() and self.need_reload:
                self.try_reload_model()
                last_model_check_time = time()
            ready = connection.wait(self.pipes, timeout=0.001)
            if not ready:
                continue
            data, result_pipes, data_len = [], [], []
            for pipe in ready:
                while pipe.poll():
                    try:
                        tmp = pipe.recv()
                    except EOFError as e:
                        print(f"EOF error: {e}")
                        pipe.close()
                    else:
                        data.extend(tmp)
                        data_len.append(len(tmp))
                        result_pipes.append(pipe)
            if not data:
                continue
            data = np.asarray(data, dtype=np.float32)
            with self.agent_model.graph.as_default():
                policy_ary, value_ary = self.agent_model.model.predict_on_batch(data)
            buf = []
            k, i = 0, 0
            for p, v in zip(policy_ary, value_ary):
                buf.append((p, float(v)))
                k += 1
                if k >= data_len[i]:
                    result_pipes[i].send(buf)
                    buf = []
                    k = 0
                    i += 1

    def try_reload_model(self):
        try:
            if self.need_reload and need_to_reload_best_model_weight(self.agent_model):
                with self.agent_model.graph.as_default():
                    load_best_model_weight(self.agent_model)
        except Exception as e:
            print(e)

    def close(self):
        self.done = True
