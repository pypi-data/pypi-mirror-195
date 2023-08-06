import pandas as pd
import numpy as np

class CDAMetadata(object):
        def __init__(self,
        img,
        maxrow,
        maxcol,
        row,
        col,
        pos):
            self.img = img
            self.maxrow = maxrow
            self.maxcol = maxcol
            self.row = row
            self.col = col
            self.pos = pos
            self.score = None
            self.x1 = None
            self.x2 = None
            self.y1 = None
            self.y2 = None

        def __str__(self):
            return f"""----------
CURRENT METADATA:
            Img: {self.img}
            Maxrow: {self.maxrow}
            Maxcol: {self.maxcol}
            Row: {self.row}
            Col: {self.col}
            Pos: {self.pos}
            Score: {self.score}
            x1: {self.x1}
            x2: {self.x2}
            y1: {self.y1}
            y2: {self.y2}
----------
            """

        def _update(self, num_spots):
            print("Updating CDA reference metadata")
            # Check if there are any spots left
            if not self.pos == num_spots:
                self.pos += 1
            else:
                self.pos = 1
                # Check if there are any leaves left in the row
                if not self.col == self.maxcol:
                    self.col += 1
                else:
                    self.col = 1
                    # Check if there are any columns left in the image
                    if not self.row == self.maxrow:
                        self.row += 1
                    else:
                        self.pos = 1
                        self.row = 1
                        self.col = 1
                        return self, True
            return self, False

        def _make_pandas(self):
            data = {'img': self.img,
            'maxrow': self.maxrow,
            'maxcol': self.maxcol,
            'row': self.row,
            'col': self.col,
            'pos': self.pos,
            'score': self.score,
            'x1': self.x1,
            'x2': self.x2,
            'y1': self.y1,
            'y2': self.y2}
            series = pd.Series(data=data, index=["img", "maxrow", "maxcol", "row", "col", "pos", "score", "x1", "x2", "y1", "y2"])
            return series.to_frame().T
