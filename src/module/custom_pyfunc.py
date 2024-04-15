"""Custom PyFunc implementation."""
from savant.deepstream.meta.frame import NvDsFrameMeta
from savant.deepstream.pyfunc import NvDsPyFuncPlugin
from savant.gstreamer import Gst
# import redis
# from statsd import StatsClient
# import socketio
from collections import deque
import statistics
# from aiohttp import web
# import asyncio
# import zmq

class CustomPyFunc(NvDsPyFuncPlugin):
    """Custom frame processor."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.buf = deque(maxlen=30)
        # context = zmq.Context()
        # self.socket = context.socket(zmq.PUB)
        # self.socket.bind("tcp://0.0.0.0:5002")
        # self.redis = redis.Redis(host = 'localhost', port = 6379)
        # self.stats_client = StatsClient(
        #     'graphite', 8125, prefix='savant.module.dust-rec'
        # )
        # self.sio = socketio.AsyncServer(cors_allowed_origins='*')
        # self.app = web.Application()
        # self.sio.attach(self.app)
        # web.run_app(self.app, port=5002)



    def process_frame(self, buffer: Gst.Buffer, frame_meta: NvDsFrameMeta):
        """Process frame.

        :param buffer: GStreamer buffer.
        :param frame_meta: Processed frame metadata.
        """
        # object_count = len([i for i in frame_meta.objects])
        # self.buf.append(object_count)
        self.logger.info(
            'Processing frame #%d of source %s and batch %s',
            frame_meta.frame_num,
            frame_meta.source_id,
            frame_meta.batch_id,
        )
        
        # self.sio.emit('message', "12345668")
        # self.logger.info("finded %d items, mean %d", object_count, statistics.mean(self.buf))
        # self.socket.send_pyobj({ 'mean-person' : statistics.mean(self.buf) })
        # if statistics.mean(self.buf) > 10:
        #     self.logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     work_message = { 'num' : statistics.mean(self.buf) }
            # self.socket.send_json(work_message)
            # self.sio.emit('message', "12345668")

        # self.logger.info(len(self.buf))
        # if len([i for i in frame_meta.objects]) > 10:
            # self.redis.publish(frame_meta.source_id, "10 items!!")

        # self.stats_client.incr(
        #     '.'.join(
        #         (
        #             frame_meta.source_id,
        #             self.target_obj_label,
        #             "entry"
        #         )
        #     )
        # )


    def on_source_eos(self, source_id: str):
        """On source EOS event callback."""
        self.logger.debug('Got GST_NVEVENT_STREAM_EOS for source %s.', source_id)

    # def process_buffer(self, buffer: Gst.Buffer):
    #     """Process Gst.Buffer, parse DS batch manually."""

    #     self.logger.info("process_buffer")
    #     self.logger.info(str(buffer))

    #     self.redis.publish("test", "test message")



    # def on_start(self) -> bool:
    #     """Do on plugin start."""
    #     self.logger.info('start!!!!!!!!!!!!!!!!!!!!')
    #     return True

    # def on_event(self) -> bool:
    #     """Do on plugin start."""
    #     self.logger.info('eventy !!!!!!!!!!!!!!!!!!!!')

