        def get_display_page(self, page_num, max_image_size, zoom=False,
                             fit_screen=True, reset_cached=False):
            """Return a `tkinter.PhotoImage` or a PNG image for a document page number.
                - The `page_num` argument is a 0-based page number.
                - The `zoom` argument is the top-left of old clip rect, and one of -1, 0,
                  +1 for dim. x or y to indicate the arrow key pressed.
                - The `max_image_size` argument is the (width, height) of available image area.
            """
            zoom_x = 1
            zoom_y = 1
            scale = fitz.Matrix(zoom_x, zoom_y)

            page_display_list = self.page_display_list_cache[page_num] if not reset_cached else None
            if not page_display_list:  # Create if not yet there.
                self.page_display_list_cache[page_num] = self.document[page_num].get_displaylist()
                page_display_list = self.page_display_list_cache[page_num]

            page_rect = page_display_list.rect  # The page rectangle.
            clip = page_rect

            # Make sure that the image will fit the screen.
            zoom_0 = 1
            if max_image_size: # TODO: this is currently a required param...
                zoom_0 = min(1, max_image_size[0] / page_rect.width, max_image_size[1] / page_rect.height)
                if zoom_0 == 1:
                    zoom_0 = min(max_image_size[0] / page_rect.width, max_image_size[1] / page_rect.height)
            mat_0 = fitz.Matrix(zoom_0, zoom_0)

            if zoom:
                width2 = page_rect.width / 2
                height2 = page_rect.height / 2

                clip = page_rect * 0.5     # Clip rect size is a quarter page.
                top_left = zoom[0]
                top_left.x += zoom[1] * (width2 / 2)     # adjust top-left ...
                top_left.x = max(0, top_left.x)          # according to ...
                top_left.x = min(width2, top_left.x)     # arrow key ...
                top_left.y += zoom[2] * (height2 / 2)    # provided, but ...
                top_left.y = max(0, top_left.y)          # stay within ...
                top_left.y = min(height2, top_left.y)    # the page rect
                clip = fitz.Rect(top_left, top_left.x + width2, top_left.y + height2)

                # Clip rect is ready, now fill it.
                mat = mat_0 * fitz.Matrix(2, 2)  # The zoom matrix.
                pixmap = page_display_list.get_pixmap(alpha=False, matrix=mat, clip=clip)

            else:  # Show the total page.
                pixmap = page_display_list.get_pixmap(matrix=mat_0, alpha=False)

            #image_png = pixmap.tobytes()  # get the PNG image
            image_height, image_width = pixmap.height, pixmap.width
            image_ppm = pixmap.tobytes("ppm")  # Make PPM image from pixmap for tkinter.
            image_tl = clip.tl # Clip position (top left).
            return image_ppm, image_tl, image_height, image_width

