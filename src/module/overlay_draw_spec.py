"""Custom DrawFunc implementation."""
from savant_rs.draw_spec import BoundingBoxDraw, ColorDraw, ObjectDraw, PaddingDraw

from savant.deepstream.drawfunc import NvDsDrawFunc
from savant.meta.object import ObjectMeta
from savant.deepstream.meta.frame import NvDsFrameMeta
from savant.utils.artist import Artist, Position
from datetime import datetime

class Overlay(NvDsDrawFunc):
    """Custom implementation of PyFunc for drawing on frame."""

    def override_draw_spec(
        self, object_meta: ObjectMeta, draw_spec: ObjectDraw
    ) -> ObjectDraw:
        """Override draw spec for objects."""
        # When the dev_mode is enabled in the module config
        # The draw func code changes are applied without restarting the module

        if object_meta.label == 'person':
            # For example, change the border color of the bounding box
            # by specifying the new RGBA color in the draw spec
            bbox_draw = BoundingBoxDraw(
                border_color=ColorDraw(255, 255, 255, 255),
                background_color=ColorDraw(0, 0, 0, 0),
                thickness=1,
                padding=PaddingDraw(),
            )

            draw_spec = ObjectDraw(
                bounding_box=bbox_draw,
                label=draw_spec.label,
                central_dot=draw_spec.central_dot,
                blur=draw_spec.blur,
            )

        # elif object_meta.label == 'face':
        #     # For example, switch face blur on or off
        #     draw_spec = ObjectDraw(
        #         bounding_box=draw_spec.bounding_box,
        #         label=draw_spec.label,
        #         central_dot=draw_spec.central_dot,
        #         blur=True,
        #     )

        return draw_spec
    

    # def draw_on_frame(self, frame_meta: NvDsFrameMeta, artist: Artist):
    #     self.logger.info(
    #         'draw_on_frame %s',
    #         frame_meta.frame_num,
    #     )
    #     artist.add_text(
    #         f'Entries: {frame_meta.frame_num}',
    #         (50, 50),
    #         2.5,
    #         5,
    #         anchor_point_type=Position.LEFT_TOP,
    #     )

    def draw_on_frame(self, frame_meta: NvDsFrameMeta, artist: Artist):
        """Draws on frame using the artist and the frame's metadata.

        :param frame_meta: Frame metadata.
        :param artist: Artist to draw on the frame.
        """
        # When the dev_mode is enabled in the module config
        # The draw func code changes are applied without restarting the module

        # super().draw_on_frame(frame_meta, artist)

        # for example, draw a white bounding box around persons
        # and a green bounding box around faces
        for obj in frame_meta.objects:
            if obj.label == 'person':
                artist.add_bbox(obj.bbox, 3, (255, 255, 255, 255))
            elif obj.label == 'face':
                artist.add_bbox(obj.bbox, 3, (0, 255, 0, 255))

        artist.add_text(
            f'Date: {datetime.now()}',
            (10, 10),
            1.5,
            2,
            anchor_point_type=Position.LEFT_TOP,
        )
