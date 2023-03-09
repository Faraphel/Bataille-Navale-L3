import unittest

from source.gui.position import *
from source.gui.scene.abc import Scene
from source.gui.widget.abc import BoxWidget
from source.gui.window import Window


class TestWindow(Window):  # NOQA
    def __init__(self, *args, **kwargs):
        super().__init__(width=1920, height=1080, visible=False, *args, **kwargs)


class TestScene(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window=window, **kwargs)


class TestBoxWidget(BoxWidget):
    def __init__(self, scene: "Scene"):
        super().__init__(x=100, y=200, width=150, height=175, scene=scene)


window = TestWindow()
scene = TestScene(window)
widget = TestBoxWidget(scene)


class TestPosition(unittest.TestCase):
    def test_unit_px(self):
        for value in range(1, 500):
            self.assertEqual((value*px)(widget), value)

    def test_unit_vw(self):
        for value in range(1, 200):
            self.assertEqual((value*vw)(widget), int(window.width * (value / 100)))

    def test_unit_vh(self):
        for value in range(1, 200):
            self.assertEqual((value*vh)(widget), int(window.height * (value / 100)))

    def test_unit_ww(self):
        for value in range(1, 200):
            self.assertEqual((value*ww)(widget), int(widget.width * (value / 100)))

    def test_unit_wh(self):
        for value in range(1, 200):
            self.assertEqual((value * wh)(widget), int(widget.height * (value / 100)))

    def test_unit_add(self):
        for value_px in range(1, 100):
            for value_vw in range(1, 100):
                self.assertEqual(
                    (value_px*px + value_vw*vw)(widget),
                    value_px + int(window.width * (value_vw / 100))
                )

    def test_unit_sub(self):
        for value_px in range(1, 100):
            for value_vw in range(1, 100):
                self.assertEqual(
                    (value_px * px - value_vw * vw)(widget),
                    value_px - int(window.width * (value_vw / 100))
                )

    def test_unit_rsub(self):
        for value_px in range(1, 100):
            for value_vw in range(1, 100):
                self.assertEqual(
                    (value_vw * vw - value_px * px)(widget),
                    int(window.width * (value_vw / 100)) - value_px
                )


if __name__ == '__main__':
    unittest.main()
