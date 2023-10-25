# Modify the `strings` variable to control what values get rendered in the
# viewport.

import os

import PySide6

import signac


def render(args, alpha=95):
    """Render information from a job's document and/or statepoint.

    Args:
        alpha (float): Opacity of textbox, in percent. 100 = fully opaque.
    """
    pipeline = args.scene.selected_pipeline
    window_height = args.size[1]

    if pipeline:
        data = pipeline.compute(args.frame)
        source_file = data.attributes["SourceFile"]
        dirname = os.path.dirname(source_file)
        job = signac.get_job(dirname)
        jobid = job._id[:8]

        # get data from job statepoint and/or doc and create strings
        strings = [
            jobid,
            f"{job.sp.num_particles} particles",
            f"param1 = {job.sp.param1}",
            f"param2 = {job.doc.param2}",
            # etc...
        ]

        # make fontsize scale with window size
        font = args.painter.font()
        fontsize = window_height * 13 / 500
        font.setPointSizeF(fontsize)
        whitespace_buffer = int(window_height / 100)
        args.painter.setFont(font)
        horizontal_advance = 0
        descent = args.painter.fontMetrics().descent()
        ascent = args.painter.fontMetrics().ascent()

        # figure out how wide to make the text box
        for _str in strings:
            horizontal_advance = max(
                args.painter.fontMetrics().horizontalAdvance(_str),
                horizontal_advance,
            )
        width = horizontal_advance + fontsize // 3

        # draw textbox
        x1 = whitespace_buffer
        y1 = int(whitespace_buffer)
        height = int(1.3 * fontsize * len(strings) - 1)
        args.painter.fillRect(
            x1,
            y1,
            width,
            height,
            PySide6.QtGui.QColor(255, 255, 255, int(alpha / 100 * 255)),
        )
        args.painter.drawRect(x1, y1, width, height)

        # add text on top of box
        for i, _str in enumerate(strings):
            x = args.painter.drawText(
                fontsize // 6 + whitespace_buffer,
                int(0.75 * fontsize + whitespace_buffer + 1.3 * fontsize * i)
                + fontsize // 6,
                _str,
            )
