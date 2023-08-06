from asteria.instruments import *

TEST_COLOUR_HEX = "#00ff00"
TEST_COLOUR = RGBColor.fromHEX(TEST_COLOUR_HEX)


class TestStaticColour:
    def test_basic(self):
        instrument = StaticColour(TEST_COLOUR_HEX)
        output = instrument.display(4)
        assert len(output) == 4
        assert output[0] == TEST_COLOUR
        assert output[1] == TEST_COLOUR
        assert output[2] == TEST_COLOUR
        assert output[3] == TEST_COLOUR


class TestLinearHueRange:
    def test_basic(self):
        instrument = LinearHueRange(lambda: 0.5, 0, 360)
        output = instrument.display(1)
        assert len(output) == 1
        assert output[0] == RGBColor.fromHSV(180, 100, 100)

    def test_out_of_bounds(self):
        instrument = LinearHueRange(lambda: 42, 0, 180)
        output = instrument.display(1)
        assert len(output) == 1
        assert output[0] == RGBColor.fromHSV(180, 100, 100)


class TestPercentageBar:
    def test_basic(self):
        instrument = PercentageBar(lambda: 0.5, TEST_COLOUR_HEX)
        output = instrument.display(4)
        assert len(output) == 4
        assert output[0] == LED_OFF
        assert output[1] == LED_OFF
        assert output[2] == TEST_COLOUR
        assert output[3] == TEST_COLOUR
